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

# ---------- the Bangladesh material from the original roadmap ----------
a = ORIG.index('<div role="tabpanel" id="pan-bd" aria-labelledby="tab-bd" hidden>')
b = ORIG.index('<p class="pai-caveat">Experience in one setting')
bd_block = ORIG[a:b]
bd_block = bd_block.split('\n', 1)[1]  # drop the tabpanel opener
assert bd_block.rstrip().endswith('</div>')
bd_block = bd_block.rstrip()[:-6].rstrip()  # drop the tabpanel closer
# the cview "where it would run" row is restated in the hero; drop it
bd_block = re.sub(r'^<div class="cview">.*?</div></div>\n', '', bd_block, count=1, flags=re.S)
bd_block = bd_block.replace('href="initiative.html#host"', 'href="%s/initiative.html#host"' % MAIN)
bd_block = bd_block.replace('href="initiative.html#pilot"', 'href="%s/initiative.html#pilot"' % MAIN)
# the old h3 becomes a section header, so drop it and its prospective note (restated below)
bd_block = re.sub(r'<h3 id="bangladesh"[^>]*>Different partners, different value, same routine</h3>\n', '', bd_block, count=1)
bd_block = re.sub(r'<span class="mono" style="display:block;color:var\(--muted\);font-size:10px;margin-bottom:10px">Organizations named here are prospective\. None is a confirmed partner\.</span>\n', '', bd_block, count=1)
# split: comparison grid | partner cards + role cards + brief
grid, partners = bd_block.split('</div></div>\n', 1)
grid += '</div></div>\n'
assert 'sysp-grid' in grid and 'for-publicbd' in partners and 'Brief_Bangladesh.pdf' in partners
assert 'href="initiative.html' not in bd_block


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
<p class="dek">HSREP is an independent public-health research and advocacy platform, founded in Michigan by Md Shafaat Ali Choyon, MBA, MCIM, MPH, CHES&reg;. Its first season examined health systems in the United States and Bangladesh. This edition collects the Bangladesh side: the Season 1 pieces written for readers here, and what the Prevention Adoption Initiative could look like in Bangladesh once its first pilot has been evaluated.</p>
<div class="pai-cta"><a class="btn pai-primary" href="initiative.html">Where the routine could run here <span class="ar">&rarr;</span></a><a class="btn pai-secondary" href="{MAIN}/">The main site <span class="ar">&rarr;</span></a></div>
</div>
<div class="bdstat" aria-label="This edition in numbers">
<div><div class="n">4</div><p>Season 1 pieces on Bangladesh, three of them in The Daily Star.</p></div>
<div><div class="n">1</div><p>Initiative that could later run here, after its Michigan pilot.</p><span class="st fut">Future possibility</span></div>
</div>
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
<p {P}>The first pilot is proposed for one health center in Michigan, on colorectal cancer screening, including the colonoscopy after a positive test. It has no host clinic yet. Bangladesh is where I have standing and screening-service experience, and the national cervical and breast screening program has published its own follow-up gap, so it is the natural second setting, after that pilot has been evaluated and not before.</p>
<p class="pai-small" style="margin:0">An HSREP initiative in development. No Bangladesh partner, site or funding is confirmed.</p>
</div>
<div class="pai-close" style="margin:0;padding:22px 24px"><p><b>Where the routine could run here.</b><br>The national program, private networks, and the organisations that could matter, named as prospective.</p><a class="btn pai-primary" href="initiative.html">Read the page <span class="ar">&rarr;</span></a></div>
</div>
</section>

<section class="pai-card" id="about" aria-labelledby="abh">
<span class="mono">03 &middot; This edition</span>
<h2 id="abh">Why a .bd address.</h2>
<p class="lede">So that readers, journalists and institutions in Bangladesh have an address that is theirs, and so that the Bangladesh work has a home that does not sit inside the page describing the Michigan pilot.</p>
<div class="bdtwo">
<div><p {P}>Everything else, the articles, the engagement data, the corrections log, the editorial standards, lives on <a href="{MAIN}/" {LINK}>hsraep.org</a> and is not duplicated here. This is the same HSREP, not a separate body.</p></div>
<div><p {P}>Write to <a href="mailto:contact@hsraep.org" {LINK}>contact@hsraep.org</a>. For the initiative, <a href="https://calendly.com/shafaat-alic/30min" {LINK}>book thirty minutes</a>.</p></div>
</div>
</section>
</div>
'''

# ---------- initiative.html ----------
init_body = f'''{BD_CSS}
<section class="pai-hero"><div class="wrap">
<div class="copy">
<span class="pai-chip" style="align-self:flex-start">Future direction &middot; not part of the first pilot</span>
<h1>Finish the tests people already start.</h1>
<p class="dek">The Prevention Adoption Initiative is a weekly routine for recommended care that people begin and do not complete. Its first pilot is proposed for one Michigan health center, on colorectal cancer screening. This page is about what the same routine could look like in Bangladesh, after that pilot has been evaluated. Nothing here has a partner, a date or funding.</p>
<div class="pai-cta"><a class="btn pai-primary" href="{MAIN}/initiative.html">The first pilot, on the main site <span class="ar">&rarr;</span></a><a class="btn pai-secondary" href="index.html">Back to the edition <span class="ar">&rarr;</span></a></div>
</div>
<div class="pai-legend" aria-label="Status labels used on this page">
<div><span class="st prop">Proposed</span>What the first pilot would do, in Michigan</div>
<div><span class="st req">Requires evaluation</span>Only if that pilot passes its month-twelve evaluation</div>
<div><span class="st fut">Future possibility</span>Everything on this page</div>
</div>
</div></section>

<div class="wrap" style="padding:8px 0 56px">
<section class="pai-card" id="routine" aria-labelledby="rth">
<span class="mono">01 &middot; The routine</span>
<h2 id="rth">Four steps, every week, the same in any system.</h2>
<p class="lede">The clinic&rsquo;s own staff run it. HSREP keeps the list and the rules. An independent evaluator judges the result.</p>
{STEPS}
<p class="gpat bdpat"><span class="mono">Invented patient &middot; what one row looks like here</span>Rina B. &middot; VIA-positive at a community clinic &middot; 70 days, no colposcopy &rarr; called in Bangla, booked at the upazila health complex, reminder two days before, transport arranged.</p>
{grid}
</section>

<section class="pai-card" id="partners" aria-labelledby="pth">
<span class="mono">02 &middot; Who could matter</span>
<h2 id="pth">Different partners, different value, same routine.</h2>
<p class="lede">Organisations named here are prospective. None is a confirmed partner, and none has been approached on behalf of this page.</p>
{partners}
</section>

<p class="pai-caveat">Experience in one setting does not show that the routine will work in another. Bangladesh is where I already have standing and screening-service experience; that is a reason to start here one day, not evidence that it would work here. The first pilot, its evaluation and its published toolkit come first.</p>

<div class="pai-close" style="margin-top:28px"><p><b>All of this depends on the first pilot.</b><br>If your organisation wants to talk about a Bangladesh adaptation, that is the conversation to have, after the Michigan pilot has a host.</p><a class="btn pai-primary" href="https://calendly.com/shafaat-alic/30min">Book 30 min <span class="ar">&rarr;</span></a></div>
<p class="pai-small">An HSREP initiative in development. Everything on this page is future direction and illustrative; no patient data has been collected.</p>
</div>
'''

page('index.html', 'HSREP Bangladesh',
     'The Bangladesh edition of HSREP: the Season 1 pieces on Bangladesh, and where the Prevention Adoption Initiative could run after its first pilot.',
     'HSREP Bangladesh', index_body, 'index.html')
page('initiative.html', 'Where the routine could run in Bangladesh - HSREP Bangladesh',
     'What the Prevention Adoption Initiative could look like in Bangladesh after its first pilot: the national screening program, private networks, and the organisations that could matter. None is confirmed.',
     'Where the Prevention Adoption Initiative could run in Bangladesh', init_body, 'initiative.html')

(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % BD)
(ROOT / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join('  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n' % (BD, p, TODAY) for p in ('index.html', 'initiative.html'))
    + '</urlset>\n')
print('done')
