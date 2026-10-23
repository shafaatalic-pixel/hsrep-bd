#!/usr/bin/env python3
"""Build the HSREP Bangladesh edition (hsrep.bd) from the main site's roadmap page.

Run from the hsrep-bd repo root:  python3 scripts/build.py
Reads ../website/initiative-next.html for the head, header, footer and scripts,
and scripts/_orig_initiative-next.html (main at f377a49) for the Bangladesh
material that left the main site on 21 Oct 2026.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = (ROOT.parent / 'website' / 'initiative-next.html').read_text(encoding='utf-8')
ORIG = (ROOT / 'scripts' / '_orig_initiative-next.html').read_text(encoding='utf-8')
MAIN = 'https://hsraep.org'
BD = 'https://hsrep.bd'
TODAY = '2026-10-23'

# ---------- pieces of the template ----------
head, rest = TPL.split('<header class="site hs-top">', 1)
header, rest = rest.split('<main id="main" tabindex="-1" class="pai">', 1)
header = '<header class="site hs-top">' + header
_, tail = rest.split('</main><footer>', 1)
tail = '</main><footer>' + tail


def relativize(s):
    s = s.replace('href="/assets/', 'href="assets/').replace('src="/assets/', 'src="assets/')
    s = s.replace('url(/assets/', 'url(assets/')
    for f in ('favicon.ico', 'favicon-32.png', 'favicon-16.png', 'favicon-192.png', 'apple-touch-icon.png', 'site.webmanifest'):
        s = s.replace('href="/' + f + '"', 'href="' + f + '"')
    return s


def absolutize(s):
    # Links to main-site pages become absolute. Our own two pages are written explicitly later.
    s = re.sub(r'href="/([a-z0-9-]+\.html(?:#[^"]*)?)"', r'href="%s/\1"' % MAIN, s)
    s = re.sub(r'href="(?!https?:|mailto:|#|assets/)([a-z0-9-]+\.html(?:#[^"]*)?)"', r'href="%s/\1"' % MAIN, s)
    s = s.replace('href="/"', 'href="%s/"' % MAIN)
    return s


# head: drop analytics and assistant, relativize assets, strip page-specific JSON-LD and meta
head = re.sub(r'<script src="/assets/analytics\.js[^"]*" defer></script>', '', head)
head = re.sub(r'<script src="/assets/assistant\.js[^"]*" defer></script>', '', head)
head = relativize(head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '%%JSONLD%%', head, count=1, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', '%%DESC%%', head, count=1)
head = re.sub(r'<title>[^<]*</title>', '%%TITLE%%', head, count=1)
head = re.sub(r'<link rel="canonical" href="[^"]*">', '%%CANON%%', head, count=1)
head = re.sub(r'<meta property="og:title" content="[^"]*">', '%%OGT%%', head, count=1)
head = re.sub(r'<meta property="og:description" content="[^"]*">', '%%OGD%%', head, count=1)
head = re.sub(r'<meta property="og:url" content="[^"]*">', '%%OGU%%', head, count=1)
head = head.replace('content="https://hsraep.org/assets/social/og/og-initiative.png"', 'content="%s/assets/social/og/og-initiative.png"' % BD)
head = re.sub(r'<meta name="twitter:title" content="[^"]*">', '%%TWT%%', head, count=1)
head = re.sub(r'<meta name="twitter:description" content="[^"]*">', '%%TWD%%', head, count=1)
assert head.count('%%JSONLD%%') == 1 and head.count('%%TITLE%%') == 1 and head.count('%%CANON%%') == 1

# header: absolute nav, no assistant button, no current-page mark, our own sub-nav
header = relativize(absolutize(header))
header = re.sub(r'<button class="hs-ask".*?</button>', '', header, count=1, flags=re.S)
header = header.replace('<a class="here" aria-current="page" href="%s/initiative.html">Initiative</a>' % MAIN,
                        '<a href="%s/initiative.html">Initiative</a>' % MAIN)
header = re.sub(r'<nav id="secnav" class="hs-band" aria-label="Prevention Adoption Initiative">.*?</nav>',
                '%%SECNAV%%', header, count=1, flags=re.S)
assert '%%SECNAV%%' in header and 'hs-ask' not in header

# footer and scripts: absolute links, relative assets, an edition line
tail = relativize(absolutize(tail))
old_tag = '<p>An independent public-health research and advocacy platform examining health-system resilience as economic protection infrastructure.</p>'
assert tail.count(old_tag) == 1
tail = tail.replace(old_tag, old_tag[:-4] + ' This is the Bangladesh edition; the record of work is on <a href="%s/" style="color:inherit;display:inline">hsraep.org</a>.</p>' % MAIN)

# (the roadmap's old Bangladesh block is no longer used; the page is written from the strategy memo of 23 Oct 2026)

# ---------- helpers ----------
def secnav(current):
    items = [('index.html', 'Overview'), ('initiative.html', 'Where the routine could run')]
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else '', t) for h, t in items)
    return ('<nav id="secnav" class="hs-band" aria-label="HSREP Bangladesh"><div class="sn-label">HSREP Bangladesh</div>'
            + links + '<a href="%s/">Main site &rarr;</a></nav>' % MAIN)


def jsonld(path, name, desc):
    return ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebPage", "@id": "%s/%s#webpage", '
            '"url": "%s/%s", "name": "%s", "description": "%s", "inLanguage": "en", "dateModified": "%s", '
            '"isPartOf": {"@type": "WebSite", "@id": "%s/#website", "name": "HSREP Bangladesh", "url": "%s/", '
            '"publisher": {"@type": "Organization", "name": "HSREP", "url": "%s/"}}}</script>'
            % (BD, path, BD, path, name, desc, TODAY, BD, BD, MAIN))


def page(path, title, desc, og_title, body, current):
    h = head.replace('%%TITLE%%', '<title>%s</title>' % title)
    h = h.replace('%%DESC%%', '<meta name="description" content="%s">' % desc)
    h = h.replace('%%CANON%%', '<link rel="canonical" href="%s/%s">' % (BD, path))
    h = h.replace('%%OGT%%', '<meta property="og:title" content="%s">' % og_title)
    h = h.replace('%%OGD%%', '<meta property="og:description" content="%s">' % desc)
    h = h.replace('%%OGU%%', '<meta property="og:url" content="%s/%s">' % (BD, path))
    h = h.replace('%%TWT%%', '<meta name="twitter:title" content="%s">' % og_title)
    h = h.replace('%%TWD%%', '<meta name="twitter:description" content="%s">' % desc)
    h = h.replace('%%JSONLD%%', jsonld(path, og_title, desc))
    hd = header.replace('%%SECNAV%%', secnav(current))
    out = h + hd + '<main id="main" tabindex="-1" class="pai">\n' + body + '\n' + tail
    assert '%%' not in out
    (ROOT / path).write_text(out, encoding='utf-8')
    print('wrote', path, len(out))


P = 'style="margin:0 0 14px;font-size:15px;line-height:1.6;max-width:66ch"'
LINK = 'style="color:var(--coral);text-decoration:none;border-bottom:1px solid rgba(242,109,90,.45)"'

# Shared block: the four steps, in the roadmap's own gsteps style.
STEPS = '''<ol class="gsteps bdsteps">
<li><span class="mono">01 &middot; Find</span><p>Everyone who was told to get a test and has no result recorded.</p></li>
<li><span class="mono">02 &middot; Rank</span><p>Days overdue, days since a positive result, prior no-shows. Three rules, no model.</p></li>
<li><span class="mono">03 &middot; Act</span><p>A call in the patient&rsquo;s language, a kit, a booking, help with transport.</p></li>
<li><span class="mono">04 &middot; Close</span><p>The test is done, and the days from referral to result are counted.</p></li>
</ol>'''

# Extra CSS for the edition (small; everything else comes from the main site's sheets).
BD_CSS = '''<style id="bd">
.bdgrid{grid-template-columns:repeat(2,minmax(0,1fr))}
.bdsteps{list-style:none;margin:0 0 14px;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.bdsteps li{border-top:2px solid var(--heading);padding-top:10px}
.bdsteps .mono{display:block;font-size:10.5px;color:var(--pai-coral-text);margin-bottom:5px}
.bdsteps p{margin:0;font-size:14px;line-height:1.5}
.bdpat{margin:0 0 22px;background:var(--panel);border-radius:8px;padding:12px 14px;font-size:14px;line-height:1.5;color:var(--heading)}
.bdpat .mono{display:block;font-size:10px;color:var(--muted);margin-bottom:4px}
.bdtoc{display:flex;flex-direction:column;gap:0;border:1px solid var(--pai-line);border-radius:12px;background:#fff;padding:14px 18px 6px;align-self:start}
.bdtoc>.mono{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.bdtoc a{display:grid;grid-template-columns:34px minmax(0,1fr);gap:8px;align-items:start;padding:10px 0;border-top:1px solid var(--pai-line);text-decoration:none;color:var(--heading)}
.bdtoc a b{font-family:var(--font-mono);font-weight:500;font-size:12px;color:var(--pai-coral-text);padding-top:2px}
.bdtoc a span{font-family:var(--font-display);font-size:1.08rem;line-height:1.25}
.bdtoc a small{display:block;font-family:var(--font-body,inherit);font-size:13px;line-height:1.4;color:var(--muted);margin-top:2px}
.bdtoc a:hover span{color:var(--coral)}
.bdstat{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;align-self:start}
.bdstat>div{border:1px solid var(--pai-line);border-radius:10px;padding:18px 20px;background:#fff}
.bdstat .n{font-family:var(--font-mono);font-size:1.6rem;color:var(--heading);margin-bottom:4px}
.bdstat p{margin:0;font-size:13.5px;line-height:1.5;color:var(--ink)}
.bdstat .st{margin-top:10px}
.bdmeta{font-family:var(--font-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.bdcard p.d{margin:0 0 10px}
.bdtwo{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:36px;align-items:start}
.bdnote{margin:0 0 14px;font-family:var(--font-mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
@media(max-width:760px){.bdgrid,.bdstat,.bdtwo{grid-template-columns:1fr}.bdsteps{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:480px){.bdsteps{grid-template-columns:1fr}}
</style>'''

# ---------- index.html ----------
articles = [
    ('The Daily Star', 'Commentary', '19 Feb 2026', '4 min', 'Increasing public health investment must be a top priority',
     'Why health financing is economic protection, not a residual cost line.',
     'articles/increasing-public-health-investment/increasing-public-health-investment.html'),
    ('The Daily Star', 'Commentary', '12 Mar 2026', '5 min', 'Can we use private healthcare to improve health literacy?',
     'When patients cannot read the system, costs rise for everyone.',
     'articles/private-healthcare-health-literacy/private-healthcare-health-literacy.html'),
    ('HSREP', 'Special report', '1 Mar 2026', '9 min', 'When the Ground Shakes, Neighbors Respond First',
     'Community preparedness as Dhaka&rsquo;s most affordable defense against a catastrophic earthquake.',
     'articles/when-the-ground-shakes/when-the-ground-shakes.html'),
    ('The Daily Star', 'Earlier piece', '6 Feb 2025', '4 min', 'We need public health reform for steady economic growth',
     'The earliest foundation piece connecting reform to growth.',
     'articles/public-health-reform-for-economic-growth/public-health-reform-for-economic-growth.html'),
]
cards = ''.join(
    '<div class="gcard bdcard"><p class="bdmeta">%s &middot; %s &middot; %s &middot; %s read</p><h3>%s</h3><p class="d">%s</p><p><a href="%s/%s" %s>Read on hsraep.org &rarr;</a></p></div>'
    % (pub, kind, date, mins, t, d, MAIN, href, LINK) for pub, kind, date, mins, t, d, href in articles)

index_body = f'''{BD_CSS}
<section class="pai-hero"><div class="wrap">
<div class="copy">
<span class="pai-chip" style="align-self:flex-start">Bangladesh edition</span>
<h1>HSREP in Bangladesh.</h1>
<p class="dek">HSREP is an independent public-health research and advocacy platform, founded in Michigan by Md Shafaat Ali Choyon, MBA, MCIM, MPH, CHES&reg;. Its first season examined health systems in the United States and Bangladesh. This edition collects the Bangladesh side: the Season 1 pieces written for readers here, and what the Prevention Adoption Initiative could look like in Bangladesh after its first pilot in Michigan.</p>
<div class="pai-cta"><a class="btn pai-primary" href="initiative.html">Where the routine could run here <span class="ar">&rarr;</span></a><a class="btn pai-secondary" href="{MAIN}/">The main site <span class="ar">&rarr;</span></a></div>
</div>
<nav class="bdtoc" aria-label="On this page">
<span class="mono">On this page</span>
<a href="#season-1"><b>01</b><span>The Bangladesh pieces<small>Four Season 1 articles, three in The Daily Star</small></span></a>
<a href="#initiative"><b>02</b><span>The initiative<small>A weekly routine for the step after the referral</small></span></a>
<a href="#who"><b>03</b><span>Who is behind it<small>The founder, and where the record of work lives</small></span></a>
</nav>
</div></section>

<div class="wrap" style="padding:8px 0 56px">
<section class="pai-card" id="season-1" aria-labelledby="s1h">
<span class="mono">01 &middot; Season 1</span>
<h2 id="s1h">The Bangladesh pieces.</h2>
<p class="lede">Season 1 was one argument told across nine pieces in two countries: that health protection is economic infrastructure, not a residual budget line. These are the four about Bangladesh.</p>
<div class="grid3 bdgrid">{cards}</div>
<p style="margin:18px 0 0;font-size:13.5px;color:var(--muted)">The full season, its engagement record and its methods are on the main site: <a href="{MAIN}/season-1.html" style="color:inherit">Season 1 record</a> &middot; <a href="{MAIN}/methodology.html" style="color:inherit">Methods and sources</a>.</p>
</section>

<section class="pai-card" id="initiative" aria-labelledby="inh">
<span class="mono">02 &middot; The initiative</span>
<h2 id="inh">Finish the tests people already start.</h2>
<p class="lede">The Prevention Adoption Initiative is a weekly routine for recommended care that people begin and do not complete. Four steps, run by a clinic&rsquo;s own staff.</p>
{STEPS}
<div class="bdtwo" style="margin-top:22px">
<div>
<p {P}>The first pilot is designed for one health center in Michigan, on colorectal cancer screening, including the colonoscopy after a positive test; the design is published and the next step is a host clinic. Bangladesh is where I have standing and screening-service experience, and the national cervical and breast screening program has published its own follow-up gap, so it is the natural second setting, with its own three-month pilot and its own number.</p>
<p class="pai-small" style="margin:0">An HSREP initiative in development. The design is published; a Bangladesh partner, site and funding come next.</p>
</div>
<div class="pai-close" style="margin:0;padding:22px 24px"><p><b>Where the routine could run here.</b><br>The gap in numbers, three ways to run it, who would do what and who would pay, in plain words.</p><a class="btn pai-primary" href="initiative.html">Read the page <span class="ar">&rarr;</span></a></div>
</div>
</section>

<section class="pai-card" id="who" aria-labelledby="whoh">
<span class="mono">03 &middot; Who is behind it</span>
<h2 id="whoh">One person, with a record on both sides of the problem.</h2>
<p class="lede">HSREP is founded and run by Md Shafaat Ali Choyon, MBA, MCIM, MPH, CHES&reg;. Seventeen years getting people to follow through, in health care since 2021.</p>
<div class="bdtwo">
<div>
<p {P}><b style="color:var(--heading)">Inside a Bangladeshi delivery system.</b> At Praava Health in Dhaka, as Head of Marketing &amp; Corporate Sales, I redesigned the diagnostic packages and launched Ghore Lab, a home sample-collection service, during COVID; laboratory screening utilization rose 34% from 2021 to 2022. I sold corporate health to employers, and I watched the break between a test started and a test finished happen, for years, from the inside. Later, as chief operating officer at Laser Treat Group, I ran the company&rsquo;s ERP, BI and CRM systems.</p>
<p {P}><b style="color:var(--heading)">Public health, published.</b> An MPH in Health Education &amp; Promotion from Eastern Michigan University and CHES&reg; certification. Season 1 of HSREP: nine published pieces across the United States and Bangladesh, with the engagement record, the methods and the corrections log all public.</p>
</div>
<div>
<p {P}><b style="color:var(--heading)">One HSREP.</b> This edition is not a separate body. The record of work, the editorial standards, the methods and the corrections log live on <a href="{MAIN}/" {LINK}>hsraep.org</a>; the .bd address exists so that readers and institutions in Bangladesh have one that is theirs, and so the Bangladesh work has a home that does not sit inside the page describing the Michigan pilot.</p>
<p {P}>Write to <a href="mailto:contact@hsraep.org" {LINK}>contact@hsraep.org</a>. For the initiative, <a href="https://calendly.com/shafaat-alic/30min" {LINK}>book thirty minutes</a>. More on the founder: <a href="{MAIN}/initiative.html#why-me" {LINK}>why I can do this</a>.</p>
</div>
</div>
</section>
</div>
'''

# ---------- initiative.html ----------
import sys; sys.path.insert(0, str(ROOT / 'scripts'))
from bd_init_body import init_body as _init_body
init_body = _init_body(MAIN, STEPS, BD_CSS)

page('index.html', 'HSREP Bangladesh',
     'The Bangladesh edition of HSREP: the Season 1 pieces on Bangladesh, and where the Prevention Adoption Initiative could run after its first pilot.',
     'HSREP Bangladesh', index_body, 'index.html')
page('initiative.html', 'Where the routine could run in Bangladesh - HSREP Bangladesh',
     'Six in ten VIA-positive women never reach colposcopy. How a weekly follow-up routine could run in Bangladesh after its first pilot: who would do what, who would pay, and why each party would say yes. Nothing is confirmed.',
     'Where the Prevention Adoption Initiative could run in Bangladesh', init_body, 'initiative.html')

(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % BD)
(ROOT / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join('  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n' % (BD, p, TODAY) for p in ('index.html', 'initiative.html'))
    + '</urlset>\n')
print('done')
