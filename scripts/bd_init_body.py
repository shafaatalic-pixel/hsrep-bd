# New initiative.html body for hsrep.bd (spliced into build.py)

BD_CSS2 = '''<style id="bd2">
.bdside{display:flex;flex-direction:column;gap:14px;align-self:start;min-width:0}
.bdlist{margin:0;border:1px solid var(--pai-line);border-radius:10px;background:#fff;padding:16px 18px 14px;box-shadow:var(--pai-shadow)}
.bdlist figcaption{display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 12px;margin-bottom:8px}
.bdlist .mono{font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.bdlist ol{list-style:none;margin:0;padding:0}
.bdlist li{display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:12px;align-items:center;padding:10px 0;border-top:1px solid var(--pai-soft)}
.bdlist .rk{font-family:var(--font-mono);font-size:12px;color:var(--heading);width:24px;height:24px;border-radius:50%;background:var(--pai-soft);display:grid;place-items:center}
.bdlist .who b{display:block;font-size:14px;color:var(--heading)}
.bdlist .who small{display:block;font-size:12.5px;line-height:1.4;color:var(--muted)}
.bdlist .st{font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--pai-coral-wash);color:var(--pai-coral-text);white-space:nowrap}
.bdlist .st.done{background:var(--pai-green-wash);color:var(--pai-green)}
.bdlist .foot{margin:10px 0 0;padding-top:10px;border-top:1px solid var(--pai-soft);font-size:12.5px;line-height:1.5;color:var(--muted)}
@media(max-width:420px){.bdlist li{grid-template-columns:24px minmax(0,1fr)}.bdlist .st{grid-column:2;justify-self:start}}

.bdfun{margin:8px 0 6px}
.bdfun .row{display:grid;grid-template-columns:200px minmax(0,1fr) 120px;gap:14px;align-items:center;padding:9px 0;border-bottom:1px solid var(--pai-line)}
.bdfun .row:last-child{border-bottom:0}
.bdfun .lab{font-size:14px;line-height:1.35;color:var(--ink)}
.bdfun .lab small{display:block;font-family:var(--font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-top:2px}
.bdfun .bar{height:22px;background:var(--panel);border-radius:4px;overflow:hidden}
.bdfun .bar i{display:block;height:100%;background:var(--heading);border-radius:4px}
.bdfun .row.hot .bar i{background:var(--coral)}
.bdfun .num{font-family:var(--font-mono);font-size:13px;color:var(--heading);text-align:right;white-space:nowrap}
.bdfun .num b{display:block;font-size:1.25rem;line-height:1.1}
.bdsrc{margin:12px 0 0;font-size:12.5px;line-height:1.5;color:var(--muted);max-width:70ch}
.bdsrc a{color:inherit}
.bdrule{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin:22px 0 0;padding:16px 20px;border-left:3px solid var(--coral);background:var(--pai-tint,rgba(242,109,90,.06));border-radius:0 10px 10px 0}
.bdrule b{font-family:var(--font-display);font-size:1.15rem;color:var(--heading)}
.bdrule span{font-size:14.5px;line-height:1.5;color:var(--ink);max-width:60ch}
.bdmodels{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:6px}
.bdm{border:1px solid var(--pai-line);border-radius:12px;padding:20px 20px 18px;background:#fff;display:flex;flex-direction:column;gap:10px}
.bdm.first{border-color:var(--coral);box-shadow:0 0 0 3px rgba(242,109,90,.08)}
.bdm .k{display:flex;justify-content:space-between;align-items:center;gap:8px}
.bdm .k .mono{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--pai-coral-text)}
.bdm h3{margin:0;font-size:1.2rem;line-height:1.25;font-weight:600}
.bdm p{margin:0;font-size:14px;line-height:1.55;color:var(--ink)}
.bdm dl{margin:6px 0 0;display:grid;grid-template-columns:78px minmax(0,1fr);gap:6px 10px;font-size:13.5px;line-height:1.45}
.bdm dt{font-family:var(--font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding-top:3px}
.bdm dd{margin:0;color:var(--ink)}
.bdm .m{margin-top:auto;padding-top:10px;border-top:1px dashed var(--pai-line);font-size:13px;color:var(--heading)}
.bdm .m .mono{color:var(--muted);font-size:10px;letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:3px}
.bdmat{width:100%;border-collapse:collapse;margin-top:4px;font-size:14px;line-height:1.5}
.bdmat th{text-align:left;font-family:var(--font-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500;padding:0 12px 10px 0;border-bottom:2px solid var(--heading)}
.bdmat td{padding:12px 12px 12px 0;border-bottom:1px solid var(--pai-line);vertical-align:top;color:var(--ink)}
.bdmat td:first-child{font-weight:600;color:var(--heading);white-space:nowrap}
.bdmat tr:last-child td{border-bottom:0}
.bdq{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:6px}
.bdq blockquote{margin:0;padding:20px 22px;border-radius:12px;background:var(--heading);color:#D5DEE8;font-size:14.5px;line-height:1.6}
.bdq blockquote .mono{display:block;color:#F2A08F;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px}
.bdq blockquote b{color:#fff}
.bdorg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:6px}
.bdorg div{border-top:2px solid var(--heading);padding-top:10px}
.bdorg .mono{display:block;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--pai-coral-text);margin-bottom:6px}
.bdorg ul{margin:0;padding:0;list-style:none;font-size:14px;line-height:1.6;color:var(--ink)}
.bdchron p b{color:var(--heading)}
.bdchron p.fl{margin-top:8px;padding-top:8px;border-top:1px dashed var(--pai-line);font-size:13px;color:var(--heading)}
.bdpath{margin:-28px 0 28px;padding:16px 20px 12px;border:1px solid var(--pai-line);border-radius:12px;background:#fff}
.bdpath>.mono{display:block;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}
.bdpath ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;counter-reset:p}
.bdpath li{position:relative;padding-left:34px;counter-increment:p;font-size:13.5px;line-height:1.5;color:var(--ink)}
.bdpath li::before{content:counter(p);position:absolute;left:0;top:1px;width:24px;height:24px;border-radius:50%;background:var(--heading);color:#fff;font-family:var(--font-mono);font-size:11px;display:flex;align-items:center;justify-content:center}
.bdpath li b{display:block;font-family:var(--font-display);font-size:1.05rem;color:var(--heading);margin-bottom:3px}
@media(max-width:760px){.bdpath ol{grid-template-columns:1fr}.bdpath{margin-top:-12px}}
.bdsources{margin:0;padding:0;list-style:none;font-size:13px;line-height:1.55;color:var(--ink);columns:2;column-gap:28px}
.bdsources li{break-inside:avoid;margin-bottom:6px}
.bdsources a{color:inherit}
@media(max-width:900px){.bdmodels,.bdq{grid-template-columns:1fr}.bdorg{grid-template-columns:repeat(2,minmax(0,1fr))}.bdsources{columns:1}}
@media(max-width:620px){.bdfun .row{grid-template-columns:1fr;gap:6px}.bdfun .num{text-align:left}.bdorg{grid-template-columns:1fr}.bdmat{font-size:13px}.bdmat td:first-child{white-space:normal}}
</style>'''

SRC = {
 'nessa': 'https://link.springer.com/article/10.1186/s44263-025-00145-x',
 'dash': 'https://cancer-dashboard.mohfw.gov.bd/cervical-breast',
 'ehis': 'https://doi.org/10.1186/s12889-025-22668-6',
 'ncd': 'https://link.springer.com/article/10.1186/s12913-026-14013-3',
 'jhp': 'https://jhpiego.org/our-stories/p/workplace-health-clinics-lead-to-life-saving-care-in-bangladeshs-garment-factories/',
 'unfpa': 'https://www.unfpa.org/press/bangladesh-announces-landmark-%E2%82%AC250-million-investment-womens-health-and-resilient-health-care',
 'bgmea': 'https://unb.com.bd/category/Business/bgmea-secures-special-healthcare-benefits-for-members/172419',
 'tib': 'https://www.dhakatribune.com/bangladesh/corruption/137638/tib-form-independent-body-to-curb-irregularities',
 'ncd360': 'https://www.dailywaadaa.com/health/2026/09/23/bangladesh-seeks-to-shift-health-system-from-treatment-to-prevention',
}


def init_body(MAIN, STEPS, BD_CSS):
    return f'''{BD_CSS}{BD_CSS2}
<section class="pai-hero"><div class="wrap">
<div class="copy">
<span class="pai-chip" style="align-self:flex-start">Future direction &middot; not part of the first pilot</span>
<h1>Six in ten referred women never reach colposcopy. The screening already found them.</h1>
<p class="dek">Bangladesh&rsquo;s national programme screens millions of women and records every positive result. Then it loses most of them at the next step. The Prevention Adoption Initiative is a weekly routine for that step: find who is overdue, rank by urgency, act with a call and a booking and the fare, close when it is done. This page shows how it could run here, first on cancer screening and then on the chronic conditions a corporate check-up finds, who would do what, and who would pay. The design is published; the first pilot is in Michigan; this is the Bangladesh adaptation, ready for a first conversation.</p>
<div class="pai-cta"><a class="btn pai-primary" href="https://calendly.com/shafaat-alic/30min">Talk to me, 30 minutes <span class="ar">&rarr;</span></a><a class="btn pai-secondary" href="assets/HSREP_Prevention_Adoption_Initiative_Brief_Bangladesh.pdf" download>The one-page brief (PDF) <span class="ar">&rarr;</span></a></div>
</div>
<div class="bdside">
<div class="bdstat" aria-label="The gap in numbers">
<div><div class="n">40.4%</div><p>of VIA-positive women reached colposcopy, 2018&ndash;2023. Six in ten did not.</p></div>
<div><div class="n">32%</div><p>of newly diagnosed hypertension and diabetes patients at NCD corners did not return within three months.</p></div>
</div>
<figure class="bdlist" aria-label="What the weekly list looks like, with invented rows">
<figcaption><span class="mono">This week&rsquo;s list &middot; invented rows</span><span class="mono">2 hours &middot; the provider&rsquo;s nurse</span></figcaption>
<ol>
<li><span class="rk">1</span><span class="who"><b>Rina B.</b><small>VIA-positive &middot; 70 days, no colposcopy</small></span><span class="st done">Done, day 76</span></li>
<li><span class="rk">2</span><span class="who"><b>Nasima K.</b><small>VIA-positive &middot; 48 days &middot; missed one booking</small></span><span class="st">Booked, fare sent</span></li>
<li><span class="rk">3</span><span class="who"><b>Shirin A.</b><small>VIA-positive &middot; 23 days</small></span><span class="st">Called in Bangla</span></li>
</ol>
<p class="foot">Ranked by days overdue, days since the positive result and prior no-shows. Three rules, no model. The factory never sees this list.</p>
</figure>
</div>
</div></section>

<div class="wrap"><div class="bdpath" aria-label="How it moves">
<span class="mono">How it moves &middot; every stage ends with its own number</span>
<ol>
<li><b>Michigan, one clinic</b><span>Three months of feasibility, then the clinic decides whether to go to month twelve. An independent evaluator, once one is confirmed, judges against the clinic&rsquo;s own trend; without one, the result is the clinic&rsquo;s own before-and-after.</span></li>
<li><b>Bangladesh, one provider</b><span>Model A: one provider, one factory client, three months, then the same decision. The evaluator here is a university or research institute, named before the start (see 06).</span></li>
<li><b>Then the programme</b><span>Model C goes to the national programme on model A&rsquo;s number, not before. Each stage is judged by the number it set out to move.</span></li>
</ol>
</div></div>

<div class="wrap" style="padding:8px 0 56px">

<section class="pai-card" id="gap" aria-labelledby="gaph">
<span class="mono">01 &middot; The gap</span>
<h2 id="gaph">The system finds people. It loses them after the result.</h2>
<p class="lede">One national cohort, Jan 2018 to May 2023: 1,557,002 women screened by VIA at 497 facilities and 6,398 community clinics. What happened to the women with a positive result:</p>
<div class="bdfun" role="img" aria-label="Of 51,913 VIA-positive women, 20,954 attended colposcopy, 6,205 were treated, and 3,079 have a histopathology report on record">
<div class="row"><div class="lab">VIA-positive<small>3.3% of women screened</small></div><div class="bar"><i style="width:100%"></i></div><div class="num"><b>51,913</b></div></div>
<div class="row hot"><div class="lab">Attended colposcopy<small>the step this page is about</small></div><div class="bar"><i style="width:40.4%"></i></div><div class="num"><b>20,954</b>40.4%</div></div>
<div class="row"><div class="lab">Treated<small>only those who needed it</small></div><div class="bar"><i style="width:12%"></i></div><div class="num"><b>6,205</b></div></div>
<div class="row hot"><div class="lab">Histopathology on record<small>the registry cannot store it</small></div><div class="bar"><i style="width:5.9%"></i></div><div class="num"><b>3,079</b>of 6,205</div></div>
</div>
<p class="bdsrc">Nessa et al., <a href="{SRC['nessa']}" target="_blank" rel="noopener"><i>BMC Global and Public Health</i> 2025;3:34</a>, from the national DHIS2 case-based registry, which already sends each positive woman an SMS. The same shape appears outside cancer: 32% of new NCD-corner patients lost within three months, mostly to medicine stock-outs, transport cost and queues (<a href="{SRC['ncd']}" target="_blank" rel="noopener"><i>BMC Health Services Research</i>, Jan 2026</a>); BRAC&rsquo;s NCD360 could track 22% of the patients it referred into government facilities (<a href="{SRC['ncd360']}" target="_blank" rel="noopener">Daily Waadaa, Sep 2026</a>); factory VIA clinics treat about half of abnormals on site and refer the rest, with nothing published on the referred half (<a href="{SRC['jhp']}" target="_blank" rel="noopener">Jhpiego, Jan 2026</a>).</p>
<div class="bdrule"><b>Nobody in Bangladesh publishes a completion rate for an abnormal result.</b><span>Screening counts are published everywhere. The number that matters, how many positive results reached the next step, is not. That is the number this routine produces.</span></div>
</section>

<section class="pai-card" id="routine" aria-labelledby="rth">
<span class="mono">02 &middot; The routine</span>
<h2 id="rth">Two hours a week, one short list, four steps.</h2>
<p class="lede">The provider&rsquo;s own nurse runs it with a worklist. HSREP keeps the list and the rules. An independent evaluator judges the number. No software to buy, no new staff.</p>
{STEPS}
<p class="gpat bdpat"><span class="mono">Invented patient &middot; what one row looks like</span>Rina B. &middot; VIA-positive at a factory screening camp &middot; 70 days, no colposcopy &rarr; called in Bangla, booked at the medical college colposcopy clinic, fare sent by bKash, reminder the day before, a paid morning off agreed with the factory &rarr; done on day 76.</p>
<div class="bdrule"><b>Paid per completion, never per referral.</b><span>Doctors paid a commission for each test have no reason to chase a patient who already paid, and patients who suspect padded tests have a reason not to come back. In this routine the outreach nurse is paid for the list, and the provider is paid when the woman finishes.</span></div>
</section>

<section class="pai-card" id="models" aria-labelledby="mdh">
<span class="mono">03 &middot; Three ways it could run</span>
<h2 id="mdh">Same routine, three places to put it.</h2>
<p class="lede">In order. The first is small enough to start with one provider and one factory client, and it is where the money for screening is already being spent.</p>
<div class="bdmodels">
<article class="bdm first">
<div class="k"><span class="mono">A &middot; Start here</span></div>
<h3>The referral tail of factory screening</h3>
<p>A private provider already screens garment workers in the factory and refers the women it cannot treat on site. The routine follows those women to the public colposcopy clinic.</p>
<dl>
<dt>The list</dt><dd>The provider&rsquo;s own register of referred women. The factory never sees a result.</dd>
<dt>Who acts</dt><dd>The provider&rsquo;s outreach nurse, two hours a week. The factory doctor or welfare officer releases the right women on the right days.</dd>
<dt>The test</dt><dd>Free at the public colposcopy clinic. Private only where the public clinic is far or slow, at a fixed price.</dd>
<dt>Who pays</dt><dd>The sponsor that already pays for the screening, for example a brand programme, UNFPA, or the factory as a corporate client. A small fee per completed follow-up, plus the fare.</dd>
</dl>
<div class="m"><span class="mono">Measure</span>Share of referred women reaching colposcopy within 90 days, against the national 40.4%.</div>
</article>
<article class="bdm">
<div class="k"><span class="mono">B &middot; Alongside A</span></div>
<h3>A completion contract on corporate check-ups</h3>
<p>A network already sells annual check-ups to employers. Every round produces high blood pressure readings, HbA1c over the line, abnormal creatinine. Then nothing happens. The routine follows each abnormal result to its next step inside the network.</p>
<dl>
<dt>The list</dt><dd>Abnormal results from the network&rsquo;s own corporate check-ups with no next step recorded. See the finish lines below.</dd>
<dt>Who acts</dt><dd>Its outreach staff, paid for the list. No doctor is paid for the referral. One transparent price for the next step.</dd>
<dt>The test</dt><dd>In-house: a repeat reading, a confirmatory test, a doctor visit, the yearly eye and kidney tests.</dd>
<dt>Who pays</dt><dd>The network, and the employer through the check-up contract. It is buying completion from people it already tested, and a product every employer can buy: completion, not a check-up.</dd>
</dl>
<div class="m"><span class="mono">Measure</span>Share of abnormal results that reached their next step within the window, per employer.</div>
</article>
<article class="bdm">
<div class="k"><span class="mono">C &middot; After A</span></div>
<h3>A follow-up cell inside the national programme</h3>
<p>Two or three upazilas use the registry&rsquo;s existing list of VIA-positive women and add what the SMS cannot do.</p>
<dl>
<dt>The list</dt><dd>Already in the DHIS2 tracker, with a national ID.</dd>
<dt>Who acts</dt><dd>The community clinic&rsquo;s own provider: a phone call, a booked slot, the fare; colposcopy and histopathology written back.</dd>
<dt>The test</dt><dd>Public, with contracted private capacity at a fixed price where the public clinic is overloaded.</dd>
<dt>Who pays</dt><dd>It could come from programme money already committed for 2027&ndash;2031, the EIB Women&rsquo;s Health Initiative with UNFPA technical assistance. None of it is agreed for this.</dd>
</dl>
<div class="m"><span class="mono">Measure</span>The national 40.4% in those upazilas, a year later, and the share of treatments with histopathology on record.</div>
</article>
</div>
<p class="pai-small" style="margin-top:14px">Each stage ends with its own number, judged by an independent evaluator named before the start, and the next stage begins on that number.</p>
</section>

<section class="pai-card" id="chronic" aria-labelledby="chh">
<span class="mono">03b &middot; Beyond cancer screening</span>
<h2 id="chh">The same routine on a corporate check-up: three conditions, six finish lines.</h2>
<p class="lede">Chronic disease is where the corporate check-up finds the most abnormal results and does the least about them. Each line below is a recommended step that people start and do not finish, with the size of the condition in Bangladesh and the finish line the pilot would count. Stress and lifestyle are real causes and bad finish lines: they belong in the Act step, never in the measure.</p>
<ol class="gsteps bdsteps bdchron">
<li><span class="mono">01 &middot; Hypertension &middot; first</span><p><b>21% of adults</b> have raised blood pressure; nationally about 14% of those with it are controlled, and the public programme that tracks every patient reaches 58%.</p><p class="fl">Finish lines: a repeat reading on another day and a doctor visit, within the month; a repeat reading at 90 days after treatment starts.</p></li>
<li><span class="mono">02 &middot; Diabetes &middot; second</span><p><b>13% of adults</b>, about 13.9 million people, and 39% of them do not know. HbA1c is already in the check-up.</p><p class="fl">Finish lines: a second test to confirm, with a doctor visit, within the month; HbA1c at 90 days after treatment starts; for everyone already diagnosed, the eye exam and the urine-albumin and eGFR check, at least yearly.</p></li>
<li><span class="mono">03 &middot; Kidney &middot; rides on the panel</span><p><b>About 22% of adults</b> in pooled studies, almost always found late. Creatinine is already in the panel, so an abnormal result costs nothing extra to find.</p><p class="fl">Finish line: a repeat creatinine and urine-albumin test to confirm; chronic means abnormal for three months or more.</p></li>
<li><span class="mono">For factories &middot; anaemia</span><p><b>About eight in ten</b> female garment workers are anaemic in published samples. Haemoglobin is cheap and pairs with the VIA camp.</p><p class="fl">Finish line: a repeat haemoglobin after three months of iron.</p></li>
</ol>
<p class="bdsrc">Raised blood pressure 21.0% and raised blood glucose 8.3%, adults 18&ndash;69: <a href="https://cdn.who.int/media/docs/default-source/searo/bangladesh/bangladesh-ncd-risk-factor-survey-2018.pdf?sfvrsn=266ad1da_1" target="_blank" rel="noopener">WHO STEPS Bangladesh 2018</a>. Control about 14% nationally and 58% in the Bangladesh Hypertension Control Initiative, 328 facilities, March 2026: <a href="https://epidemiology.nhf.org.bd/programs/bhci" target="_blank" rel="noopener">National Heart Foundation</a>. Diabetes 13.2% of adults 20&ndash;79, 13.9 million, 39.1% undiagnosed, 2024: <a href="https://diabetesatlas.org/data-by-location/country/bangladesh/" target="_blank" rel="noopener">IDF Diabetes Atlas</a>. CKD 22.48% pooled: <a href="https://link.springer.com/article/10.1007/s11255-020-02597-6" target="_blank" rel="noopener">Banik et al., Int Urol Nephrol 2021</a>. Anaemia in female garment workers: <a href="https://www.mdpi.com/2072-6643/11/6/1259" target="_blank" rel="noopener">Hossain et al., Nutrients 2019</a>. Finish lines follow the Bangladesh National Hypertension Guideline, the ADA Standards of Care and KDIGO 2024; the windows (the month, 90 days) are the pilot&rsquo;s own and would be set with the clinical lead.</p>
<p class="pai-small" style="margin-top:10px">Declined for now: lipids on their own (the next step is a risk decision, not a test), stress and mental health (no finish line a nurse can close), fatty liver, tobacco.</p>
</section>

<section class="pai-card" id="who" aria-labelledby="whh">
<span class="mono">04 &middot; Who puts in what, who gets what</span>
<h2 id="whh">Why each party would say yes, for model A.</h2>
<p class="lede">Nobody is asked to do a job that is not already theirs, and nobody pays for a test the public clinic gives for free.</p>
<table class="bdmat">
<thead><tr><th>Party</th><th>Puts in</th><th>Gets</th></tr></thead>
<tbody>
<tr><td>Private provider</td><td>Its nurse, two hours a week on the worklist</td><td>The colposcopies, biopsies and pathology on referred cases where private, by contract; a per-completion fee; a completion rate to sell to the next corporate client</td></tr>
<tr><td>Factory</td><td>The worker&rsquo;s paid morning; a room on screening day; fifteen minutes a week from the welfare officer</td><td>Compliance evidence for buyers; fewer women lost to long illness</td></tr>
<tr><td>Sponsor (brand, UNFPA or the factory as client)</td><td>The screening it already funds; a small fee per completed follow-up; the fare</td><td>A completion rate per factory instead of a screening count</td></tr>
<tr><td>Public programme</td><td>Nothing new. The colposcopy clinics exist</td><td>Its 40.4% moving; results written back to the registry when the camp runs under the programme</td></tr>
<tr><td>The woman</td><td>Nothing</td><td>Reaches the next step, with the morning paid and the fare covered</td></tr>
<tr><td>HSREP</td><td>The worklist, the three rules, the training, the written routine. The sponsor or the provider pays for the founder&rsquo;s time; HSREP adds no fee on top</td><td>The first published completion number in Bangladesh, and the toolkit</td></tr>
</tbody>
</table>
</section>

<section class="pai-card" id="plain" aria-labelledby="plh">
<span class="mono">05 &middot; In plain words</span>
<h2 id="plh">What I would say in the room.</h2>
<div class="bdq">
<blockquote><span class="mono">If you run a private network</span>You already screen factory workers. Around six in a hundred have an abnormal result; some you treat that day, the rest you refer, and then nobody knows. <b>Your nurse keeps the list of referred women and works it two hours a week: call, book, send the fare, remind, write down when it is done.</b> The follow-up cases come to you by contract, and you get a number no one else here has. One network, three months, one factory client, then a decision.</blockquote>
<blockquote><span class="mono">If you fund factory screening</span>Your screening finds the women. The programme loses them at the next step: nationally, four in ten reach colposcopy. <b>Add a small fee per completed follow-up and the fare. The test itself is free at the public clinic.</b> You get, for the first time, a completion rate per factory instead of a screening count.</blockquote>
<blockquote><span class="mono">If you run the national programme</span>Your registry already lists every VIA-positive woman and sends her an SMS. <b>In two or three upazilas, add a phone call from the community clinic, a booked slot, the fare, and the result written back, including histopathology.</b> The measure is your own 40.4%, in those upazilas, a year later.</blockquote>
</div>
</section>

<section class="pai-card" id="partners" aria-labelledby="pth">
<span class="mono">06 &middot; Who could matter</span>
<h2 id="pth">Organisations that fit, none of them confirmed.</h2>
<p class="lede">Named because of what they already do, not because they have agreed to anything. None has been approached on behalf of this page.</p>
<div class="bdorg">
<div><span class="mono">Providers (model A, B)</span><ul><li>The ten providers under BGMEA&rsquo;s member-care MoUs of Nov 2025, including Praava, United, LabAid and Popular</li><li>Surjer Hashi Network</li><li>Grameen Kalyan</li></ul></div>
<div><span class="mono">Screening and sponsors (A)</span><ul><li>UNFPA Bangladesh and Jhpiego, whose factory clinics already screen</li><li>Brand worker-health programmes</li><li>BGMEA, as a door to member factories, not an operator</li></ul></div>
<div><span class="mono">Public programme (C)</span><ul><li>DGHS Non-Communicable Disease Control Programme</li><li>The national cervical and breast screening programme at Bangladesh Medical University</li><li>Community Clinic Health Support Trust</li></ul></div>
<div><span class="mono">Evaluation (all)</span><ul><li>Bangladesh Medical University</li><li>icddr,b</li><li>BRAC James P Grant School of Public Health</li></ul></div>
</div>
</section>

<section class="pai-card" id="sources" aria-labelledby="srh">
<span class="mono">07 &middot; Sources and status</span>
<h2 id="srh">Where the numbers come from.</h2>
<ul class="bdsources">
<li>Nessa A, et al. Cervical cancer screening programme in Bangladesh: the national registry, 2018&ndash;2023. <a href="{SRC['nessa']}" target="_blank" rel="noopener">BMC Global and Public Health 2025;3:34</a>.</li>
<li>MOHFW, National Cervical &amp; Breast Cancer Statistics of Bangladesh. <a href="{SRC['dash']}" target="_blank" rel="noopener">cancer-dashboard.mohfw.gov.bd</a>.</li>
<li>The e-HIS case-based registry and its gaps. <a href="{SRC['ehis']}" target="_blank" rel="noopener">BMC Public Health, May 2025</a>.</li>
<li>Retention at NCD corners, 12 upazilas, 2023. <a href="{SRC['ncd']}" target="_blank" rel="noopener">BMC Health Services Research, Jan 2026</a>.</li>
<li>Factory VIA clinics, five factories. <a href="{SRC['jhp']}" target="_blank" rel="noopener">Jhpiego, 21 Jan 2026</a>.</li>
<li>EIB Women&rsquo;s Health Initiative, 2027&ndash;2031. <a href="{SRC['unfpa']}" target="_blank" rel="noopener">UNFPA, 10 Oct 2026</a>.</li>
<li>BGMEA member-care MoUs with ten providers. <a href="{SRC['bgmea']}" target="_blank" rel="noopener">UNB, 6 Nov 2025</a>.</li>
<li>Commission-based referral, 66 hospitals and 50 diagnostic centres. <a href="{SRC['tib']}" target="_blank" rel="noopener">TIB via Dhaka Tribune, 7 Feb 2018</a>.</li>
<li>BRAC NCD360 referral tracking. <a href="{SRC['ncd360']}" target="_blank" rel="noopener">Daily Waadaa, 23 Sep 2026</a>.</li>
<li>Raised blood pressure and blood glucose, adults 18&ndash;69. <a href="https://cdn.who.int/media/docs/default-source/searo/bangladesh/bangladesh-ncd-risk-factor-survey-2018.pdf?sfvrsn=266ad1da_1" target="_blank" rel="noopener">WHO STEPS Bangladesh 2018</a>.</li>
<li>Hypertension control, national and programme. <a href="https://epidemiology.nhf.org.bd/programs/bhci" target="_blank" rel="noopener">National Heart Foundation, BHCI, Mar 2026</a>.</li>
<li>Diabetes, adults 20&ndash;79, 2024. <a href="https://diabetesatlas.org/data-by-location/country/bangladesh/" target="_blank" rel="noopener">IDF Diabetes Atlas</a>.</li>
<li>Chronic kidney disease, pooled prevalence. <a href="https://link.springer.com/article/10.1007/s11255-020-02597-6" target="_blank" rel="noopener">Banik et al., Int Urol Nephrol 2021</a>.</li>
<li>Anaemia among female garment workers. <a href="https://www.mdpi.com/2072-6643/11/6/1259" target="_blank" rel="noopener">Hossain et al., Nutrients 2019</a>.</li>
<li>Next steps: <a href="https://prescribingcompanion.com/bangladesh/other-common-clinical-conditions/hypertension-national-guideline/chapter-5-management-of-hypertension/53-pharmacological-management" target="_blank" rel="noopener">Bangladesh National Hypertension Guideline</a>; <a href="https://diabetesjournals.org/care/article/48/Supplement_1/S27/157566/2-Diagnosis-and-Classification-of-Diabetes" target="_blank" rel="noopener">ADA Standards of Care 2025</a>; <a href="https://kdigo.org/wp-content/uploads/2026/05/KDIGO-2024-CKD-Guideline-Summary-Recommendations-and-Practice-Points.pdf" target="_blank" rel="noopener">KDIGO 2024</a>.</li>
</ul>
<div style="margin:16px 0 4px"><a class="btn ghost" href="assets/HSREP_Prevention_Adoption_Initiative_Brief_Bangladesh.pdf" download>The one-page brief (PDF)</a></div>
<p class="pai-caveat" style="margin-top:18px">Experience in one setting does not show that the routine will work in another. Bangladesh is where I already have standing and screening-service experience; that is a reason to start here one day, not evidence that it would work here. The first pilot in Michigan, its evaluation and its published toolkit come first. Figures above are from the sources named; none is HSREP&rsquo;s own data.</p>
</section>

<div class="pai-close"><p><b>All of this depends on the first pilot.</b><br>If you run a provider, fund factory screening, or sit inside the programme, and you want to talk about the step after the referral, that is the conversation to have.</p><a class="btn pai-primary" href="https://calendly.com/shafaat-alic/30min">Book 30 min <span class="ar">&rarr;</span></a></div>
<p class="pai-small">An HSREP initiative in development. The design is published; a Bangladesh partner, site and funding come next. Everything on this page is illustrative, and no patient data has been collected.</p>
</div>
'''
