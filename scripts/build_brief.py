#!/usr/bin/env python3
"""Build the one-page Bangladesh brief for hsrep.bd as HTML (then print to PDF with headless Chrome).

Reuses the fonts and stylesheet of the main site's brief builder
(../website/scripts/briefs/build_briefs.py) so the PDF matches the other briefs.
Run from the hsrep-bd repo root:  python3 scripts/build_brief.py
"""
import os, re, base64, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAINB = os.path.join(os.path.dirname(ROOT), 'website', 'scripts', 'briefs')
F = os.path.join(MAINB, 'fonts', 'node_modules', '@fontsource')
src = open(os.path.join(MAINB, 'build_briefs.py'), encoding='utf-8').read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)


def font_face(family, pkg, weight, style='normal'):
    p = os.path.join(F, pkg, 'files', f'{pkg}-latin-{weight}-{style}.woff2')
    b64 = base64.b64encode(open(p, 'rb').read()).decode()
    return f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2');}}"


FONTS = '\n'.join([
    font_face('Inter', 'inter', 400), font_face('Inter', 'inter', 500), font_face('Inter', 'inter', 600), font_face('Inter', 'inter', 700),
    font_face('Spectral', 'spectral', 600), font_face('Spectral', 'spectral', 700),
    font_face('IBM Plex Mono', 'ibm-plex-mono', 400), font_face('IBM Plex Mono', 'ibm-plex-mono', 500),
])

EXTRA = """
h1{font-size:21px;margin:6px 0 4px}
.sub{margin:0 0 9px}
.pitch .row{font-size:9.2px;padding:5px 0}
.stat{padding:8px 12px}
.stat .t{font-size:8.2px}
.card p{font-size:8.5px}
.eyebrow{margin:9px 0 4px}
.foot .src{margin:6px 0 .16in}
.band .cols3{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:14px}
.band table{width:100%;border-collapse:collapse;font-size:8.6px;line-height:1.35}
.band th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:7.8px;letter-spacing:.12em;text-transform:uppercase;color:#C9D3DF;font-weight:500;padding:0 8px 4px 0;border-bottom:1px solid rgba(255,255,255,.22)}
.band td{padding:4px 8px 4px 0;vertical-align:top;border-bottom:1px solid rgba(255,255,255,.1)}
.band td:first-child{font-weight:600;color:#fff;white-space:nowrap}
.band tr:last-child td{border-bottom:0}
.rule{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid var(--hair);border-left:4px solid var(--coral);border-radius:6px;padding:7px 14px;margin-top:9px;font-size:9.2px;line-height:1.4}
.rule b{font-family:'Spectral',serif;font-size:11.5px;color:var(--navy);white-space:nowrap}
"""

pitch = [
    ('The gap', 'Bangladesh&rsquo;s national programme screened 1.56 million women by VIA between 2018 and 2023 and recorded every positive result. <b>Only 40.4% of the 51,913 VIA-positive women reached colposcopy.</b> The registry already sends each of them an SMS; it cannot store the histopathology result. Nobody in Bangladesh publishes a completion rate for an abnormal result.'),
    ('The routine', 'Two hours a week, one short list, four steps, run by the provider&rsquo;s own nurse with a worklist: <b>find</b> who is overdue, <b>rank</b> by days since the positive result and prior no-shows, <b>act</b> with a call in Bangla, a booked slot and the fare, <b>close</b> when the result is back. No software to buy, no new staff.'),
    ('Where first', 'The referral tail of factory screening. A private provider already screens garment workers in the factory and refers the women it cannot treat on site. <b>Provider-run, factory-hosted, sponsor-paid, with the public colposcopy clinic as the endpoint.</b> The factory never sees a result; it releases the right women on the right mornings.'),
    ('The rule', '<b>Paid per completion, never per referral.</b> The outreach nurse is paid for the list; the provider is paid when the woman finishes. The colposcopy itself is free at the public clinic.'),
    ('The ask', 'One private provider, one factory client, three months, then a decision. After the Michigan pilot has a number, and not before. Step one, now, is a 30-minute conversation.'),
]
stats = [
    ('51,913 &rarr; 20,954', 'VIA-positive women, and the number who reached colposcopy: 40.4%, Jan 2018 to May 2023 (Nessa et al., 2025).'),
    ('32%', 'of newly diagnosed hypertension and diabetes patients at NCD corners did not return within three months; stock-outs, transport cost and queues (BMC Health Services Research, 2026).'),
    ('6 in 100', 'factory workers screened by VIA had an abnormal result; about half were treated on site, the rest referred, with nothing published on what happened next (Jhpiego, 2026).'),
]
cards = [
    ('A &middot; Start here', 'The referral tail of factory screening', 'The provider&rsquo;s nurse follows the referred women to the public colposcopy clinic. Paid by the sponsor that already funds the screening: a brand programme, UNFPA, or the factory as a corporate client. Measure: referred women reaching colposcopy within 90 days, against 40.4%.'),
    ('B &middot; Alongside', 'A completion contract inside one private network', 'The network runs the routine on its own abnormal results where the next step is in-house, with one transparent price and no per-referral payment. It pays for it, and gains completion from patients it already acquired. Measure: completion within the clinical window, by result type.'),
    ('C &middot; At scale', 'A follow-up cell inside the national programme', 'Two or three upazilas use the registry&rsquo;s own list and add a phone call, a booked slot, the fare, and the result written back. Funded from programme money already committed for 2027&ndash;2031. Measure: the national 40.4% in those upazilas, a year later.'),
]
matrix = [
    ('Private provider', 'Its nurse, two hours a week', 'Referred cases by contract where private; a per-completion fee; a completion rate to sell'),
    ('Factory', 'The worker&rsquo;s paid morning; a room; 15 minutes a week', 'Compliance evidence for buyers; fewer women lost to long illness'),
    ('Sponsor', 'Screening it already funds; a small fee per completion; the fare', 'A completion rate per factory instead of a screening count'),
    ('Public programme', 'Nothing new; the colposcopy clinics exist', 'Its 40.4% moving; results written back to the registry'),
    ('The woman', 'Nothing', 'Reaches the next step, morning paid, fare covered'),
    ('HSREP', 'The worklist, the rules, the training; takes no fee', 'The first published completion number in Bangladesh'),
]

rows = ''.join(f'<div class="row"><div class="k">{k}</div><div>{v}</div></div>' for k, v in pitch)
st = ''.join(f'<div class="stat"><div class="n">{n}</div><div class="t">{t}</div></div>' for n, t in stats)
cd = ''.join(f'<div class="card"><div class="e">{e}</div><h3>{h}</h3><p>{p}</p></div>' for e, h, p in cards)
mt = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in matrix)

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Prevention Adoption Initiative &middot; Bangladesh brief</title>
<style>{FONTS}{CSS}{EXTRA}</style></head><body><div class="page">
<div class="top"><span>Prevention Adoption Initiative &middot; Bangladesh &middot; Future direction</span><span class="r">HSREP &middot; hsrep.bd</span></div>
<div class="body">
<h1>Six in ten referred women never reach colposcopy. The screening already found them.</h1>
<p class="sub">A one-page brief on the step after the referral: how a weekly follow-up routine could run in Bangladesh after its first pilot in Michigan, who would do what, who would pay, and why each party would say yes. Nothing here has a partner, a date or funding.</p>
<div class="pitch"><div class="ph"><span>The pitch in 30 seconds</span><span class="st">Future direction &middot; In development</span></div>{rows}</div>
<div class="eyebrow">The gap, in three numbers</div><div class="grid3">{st}</div>
<div class="eyebrow">Three ways it could run, in order</div><div class="grid3">{cd}</div>
<div class="eyebrow">Who puts in what, who gets what &middot; model A</div>
<div class="band"><table><thead><tr><th>Party</th><th>Puts in</th><th>Gets</th></tr></thead><tbody>{mt}</tbody></table></div>
<div class="rule"><b>Paid per completion, never per referral.</b><span>Doctors paid per test have no reason to chase a patient who already paid, and patients who suspect padded tests have a reason not to come back. The routine is written around that, not on top of it.</span></div>
<div class="foot"><div class="cols">
<div class="l"><b>Md Shafaat Ali Choyon</b> &mdash; Founder, HSREP &middot; MBA, MCIM, MPH, CHES&reg;<br>hsrep.bd/initiative &middot; hsraep.org/initiative &middot; Book 30 min: calendly.com/shafaat-alic/30min<br>LinkedIn: /in/sacgrowthspecialist</div>
<div class="r">An HSREP initiative in development. Everything here is future direction and illustrative; no patient data has been collected; no Bangladesh partner, site or funding is confirmed, and no organisation named has been approached. Figures are from the sources named, none from HSREP&rsquo;s own data. Operational materials will be reviewed by counsel before any launch.</div>
</div><div class="src">SOURCES &mdash; Nessa et al., BMC Global and Public Health 2025;3:34 &middot; MOHFW National Cervical &amp; Breast Cancer Statistics dashboard &middot; BMC Public Health, May 2025 (e-HIS registry) &middot; BMC Health Services Research, Jan 2026 (NCD corners, 12 upazilas) &middot; Jhpiego, Jan 2026 (factory VIA clinics) &middot; UNFPA, 10 Oct 2026 (EIB Women&rsquo;s Health Initiative 2027&ndash;2031) &middot; UNB, 6 Nov 2025 (BGMEA member-care MoUs) &middot; TIB via Dhaka Tribune, Feb 2018 (commission-based referral). Version 23 Oct 2026.</div></div>
</div></div></body></html>"""

out = os.path.join(ROOT, 'scripts', 'brief_bd.html')
open(out, 'w', encoding='utf-8').write(html)
print('html written', out)
