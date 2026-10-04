#!/usr/bin/env python3
"""Builds the command reference of the rkeeper-xml skill from r_keeper XSD schemas.

Usage:
    python xsd_to_reference.py <xsd_dir> <skill_dir> [--examples examples.json]

Reads every qry*.xsd (request) and the matching res*.xsd (response) under
<xsd_dir>, recursively, and writes:
    <skill_dir>/references/commands/<CMD>.md   one file per command
    <skill_dir>/references/commands.md         index of all commands

Standard library only, so it runs wherever Python 3.8+ does. Rerun it when a
newer set of XSD schemas arrives; hand-written notes live in
references/command_notes.json and are merged in, not overwritten.
"""
import argparse
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

XS = "{http://www.w3.org/2001/XMLSchema}"
# Types every command uses; expanding them each time would bury the tree.
# They are described once in references/protocol.md.
OPAQUE = {"refItem", "orderElement", "resRefItem", "guidString"}
DOC_LIMIT = 300


def load_xml(path):
    raw = open(path, "rb").read()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        # A few schemas declare UTF-8 but are saved in cp1251.
        raw = raw.decode("cp1251").encode("utf-8")
        raw = raw.replace(b'encoding="UTF-8"', b'encoding="utf-8"')
    return ET.fromstring(raw)


class Schema:
    """One schema file with everything it includes, as a name -> node index."""

    def __init__(self, path, cache):
        self.path = path
        self.root = load_xml(path)
        self.types = {}
        self.base_types = {}  # what a redefine extends: the original definition
        base_dir = os.path.dirname(path)
        for child in self.root:
            tag = child.tag.replace(XS, "")
            if tag in ("include", "redefine"):
                loc = child.get("schemaLocation").replace("\\", "/").lstrip("./")
                inc_path = os.path.join(base_dir, loc)
                if not os.path.exists(inc_path):
                    inc_path = os.path.join(os.path.dirname(base_dir), loc)
                inc = cache.get(inc_path)
                if inc is None:
                    inc = Schema(inc_path, cache)
                    cache[inc_path] = inc
                for k, v in inc.types.items():
                    self.types.setdefault(k, v)
                if tag == "redefine":
                    for r in child:
                        name = r.get("name")
                        if name:
                            key = (r.tag.replace(XS, ""), name)
                            self.base_types[key] = inc.types.get(key)
                            self.types[key] = r
        for child in self.root:
            name = child.get("name")
            if name and child.tag.replace(XS, "") != "element":
                self.types[(child.tag.replace(XS, ""), name)] = child

    def find(self, kind, name):
        return self.types.get((kind, name))


def doc(node):
    ann = node.find(XS + "annotation")
    if ann is None:
        return ""
    text = " ".join((d.text or "") for d in ann.findall(XS + "documentation"))
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= DOC_LIMIT else text[: DOC_LIMIT - 1] + "…"


def local(name):
    return name.split(":")[-1] if name else name


def enum_values(st):
    if st is None:
        return ""
    restriction = st.find(XS + "restriction")
    if restriction is None:
        return ""
    values = [e.get("value") for e in restriction.findall(XS + "enumeration")]
    if not values:
        return ""
    if len(values) > 40:
        return " {%d значений, см. XSD}" % len(values)
    return " {" + " | ".join(v if v else '""' for v in values) + "}"


def occurs(e):
    lo, hi = e.get("minOccurs", "1"), e.get("maxOccurs", "1")
    if hi == "0":
        return " [запрещен]"
    if hi == "unbounded":
        return "*" if lo == "0" else "+"
    return "?" if lo == "0" else ""


class Printer:
    def __init__(self, schema):
        self.s = schema
        self.out = []
        self.expanded = set()

    def line(self, indent, text):
        self.out.append("  " * indent + text.rstrip())

    def attributes(self, node, indent):
        for a in node:
            tag = a.tag.replace(XS, "")
            if tag == "attribute":
                name = a.get("name") or a.get("ref")
                typ = local(a.get("type") or "")
                values = ""
                st = a.find(XS + "simpleType")
                if st is not None:
                    values = enum_values(st)
                elif typ and typ != "guidString":
                    values = enum_values(self.s.find("simpleType", typ))
                req = "!" if a.get("use") == "required" else ""
                extra = ""
                if a.get("fixed") is not None:
                    extra = ' = "%s"' % a.get("fixed")
                elif a.get("default") is not None:
                    extra = ' (по умолчанию "%s")' % a.get("default")
                d = doc(a)
                self.line(indent, "@%s%s: %s%s%s%s" % (name, req, typ or "string", values, extra, ("  - " + d) if d else ""))
            elif tag == "attributeGroup":
                group = self.s.find("attributeGroup", local(a.get("ref")))
                if group is not None:
                    self.attributes(group, indent)
            elif tag == "anyAttribute":
                self.line(indent, "@* - допускаются любые другие атрибуты")

    def body(self, node, indent, chain):
        for c in node:
            tag = c.tag.replace(XS, "")
            if tag == "choice":
                self.line(indent, "(одно из%s:)" % (" - повторяется" if c.get("maxOccurs") == "unbounded" else ""))
                self.body(c, indent + 1, chain)
            elif tag in ("sequence", "all"):
                self.body(c, indent, chain)
            elif tag == "element":
                self.element(c, indent, chain)
            elif tag == "any":
                self.line(indent, "<любой XML>")
            elif tag in ("complexContent", "simpleContent"):
                for ext in c:
                    et = ext.tag.replace(XS, "")
                    if et not in ("extension", "restriction"):
                        continue
                    base = local(ext.get("base"))
                    if tag == "simpleContent":
                        self.line(indent, "(текстовое содержимое: %s)" % base)
                    elif base not in OPAQUE and base != "RK7QueryResult":
                        key = ("complexType", base)
                        if base in chain:
                            # A redefine extending the original of the same name.
                            original = self.s.base_types.get(key)
                            if original is not None:
                                self.body(original, indent, chain)
                        else:
                            bt = self.s.find("complexType", base)
                            if bt is not None:
                                self.body(bt, indent, chain | {base})
                    elif base in OPAQUE:
                        self.line(indent, "(%s: id | code | guid)" % base)
                    self.body(ext, indent, chain)
        self.attributes(node, indent)

    def element(self, e, indent, chain):
        name = e.get("name") or local(e.get("ref"))
        typ = local(e.get("type") or "")
        d = doc(e)
        head = "<%s>%s%s%s" % (name, occurs(e), (" [" + typ + "]") if typ else "", ("  - " + d) if d else "")
        ct = e.find(XS + "complexType")
        if ct is None and typ and typ not in OPAQUE and not typ.startswith("xs") and typ not in ("int", "long", "string", "anyType"):
            ct = self.s.find("complexType", typ)
            if ct is not None:
                if typ in self.expanded:
                    self.line(indent, head + " (структура - см. выше)")
                    return
                self.expanded.add(typ)
                chain = chain | {typ}
        self.line(indent, head)
        if ct is not None and len(chain) < 12:
            self.body(ct, indent + 1, chain)
        elif ct is None:
            # Invalid but real: some UCS schemas put xs:attribute straight under
            # xs:element, without a complexType. The server still expects them.
            self.attributes(e, indent + 1)


def summarize(path, cache):
    schema = Schema(path, cache)
    roots = [e for e in schema.root.findall(XS + "element")
             if e.get("name") in ("RK7Query", "RK7CMD", "RK7Command", "RK7QueryResult")]
    if not roots:
        return None, "", []
    root_el = roots[0]
    printer = Printer(schema)
    ct = root_el.find(XS + "complexType")
    indent = 0
    if root_el.get("name") in ("RK7CMD", "RK7Command"):
        # Some schemas describe the command element alone, without RK7Query.
        printer.line(0, "<%s>" % root_el.get("name"))
        indent = 1
    if ct is not None:
        printer.body(ct, indent, set())
    elif root_el.get("type"):
        t = schema.find("complexType", local(root_el.get("type")))
        if t is not None:
            printer.body(t, indent, set())
    return root_el, doc(root_el), printer.out


def command_name(lines, fallback):
    for l in lines:
        m = re.search(r'@CMD!?: \S* = "([A-Za-z0-9]+)"', l)
        if m:
            return m.group(1)
    return fallback


def where_from_doc(d):
    m = re.match(r"\s*\[([^\]]+)\]", d)
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xsd_dir")
    ap.add_argument("skill_dir")
    args = ap.parse_args()

    refs = os.path.join(args.skill_dir, "references")
    out_dir = os.path.join(refs, "commands")
    os.makedirs(out_dir, exist_ok=True)
    notes_path = os.path.join(refs, "command_notes.json")
    notes = json.load(open(notes_path, encoding="utf-8")) if os.path.exists(notes_path) else {}
    groups = notes.get("_groups", {})

    cache = {}
    index = []
    for qry in sorted(glob.glob(os.path.join(args.xsd_dir, "**", "qry*.xsd"), recursive=True)):
        base = os.path.basename(qry)[3:-4]
        try:
            root_el, description, req_lines = summarize(qry, cache)
        except ET.ParseError as e:
            # UCS ships an occasional malformed schema; one bad file should not stop the rest.
            print("skip (malformed XML: %s): %s" % (e, qry), file=sys.stderr)
            continue
        if root_el is None or root_el.get("name") == "RK7QueryResult":
            print("skip (not an RK7Query): %s" % qry, file=sys.stderr)
            continue
        cmd = command_name(req_lines, base)
        res = os.path.join(os.path.dirname(qry), "res" + base + ".xsd")
        res_lines, res_doc = [], ""
        if os.path.exists(res):
            try:
                _, res_doc, res_lines = summarize(res, cache)
            except ET.ParseError as e:
                print("response schema skipped (malformed XML: %s): %s" % (e, res), file=sys.stderr)
        rel_q = os.path.relpath(qry, args.xsd_dir).replace("\\", "/")
        rel_r = os.path.relpath(res, args.xsd_dir).replace("\\", "/") if os.path.exists(res) else None
        n = notes.get(cmd, {})

        md = ["# %s" % cmd, ""]
        if description:
            md += [description, ""]
        md.append("Схемы: `schemas/%s`%s" % (rel_q, (", `schemas/%s`" % rel_r) if rel_r else " (схемы ответа нет)"))
        if n.get("impact"):
            md.append("Влияние: %s" % {"read": "только чтение", "write": "изменяет данные",
                                        "danger": "**опасно** - необратимые или массовые изменения, блокировка кассы"}[n["impact"]])
        md.append("")
        if n.get("notes"):
            md += ["## Практика", ""] + ["- " + x for x in n["notes"]] + [""]
        md += ["## Запрос", "", "Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.", "", "```"]
        md += req_lines + ["```", ""]
        if res_lines:
            md += ["## Ответ", "", "Помимо общих атрибутов RK7QueryResult (см. protocol.md):", "", "```"] + res_lines + ["```", ""]
        for ex in n.get("examples", []):
            md += ["## Пример: %s" % ex["title"], "", "```xml", ex["xml"].rstrip(), "```", ""]
        # newline="\n": on Windows text mode would write CRLF, which breaks frontmatter parsers.
        open(os.path.join(out_dir, cmd + ".md"), "w", encoding="utf-8", newline="\n").write("\n".join(md))
        index.append((groups.get(cmd, "Прочее"), cmd, description, n.get("impact", ""), bool(n.get("examples"))))

    order = notes.get("_group_order", [])
    index.sort(key=lambda r: (order.index(r[0]) if r[0] in order else len(order), r[1]))
    lines = ["# Команды XML-интерфейса r_keeper 7", "",
             "Сгенерировано из XSD скриптом `scripts/xsd_to_reference.py`. Подробности по команде -",
             "в `commands/<CMD>.md`. Влияние: R - чтение, W - изменяет данные, D - опасно. ✓ - есть",
             "пример, проверенный на живом сервере.", ""]
    current = None
    for group, cmd, description, impact, has_ex in index:
        if group != current:
            lines += ["", "## " + group, "", "| Команда | Влияние | Назначение |", "|---|---|---|"]
            current = group
        flag = {"read": "R", "write": "W", "danger": "D"}.get(impact, "")
        lines.append("| [%s](commands/%s.md)%s | %s | %s |" % (cmd, cmd, " ✓" if has_ex else "", flag, description.replace("|", "/")))
    open(os.path.join(refs, "commands.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("%d commands written to %s" % (len(index), out_dir))


if __name__ == "__main__":
    main()
