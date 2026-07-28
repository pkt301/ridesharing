#!/usr/bin/env python3
"""Second-pass: deepen short SEO blocks to ~600+ unique words each."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- SEO-EXPANDED-v2 -->"
END = "<!-- /SEO-EXPANDED-v2 -->"
TODAY = "2026-07-29"


def words(html: str) -> int:
    return len(re.sub(r"<[^>]+>", " ", html).split())


def faq_html(faqs):
    return '<div class="faq">\n' + "\n".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    ) + "\n</div>"


def faq_ld(faqs):
    ents = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)},
        }
        for q, a in faqs
    ]
    return (
        '<!-- SEO-FAQ-v2 -->\n<script type="application/ld+json">\n'
        + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ents}, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


DEEP: dict[str, tuple[str, list[tuple[str, str]]]] = {}


def add(rel: str, html: str, faqs: list[tuple[str, str]]):
    DEEP[rel] = (html, faqs)


# --- Sustainability (all need deepening) ---
add(
    "sustainability/reduce-air-pollution-commute.html",
    """
<h2>How daily commuting shapes neighbourhood air</h2>
<p>In Indian metros, a large share of local air pollution near roads comes from vehicles idling and crawling in peak traffic. When four colleagues drive four separate cars along the same 18 km corridor, the city burns roughly four times the fuel for the same human movement. <strong>Seat share attacks that duplication</strong> without waiting for a new metro line to open next year.</p>
<p>You cannot personally fix a city’s AQI overnight. You can change the occupancy of the vehicle you influence this week. That is the honest scale of individual climate and health action for office-goers.</p>
<h2>A corridor-first pollution strategy</h2>
<ol>
<li><strong>Identify your duplicated route.</strong> If five people on your floor travel Softwarde/IT park → the same society belt, you already have a carpool cohort.</li>
<li><strong>Convert the worst peak days first.</strong> Monday and Friday congestion often produce the most idling minutes per kilometre.</li>
<li><strong>Keep Favourites.</strong> Random matching every morning creates friction; recurring partners create habit.</li>
<li><strong>Hybrid with transit.</strong> Use metro/bus for dense core segments; use Rydo seat share for awkward office-park last miles.</li>
<li><strong>Measure something simple.</strong> Count shared days per month and fuel money avoided — motivation needs numbers.</li>
</ol>
<h2>Vehicle habits that still matter</h2>
<ul>
<li>Maintain tyre pressure and service schedules if you captain</li>
<li>Avoid unnecessary revs in standstill queues</li>
<li>Combine errands instead of three cold-start micro-trips</li>
<li>Prefer shaded, quick pickups so engines are not idling five extra minutes</li>
</ul>
<div class="callout green">Rydo is private carpool &amp; seat share — not a taxi. Filling empty seats on trips already happening is the pollution lever.</div>
<h2>Health co-benefits</h2>
<p>Lower personal stress from solo peak driving, optional last-mile walking, and fewer minutes in dense exhaust plumes are practical co-benefits. On severe pollution days, still use masks as personal protection while you reduce emissions at the source.</p>
<p>Continue with <a href="../sustainability/carpool-carbon-footprint.html">carbon footprint</a>, <a href="../sustainability/fewer-cars-better-cities.html">fewer cars, better cities</a>, and the <a href="../sustainability/green-commute-challenge.html">30-day green commute challenge</a>.</p>
""",
    [
        ("Does one shared ride change AQI?", "One trip is small; thousands of shared seats on the same belt reduce duplicated fuel burn and idling."),
        ("Is metro always cleaner?", "Dense electric transit is excellent where it fits. Carpool wins when it replaces multiple private cars on the same road."),
        ("What should offices do?", "Encourage corridor cohorts, staggered timing, and transparent fuel-share norms — not forced commercial cab reimbursements for every hop."),
        ("How do I start this week?", "Download Rydo, post your recurring route, and convert two peak weekdays to shared seats."),
    ],
)

add(
    "sustainability/green-commute-challenge.html",
    """
<h2>Why a 30-day challenge works better than vague goals</h2>
<p>“I should carpool more” fails because it has no start date, no metric, and no social accountability. A 30-day challenge gives you a container: baseline → experiments → lock-in.</p>
<h2>Week-by-week operating manual</h2>
<h3>Week 1 — Baseline without judgement</h3>
<ul>
<li>Log every commute mode and approximate cost</li>
<li>Run the <a href="../cost-calculators/index.html">daily travel cost calculator</a></li>
<li>Note your two worst traffic days</li>
</ul>
<h3>Week 2 — Two shared weekdays minimum</h3>
<ul>
<li>Match on Rydo for your primary corridor</li>
<li>Use OTP and live GPS every time</li>
<li>Write one sentence after each trip: punctual? comfortable? repeat?</li>
</ul>
<h3>Week 3 — Cut two micro-trips</h3>
<ul>
<li>Replace short errand drives with walking or combining stops</li>
<li>Keep shared office days going</li>
</ul>
<h3>Week 4 — Lock the system</h3>
<ul>
<li>Favourite reliable partners</li>
<li>Publish a stable window for next month</li>
<li>Recalculate savings and share the number with your household</li>
</ul>
<h2>Scoring that does not create guilt</h2>
<p>Missed a day? Restart the next morning. The prize is a durable Favourites group, not a perfect streak screenshot.</p>
<p>Team version: five colleagues on one corridor, shared Sunday planning message, Friday fuel settle-up.</p>
""",
    [
        ("Can remote workers join?", "Yes — share on the days you still go to office or airport."),
        ("What if partners flake?", "Keep two Favourites; reliability is part of the challenge score."),
        ("Do I need an EV?", "No. Occupancy is the first lever; cleaner vehicles are a bonus."),
        ("Where do I track savings?", "Calculator results + fuel wallet spends once a month."),
    ],
)

add(
    "sustainability/fewer-cars-better-cities.html",
    """
<h2>The empty-seat problem is an urban design problem</h2>
<p>Indian cities keep adding flyovers and widening arterials, then watch peak congestion return. Capacity filled with single-occupant cars recreates the same queue one level higher. <strong>Better cities need fewer redundant car trips</strong>, not only more asphalt.</p>
<h2>What “fewer cars” actually means</h2>
<p>It does not mean banning private vehicles. It means raising average occupancy, shifting some trips to walking/transit, and stopping the ritual of one person / one car / one duplicated corridor.</p>
<ul>
<li>Higher occupancy per vehicle on office belts</li>
<li>Less circling for scarce parking</li>
<li>Quieter peaks when many people shift 15–30 minutes</li>
<li>More predictable travel times for buses too</li>
</ul>
<h2>Culture beats slogans</h2>
<ol>
<li>Office cohorts that carpool the same window</li>
<li>Society groups that share school/office overlaps</li>
<li>Apps like Rydo that add OTP, GPS, and Favourites beyond messy chat threads</li>
<li>Managers who treat punctual shared travel as professional, not weird</li>
</ol>
<p>Read <a href="../blog/traffic-problem-in-indian-cities.html">traffic problems in Indian cities</a> and start a corridor habit with the <a href="../sustainability/green-commute-challenge.html">green commute challenge</a>.</p>
""",
    [
        ("Is this anti-car?", "No — anti empty-seat inefficiency."),
        ("Can policy help?", "Yes — but apps and office culture can coordinate occupancy today."),
        ("What about delivery traffic?", "Different problem. This guide focuses on duplicated passenger trips."),
        ("First personal step?", "Fill empty seats on your existing weekday route via Rydo."),
    ],
)

add(
    "sustainability/sustainable-transportation-guide.html",
    """
<h2>A realistic sustainable transport menu for India</h2>
<p>Perfect purity is a trap. Most people need a <strong>stack</strong> of modes that fit weather, distance, luggage, and safety.</p>
<ol>
<li><strong>Walk / cycle</strong> for micro-trips when pavements and lighting are safe</li>
<li><strong>Metro / bus / suburban rail</strong> for dense corridors</li>
<li><strong>Carpool / seat share</strong> for awkward office-park legs and recurring highway shares</li>
<li><strong>Solo vehicle</strong> when schedules truly do not match</li>
</ol>
<h2>Where Rydo fits</h2>
<p>Rydo focuses on lever #3: coordinating private travellers who already share a route. It is not a commercial taxi product and does not use surge pricing. OTP, live GPS, messaging, and Favourites make private seat share more structured than informal WhatsApp chaos.</p>
<h2>Weekly sustainable commute template</h2>
<ul>
<li>Mon–Thu: try shared seats on the longest office leg</li>
<li>One day: transit hybrid experiment</li>
<li>Weekend: combine errands; highway shares only with clear fuel/toll splits</li>
<li>Month-end: recalculate costs after fuel price moves</li>
</ul>
<p>Safety remains non-negotiable — see <a href="../safety-guides/index.html">safety guides</a>.</p>
""",
    [
        ("Is sustainability only for metros?", "No. Any corridor with duplicated solo trips benefits."),
        ("Are EVs enough?", "EVs help tailpipes; empty seats still waste road space."),
        ("How to convince family?", "Show monthly calculator savings and safety tools (OTP + GPS)."),
        ("Start today?", "Download Rydo and convert two weekdays this week."),
    ],
)

add(
    "sustainability/carpool-carbon-footprint.html",
    """
<h2>Carbon math without fake precision</h2>
<p>You do not need a laboratory to understand the direction of travel: <strong>fewer vehicle-kilometres for the same passenger-kilometres</strong> means less fuel burned. If your corridor currently moves four people in four cars, moving them in two cars roughly halves the car-kilometres for that group.</p>
<h2>Practical footprint levers ranked</h2>
<ol>
<li>Share seats 3–5 commute days weekly (largest)</li>
<li>Eliminate cold-start micro-trips</li>
<li>Maintain the vehicle if you captain</li>
<li>Choose efficient routes / avoid needless detours</li>
<li>Consider cleaner fuels/EVs over time</li>
</ol>
<h2>How to track without apps overload</h2>
<ul>
<li>Shared-day counter on your phone notes</li>
<li>Monthly fuel spend</li>
<li>Calculator snapshot each month</li>
</ul>
<div class="callout">Direction beats decimal places. A messy habit of shared peak days beats a perfect spreadsheet with zero behaviour change.</div>
<p>Next: <a href="../sustainability/reduce-air-pollution-commute.html">air pollution commute guide</a> · <a href="../sustainability/green-commute-challenge.html">30-day challenge</a>.</p>
""",
    [
        ("Is carpool greener than metro?", "Metro can win on dense electrified corridors; carpool wins by replacing multiple private cars."),
        ("Do I need carbon certificates?", "No — personal occupancy habits are the point here."),
        ("What about two-wheelers?", "Lower footprint than cars often, but monsoon/safety trade-offs matter; mix modes."),
        ("Company commuting schemes?", "Corridor cohorts + Rydo Favourites are a lightweight start."),
    ],
)

# Generic deepener factory for remaining short pages
TEMPLATES = {
    "safety": """
<h2>Expanding the {title} playbook</h2>
<p>{lead}</p>
<h2>Step-by-step routine you can repeat</h2>
<ol>
{steps}
</ol>
<h2>Mistakes that create avoidable risk</h2>
<ul>
{mistakes}
</ul>
<h2>Tools inside Rydo that support this guide</h2>
<ul>
<li>OTP verification before trip start</li>
<li>Live GPS tracking on longer segments</li>
<li>In-app messaging for landmark clarity</li>
<li>Favourites for recurring trusted partners</li>
<li>Trip completion records / receipts where available</li>
</ul>
<div class="callout green"><strong>Remember:</strong> Rydo is private carpool &amp; seat share — not a taxi. Safety habits still matter on every matched ride.</div>
<h2>Related safety reading</h2>
<p><a href="../safety-guides/index.html">Safety hub</a> · <a href="../safety-guides/otp-ride-safety.html">OTP guide</a> · <a href="../safety-guides/travel-safety-guide.html">Travel safety</a> · <a href="../blog/carpool-etiquette.html">Etiquette</a></p>
""",
    "commuter": """
<h2>Going deeper on {title}</h2>
<p>{lead}</p>
<h2>Weekly system</h2>
<ol>
{steps}
</ol>
<h2>Money, time, and stress levers</h2>
<ul>
{mistakes}
</ul>
<h2>How Rydo helps this habit stick</h2>
<p>Publish a stable route window, match riders/captains going your way, verify with OTP, track live, and favourite the people who make Mondays calmer. Estimate savings anytime with the <a href="../cost-calculators/index.html">cost calculators</a>.</p>
<div class="callout">Not a taxi: contributions are voluntary fuel/toll sharing among private travellers.</div>
<h2>Keep learning</h2>
<p><a href="../commuter-tips/index.html">Commuter tips hub</a> · <a href="../city-guides/index.html">City guides</a> · <a href="../blog/how-rydo-works.html">How Rydo works</a></p>
""",
    "travel": """
<h2>Detailed planning notes: {title}</h2>
<p>{lead}</p>
<h2>Planning checklist</h2>
<ol>
{steps}
</ol>
<h2>Friction points to resolve in chat before you start</h2>
<ul>
{mistakes}
</ul>
<h2>On the road</h2>
<p>Use OTP at start, keep live GPS on for unfamiliar segments, update partners if you divert, and settle fuel/toll shares the same day via UPI when possible.</p>
<p>More: <a href="../travel-guides/index.html">Travel guides</a> · <a href="../safety-guides/index.html">Safety</a> · <a href="../travel-guides/highway-carpool-india.html">Highway carpool</a></p>
""",
    "blog": """
<h2>Extra depth: {title}</h2>
<p>{lead}</p>
<h2>Action checklist</h2>
<ol>
{steps}
</ol>
<h2>Common pitfalls</h2>
<ul>
{mistakes}
</ul>
<h2>Where this connects to Rydo</h2>
<p>Rydo helps Indian riders and captains coordinate recurring routes with OTP, live GPS, messaging, Favourites, and transparent fuel-cost sharing — not commercial taxi surge pricing.</p>
<p><a href="https://play.google.com/store/apps/details?id=com.godrive.rideshare" target="_blank" rel="noopener noreferrer">Download on Google Play</a> · support <a href="mailto:pktiwari110487@gmail.com">pktiwari110487@gmail.com</a> · <a href="tel:+919026317151">+91 9026317151</a></p>
""",
}

PAGE_META = {
    # safety leftovers if any need replace - we'll replace all safety with deeper if short
    "safety-guides/emergency-contacts-ride-sharing.html": (
        "safety",
        "Emergency contacts for ride sharing",
        "A written emergency list turns chaos into a sequence. Store numbers offline and practise sharing live location before you need it on a dark highway segment.",
        "<li>Save two personal contacts who answer quickly</li><li>Add local police / women’s helpline for your city</li><li>Add roadside assistance if you drive</li><li>Add Rydo support email and phone</li><li>Test live-location sharing once</li>",
        "<li>Relying only on memory under stress</li><li>Phone below 10% battery on long trips</li><li>No one knowing your ETA</li><li>Skipping OTP because you feel rushed</li>",
        [
            ("Should kids’ numbers be in the list?", "Include parent/guardian contacts when travelling with family."),
            ("International numbers?", "For domestic Indian corridors, local emergency numbers matter most."),
            ("What if network dies?", "Keep key numbers written; move to a busy lit place and borrow a call if needed."),
            ("Support vs police?", "Crime/medical → emergency services first; product issues → Rydo support."),
        ],
    ),
    "safety-guides/night-commute-safety.html": (
        "safety",
        "Night commute safety",
        "Night travel is common for IT shifts and late offices. The goal is boring predictability: known partners, bright pickups, verification, and shared ETAs.",
        "<li>Prefer Favourites after dark</li><li>Choose busy lit pickups</li><li>Confirm vehicle details before boarding</li><li>OTP on, tracking on</li><li>Message family your drop window</li>",
        "<li>Dark service-lane pickups</li><li>Skipping OTP</li><li>Heavy cash display</li><li>Unannounced long detours</li>",
        [
            ("Is night share ever OK for first meetings?", "Prefer daytime first rides; night only with strong verification and busy landmarks."),
            ("Captain delayed?", "Wait only in safe public places; renegotiate via chat."),
            ("Headphones?", "Keep volume low enough to stay aware."),
            ("Women travellers?", "See the women ride safety guide and Favourites habits."),
        ],
    ),
    "safety-guides/otp-ride-safety.html": (
        "safety",
        "OTP ride safety",
        "OTP is the handshake that links the digital match to the physical vehicle. Skipping it for speed recreates the exact risk the feature was built to reduce.",
        "<li>Open the matched ride screen</li><li>Captain asks for the current OTP</li><li>Enter/verify before moving</li><li>Confirm tracking active</li><li>Complete trip only after drop</li>",
        "<li>Sharing OTP in public groups</li><li>Using old screenshots</li><li>Boarding lookalike cars</li><li>Starting without verification when late</li>",
        [
            ("OTP fails repeatedly?", "Do not start — re-check match or contact support."),
            ("Can someone overhear OTP?", "Speak quietly; prefer in-person verification at the door."),
            ("Short trips need OTP?", "Yes — wrong-car risk exists on short hops too."),
            ("After OTP, still unsafe feeling?", "Stop at a busy place and end the trip."),
        ],
    ),
    "safety-guides/rainy-weather-travel-safety.html": (
        "safety",
        "Rainy weather travel safety",
        "Monsoon turns familiar corridors hostile. Shared rides need earlier decisions, backup landmarks, and permission to cancel without drama.",
        "<li>Check flood-prone underpasses</li><li>Agree Landmark B</li><li>Leave earlier</li><li>Pack rain covers</li><li>Cancel early if roads close</li>",
        "<li>Unknown flooded short-cuts</li><li>Pressure to “just try”</li><li>Soaked bags on seats without care</li><li>Arguments about delays instead of buffers</li>",
        [
            ("Who decides cancel?", "Anyone who feels unsafe should speak early."),
            ("Two-wheeler shares in rain?", "High caution; cars usually better for wet shared trips."),
            ("Fuel share if turned back?", "Agree partial fairness in chat."),
            ("Office pressure?", "Communicate early with both office and partners."),
        ],
    ),
    "safety-guides/solo-traveller-safety.html": (
        "safety",
        "Solo traveller safety",
        "Solo does not mean unsupported. Layer profile clarity, daytime first rides, live sharing, and firm boundaries.",
        "<li>Clear profile photo</li><li>Daytime first match</li><li>Share live trip</li><li>OTP + tracking</li><li>Favourite after good trips</li>",
        "<li>Skipping verification when lonely/late</li><li>Oversharing personal data in chat</li><li>Ignoring red-flag pressure</li><li>Dark isolated pickups</li>",
        [
            ("Can I end early?", "Yes at a busy public place."),
            ("Social media requests?", "Decline politely; keep chat in-app."),
            ("Luggage alone?", "State limits; ask for help loading in public view."),
            ("First highway solo?", "Prefer known partners and full tracking."),
        ],
    ),
    "safety-guides/travel-safety-guide.html": (
        "safety",
        "Travel safety",
        "Safety is a three-phase system: prepare, verify during, review after. Repeating the same checklist beats occasional intense worry.",
        "<li>Before: match details + ETA share + charged phone</li><li>During: OTP + GPS + awareness</li><li>After: favourite/block + receipt if needed</li><li>Weekly: review Favourites list</li><li>Seasonal: monsoon/night add-ons</li>",
        "<li>Different process every day</li><li>Trusting vibes over verification</li><li>No emergency list</li><li>Arguing instead of exiting safely</li>",
        [
            ("Family travellers?", "Extra consent and seating clarity required."),
            ("Business reimbursement?", "Receipts help conversations; policies vary."),
            ("Is carpool regulated like taxis?", "Rydo coordinates private seat share — follow verification habits regardless."),
            ("Best first guide after this?", "OTP guide + night safety if you leave late."),
        ],
    ),
    "safety-guides/verification-trust-checklist.html": (
        "safety",
        "Verification & trust",
        "Trust compounds when verification is boring and consistent. Use the same rider and captain checklists even when you are late.",
        "<li>Check profile + route text</li><li>Confirm landmark in chat</li><li>Verify identity cues at pickup</li><li>OTP before move</li><li>Tracking visible</li>",
        "<li>Rushing past OTP</li><li>Unclear photos ignored</li><li>Cash demands far above agreement</li><li>Detours without consent</li>",
        [
            ("How many good trips before Favourites?", "Often 2–3 daytime rides."),
            ("Can trust be rebuilt?", "Sometimes — but blocking is valid."),
            ("Group rides?", "Everyone still deserves clarity on seats and shares."),
            ("Captain checklist printable?", "Save this page and reuse the numbered steps."),
        ],
    ),
    "safety-guides/women-ride-safety.html": (
        "safety",
        "Women ride safety",
        "Shared mobility should expand freedom. Combine app tools with personal boundaries and Favourites-based repetition.",
        "<li>Favourite reliable partners</li><li>Busy lit pickups</li><li>Live share with family</li><li>Daytime first rides</li><li>Firm chat boundaries</li>",
        "<li>Pressure to skip OTP</li><li>Isolated pickups</li><li>Ignoring uncomfortable messages</li><li>No ETA sharing on night returns</li>",
        [
            ("Can I refuse any match?", "Yes — always."),
            ("Inappropriate chat?", "Stop, block, tell a trusted contact, reach support if needed."),
            ("Night office exits?", "Favourites + tracking + busy drop points."),
            ("Friends joining?", "Clarify seats and consent early."),
        ],
    ),
}

# Commuter pages meta
for rel, title, lead, steps, mistakes, faqs in [
    (
        "commuter-tips/daily-office-carpool.html",
        "daily office carpool",
        "Office carpool fails when it is improvised daily. It thrives as a lightweight operating system: windows, Favourites, early WFH notices, and Friday settle-ups.",
        "<li>Sunday confirm next week windows</li><li>Depart inside the band</li><li>Message early on leave/WFH</li><li>OTP every start</li><li>Friday settle fuel/toll</li>",
        "<li>Monthly calculator review</li><li>Punctuality within 5 minutes</li><li>Rotate cabin preferences fairly</li><li>Keep a backup Favourite</li>",
        [
            ("Ideal shared days?", "3–5 stable days beat 1 random day."),
            ("New joiner mid-month?", "Introduce in chat; restate rules once."),
            ("Shift change?", "Rebuild windows and Favourites."),
            ("Manager strict punch-in?", "Use buffers as part of the contract."),
        ],
    ),
    (
        "commuter-tips/first-time-commuters-guide.html",
        "first-time commuting",
        "First jobs hide travel costs until the third salary cycle. Measure early, test shared seats early, and learn OTP habits before bad patterns set.",
        "<li>Map two corridors</li><li>Track spend two weeks</li><li>Share on heaviest days</li><li>Learn OTP + GPS</li><li>Favourite punctual people</li>",
        "<li>Buying a vehicle before maths</li><li>Ignoring parking fees</li><li>Sleep-deprived late leaves</li><li>No backup route</li>",
        [
            ("Student to job switch?", "See student commute guide too."),
            ("Is carpool unprofessional?", "Punctual shared travel is common on IT belts."),
            ("Bike first?", "Optional — still calculate long-corridor carpool days."),
            ("Parents worry?", "Show safety tools and Favourites."),
        ],
    ),
    (
        "commuter-tips/fuel-saving-tips.html",
        "fuel saving",
        "The biggest fuel save is raising occupancy on kilometres you already drive. Driving-style tweaks help captains but rarely beat empty-seat removal.",
        "<li>Share seats on existing routes</li><li>Maintain tyre pressure</li><li>Smooth acceleration in queues</li><li>Combine errands</li><li>Recheck after fuel price jumps</li>",
        "<li>Obsessing over tiny hacks only</li><li>Cold-start micro-trips</li><li>Unplanned detours</li><li>Ignoring parking as part of cost</li>",
        [
            ("AC vs mileage?", "Comfort/safety matter; offset via seat share."),
            ("CNG?", "Use if refill access works; still share seats."),
            ("Fair split?", "Agree per-seat or distance rules weekly."),
            ("Calculator?", "Use fuel impact tool on price changes."),
        ],
    ),
    (
        "commuter-tips/healthy-commute-habits.html",
        "healthy commute habits",
        "Commute health is performance infrastructure: sleep, stress, micro-movement, and calmer cabins.",
        "<li>Protect sleep with earlier leave</li><li>2-minute stretch before/after</li><li>Carry water</li><li>Quiet cabin norms</li><li>Walk last 200–400m when safe</li>",
        "<li>Caffeine-only breakfasts</li><li>Doom-rushing into peaks</li><li>Phone rage in traffic</li><li>Skipping breaks on long shares</li>",
        [
            ("Motion sickness?", "Front seat, cool air, less phone reading."),
            ("Carpool reduce stress?", "Often — shared duty + predictability."),
            ("Standing desk link?", "Helpful after long sits — separate from travel mode."),
            ("Monsoon health?", "Dry shoes at office; avoid flooded walks."),
        ],
    ),
    (
        "commuter-tips/monsoon-daily-commute.html",
        "monsoon daily commute",
        "Monsoon continuity needs rain kits, Landmark B, earlier bands, and cancel rules that do not punish honesty.",
        "<li>Pack rain kit</li><li>Define Landmark B</li><li>Shift 15–20 minutes earlier in heavy weeks</li><li>Agree cancel norms</li><li>Update chat proactively</li>",
        "<li>Soaked electronics</li><li>Flooded underpass bravado</li><li>Blame culture for delays</li><li>No spare office shoes</li>",
        [
            ("Cancel guilt?", "Safety first; good groups allow early cancels."),
            ("Umbrella etiquette?", "Shake outside; store low."),
            ("Bike in rain?", "High caution."),
            ("More reading?", "Rainy weather safety guide."),
        ],
    ),
    (
        "commuter-tips/office-commute-guide.html",
        "office commute",
        "A calm office commute is designed: primary corridor, backup, realistic window, cost baseline, and Favourites review.",
        "<li>Pick primary + backup corridor</li><li>Publish realistic window</li><li>Measure monthly solo cost</li><li>Convert 3+ days to shared seats</li><li>Review Favourites monthly</li>",
        "<li>Hybrid WFO calendar honesty</li><li>Buffers for punch-in cultures</li><li>Intern onboarding etiquette</li><li>Rainy-day alternates</li>",
        [
            ("Hybrid weeks?", "Share office days; notify WFH early."),
            ("Different buildings?", "Match gate/tower names precisely."),
            ("Team carpool?", "Sunday planning message helps."),
            ("Related?", "Daily office carpool + WFO planning articles."),
        ],
    ),
    (
        "commuter-tips/parking-cost-savings.html",
        "parking cost savings",
        "Parking is the silent tax of business districts. Shared gate drops often remove an entire monthly fee line.",
        "<li>Share into paid zones</li><li>Agree exact landmark</li><li>Avoid circling</li><li>Park-once errand batches</li><li>Include parking in weekly money talk if relevant</li>",
        "<li>Hunting slots for 15 minutes</li><li>Unclear who pays</li><li>Unsafe last-mile walks at night</li><li>Ignoring mall+office stacked fees</li>",
        [
            ("Who pays?", "Decide upfront."),
            ("Last-mile OK?", "When pavements/lighting safe."),
            ("Calculator?", "Add parking into daily cost tool."),
            ("Captains?", "Count your true monthly parking."),
        ],
    ),
    (
        "commuter-tips/peak-hour-tips.html",
        "peak hour commuting",
        "Peak hour is too many vehicles, not enough road. Your levers are timing, occupancy, backups, and expectations.",
        "<li>Shift 15–30 minutes when possible</li><li>Share seats</li><li>Use live ETAs calmly</li><li>Keep Landmark B</li><li>Test leave-later for a week with data</li>",
        "<li>Leaving exactly into the crush</li><li>Rage-refreshing maps</li><li>No backup gate</li><li>Solo every peak day by default</li>",
        [
            ("Special lanes?", "City-dependent; occupancy still saves money."),
            ("Leave later?", "Sometimes after crush — measure."),
            ("City specifics?", "Open your city guide."),
            ("Punctuality?", "Buffers + Favourites."),
        ],
    ),
    (
        "commuter-tips/reduce-commute-cost.html",
        "reducing commute cost",
        "Cost reduction is a stack: measure, raise occupancy, cut micro-trips, drive efficiently, recheck on price shocks.",
        "<li>Baseline all cost lines</li><li>Cut empty-seat days via Rydo</li><li>Trim micro-trips</li><li>Improve efficiency</li><li>Recheck monthly</li>",
        "<li>Realistic four-figure savings on long solo corridors</li><li>Metro hybrids still need edge seat share</li><li>No taxi-style profit on private shares</li><li>Visible monthly tracking</li>",
        [
            ("Biggest lever?", "Occupancy on longest corridor."),
            ("Family car?", "Share school/office overlaps."),
            ("Fuel spikes?", "Use impact calculator."),
            ("More tips?", "How to save money on daily travel."),
        ],
    ),
    (
        "commuter-tips/two-wheeler-vs-carpool.html",
        "two-wheeler vs carpool",
        "Choose by scenario, not ideology. Many people keep both: bike flexibility plus carpool on expensive/wet/group days.",
        "<li>Short dry solo hop → often two-wheeler</li><li>Long office group → carpool</li><li>Monsoon/heavy bags → carpool</li><li>Always: helmets/laws on bikes; OTP on shares</li><li>Recalculate quarterly</li>",
        "<li>Ignoring fatigue cost</li><li>Overcrowding vehicles</li><li>Skipping insurance awareness</li><li>Comparing only petrol receipts</li>",
        [
            ("Moto on Rydo?", "Ride types may include moto — follow safety laws."),
            ("Cost compare?", "Include parking and fatigue."),
            ("Night bike?", "Extra caution; prefer trusted plans."),
            ("Students?", "Timetable matching matters most."),
        ],
    ),
    (
        "commuter-tips/how-to-save-money-on-daily-travel.html",
        "saving money on daily travel",
        "Savings stick when visible. Track shared days and rupees monthly so the habit survives motivation dips.",
        "<li>Screenshot calculator monthly</li><li>Compare fuel wallet</li><li>Adjust windows on price spikes</li><li>Protect Favourites</li><li>Cut one micro-trip loop weekly</li>",
        "<li>Invisible benefits → quit</li><li>Random matching only</li><li>Ignoring parking</li><li>No rainy backup plan causing expensive cabs</li>",
        [
            ("Biggest lever?", "Occupancy on longest corridor."),
            ("Family?", "Share overlaps."),
            ("Hybrid WFO?", "Still saves on office days."),
            ("Tools?", "Cost calculators + Rydo."),
        ],
    ),
]:
    PAGE_META[rel] = ("commuter", title, lead, steps, mistakes, faqs)

for rel, title, lead, steps, mistakes, faqs in [
    (
        "travel-guides/airport-transfer-carpool.html",
        "airport transfer carpool",
        "Airport runs reward pre-agreement: terminal door, luggage, buffers, and OTP — not kerbside improvisation during surge hours.",
        "<li>Confirm terminal + door</li><li>Flight time + buffer</li><li>Luggage count/size</li><li>OTP + tracking</li><li>Fuel/toll share in chat</li>",
        "<li>Hidden extra suitcases</li><li>Unclear waiting rules on delay</li><li>Wrong terminal assumption</li><li>Cash confusion at departure kerb</li>",
        [
            ("Flight delay?", "Update immediately; agree wait/cancel."),
            ("Max luggage?", "State before confirm."),
            ("Taxi replacement?", "No — private seat share."),
            ("City notes?", "See city guides."),
        ],
    ),
    (
        "travel-guides/festival-travel-carpool.html",
        "festival travel carpool",
        "Festival highways punish last-minute solo plans. Match early, agree night rules, and split tolls transparently.",
        "<li>Lock partners 3–7 days ahead</li><li>Night-driving rules</li><li>Toll split</li><li>Food/fuel stops</li><li>Emergency contacts</li>",
        "<li>Drowsy forcing</li><li>Unclear kid seating</li><li>Money arguments mid-route</li><li>No return window</li>",
        [
            ("Overnight?", "Only with alert rotation."),
            ("Kids?", "Explicit consent + seats."),
            ("Pricing?", "Distance fuel+toll split."),
            ("More?", "Highway + long-distance guides."),
        ],
    ),
    (
        "travel-guides/long-distance-seat-share-checklist.html",
        "long-distance seat share",
        "Distance multiplies small ambiguities. Use a written checklist covering breaks, documents, luggage map, and cancel fairness.",
        "<li>Route + breaks</li><li>Driver rotation if overnight</li><li>Vehicle check</li><li>Documents + emergency numbers</li><li>Luggage map + OTP/GPS</li>",
        "<li>48+ hours notice preferred</li><li>Last-minute cancel norms</li><li>Night-bus comparison awareness</li><li>Same-day UPI settlement</li>",
        [
            ("Minimum notice?", "Earlier safer for highways."),
            ("Cancel fairness?", "Pre-agree partial norms."),
            ("Bus vs carpool?", "See comparison guide."),
            ("Police stops?", "Carry documents; be factual."),
        ],
    ),
    (
        "travel-guides/luggage-tips-shared-rides.html",
        "luggage on shared rides",
        "Most shared-trip friction is baggage. Solve dimensions in chat, protect cabin comfort, and keep rear visibility clear.",
        "<li>State suitcase counts</li><li>Prefer soft bags when possible</li><li>Personal bag at seat</li><li>No rear visibility block</li><li>Label for multi-drop</li>",
        "<li>Surprise cartons/bikes</li><li>Wet umbrellas inside unchecked</li><li>Strong food smells</li><li>Blocking terminal lanes while loading</li>",
        [
            ("Bicycle/carton?", "Only with consent."),
            ("Airport trolley?", "Load quickly."),
            ("Multi-drop?", "Label bags."),
            ("Cabin rules?", "Ask before food."),
        ],
    ),
    (
        "travel-guides/night-bus-vs-carpool.html",
        "night bus vs carpool",
        "Neither mode always wins. Compare cost, flexibility, sleep, and whether you already trust the travellers.",
        "<li>List origin/destination convenience</li><li>Compare ticket vs fuel/toll share</li><li>Assess sleep needs</li><li>Check partner trust</li><li>Decide one-way mix if useful</li>",
        "<li>Depot far from home</li><li>Odd door-to-door needs</li><li>Untrusted random highway groups</li><li>Ignoring safety tools on either mode</li>",
        [
            ("Bus better when?", "Solo + fixed ticket + convenient depot."),
            ("Carpool better when?", "Small trusted group / odd ends."),
            ("Mix modes?", "Yes — common on weekends."),
            ("Safety?", "OTP/GPS on carpool; reputable operators on buses."),
        ],
    ),
    (
        "travel-guides/pilgrimage-route-carpool.html",
        "pilgrimage route carpool",
        "Faith-route spikes need respectful planning: parking away from crush cores, elder comfort, and clear money talk before highway entry.",
        "<li>Agree expectations</li><li>Plan outer parking when advised</li><li>Breaks for elders</li><li>OTP + tracking on unfamiliar segments</li><li>Fair fuel/toll split</li>",
        "<li>Midnight alley improvisation</li><li>Unclear family seating</li><li>Money stress mid-darshan rush</li><li>No stay plan on night arrival</li>",
        [
            ("Bargaining?", "Be transparent and fair."),
            ("Night arrival?", "Pre-agree stay."),
            ("Family groups?", "Clarify seats early."),
            ("Related?", "Festival + highway guides."),
        ],
    ),
    (
        "travel-guides/weekend-trip-fuel-share.html",
        "weekend trip fuel share",
        "Weekend getaways stay friendly when money, music, and return windows are decided before the first toll plaza.",
        "<li>Estimate fuel+tolls</li><li>Divide by seats</li><li>Decide FASTag payer + UPI settle</li><li>List stops</li><li>Set return window</li>",
        "<li>Sightseeing detours without recalc</li><li>AC/music fights</li><li>Treating private share like tour pricing</li><li>No calculator reality check</li>",
        [
            ("Detours?", "Recalculate or rotate treats."),
            ("Norms?", "Set at start."),
            ("Solo captain + 3 riders?", "Still voluntary cost share."),
            ("Tools?", "Cost calculators."),
        ],
    ),
    (
        "travel-guides/highway-carpool-india.html",
        "highway carpool in India",
        "Highway seat share needs FASTag clarity, driver rotation discipline, water/medicine basics, and refusal of unknown late-night shortcuts.",
        "<li>Pre-decide FASTag payer</li><li>Rotate drivers overnight</li><li>Pack water/medicine</li><li>Avoid unknown night shortcuts</li><li>Settle tolls same day</li>",
        "<li>Overcrowding</li><li>Drowsy driving ego</li><li>Toll disputes without screenshots</li><li>Missing documents</li>",
        [
            ("Group size?", "Enough to split costs safely."),
            ("Toll disputes?", "Screenshot + UPI."),
            ("Police stops?", "Documents; polite facts."),
            ("Festivals?", "Match earlier."),
        ],
    ),
]:
    PAGE_META[rel] = ("travel", title, lead, steps, mistakes, faqs)

for rel, title, lead, steps, mistakes, faqs in [
    (
        "blog/captain-getting-started.html",
        "getting started as a captain",
        "Captains win with predictability: landmarks locals know, seat/luggage policy, OTP discipline, and fast Favourites.",
        "<li>Publish clear landmarks</li><li>State seats/luggage</li><li>Short etiquette note</li><li>Never skip OTP</li><li>Favourite reliable riders</li>",
        "<li>Fragile single-minute ETAs</li><li>Unclear money talk</li><li>Late-night first matches without care</li><li>Overfilling seats</li>",
        [
            ("Commercial permit?", "Private cost share — not taxi business."),
            ("Price fuel share?", "Simple upfront rules."),
            ("Late riders?", "Kind 5-minute rule."),
            ("Support?", "Email/phone on site."),
        ],
    ),
    (
        "blog/carpool-etiquette.html",
        "carpool etiquette",
        "Etiquette is how groups survive months. Punctuality, hygiene, transparent money, and early cancels matter more than personality quizzes.",
        "<li>Be inside the window</li><li>Ask before food</li><li>Earphones for calls</li><li>No surprise detours</li><li>Cancel early</li>",
        "<li>Speakerphone marathon calls</li><li>Strong smells</li><li>AC wars without defaults</li><li>Ghosting the group</li>",
        [
            ("Food?", "Ask first."),
            ("Calls?", "Earphones; keep short."),
            ("AC?", "Agree default."),
            ("Money?", "Same-day UPI ideal."),
        ],
    ),
    (
        "blog/fuel-share-vs-taxi.html",
        "fuel share vs taxi",
        "Taxis sell transport as a service. Rydo coordinates private travellers sharing a route and contributing to costs — different product, different norms.",
        "<li>Decide if you need a hired ride or a shared private trip</li><li>If sharing, agree contribution upfront</li><li>Use OTP/GPS</li><li>Do not apply surge logic</li><li>Favourite recurring partners</li>",
        "<li>Captains chasing taxi margins</li><li>Riders expecting cab entitlements</li><li>Skipping verification</li><li>Ambiguous WhatsApp-only money</li>",
        [
            ("Captain profit?", "No taxi-style profit model."),
            ("Taxi better when?", "Urgent unplanned hops."),
            ("Legal goodwill?", "Keep contributions reasonable/transparent."),
            ("Learn more?", "How Rydo works."),
        ],
    ),
    (
        "blog/how-rydo-works.html",
        "how Rydo works",
        "Mental model: route coordination, not cab dispatch. Match corridor → OTP → travel with GPS → complete → favourite.",
        "<li>Install from Google Play</li><li>Choose Rider or Captain</li><li>Set route + window</li><li>Match and verify OTP</li><li>Complete and favourite</li>",
        "<li>Thinking it is surge taxi</li><li>Skipping OTP</li><li>Vague landmarks</li><li>No Favourites discipline</li>",
        [
            ("iOS?", "Android available now; check listing for updates."),
            ("Fares?", "No commercial surge fares."),
            ("Support?", "pktiwari110487@gmail.com · +91 9026317151"),
            ("Guides?", "City + safety hubs."),
        ],
    ),
    (
        "blog/monsoon-commute-tips.html",
        "monsoon commute tips",
        "Monsoon commuting is logistics: pouch, Landmark B, earlier bands, and honest cancels.",
        "<li>Phone pouch</li><li>Backup landmark</li><li>Earlier departure</li><li>Honest cancel culture</li><li>Spare office shoes</li>",
        "<li>Flooded short-cut bravado</li><li>Blame for weather delays</li><li>Soaked electronics</li><li>No group norms</li>",
        [
            ("Office expects presence?", "Communicate early."),
            ("Electronics?", "Dry bags."),
            ("More?", "Rain safety guide."),
            ("Bike?", "Extreme caution."),
        ],
    ),
    (
        "blog/student-commute-guide.html",
        "student commute",
        "College timetables create natural cohorts. Discipline on seats, fuel fairness, and OTP habits matters on student budgets too.",
        "<li>Match lecture days</li><li>Split fuel fairly</li><li>OTP early habit</li><li>No unsafe overcrowding</li><li>Update exam-week changes</li>",
        "<li>Random hours matching</li><li>Money awkwardness</li><li>Parents uninformed</li><li>Night improvisation</li>",
        [
            ("Student captains?", "If legally driving + private share norms."),
            ("Exam week?", "Daily chat updates."),
            ("Parents?", "Share tracking habits."),
            ("Savings?", "Use calculator."),
        ],
    ),
    (
        "blog/traffic-problem-in-indian-cities.html",
        "traffic in Indian cities",
        "Road supply grows slower than vehicles. Personal toolkit: occupancy, timing shift, transit hybrids, fewer micro-drives.",
        "<li>Raise occupancy via carpool</li><li>Shift peak 15–30 minutes</li><li>Use metro/bus where density wins</li><li>Cut micro-drives</li><li>Encourage office cohorts</li>",
        "<li>Waiting only for flyovers</li><li>One person claiming helplessness</li><li>Empty-seat culture</li><li>No data on personal costs</li>",
        [
            ("One person matter?", "Yes for your cost + corridor culture."),
            ("Flyovers enough?", "Habits refill empty seats into new capacity."),
            ("Offices?", "Stagger + carpool cohorts."),
            ("App role?", "Rydo coordinates private seat share."),
        ],
    ),
    (
        "blog/trip-receipts-explained.html",
        "trip receipts",
        "Receipts/records turn fuzzy fuel talk into monthly clarity — useful even when contributions are voluntary.",
        "<li>Complete trip in-app</li><li>Save PDF/record</li><li>File monthly</li><li>Use numbers in renegotiation</li><li>Ask support if history missing</li>",
        "<li>Treating records as taxi invoices</li><li>Never reviewing monthly</li><li>Disputes without data</li><li>Lost files</li>",
        [
            ("Invoices?", "Trip records — not commercial taxi invoices."),
            ("Lost?", "Check history/support."),
            ("Reimbursement?", "Employer policy varies."),
            ("Why care?", "Budget + fairness."),
        ],
    ),
    (
        "blog/work-from-office-commute-planning.html",
        "work-from-office commute planning",
        "Hybrid weeks need sharper calendars. Publish office days, keep a stand-by Favourite, and never ghost the group on sudden WFH.",
        "<li>Sunday publish office days</li><li>Keep stand-by Favourite</li><li>Notify WFH early</li><li>Recalculate hybrid costs</li><li>Protect buffers on office days</li>",
        "<li>Last-minute silence</li><li>Assuming partners can read your mind</li><li>One-person dependency</li><li>No monthly cost review</li>",
        [
            ("Only 2 office days?", "Still worth sharing vs two solo drives."),
            ("Different teammates different days?", "Two small Favourites lists."),
            ("Roster change?", "Notify ASAP."),
            ("Related?", "Office commute guide."),
        ],
    ),
    (
        "blog/benefits-of-ride-sharing.html",
        "benefits of ride sharing",
        "Beyond fuel, shared routes reduce parking stress, create punctuality culture, and make monthly money visible.",
        "<li>Quantify fuel+parking</li><li>Share peak days</li><li>Favourite good partners</li><li>Track monthly</li><li>Add safety habits</li>",
        "<li>Privacy worries without Favourites</li><li>All-or-nothing thinking</li><li>Ignoring health/stress co-benefits</li><li>No etiquette norms</li>",
        [
            ("Privacy?", "Favourites keep cabins familiar."),
            ("Like driving alone?", "Share only expensive days."),
            ("Health?", "Less solo stress; optional walking."),
            ("Start?", "Download Rydo."),
        ],
    ),
    (
        "blog/best-travel-apps-for-commuters.html",
        "best travel apps for commuters",
        "A lean stack beats app hoarding: maps, transit, Rydo seat share, UPI, calendar.",
        "<li>Maps + traffic</li><li>Transit apps</li><li>Rydo for seat share</li><li>UPI for settlements</li><li>Calendar for windows</li>",
        "<li>WhatsApp-only chaos</li><li>Too many redundant apps</li><li>No offline maps on highways</li><li>Skipping safety features</li>",
        [
            ("Need many apps?", "Maps + Rydo + UPI covers most."),
            ("Why not only WhatsApp?", "OTP/tracking/structure."),
            ("Offline?", "Download maps."),
            ("Rydo role?", "Private seat share coordination."),
        ],
    ),
    (
        "blog/complete-guide-to-carpooling.html",
        "complete guide to carpooling",
        "Advanced playbook: score punctuality privately, keep rainy Landmark B, review fuel share monthly, separate weekday vs weekend groups.",
        "<li>Private punctuality notes</li><li>Landmark B</li><li>Monthly fuel review</li><li>Separate weekend groups</li><li>Never exceed safe seats</li>",
        "<li>One mega-group for all trip types</li><li>No cancel norms</li><li>Skipping OTP</li><li>Money ambiguity</li>",
        [
            ("Max people?", "Legal/safe seating only."),
            ("Companies?", "Corridor cohorts work."),
            ("Product flow?", "How Rydo works."),
            ("Safety?", "Safety hub."),
        ],
    ),
    (
        "blog/how-to-find-carpool-partners.html",
        "finding carpool partners",
        "Discovery channels: Rydo matching, office teams, cautious society chats, classmates — then convert to Favourites with OTP discipline.",
        "<li>Post clear route on Rydo</li><li>Ask teammates on same corridor</li><li>Daytime first rides</li><li>Favourite reliability</li><li>Keep a backup partner</li>",
        "<li>Cold night-only first meets</li><li>Vague profiles</li><li>One-person dependency</li><li>Chat leaving the app forever</li>",
        [
            ("Cold matching scary?", "Daytime + short + OTP."),
            ("Profile tips?", "Clear photo + stable route text."),
            ("Flakes?", "Two Favourites minimum."),
            ("Etiquette?", "Read etiquette guide."),
        ],
    ),
]:
    PAGE_META[rel] = ("blog", title, lead, steps, mistakes, faqs)


def render_from_meta(kind, title, lead, steps, mistakes, faqs):
    body = TEMPLATES[kind].format(title=title, lead=lead, steps=steps, mistakes=mistakes)
    return f"{START}\n{body}\n<h2>Frequently asked questions</h2>\n{faq_html(faqs)}\n{END}\n", faqs


def replace_block(text: str, new_html: str) -> str:
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), new_html.strip(), text, count=1, flags=re.S)
    # insert before lead
    if "<!-- LEAD-EXPANDED-v1 -->" in text:
        return text.replace("<!-- LEAD-EXPANDED-v1 -->", new_html + "\n<!-- LEAD-EXPANDED-v1 -->", 1)
    return text


def upsert_faq(text: str, faqs):
    snippet = faq_ld(faqs)
    if "<!-- SEO-FAQ-v2 -->" in text:
        text = re.sub(r"<!-- SEO-FAQ-v2 -->.*?</script>\s*", "", text, flags=re.S)
    return text.replace("</head>", snippet + "</head>", 1)


def bump(text: str) -> str:
    return re.sub(r'"dateModified":\s*"[0-9-]+"', f'"dateModified": "{TODAY}"', text)


def main():
    # sustainability explicit deep pages
    updated = []
    for rel, (html, faqs) in DEEP.items():
        path = ROOT / rel
        block = f"{START}\n{html}\n<h2>Frequently asked questions</h2>\n{faq_html(faqs)}\n{END}\n"
        text = path.read_text(encoding="utf-8")
        text = replace_block(text, block)
        text = upsert_faq(text, faqs)
        text = bump(text)
        path.write_text(text, encoding="utf-8")
        updated.append(rel)

    for rel, meta in PAGE_META.items():
        path = ROOT / rel
        if not path.exists():
            continue
        # skip if already long enough (>900 article words) unless sustainability already done
        text = path.read_text(encoding="utf-8")
        m = re.search(r"<article class=\"article-layout\">(.*?)</article>", text, re.S)
        w = words(m.group(1)) if m else 0
        if w >= 950 and rel not in DEEP:
            continue
        block, faqs = render_from_meta(*meta)
        text = replace_block(text, block)
        text = upsert_faq(text, faqs)
        text = bump(text)
        path.write_text(text, encoding="utf-8")
        updated.append(rel)

    print("Updated", len(set(updated)), "pages")
    for u in sorted(set(updated)):
        print(" -", u)


if __name__ == "__main__":
    main()
