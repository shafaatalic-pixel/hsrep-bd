#!/usr/bin/env python3
"""Build the HSREP Bangladesh edition (hsrep.bd) from the main site's roadmap page.

Run from the hsrep-bd repo root:  python3 scripts/build.py
Reads ../website/initiative-next.html for the head, header, footer and scripts,
and scripts/_orig_initiative-next.html (main at f377a49) for the Bangladesh
material that left the main site on 21 Oct 2026.
"""
import re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = (ROOT.parent / 'website' / 'initiative-next.html').read_text(encoding='utf-8')
ORIG = (ROOT / 'scripts' / '_orig_initiative-next.html').read_text(encoding='utf-8')
MAIN = 'https://hsraep.org'
BD = 'https://hsrep.bd'
TODAY = '2026-10-21'

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
tail = tail.replace(old_tag, old_tag[:-4] + ' This is the Bangladesh edition; the record of work is on <a href="%s/" style="color:inherit">hsraep.org</a>.</p>' % MAIN)

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
assert 'sysp-grid' in bd_block and 'for-publicbd' in bd_block and 'Brief_Bangladesh.pdf' in bd_block
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


H3 = 'style="margin:30px 0 14px;font-size:1.35rem;font-weight:600;scroll-margin-top:90px"'
P = 'style="margin:0 0 14px;font-size:15px;line-height:1.6;max-width:66ch"'

# ---------- index.html ----------
articles = [
    ('The Daily Star · Commentary', 'Increasing public health investment must be a top priority',
     'Why health financing is economic protection, not a residual cost line.',
     'articles/increasing-public-health-investment/increasing-public-health-investment.html'),
    ('The Daily Star · Commentary', 'Can we use private healthcare to improve health literacy?',
     'When patients cannot read the system, costs rise for everyone.',
     'articles/private-healthcare-health-literacy/private-healthcare-health-literacy.html'),
    ('HSREP · Special report', 'When the Ground Shakes, Neighbors Respond First',
     'Community preparedness as Dhaka&rsquo;s most affordable defense against a catastrophic earthquake.',
     'articles/when-the-ground-shakes/when-the-ground-shakes.html'),
    ('The Daily Star · Earlier piece, 2025', 'We need public health reform for steady economic growth',
     'The earliest foundation piece connecting reform to growth.',
     'articles/public-health-reform-for-economic-growth/public-health-reform-for-economic-growth.html'),
]
cards = ''.join(
    '<div class="gcard"><div class="n">%s</div><h3>%s</h3><p>%s</p><p style="margin-top:10px"><a href="%s/%s" style="color:var(--coral);text-decoration:none;border-bottom:1px solid rgba(242,109,90,.45)">Read on hsraep.org &rarr;</a></p></div>'
    % (lab, t, d, MAIN, href) for lab, t, d, href in articles)

index_body = f'''
<section class="pai-hero"><div class="wrap">
<div class="copy">
<span class="pai-chip" style="align-self:flex-start">Bangladesh edition</span>
<h1>HSREP in Bangladesh.</h1>
<p class="dek">HSREP is an independent public-health research and advocacy platform, founded in Michigan by Md Shafaat Ali Choyon, MBA, MCIM, MPH, CHES&reg;. Its first season examined health systems in the United States and Bangladesh. This edition collects the Bangladesh side: the Season 1 pieces written for readers here, and what the Prevention Adoption Initiative could look like in Bangladesh once its first pilot has been evaluated.</p>
<div class="pai-cta"><a class="btn pai-primary" href="initiative.html">Where the routine could run here <span class="ar">&rarr;</span></a><a class="btn pai-secondary" href="{MAIN}/">The main site <span class="ar">&rarr;</span></a></div>
</div>
<div class="pai-legend" aria-label="What this edition is">
<div><span class="st prop">Published</span>Four Season 1 pieces on Bangladesh, three of them in The Daily Star</div>
<div><span class="st fut">Future possibility</span>A Bangladesh adaptation of the initiative, with no partner, date or funding yet</div>
<div><span class="st req">One HSREP</span>Not a separate body; the same HSREP, with a .bd address for readers and institutions here</div>
</div>
</div></section>

<div class="wrap" style="padding:36px 0 56px">
<h2 id="season-1" style="font-size:1.6rem;margin:0 0 6px">Season 1, the Bangladesh pieces</h2>
<p {P}>Season 1 was one argument told across nine pieces in two countries: that health protection is economic infrastructure, not a residual budget line. These are the four about Bangladesh. The full season, its engagement record and its methodology are on the main site.</p>
<style>.bdgrid{{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:700px){{.bdgrid{{grid-template-columns:1fr}}}}</style>
<div class="grid3 bdgrid">{cards}</div>
<p style="margin:14px 0 0;font-size:13px;color:var(--muted)"><a href="{MAIN}/season-1.html" style="color:inherit">Season 1 record</a> &middot; <a href="{MAIN}/methodology.html" style="color:inherit">Methods and sources</a></p>

<h2 id="initiative" {H3.replace('1.35rem','1.6rem').replace('30px 0 14px','44px 0 6px')}>The Prevention Adoption Initiative, and Bangladesh</h2>
<p {P}>The initiative is a weekly routine for recommended care that people start and do not finish: find who is overdue, rank by urgency, act with a call or a kit or a ride, and close the loop when the test is done. Its first pilot is proposed for one health center in Michigan, on colorectal cancer screening. That pilot has no host clinic yet.</p>
<p {P}>Bangladesh is where I have standing and screening-service experience, and the national cervical and breast screening program has published its own follow-up gap. So it is the natural second setting, after the first pilot has been evaluated and not before. The page on <a href="initiative.html">where the routine could run here</a> keeps that plan in one place, with the organisations that could matter named as prospective and none of them confirmed.</p>
<p class="pai-small" style="margin-top:6px">An HSREP initiative in development. No Bangladesh partner, site or funding is confirmed.</p>

<h2 id="about" {H3.replace('1.35rem','1.6rem').replace('30px 0 14px','44px 0 6px')}>Why a .bd address</h2>
<p {P}>So that readers, journalists and institutions in Bangladesh have an address that is theirs, and so that the Bangladesh work has a home that does not sit inside the page describing the Michigan pilot. Everything else, the articles, the engagement data, the corrections log, the editorial standards, lives on <a href="{MAIN}/">hsraep.org</a> and is not duplicated here.</p>
<p {P}>Write to <a href="mailto:contact@hsraep.org">contact@hsraep.org</a>. For the initiative, <a href="https://calendly.com/shafaat-alic/30min">book thirty minutes</a>.</p>
</div>
'''

# ---------- initiative.html ----------
init_body = f'''
<section class="pai-hero"><div class="wrap">
<div class="copy">
<span class="pai-chip" style="align-self:flex-start">Future direction &middot; not part of the first pilot</span>
<h1>Finish the tests people already start.</h1>
<p class="dek">The Prevention Adoption Initiative is a weekly routine, Find, Rank, Act, Close, for recommended care that people begin and do not complete. Its first pilot is proposed for one Michigan health center, on colorectal cancer screening. This page is about what the same routine could look like in Bangladesh, after that pilot has been evaluated. Nothing here has a partner, a date or funding.</p>
<div class="pai-cta"><a class="btn pai-primary" href="{MAIN}/initiative.html">The first pilot, on the main site <span class="ar">&rarr;</span></a><a class="btn pai-secondary" href="index.html">Back to the edition <span class="ar">&rarr;</span></a></div>
</div>
<div class="pai-legend" aria-label="Status labels used on this page">
<div><span class="st prop">Proposed</span>What the first pilot would do, in Michigan</div>
<div><span class="st req">Requires evaluation</span>Only if that pilot passes its month-twelve evaluation</div>
<div><span class="st fut">Future possibility</span>Everything on this page</div>
</div>
</div></section>

<div class="wrap" style="padding:36px 0 56px">
<div class="cview"><div><span class="mono">Where it could run</span><p>Community clinics under the national cervical and breast screening program, and private diagnostic networks.</p></div><div><span class="mono">Status</span><p><b style="color:var(--heading)">A future direction, in development.</b></p></div></div>
{bd_block}
<p class="pai-caveat">Experience in one setting does not show that the routine will work in another. Bangladesh is where I already have standing and screening-service experience; that is a reason to start here one day, not evidence that it would work here. The first pilot, its evaluation and its published toolkit come first.</p>
</div>

<div class="wrap" style="padding-bottom:56px">
<div class="pai-close"><p><b>All of this depends on the first pilot.</b><br>If your organisation wants to talk about a Bangladesh adaptation, that is the conversation to have, after the Michigan pilot has a host.</p><a class="btn pai-primary" href="https://calendly.com/shafaat-alic/30min">Book 30 min <span class="ar">&rarr;</span></a></div>
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
