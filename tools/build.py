#!/usr/bin/env python3
"""Merge units/*.json into src/app-template.html and write index.html.

Run from the repository root:  python3 tools/build.py
"""
import glob, json, os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
units = []
for path in sorted(glob.glob(os.path.join(root, 'units', '*.json'))):
    units += json.load(open(path, encoding='utf-8'))['units']
for unit in units:
    for q in unit['questions']:
        # verification-only fields are not needed by the app
        for key in ('program', 'expect', 'stdin'):
            q.pop(key, None)
data = json.dumps({'units': units}, ensure_ascii=False).replace('</', '<\\/')
template = open(os.path.join(root, 'src', 'app-template.html'), encoding='utf-8').read()
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, 'index.html')
open(out, 'w', encoding='utf-8').write(template.replace('__COURSE_DATA__', data))
print('%s: %d units, %d lessons, %d questions, %d programs' % (
    os.path.relpath(out, root), len(units), sum(len(u['lessons']) for u in units),
    sum(len(u['questions']) for u in units), sum(len(u['programs']) for u in units)))
