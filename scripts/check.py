#!/usr/bin/env python3
"""Consistency checks for the skill. Needs no XSD and no network.

    python scripts/check.py

Checks that the scripts compile, command_notes.json parses, SKILL.md has its
frontmatter, every command in the index has a file (and back), every
generated command file is in sync with command_notes.json examples, and the
examples carry placeholders rather than ids of somebody's restaurant.
"""
import json
import os
import py_compile
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def fail(msg):
    errors.append(msg)


def main():
    for name in os.listdir(os.path.join(ROOT, "scripts")):
        if name.endswith(".py"):
            try:
                py_compile.compile(os.path.join(ROOT, "scripts", name), doraise=True)
            except py_compile.PyCompileError as e:
                fail("syntax: %s" % e)

    # CRLF breaks frontmatter parsing in some agents (Claude Code among them).
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "schemas", "__pycache__")]
        for f in filenames:
            if f.endswith((".md", ".py", ".json", ".yml")):
                path = os.path.join(dirpath, f)
                if bytes([13, 10]) in open(path, "rb").read():
                    fail("CRLF line endings: %s" % os.path.relpath(path, ROOT))

    skill = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", skill, re.S)
    if not m or not re.search(r"^name: rkeeper-xml$", m.group(1), re.M) or "description:" not in m.group(1):
        fail("SKILL.md: frontmatter with name and description is missing")

    try:
        notes = json.load(open(os.path.join(ROOT, "references", "command_notes.json"), encoding="utf-8"))
    except ValueError as e:
        fail("command_notes.json: %s" % e)
        notes = {}

    cmd_dir = os.path.join(ROOT, "references", "commands")
    files = {f[:-3] for f in os.listdir(cmd_dir) if f.endswith(".md")}
    index = open(os.path.join(ROOT, "references", "commands.md"), encoding="utf-8").read()
    listed = set(re.findall(r"\(commands/([A-Za-z0-9]+)\.md\)", index))
    for c in sorted(listed - files):
        fail("commands.md lists %s, but commands/%s.md is missing" % (c, c))
    for c in sorted(files - listed):
        fail("commands/%s.md is not in commands.md" % c)

    for cmd, entry in notes.items():
        if cmd.startswith("_") or cmd not in files:
            continue
        if entry.get("impact") not in ("read", "write", "danger"):
            fail("%s: impact must be read / write / danger" % cmd)
        text = open(os.path.join(cmd_dir, cmd + ".md"), encoding="utf-8").read()
        for ex in entry.get("examples", []):
            if ex["xml"].strip() not in text:
                fail("%s: example '%s' is not in commands/%s.md - rerun xsd_to_reference.py" % (cmd, ex["title"], cmd))
            # Long numeric ids are almost always a real restaurant's objects.
            for num in re.findall(r'(?:id|Ident|code)="(\d{5,})"', ex["xml"]):
                fail("%s: example '%s' has a concrete id %s - use a {{placeholder}}" % (cmd, ex["title"], num))
        for note in entry.get("notes", []):
            if not isinstance(note, str):
                fail("%s: notes must be strings" % cmd)

    # Schema paths must match the files letter for letter: Windows forgives a
    # wrong case, Linux (and CI) does not.
    schema_files = set()
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "schemas")):
        for f in filenames:
            schema_files.add(os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, "/"))
    if any(f.endswith(".xsd") for f in schema_files):
        for c in sorted(files):
            text = open(os.path.join(cmd_dir, c + ".md"), encoding="utf-8").read()
            for p in re.findall(r"`(schemas/[^`]+\.xsd)`", text):
                if p not in schema_files:
                    fail("commands/%s.md names %s, but no file is spelled exactly like that" % (c, p))

    out = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "rk7.py"), "--fragment", '<RK7CMD CMD="GetSystemInfo"/>', "--dry-run"],
        capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0 or "<RK7Query>" not in out.stdout:
        fail("rk7.py --dry-run failed: %s" % (out.stderr or out.stdout))

    for e in errors:
        print("FAIL " + e)
    print("%d problem(s)" % len(errors) if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
