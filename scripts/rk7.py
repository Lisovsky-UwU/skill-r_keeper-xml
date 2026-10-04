#!/usr/bin/env python3
"""Sends a query to an r_keeper 7 XML interface and prints the answer.

Standard library only (Python 3.8+). Connection settings come from arguments
or environment variables, so nothing about a particular stand lives in the skill:

    RK7_URL       full address, e.g. https://host:port/rk7api/v0/xmlinterface.xml
    RK7_HOST      or just host:port - the standard path is appended
    RK7_USER      HTTP Basic user
    RK7_PASSWORD  HTTP Basic password
    RK7_INSECURE  1 - accept self-signed / weak certificates and old TLS (typical for r_keeper)

Examples:
    python rk7.py --cmd GetSystemInfo
    python rk7.py --fragment '<RK7CMD CMD="GetRefData" RefName="CASHES" PropMask="items.(Ident,Name)"/>'
    python rk7.py query.xml --var orderGuid={...} --summary
    cat query.xml | python rk7.py -

The body may be a full RK7Query document or just the RK7CMD element(s); the
latter is wrapped automatically. {{name}} placeholders are filled from --var.
Exit code: 0 - Status "Ok" or "No changes", 1 - the server reported an error, 2 - transport failure.
"""
import argparse
import base64
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
import warnings

DEFAULT_PATH = "/rk7api/v0/xmlinterface.xml"


def build_url(args):
    url = args.url or os.environ.get("RK7_URL")
    if url:
        return url
    host = args.host or os.environ.get("RK7_HOST")
    if not host:
        sys.exit("No server: pass --url/--host or set RK7_URL/RK7_HOST.")
    scheme = "http" if args.http else "https"
    return "%s://%s%s" % (scheme, host, DEFAULT_PATH)


def ssl_context(insecure):
    if not insecure:
        return ssl.create_default_context()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # r_keeper servers often ship self-signed certificates with 1024-bit keys
    # and may only speak TLS 1.0; the default security level refuses both.
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            ctx.minimum_version = ssl.TLSVersion.TLSv1
    except (AttributeError, ValueError):
        pass
    try:
        ctx.set_ciphers("DEFAULT:@SECLEVEL=0")
    except ssl.SSLError:
        pass
    return ctx


def wrap(body):
    stripped = body.lstrip()
    if stripped.startswith("<?xml") or stripped.startswith("<RK7Query"):
        return body
    return '<?xml version="1.0" encoding="utf-8"?>\n<RK7Query>\n' + body.strip() + "\n</RK7Query>\n"


def attr(text, name):
    m = re.search(r"<RK7QueryResult\b[^>]*?\s" + name + r'="([^"]*)"', text)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="file with the query, or - for stdin")
    ap.add_argument("--cmd", help="send <RK7CMD CMD=\"...\"/> with no parameters")
    ap.add_argument("--fragment", help="RK7CMD element(s) given inline")
    ap.add_argument("--var", action="append", default=[], metavar="NAME=VALUE", help="fill a {{NAME}} placeholder")
    ap.add_argument("--url")
    ap.add_argument("--host", help="host:port, the standard path is appended")
    ap.add_argument("--http", action="store_true", help="plain HTTP with --host")
    ap.add_argument("--user", default=os.environ.get("RK7_USER"))
    ap.add_argument("--password", default=os.environ.get("RK7_PASSWORD"))
    ap.add_argument("--insecure", action="store_true", default=os.environ.get("RK7_INSECURE") == "1")
    ap.add_argument("--timeout", type=float, default=90)
    ap.add_argument("--summary", action="store_true", help="print only Status / ErrorText, not the body")
    ap.add_argument("--save", help="also write the response body to this file")
    ap.add_argument("--dry-run", action="store_true", help="print the final query and do not send it")
    args = ap.parse_args()

    if args.cmd:
        body = '<RK7CMD CMD="%s"/>' % args.cmd
    elif args.fragment:
        body = args.fragment
    elif args.file == "-":
        body = sys.stdin.read()
    elif args.file:
        body = open(args.file, encoding="utf-8").read()
    else:
        ap.error("give a file, --cmd or --fragment")

    for item in args.var:
        name, _, value = item.partition("=")
        body = body.replace("{{%s}}" % name, value)
    body = wrap(body)
    left = sorted(set(re.findall(r"\{\{([A-Za-z0-9_.-]+)\}\}", body)))
    if left:
        print("warning: unfilled placeholders: %s" % ", ".join(left), file=sys.stderr)
    if args.dry_run:
        print(body)
        return 0

    url = build_url(args)
    req = urllib.request.Request(url, data=body.encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/xml; charset=utf-8")
    if args.user is not None:
        token = base64.b64encode(("%s:%s" % (args.user, args.password or "")).encode("utf-8")).decode("ascii")
        req.add_header("Authorization", "Basic " + token)
    try:
        with urllib.request.urlopen(req, timeout=args.timeout, context=ssl_context(args.insecure)) as resp:
            text = resp.read().decode("utf-8", "replace")
            http_status = resp.status
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")
        http_status = e.code
    except Exception as e:  # DNS, refused connection, TLS, timeout
        hint = ""
        if isinstance(e, ssl.SSLError) or "CERTIFICATE" in str(e).upper():
            hint = " (self-signed certificate? try --insecure / RK7_INSECURE=1)"
        elif "timed out" in str(e):
            hint = (" (some commands - OpenWebForm, DeliveryEditOrder - open a window on the till"
                    " and answer only after it is closed)")
        print("transport error: %s%s" % (e, hint), file=sys.stderr)
        return 2

    if args.save:
        open(args.save, "w", encoding="utf-8").write(text)
    status = attr(text, "Status")
    summary = "HTTP %s | Status=%s" % (http_status, status or "?")
    for name in ("CMD", "RK7ErrorN", "ErrorText", "WorkTime", "NetName", "ServerVersion"):
        value = attr(text, name)
        if value:
            summary += " | %s=%s" % (name, value)
    if not text.strip():
        summary += " | empty body"
    print(summary, file=sys.stderr)
    if not args.summary:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
    return 0 if status in ("Ok", "No changes") else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
