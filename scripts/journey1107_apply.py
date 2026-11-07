#!/usr/bin/env python3
"""journey-1107 for hsrep.bd: link the routine and the chronic-care finish lines to the Bangla demo.
Run from the hsrep-bd/ folder: python3 <path>/bd_apply.py   (edits initiative.html and scripts/bd_init_body.py the same way)
"""
import sys, pathlib
MARK = 'journey-1107'
root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.')
CSS = ('/* journey-1107 */\n'
 '.bddemo{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 18px;margin:16px 0 0;font-size:14.5px;line-height:1.5}\n'
 '.bddemo a{font-weight:600;color:var(--pai-coral-text);text-decoration:none}.bddemo a:hover{text-decoration:underline}\n'
 '.bddemo span{flex:1 1 100%;color:var(--muted);font-size:13.5px}\n')
ROUTINE = ('<p class="bddemo"><a href="https://hsraep.org/worklist/#prog-bd-cerv">See this list in the demo, in Bangla &rarr;</a>'
 '<span>Invented women referred after a positive VIA test, ranked by the three rules, with a message a named person checks before it goes. Nothing is sent.</span></p>\n')
CHRONIC = ('<p class="bddemo"><a href="https://hsraep.org/worklist/#prog-bd-htn">Open the hypertension list in the demo &rarr;</a>'
 '<a href="https://hsraep.org/worklist/#tour-bd">Take the six-step tour in Bangla &rarr;</a>'
 '<span>Each finish line above is its own programme in the demo, diabetes, kidney and anaemia included. Invented people; nothing is sent.</span></p>\n')
OLD_ROW = 'Rina B. &middot; VIA-positive at a factory screening camp'
NEW_ROW = 'B-2041 &middot; VIA-positive at a factory screening camp'
def sub_once(s, old, new, what):
    n = s.count(old)
    if n != 1: sys.exit(f'{what}: expected 1 match, found {n}')
    return s.replace(old, new)
for rel in ['initiative.html', 'scripts/bd_init_body.py']:
    p = root / rel; s = p.read_text(encoding='utf-8')
    if MARK in s: print(rel, 'already applied'); continue
    s = sub_once(s, '<style id="bd2">\n', '<style id="bd2">\n' + CSS, rel + ' css')
    s = sub_once(s, OLD_ROW, NEW_ROW, rel + ' row')
    a = s.index('id="routine"'); b = s.index('<div class="bdrule">', a)
    s = s[:b] + ROUTINE + s[b:]
    a = s.index('id="chronic"'); b = s.index('<p class="bdsrc">', a)
    s = s[:b] + CHRONIC + s[b:]
    p.write_text(s, encoding='utf-8'); print(rel, 'patched')
