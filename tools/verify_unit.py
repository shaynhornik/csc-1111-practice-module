#!/usr/bin/env python3
"""Validate a unit JSON file and compile-check every piece of C++ in it.
Usage: python3 verify_unit.py units/<file>.json     (exit 0 = all good)"""
import json, sys, os, re, subprocess, tempfile, hashlib
path = sys.argv[1]
data = json.load(open(path))
errs, warns = [], []
ALLOWED_TAGS = {'p','ul','ol','li','strong','em','code','pre','table','thead','tbody','tr','th','td','h4','br'}
def norm(s): return '\n'.join(l.rstrip() for l in s.replace('\r','').strip('\n').split('\n')).rstrip()
tmp = tempfile.mkdtemp(prefix='cppv_')
def run_cpp(src, stdin=''):
    h = hashlib.md5(src.encode()).hexdigest()[:10]
    f = os.path.join(tmp, h + '.cpp'); exe = os.path.join(tmp, h)
    open(f, 'w').write(src)
    c = subprocess.run(['g++', '-std=c++17', '-Wall', '-Wno-parentheses', '-o', exe, f], capture_output=True, text=True)
    if c.returncode != 0: return None, 'COMPILE ERROR: ' + c.stderr[:400]
    try: r = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired: return None, 'TIMEOUT'
    return r.stdout, None
ids = set()
units = data.get('units')
if not isinstance(units, list) or not units: sys.exit('top level must be {"units": [...]}')
for u in units:
    for k in ('id','title','summary','lessons','questions','programs'):
        if k not in u: errs.append(f"unit {u.get('id')} missing {k}")
    lesson_ids = set()
    for l in u.get('lessons', []):
        for k in ('id','title','book','html'):
            if not l.get(k): errs.append(f"lesson {l.get('id')} missing {k}")
        lesson_ids.add(l.get('id'))
        for t in re.findall(r'</?([a-zA-Z0-9]+)', l.get('html','')):
            if t.lower() not in ALLOWED_TAGS: errs.append(f"lesson {l.get('id')} uses tag <{t}>")
        words = len(re.sub(r'<[^>]+>',' ',l.get('html','')).split())
        if words < 120: warns.append(f"lesson {l.get('id')} is short ({words} words)")
    per_lesson = {}
    for q in u.get('questions', []):
        qid = q.get('id')
        if not qid or qid in ids: errs.append(f"bad or duplicate id {qid}")
        ids.add(qid)
        t = q.get('type')
        if q.get('lesson') not in lesson_ids: errs.append(f"{qid}: lesson {q.get('lesson')} not found")
        per_lesson[q.get('lesson')] = per_lesson.get(q.get('lesson'), 0) + 1
        if not q.get('prompt') or not q.get('explain'): errs.append(f"{qid}: needs prompt and explain")
        if q.get('difficulty') not in (1,2,3): errs.append(f"{qid}: difficulty must be 1, 2 or 3")
        if t == 'mc':
            ch = q.get('choices')
            if not isinstance(ch, list) or len(ch) != 4 or len(set(ch)) != 4: errs.append(f"{qid}: mc needs 4 distinct choices")
            if not isinstance(q.get('answer'), int) or not 0 <= q['answer'] <= 3: errs.append(f"{qid}: mc answer must be 0-3")
        elif t == 'tf':
            if not isinstance(q.get('answer'), bool): errs.append(f"{qid}: tf answer must be true/false")
        elif t == 'fill':
            if not isinstance(q.get('answer'), str) or not isinstance(q.get('accept'), list) or not q['accept']: errs.append(f"{qid}: fill needs answer string and accept list")
            elif q['answer'].lower() not in [a.lower() for a in q['accept']]: errs.append(f"{qid}: answer must be in accept")
        elif t == 'output':
            if not q.get('code') or not q.get('program') or not isinstance(q.get('answer'), str): errs.append(f"{qid}: output needs code, program, answer")
        else: errs.append(f"{qid}: unknown type {t}")
        if q.get('program'):
            out, e = run_cpp(q['program'], q.get('stdin',''))
            if e: errs.append(f"{qid}: {e}")
            else:
                want = q['answer'] if t == 'output' else q.get('expect')
                if want is None: errs.append(f"{qid}: has program but no expect")
                elif norm(out) != norm(want): errs.append(f"{qid}: output mismatch. got {norm(out)!r} want {norm(want)!r}")
    for lid in lesson_ids:
        if per_lesson.get(lid, 0) < 4: warns.append(f"lesson {lid} has only {per_lesson.get(lid,0)} questions")
    for p in u.get('programs', []):
        pid = p.get('id')
        if not pid or pid in ids: errs.append(f"bad or duplicate id {pid}")
        ids.add(pid)
        for k in ('title','task','solution','sampleOutput'):
            if not p.get(k): errs.append(f"{pid}: missing {k}")
        if p.get('solution'):
            out, e = run_cpp(p['solution'], p.get('stdin',''))
            if e: errs.append(f"{pid}: {e}")
            elif norm(out) != norm(p.get('sampleOutput','')): errs.append(f"{pid}: sampleOutput mismatch. got {norm(out)!r}")
    types = {}
    for q in u.get('questions', []): types[q.get('type')] = types.get(q.get('type'),0)+1
    ans = [q['answer'] for q in u.get('questions', []) if q.get('type')=='mc' and isinstance(q.get('answer'),int)]
    dist = [ans.count(i) for i in range(4)]
    if ans and max(dist) > 0.4*len(ans): warns.append(f"unit {u.get('id')}: mc answer positions are lopsided {dist}")
    print(f"unit {u.get('id')}: {len(u.get('lessons',[]))} lessons, {len(u.get('questions',[]))} questions {types}, {len(u.get('programs',[]))} programs, mc positions {dist}")
for w in warns: print('WARN', w)
for e in errs: print('ERROR', e)
print('RESULT:', 'FAIL' if errs else 'PASS', f'({len(errs)} errors, {len(warns)} warnings)')
sys.exit(1 if errs else 0)
