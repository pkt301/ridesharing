#!/usr/bin/env python3
"""Inject unique long-form SEO blocks into Rydo guide/blog pages."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER_START = "<!-- SEO-EXPANDED-v2 -->"
MARKER_END = "<!-- /SEO-EXPANDED-v2 -->"
LEAD = "<!-- LEAD-EXPANDED-v1 -->"
TODAY = "2026-07-29"

CITY = {
    "ahmedabad-travel-guide": {
        "city": "Ahmedabad",
        "aka": "Amdavad",
        "corridors": [
            "SG Highway / Sola / Science City Road office belts",
            "Prahlad Nagar–Iscon–Satellite morning flows",
            "Ashram Road / Navrangpura / CG Road mid-city links",
            "Naroda–Odhav industrial approaches",
            "GIFT City / Gandhinagar weekday connectors",
        ],
        "peaks": "8:00–10:30 AM and 5:30–8:30 PM on SG Highway approaches; festival weeks and winter fog add delay.",
        "parking": "Paid parking near business parks and malls adds up fast — shared drop-offs near gate landmarks cut both fuel and parking fees.",
        "landmarks": "Iscon Circle, Karnavati Club stretch, Thaltej Cross Roads, Nehru Bridge approaches",
        "extra": "Many Ahmedabad captains prefer fixed weekday windows because industrial and IT shifts are predictable. Publish Semra-style landmark names riders actually use (circle, BRTS stop, society gate) so matching is faster.",
        "faqs": [
            ("Is carpooling common in Ahmedabad?", "Yes on stable office corridors like SG Highway. Recurring weekday seat share works better than one-off matching."),
            ("How do I save on SG Highway fuel?", "Share seats 3–5 days/week with the same partners, leave 15 minutes earlier than peak, and estimate costs with Rydo's calculator."),
            ("Is Rydo a taxi in Ahmedabad?", "No. Rydo is private carpool & seat share — voluntary fuel/toll contribution, not commercial cab pricing."),
        ],
    },
    "bangalore-carpool": {
        "city": "Bengaluru (Bangalore)",
        "aka": "Bangalore",
        "corridors": [
            "ORR / Manyata / Hebbal / North tech parks",
            "Whitefield–ITPL–Marathahalli east belt",
            "Electronic City–Bommanahalli south runs",
            "Koramangala–HSR–BTM mid-south links",
            "Sarjapur / Bellandur evening bottlenecks",
        ],
        "peaks": "Weekday peaks stretch long — 8–11 AM and 5–9 PM are common. Rain and broken signals can double travel time on ORR ramps.",
        "parking": "Tech-park parking slots are scarce; shared last-mile drop at known gates reduces circling.",
        "landmarks": "Silk Board, Hebbal flyover, Marathahalli bridge, Electronic City Toll, KR Puram",
        "extra": "Bengaluru carpools succeed when captains post exact society/tech-park gate names and a hard departure time. Favourites beat daily renegotiation.",
        "faqs": [
            ("Does carpool help Bangalore traffic stress?", "It reduces your personal cost and empty seats. City-wide relief needs many people sharing the same corridors repeatedly."),
            ("Whitefield to Indiranagar — good for seat share?", "Yes if windows are stable. Agree pickup landmarks clearly because one-ways and flyovers confuse first-time partners."),
            ("Moto vs car share in Bangalore?", "Moto helps short hops; cars work better for ORR/Whitefield distances when luggage or monsoon is a factor."),
        ],
    },
    "bengaluru-travel-guide": {
        "city": "Bengaluru",
        "aka": "Bangalore",
        "corridors": [
            "Outer Ring Road tech corridor",
            "Whitefield / ITPL / Brookefield",
            "Electronic City Phase 1 & 2",
            "Yelahanka–Manyata north cluster",
            "Airport (KIA) early-morning transfers",
        ],
        "peaks": "ORR and Silk Board remain the classic choke points; monsoon evenings are the hardest.",
        "parking": "Mall and office parking fees stack monthly — share rides to the gate and walk the last 200m when possible.",
        "landmarks": "MG Road metro, Indiranagar 100 Feet, Silk Board, Hebbal, Whitefield Main Road",
        "extra": "Use Metro + carpool hybrids: ride-share the long suburban leg, then take metro for the dense core when it is faster.",
        "faqs": [
            ("Best time to leave for ORR offices?", "Often 30–45 minutes before your team's official start beats leaving 'exactly on time' into gridlock."),
            ("Is airport carpool useful?", "Early flights work well with pre-agreed captains. Luggage limits must be clear in chat."),
            ("How do students carpool in Bengaluru?", "College belts near Koramangala/BTM/Yelahanka work if groups keep a recurring timetable."),
        ],
    },
    "chandigarh-travel-guide": {
        "city": "Chandigarh",
        "aka": "Tricity (Chandigarh–Mohali–Panchkula)",
        "corridors": [
            "Sectors to IT Park / Rajiv Gandhi Chandigarh Technology Park",
            "Mohali Phase corridors & airport road",
            "Panchkula sector connectors",
            "Inter-city Zirakpur approaches",
            "University / college morning belts",
        ],
        "peaks": "Office and college bells create sharp morning peaks; winter fog on highways needs extra buffer.",
        "parking": "Sector markets and IT Park lots fill early — shared drop near sector greens reduces circling.",
        "landmarks": "Tribune Chowk, Matka Chowk, ISBT 43, IT Park gate, Zirakpur flyover",
        "extra": "Tricity rides often cross UT/state boundaries — agree toll sharing before you start and keep OTP + live tracking on.",
        "faqs": [
            ("Can I carpool Chandigarh to Mohali daily?", "Yes — it is one of the most natural tricity seat-share corridors."),
            ("Fog season tips?", "Leave earlier, use well-lit pickups, confirm ETA in chat, and keep tracking on."),
            ("Is Rydo for tourists only?", "No — it is built for recurring private commute matching as well as occasional trips."),
        ],
    },
    "chennai-travel-guide": {
        "city": "Chennai",
        "aka": "Madras",
        "corridors": [
            "OMR / IT corridor (Sholinganallur–Thoraipakkam–Siruseri)",
            "GST Road / Guindy / airport industrial belt",
            "Mount Road / Anna Salai core links",
            "Porur–Maduravoyal west approaches",
            "Tambaram / southern suburban connectors",
        ],
        "peaks": "OMR peaks are long; cyclone/monsoon days and beach-road events change patterns suddenly.",
        "parking": "IT campus parking is managed but last-mile waits are real — agree exact tower/gate names.",
        "landmarks": "SRP Tools, Tidel Park, Kathipara, Airport, Central station approaches",
        "extra": "Chennai heat and rain make reliable AC carpools valuable. Captains should state vehicle type and luggage space upfront.",
        "faqs": [
            ("OMR carpool — worth it?", "Yes for IT shifts with stable hours. Recurring partners beat daily marketplace hunting."),
            ("How to handle monsoon floods?", "Avoid waterlogged underpasses, confirm alternate landmarks, and cancel early if roads close."),
            ("Local train + carpool?", "Common hybrid: suburban train for dense stretch, seat share for the OMR last leg."),
        ],
    },
    "delhi-ncr-commute": {
        "city": "Delhi NCR",
        "aka": "NCR (Delhi–Noida–Gurgaon–Ghaziabad)",
        "corridors": [
            "Gurgaon Cyber City / Golf Course / Sohna Road",
            "Noida Sector hubs & Greater Noida West",
            "Dwarka–Airport–south Delhi links",
            "Ghaziabad–Anand Vihar approaches",
            "Expressway office parks (Noida–Greater Noida)",
        ],
        "peaks": "8–11 AM and 5–9 PM are brutal on arterial roads; pollution emergency days and rain worsen unpredictability.",
        "parking": "Cyber City and mall parking fees are a major monthly line item — shared gate drops help.",
        "landmarks": "IFFCO Chowk, Botanical Garden, Anand Vihar ISBT, Dwarka Sector hubs, DND approaches",
        "extra": "NCR distances are long — captains with stable 9–6 schedules and Favourites lists win. Avoid last-minute matching on extreme AQI or weather days.",
        "faqs": [
            ("Noida to Gurgaon daily carpool?", "Possible but plan buffers; expressway + city-entry delays stack. Fixed partners help."),
            ("Is metro better than carpool?", "Often for dense core hops. Carpool shines on first/last mile and office-park corridors metro doesn't cover well."),
            ("Women safety on NCR night returns?", "Prefer verified recurring partners, well-lit pickups, OTP, live tracking, and share trip status with family."),
        ],
    },
    "delhi-travel-guide": {
        "city": "Delhi",
        "aka": "New Delhi / NCR",
        "corridors": [
            "South Delhi office belts",
            "Connaught Place / central business links",
            "Airport (IGI) early transfers",
            "East Delhi–Anand Vihar flows",
            "Dwarka sub-city connectors",
        ],
        "peaks": "Multiple peak waves; VIP movements and winter smog change ETAs fast.",
        "parking": "Paid parking in markets and offices adds up — share to a landmark and walk short distances.",
        "landmarks": "AIIMS, ITO, Kashmiri Gate, Saket, Nehru Place",
        "extra": "Combine Metro + seat share: use metro where density wins, carpool for awkward office-park legs.",
        "faqs": [
            ("Best carpool use-case in Delhi?", "Recurring office corridors and airport early runs with clear luggage rules."),
            ("Odd-even days?", "Higher vehicle occupancy habits help regardless of temporary schemes — keep shared routes ready."),
            ("Safety basics?", "OTP, live GPS, Favourites, and daytime first rides with new partners."),
        ],
    },
    "hyderabad-travel-guide": {
        "city": "Hyderabad",
        "aka": "Cyberabad",
        "corridors": [
            "HITEC City / Madhapur / Gachibowli",
            "Financial District / Nanakramguda",
            "ORR / Outer Ring approaches",
            "Secunderabad–Begumpet mid links",
            "Uppal / east IT & college belts",
        ],
        "peaks": "IT shift changes create waves on HITEC–Gachibowli roads; weekend ORR leisure traffic differs from weekdays.",
        "parking": "Campus parking is structured but gate waits are long — precise tower names matter.",
        "landmarks": "Cyber Towers, DLF gate areas, Raidurg metro, Mindspace, ORR exits",
        "extra": "Hyderabad captains often run fixed IT-park loops. Riders should match the exact park/tower, not just 'Gachibowli'.",
        "faqs": [
            ("HITEC City carpool tips?", "Post tower + shift time. Favourites beat random daily matching."),
            ("Airport to Financial District?", "Pre-dawn shared rides work if luggage and ETA are agreed in chat."),
            ("Is Rydo surge priced?", "No — participants agree voluntary fuel/toll share. Not a taxi."),
        ],
    },
    "jaipur-travel-guide": {
        "city": "Jaipur",
        "aka": "Pink City",
        "corridors": [
            "Tonk Road / Malviya Nagar office links",
            "Ajmer Road / Vaishali / Mansarovar",
            "Jagatpura / Sitapura industrial belt",
            "MI Road / C-Scheme mid-city",
            "Airport and station transfer windows",
        ],
        "peaks": "School + office overlap mornings; tourist season evenings near old city add friction.",
        "parking": "Old city and market parking is painful — share to outer landmarks when possible.",
        "landmarks": "Transport Nagar, Gopalpura bypass, JLN Marg, Airport road",
        "extra": "Jaipur weekday carpools work best on Ajmer Road and Tonk Road belts with recurring college/office groups.",
        "faqs": [
            ("Tourist vs commute carpool?", "Rydo is strongest for recurring private commute; occasional airport/station shares also work with clear chat."),
            ("Summer heat tips?", "Prefer AC cars, water, and shaded pickup points."),
            ("Festival traffic?", "Leave earlier and lock partners days ahead."),
        ],
    },
    "kolkata-travel-guide": {
        "city": "Kolkata",
        "aka": "Calcutta",
        "corridors": [
            "Salt Lake / Sector V IT belt",
            "Park Street / central business links",
            "Howrah approaches & bridge constraints",
            "New Town / Rajarhat office parks",
            "Southern Avenue / south suburban connectors",
        ],
        "peaks": "Office peaks plus tram/bus density; monsoon waterlogging can shut key underpasses.",
        "parking": "Limited central parking makes shared drops near metro/bus nodes smart.",
        "landmarks": "Sector V, City Center, Howrah, New Town, Gariahat",
        "extra": "Metro + carpool hybrids are natural in Kolkata. Use seat share for New Town/Sector V legs where buses are crowded.",
        "faqs": [
            ("Sector V carpool?", "Yes — one of the city's best recurring office corridors."),
            ("Monsoon plan?", "Confirm alternate pickups; cancel early if roads flood."),
            ("Cross-Howrah daily?", "Build extra buffer and prefer stable partners who know bridge delays."),
        ],
    },
    "lucknow-carpool": {
        "city": "Lucknow",
        "aka": "Awadh capital",
        "corridors": [
            "Gomti Nagar / Softwarde IT & office belts",
            "Hazratganj mid-city links",
            "Lucknow–Faizabad / Ayodhya corridor travellers",
            "Airport & Charbagh station transfers",
            "Alambagh / Kanpur road approaches",
        ],
        "peaks": "School-office mornings and evening return on Gomti Nagar arteries; fog in winter.",
        "parking": "Mall and office parking fees add up — share to society/office gates.",
        "landmarks": "Gomti Nagar Extension, Polytechnic, Charbagh, Ambedkar University belt",
        "extra": "Lucknow–Ayodhya / Faizabad route sharers benefit from highway seat share on weekends and festival weeks.",
        "faqs": [
            ("Best Lucknow carpool routes?", "Gomti Nagar office loops and weekend Faizabad/Ayodhya highway shares."),
            ("Is Rydo available in Lucknow?", "Yes — download on Android and post your recurring route."),
            ("Safety for first ride?", "Daytime, OTP, live tracking, and Favourites after a good trip."),
        ],
    },
    "lucknow-daily-travel-guide": {
        "city": "Lucknow",
        "aka": "Lucknow daily commute",
        "corridors": [
            "Gomti Nagar to Hazratganj",
            "Indira Nagar / Mahanagar school-office mix",
            "Aliganj / Nishatganj mid links",
            "SGPGI / hospital shift corridors",
            "Airport early-morning runs",
        ],
        "peaks": "8–10 AM and 5–8 PM; winter fog needs headlights and earlier departure.",
        "parking": "Hazratganj parking is scarce — shared drop + short walk wins.",
        "landmarks": "Sahara Ganj, Fun Republic stretch, Polytechnic Chauraha, Charbagh",
        "extra": "Daily Lucknow travellers save most by locking 4–5 shared weekdays with the same captain/rider set.",
        "faqs": [
            ("How much can I save monthly?", "Often thousands of rupees vs solo driving once fuel + parking are counted — use the cost calculator."),
            ("Two-wheeler or carpool?", "Two-wheelers win short hops; carpools win longer belts, monsoon, and group office runs."),
            ("Student routes?", "College belts work when groups keep fixed lecture timetables."),
        ],
    },
    "mumbai-carpool": {
        "city": "Mumbai",
        "aka": "Bombay",
        "corridors": [
            "Western Express Highway office flows",
            "Eastern Express / Thane links",
            "Bandra–Kurla Complex (BKC)",
            "Navi Mumbai / Belapur / Vashi connectors",
            "Andheri–Powai–SEEPz tech belts",
        ],
        "peaks": "Local-train peaks and road peaks overlap; monsoon days are the hardest.",
        "parking": "BKC and business-district parking is expensive — shared last drops matter.",
        "landmarks": "BKC, Powai lake side, Sion, Vashi toll, WEH exits",
        "extra": "Mumbai carpools often complement locals: seat share the awkward office-park leg your train doesn't serve well.",
        "faqs": [
            ("Carpool vs local train?", "Trains win pure speed on many corridors; carpool wins comfort, luggage, and odd office locations."),
            ("Navi Mumbai to BKC?", "Classic long seat-share candidate if windows are fixed."),
            ("Monsoon tips?", "Extra time, waterproof bags, flexible cancel policy in chat."),
        ],
    },
    "mumbai-travel-guide": {
        "city": "Mumbai",
        "aka": "MMR",
        "corridors": [
            "Island city business districts",
            "Western suburbs office belts",
            "Airport (BOM) transfers",
            "Thane / Mulund eastern approaches",
            "Panvel / Navi Mumbai growth corridors",
        ],
        "peaks": "Multiple overlapping peaks; weekend leisure traffic differs from weekday office flows.",
        "parking": "Street parking stress is high — landmark-based shared drops reduce circling.",
        "landmarks": "CST, Churchgate belt, Andheri station east/west, Airport T2 approaches",
        "extra": "Agree toll (Atal Setu / connector) sharing clearly before long MMR rides.",
        "faqs": [
            ("Airport carpool rules?", "Luggage size, terminal, and exact door must be in chat before pickup."),
            ("Is Rydo a cab app?", "No — private seat share with voluntary fuel contribution."),
            ("Best first step?", "Post one recurring weekday route and favourite good partners."),
        ],
    },
    "pune-travel-guide": {
        "city": "Pune",
        "aka": "Poona",
        "corridors": [
            "Hinjewadi IT park phases",
            "Baner / Balewadi / Aundh west belt",
            "Kharadi / Magarpatta / Hadapsar east",
            "Pimpri-Chinchwad industrial links",
            "Airport and Pune station transfers",
        ],
        "peaks": "Hinjewadi entry/exit queues define the day; rain and weekend highway traffic add variance.",
        "parking": "IT park parking + last-mile walks — precise phase/gate names are mandatory.",
        "landmarks": "Hinjewadi Chowk, Wakad bridge, Kharadi bypass, Swargate approaches",
        "extra": "Pune carpools thrive on Hinjewadi and Kharadi recurring loops. Captains should state phase number every time.",
        "faqs": [
            ("Hinjewadi Phase carpool?", "Yes — one of India's densest office seat-share opportunities."),
            ("PMPML + carpool?", "Use bus/metro where dense; seat share for park last-mile."),
            ("Weekend Lonavala shares?", "Works with clear fuel/toll split and luggage rules — see weekend trip guide."),
        ],
    },
}


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = []
    for q, a in faqs:
        items.append(
            f'<details><summary>{q}</summary><p>{a}</p></details>'
        )
    return '<div class="faq">\n' + "\n".join(items) + "\n</div>"


def faq_jsonld(faqs: list[tuple[str, str]]) -> str:
    entities = []
    for q, a in faqs:
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)},
            }
        )
    payload = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n</script>"
    )


def city_block(slug: str, data: dict) -> str:
    city = data["city"]
    corridors = "".join(f"<li>{c}</li>" for c in data["corridors"])
    faqs = data["faqs"] + [
        (
            f"How do I start carpooling in {city} with Rydo?",
            "Download Rydo on Google Play, create a Rider or Captain profile, publish your recurring route and time window, verify with OTP, and favourite reliable partners.",
        ),
        (
            "What costs are shared?",
            "Participants typically agree a voluntary fuel and toll contribution in advance. Rydo is not a taxi and does not set commercial fares.",
        ),
    ]
    return f"""
{MARKER_START}
<h2>Deep dive: daily travel in {city}</h2>
<p>{city} ({data['aka']}) rewards <strong>recurring route matching</strong> more than one-off rides. Captains already driving a corridor can fill empty seats; riders can stop paying full solo fuel and parking every weekday.</p>
<p>{data['extra']}</p>

<h2>High-value corridors &amp; landmarks</h2>
<ul>{corridors}</ul>
<p><strong>Useful landmarks for chat:</strong> {data['landmarks']}.</p>

<h2>Peak hours, delays &amp; buffers</h2>
<p>{data['peaks']}</p>
<p>Practical rule: publish a departure window (for example 8:40–8:55) instead of a single fragile minute. Build 15–30 minutes of buffer on bad-weather or event days.</p>

<h2>Parking, fuel &amp; monthly savings</h2>
<p>{data['parking']}</p>
<p>Estimate your solo spend with the <a href="../cost-calculators/index.html">daily travel cost calculator</a>, then compare a shared-seat week. Many {city} commuters recover thousands of rupees per month once fuel, tolls, and parking are counted together.</p>

<h2>How to match faster on Rydo</h2>
<ol>
<li>Write the corridor like a local: origin landmark → destination gate/tower.</li>
<li>State seats, vehicle type (Moto / Auto / Car), and luggage limits.</li>
<li>Keep the same weekday window for at least two weeks.</li>
<li>After a good trip, add the person to Favourites.</li>
<li>Always use OTP at start and keep live GPS on for longer legs.</li>
</ol>

<div class="callout green"><strong>Compliance note:</strong> Rydo is private carpool &amp; seat share for people already travelling a route — not a taxi, not surge pricing, not a commercial cab substitute.</div>

<h2>Safety checklist for {city} rides</h2>
<ul>
<li>Prefer daytime first rides with new partners</li>
<li>Choose well-lit, busy pickup points</li>
<li>Share live trip status with family on night returns</li>
<li>Keep emergency contacts handy — see <a href="../safety-guides/emergency-contacts-ride-sharing.html">emergency contacts guide</a></li>
<li>Read <a href="../safety-guides/travel-safety-guide.html">travel safety basics</a></li>
</ul>

<h2>Related {city} reading</h2>
<p><a href="../city-guides/index.html">All city guides</a> ·
<a href="../commuter-tips/office-commute-guide.html">Office commute guide</a> ·
<a href="../commuter-tips/peak-hour-tips.html">Peak-hour tips</a> ·
<a href="../blog/how-to-find-carpool-partners.html">Find carpool partners</a> ·
<a href="../blog/how-rydo-works.html">How Rydo works</a></p>

<h2>FAQs — {city} carpool &amp; commute</h2>
{faq_html(faqs)}
{MARKER_END}
"""


# Non-city page expansions keyed by path relative to ROOT
PAGE_BLOCKS: dict[str, tuple[str, list[tuple[str, str]]]] = {}


def block(title: str, body: str, faqs: list[tuple[str, str]]) -> str:
    return f"""
{MARKER_START}
{body}
<h2>Frequently asked questions</h2>
{faq_html(faqs)}
{MARKER_END}
"""


def register(rel: str, body: str, faqs: list[tuple[str, str]]):
    PAGE_BLOCKS[rel] = (body, faqs)


# ---- Safety ----
register(
    "safety-guides/emergency-contacts-ride-sharing.html",
    """
<h2>Why emergency planning matters for shared rides</h2>
<p>Most carpool trips are uneventful. The rare problem — breakdown, medical issue, harassment, or getting stranded — is far easier when you already know <strong>who to call</strong> and how to share your live location.</p>
<h2>Build your personal emergency list</h2>
<ol>
<li>Two family/friends who answer quickly</li>
<li>Local police / women’s helpline numbers for your city</li>
<li>Roadside assistance / insurer number if you drive</li>
<li>Rydo support: <a href="mailto:pktiwari110487@gmail.com">pktiwari110487@gmail.com</a> · <a href="tel:+919026317151">+91 9026317151</a></li>
</ol>
<h2>Before every longer trip</h2>
<ul>
<li>Confirm pickup landmark in chat</li>
<li>Enable live GPS tracking</li>
<li>Share ETA with a trusted contact</li>
<li>Keep phone charged above 30%</li>
<li>Know the next well-lit public place on the route</li>
</ul>
<h2>If something feels wrong</h2>
<p>Trust your instincts. Ask to stop at a busy place, end the trip politely, and contact your emergency person. Use blocking tools for anyone who violated boundaries. Read <a href="../safety-guides/solo-traveller-safety.html">solo traveller safety</a> and <a href="../safety-guides/women-ride-safety.html">women ride safety</a>.</p>
""",
    [
        ("Should I share my live location?", "Yes on longer or night trips — with a trusted contact, not publicly."),
        ("What if the vehicle breaks down?", "Move to a safe spot, call roadside help, inform your emergency contact, and rearrange via chat."),
        ("Does Rydo replace emergency services?", "No. Call local emergency numbers first for crime or medical emergencies."),
    ],
)

register(
    "safety-guides/night-commute-safety.html",
    """
<h2>Night commute realities in Indian cities</h2>
<p>Late office exits, airport runs, and shift work make night travel common. Risk is manageable with <strong>predictable partners, bright pickups, and verification habits</strong>.</p>
<h2>Night-specific habits</h2>
<ul>
<li>Prefer Favourites over brand-new matches after dark</li>
<li>Pickup at petrol pumps, building lobbies, or busy junctions — not dark service lanes</li>
<li>Share live trip + ETA with family</li>
<li>Sit where you can exit easily; keep valuables discreet</li>
<li>Avoid heavy cash display when settling fuel share</li>
</ul>
<h2>Captain checklist for night drops</h2>
<ol>
<li>Confirm rider identity with OTP before starting</li>
<li>Keep tracking on for the full segment</li>
<li>Avoid unnecessary detours without chat consent</li>
<li>Drop at the agreed well-lit point</li>
</ol>
<p>Also see <a href="../safety-guides/otp-ride-safety.html">OTP ride safety</a> and <a href="../commuter-tips/peak-hour-tips.html">peak-hour timing tips</a> for late office exits.</p>
""",
    [
        ("Is night carpool safe?", "It can be when you use verified recurring partners, OTP, live tracking, and busy pickup points."),
        ("Should women avoid night shares?", "Not necessarily — use Favourites, share live status, and prefer known corridors."),
        ("What if plans change mid-route?", "Update chat, keep tracking on, and renegotiate drop only at safe public places."),
    ],
)

register(
    "safety-guides/otp-ride-safety.html",
    """
<h2>What OTP verification actually prevents</h2>
<p>A 4-digit Ride OTP ties the physical vehicle to the matched digital request. It reduces wrong-car boarding and makes “start trip” a deliberate, confirmed action.</p>
<h2>Correct OTP flow</h2>
<ol>
<li>Rider receives OTP in the app for the matched ride</li>
<li>Captain asks for the code at pickup</li>
<li>Trip starts only after correct entry</li>
<li>Live tracking continues until completion</li>
</ol>
<div class="callout"><strong>Never share OTP over public social media</strong> or with someone who is not your matched captain/rider.</div>
<h2>Common mistakes</h2>
<ul>
<li>Starting without OTP “because we are late”</li>
<li>Boarding a similar-looking car without checking details</li>
<li>Reusing screenshots of old OTPs</li>
</ul>
<p>Pair OTP with <a href="../safety-guides/verification-trust-checklist.html">verification checklist</a> habits for stronger trust.</p>
""",
    [
        ("Who generates the OTP?", "The app issues it for the matched ride; the rider shares it only with the matched captain at pickup."),
        ("What if OTP fails?", "Do not start. Re-check the match in-app or contact support."),
        ("Is OTP enough alone?", "No — combine with Favourites, live GPS, and common-sense pickup choices."),
    ],
)

register(
    "safety-guides/rainy-weather-travel-safety.html",
    """
<h2>Monsoon and shared rides</h2>
<p>Rain multiplies risk: low visibility, flooded underpasses, sudden braking, and delayed ETAs. Good carpools plan for weather instead of improvising mid-storm.</p>
<h2>Before you leave</h2>
<ul>
<li>Check local flood-prone underpasses on your corridor</li>
<li>Agree a backup pickup if the usual gate floods</li>
<li>Carry a compact rain cover for bags</li>
<li>Leave earlier — do not compress gaps</li>
</ul>
<h2>While riding</h2>
<ol>
<li>Captains: reduce speed, increase following distance</li>
<li>Avoid unknown short-cuts through waterlogged lanes</li>
<li>Update riders in chat if you divert</li>
<li>Cancel early if authorities close roads</li>
</ol>
<p>Related: <a href="../commuter-tips/monsoon-daily-commute.html">monsoon daily commute</a> · <a href="../blog/monsoon-commute-tips.html">monsoon commute tips</a>.</p>
""",
    [
        ("Should we cancel in heavy rain?", "Yes if visibility is poor or roads are closed — safety beats punctuality."),
        ("Two-wheeler vs car in rain?", "Cars are usually safer for shared monsoon trips; helmets and rain gear are mandatory on two-wheelers."),
        ("Who pays if we turn back?", "Agree a fair partial fuel share in chat; keep it polite and transparent."),
    ],
)

register(
    "safety-guides/solo-traveller-safety.html",
    """
<h2>Solo travellers and seat share</h2>
<p>Travelling alone does not mean travelling unprotected. Layer identity checks, route transparency, and communication habits.</p>
<h2>Solo traveller playbook</h2>
<ul>
<li>Complete your profile with a clear photo</li>
<li>Prefer recurring partners after one good daytime trip</li>
<li>Share live trip with a friend</li>
<li>Keep headphones volume low enough to stay aware</li>
<li>Know how to end a trip early at a busy place</li>
</ul>
<h2>Red flags</h2>
<ol>
<li>Pressure to skip OTP</li>
<li>Unplanned long detours</li>
<li>Requests for personal social handles aggressively</li>
<li>Cash demands far above agreed fuel share</li>
</ol>
<p>See also <a href="../safety-guides/women-ride-safety.html">women ride safety</a> and <a href="../blog/carpool-etiquette.html">carpool etiquette</a>.</p>
""",
    [
        ("First solo ride tips?", "Daytime, short corridor, OTP on, live tracking shared with a friend."),
        ("Can I refuse a ride?", "Yes — before start, or stop at a safe public place if needed."),
        ("Does Favourites help?", "Yes — trust compounds when you ride with the same reliable people."),
    ],
)

register(
    "safety-guides/travel-safety-guide.html",
    """
<h2>End-to-end travel safety framework</h2>
<p>Think in three phases: <strong>before</strong>, <strong>during</strong>, and <strong>after</strong> the trip. Small habits beat occasional panic.</p>
<h2>Before</h2>
<ul>
<li>Match details: name, vehicle hints, landmark, time</li>
<li>Tell someone your ETA</li>
<li>Charge phone; keep emergency list ready</li>
</ul>
<h2>During</h2>
<ul>
<li>OTP verification</li>
<li>Live GPS on</li>
<li>Basic situational awareness</li>
</ul>
<h2>After</h2>
<ul>
<li>Confirm drop landmark</li>
<li>Favourite good partners / block bad ones</li>
<li>Download receipt if you need records</li>
</ul>
<p>Deep dives: <a href="../safety-guides/otp-ride-safety.html">OTP</a> · <a href="../safety-guides/night-commute-safety.html">night safety</a> · <a href="../safety-guides/emergency-contacts-ride-sharing.html">emergencies</a>.</p>
""",
    [
        ("Is carpooling safer than random cabs?", "Private recurring partners plus OTP/GPS can be very safe when habits are followed. It is not taxi regulation — it is coordinated private travel."),
        ("Do I need insurance talk?", "Vehicle owners should understand their own policy; riders should still practise verification habits."),
        ("Kids or elders on shared rides?", "Only with explicit consent, appropriate seats, and conservative route choices."),
    ],
)

register(
    "safety-guides/verification-trust-checklist.html",
    """
<h2>Trust is a checklist, not a vibe</h2>
<p>Use the same steps every time so you do not skip verification when late.</p>
<h2>Rider checklist</h2>
<ol>
<li>Profile photo readable</li>
<li>Route and time match your need</li>
<li>Chat confirms landmark</li>
<li>OTP at pickup</li>
<li>Tracking visible after start</li>
</ol>
<h2>Captain checklist</h2>
<ol>
<li>Rider details match request</li>
<li>Seats and luggage feasible</li>
<li>OTP entered before moving</li>
<li>No unannounced detours</li>
<li>Drop at agreed point</li>
</ol>
<div class="callout green">After 2–3 good trips, add Favourites. Trust should be earned with repetition.</div>
""",
    [
        ("What if photos are unclear?", "Ask a quick confirming detail in chat or skip the match."),
        ("Can I verify without OTP?", "OTP is the strongest start signal — do not skip it."),
        ("How to rebuild trust after a bad trip?", "Block when needed, favourite alternatives, and keep standards high."),
    ],
)

register(
    "safety-guides/women-ride-safety.html",
    """
<h2>Practical safety for women travellers</h2>
<p>Shared mobility should expand freedom, not anxiety. Combine app tools with personal boundaries.</p>
<h2>Recommended habits</h2>
<ul>
<li>Favourite reliable captains/riders</li>
<li>Well-lit public pickups</li>
<li>Live trip sharing with family</li>
<li>Daytime first rides with new people</li>
<li>Clear, firm communication in chat</li>
</ul>
<h2>Boundaries that are always OK</h2>
<ol>
<li>Refusing a match</li>
<li>Insisting on OTP</li>
<li>Choosing a different drop point that is safer</li>
<li>Ending a trip early at a busy place</li>
</ol>
<p>More: <a href="../safety-guides/night-commute-safety.html">night commute safety</a> · <a href="../safety-guides/solo-traveller-safety.html">solo traveller safety</a>.</p>
""",
    [
        ("Can I request women-only preferences informally?", "You can choose partners you trust via Favourites and clear chat. Always prioritise verified, comfortable matches."),
        ("What if someone messages inappropriately?", "Do not continue. Block, report via support channels, and tell a trusted contact."),
        ("Is OTP important for short hops?", "Yes — short trips still need correct-vehicle confirmation."),
    ],
)

# ---- Commuter tips ----
register(
    "commuter-tips/daily-office-carpool.html",
    """
<h2>Make office carpool a system, not a daily scramble</h2>
<p>The commuters who save the most treat seat share like a calendar habit: same corridor, same window, same people.</p>
<h2>Weekly operating rhythm</h2>
<ol>
<li>Sunday: confirm next week’s windows in chat</li>
<li>Weekdays: depart inside the published band</li>
<li>Friday: settle any pending fuel/toll shares</li>
<li>Monthly: re-check costs with the <a href="../cost-calculators/index.html">calculator</a></li>
</ol>
<h2>Office etiquette that keeps groups alive</h2>
<ul>
<li>Message early if WFH or leave changes</li>
<li>Do not make the car a complaint lounge every morning</li>
<li>Rotate music/AC preferences fairly</li>
<li>Keep pickup punctual within 5 minutes</li>
</ul>
""",
    [
        ("How many shared days per week is ideal?", "3–5 stable days beats 1 random day for savings and trust."),
        ("What if my shift changes?", "Update the route window and rebuild Favourites for the new timing."),
        ("Can teammates join mid-month?", "Yes — introduce via chat and clarify seats/fuel share rules once."),
    ],
)

register(
    "commuter-tips/first-time-commuters-guide.html",
    """
<h2>First job, first long commute</h2>
<p>New office-goers often underestimate monthly travel cost and overestimate how sustainable solo riding feels after three months.</p>
<h2>First 30 days plan</h2>
<ol>
<li>Map two backup corridors</li>
<li>Track every rupee for two weeks</li>
<li>Try shared rides on your heaviest days</li>
<li>Learn OTP + tracking habits early</li>
<li>Favourite people who are punctual</li>
</ol>
<p>Read <a href="../commuter-tips/how-to-save-money-on-daily-travel.html">save money on daily travel</a> and <a href="../blog/student-commute-guide.html">student commute guide</a> if you are transitioning from college.</p>
""",
    [
        ("Should I buy a vehicle immediately?", "Not always — calculate true monthly cost first."),
        ("Is carpool unprofessional?", "No — punctual shared travel is common in Indian IT/office corridors."),
        ("What app features matter first?", "Route match, OTP, live GPS, and Favourites."),
    ],
)

register(
    "commuter-tips/fuel-saving-tips.html",
    """
<h2>Fuel savings beyond “drive less”</h2>
<p>Seat share is the biggest lever, but driving style and maintenance still matter for captains.</p>
<h2>High-impact moves</h2>
<ul>
<li>Share seats on your existing route (biggest win)</li>
<li>Maintain tyre pressure</li>
<li>Avoid aggressive acceleration in bumper traffic</li>
<li>Combine errands instead of micro-trips</li>
<li>Track fuel price swings with the <a href="../cost-calculators/index.html">fuel impact tool</a></li>
</ul>
<h2>What not to obsess over</h2>
<p>Tiny hacks rarely beat removing empty-seat kilometres. Focus on occupancy and stable schedules first.</p>
""",
    [
        ("Does AC kill mileage?", "It can, but heat stress and safety matter — share seats to offset cost."),
        ("CNG vs petrol for captains?", "Depends on local refill access; still share seats either way."),
        ("How to split fuel fairly?", "Agree a simple per-seat or distance-based contribution before the week starts."),
    ],
)

register(
    "commuter-tips/healthy-commute-habits.html",
    """
<h2>Commute health is part of work performance</h2>
<p>Long sits, stress, and irregular meals show up as fatigue. Small rituals help.</p>
<ul>
<li>Stretch 2 minutes before/after the ride</li>
<li>Carry water; limit only-caffeine mornings</li>
<li>Use quieter chat norms so the cabin stays calm</li>
<li>Prefer walking the last 200–400m when safe</li>
<li>Protect sleep — leave earlier instead of doom-rushing</li>
</ul>
<p>Pair with <a href="../commuter-tips/peak-hour-tips.html">peak-hour tips</a> to reduce cortisol-heavy delays.</p>
""",
    [
        ("Can carpool reduce stress vs driving solo?", "Often yes — shared driving duty and predictable partners lower daily friction."),
        ("Is walking last-mile worth it?", "Yes for light exercise and parking avoidance when pavements are safe."),
        ("Motion sickness tips?", "Front seat if available, eyes on horizon, cool air, avoid heavy phone reading."),
    ],
)

register(
    "commuter-tips/monsoon-daily-commute.html",
    """
<h2>Monsoon-proof your weekday routine</h2>
<p>The goal is continuity: fewer panic cancels, fewer soaked bags, fewer arguments about delays.</p>
<ol>
<li>Pack a tiny rain kit (cover, napkin, phone pouch)</li>
<li>Define backup landmarks for flooded gates</li>
<li>Shift departure 15–20 minutes earlier in heavy forecast weeks</li>
<li>Agree cancel rules in your Favourites group</li>
</ol>
<p>Safety deep dive: <a href="../safety-guides/rainy-weather-travel-safety.html">rainy weather travel safety</a>.</p>
""",
    [
        ("Who decides to cancel?", "Anyone who feels roads are unsafe should speak early; groups that punish honesty fall apart."),
        ("Umbrella in shared cars?", "Shake outside, store low, keep floors dry — basic etiquette."),
        ("Two-wheeler monsoon shares?", "Use extreme caution; cars are usually better for shared wet-weather trips."),
    ],
)

register(
    "commuter-tips/office-commute-guide.html",
    """
<h2>Designing a calmer office commute</h2>
<p>Great office travel is engineered: corridor choice, timing, partners, and cost tracking.</p>
<h2>Blueprint</h2>
<ul>
<li>Pick one primary corridor and one backup</li>
<li>Publish a realistic departure window</li>
<li>Measure monthly solo cost once</li>
<li>Convert 3+ days to shared seats</li>
<li>Review Favourites monthly</li>
</ul>
<p>Related: <a href="../commuter-tips/daily-office-carpool.html">daily office carpool</a> · <a href="../blog/work-from-office-commute-planning.html">WFO planning</a>.</p>
""",
    [
        ("Hybrid WFO weeks?", "Share on office days only; keep the group updated on WFH days early."),
        ("Manager expects exact punch-in?", "Leave with buffer; reliability is part of the carpool contract."),
        ("Can interns join?", "Yes with clear etiquette and fuel-share understanding."),
    ],
)

register(
    "commuter-tips/parking-cost-savings.html",
    """
<h2>Parking is the silent commute tax</h2>
<p>In business districts, parking can rival fuel. Shared drop at the gate often removes an entire fee line.</p>
<h2>Tactics</h2>
<ul>
<li>Share rides into paid zones</li>
<li>Use park-once + walk for errands</li>
<li>Avoid circling — agree the landmark in chat</li>
<li>Captains: count parking in the weekly share discussion if relevant</li>
</ul>
<p>Run numbers in the <a href="../cost-calculators/index.html">cost calculator</a>.</p>
""",
    [
        ("Who pays parking on shared trips?", "Usually the vehicle user unless the group agrees otherwise — decide upfront."),
        ("Is last-mile walking OK?", "Yes when pavements and lighting are safe."),
        ("Mall parking with office upstairs?", "Shared drop still saves time spent hunting slots."),
    ],
)

register(
    "commuter-tips/peak-hour-tips.html",
    """
<h2>Beat the peak without magical shortcuts</h2>
<p>Peak hour is a physics problem: too many vehicles, not enough road. Your levers are timing, occupancy, and expectations.</p>
<ul>
<li>Shift 15–30 minutes earlier when life allows</li>
<li>Share seats so your corridor carries more people per car</li>
<li>Use live ETAs; do not rage-refresh every minute</li>
<li>Keep a backup landmark if the main gate queue explodes</li>
</ul>
<p>City specifics live in our <a href="../city-guides/index.html">city guides</a>.</p>
""",
    [
        ("Is leaving later ever better?", "Sometimes after the crush — test both for a week and keep data."),
        ("Does carpool get special lane access?", "Depends on city policies; the universal win is lower personal cost."),
        ("How to stay punctual in peaks?", "Buffers + recurring partners + honest ETAs in chat."),
    ],
)

register(
    "commuter-tips/reduce-commute-cost.html",
    """
<h2>A practical cost-reduction stack</h2>
<ol>
<li>Measure baseline (fuel + parking + tolls + maintenance share)</li>
<li>Cut empty-seat days via Rydo matching</li>
<li>Trim micro-trips</li>
<li>Improve driving efficiency</li>
<li>Re-check after fuel price changes</li>
</ol>
<p>Start with <a href="../commuter-tips/how-to-save-money-on-daily-travel.html">10 ways to save</a> and the <a href="../cost-calculators/index.html">calculators</a>.</p>
""",
    [
        ("What is a realistic monthly saving?", "Often meaningful four-figure INR savings for long solo car commutes — calculate your own corridor."),
        ("Does metro make carpool useless?", "No — hybrids are common: metro core + seat share edges."),
        ("Should captains charge profit?", "Rydo is for voluntary cost sharing on private trips, not commercial taxi margins."),
    ],
)

register(
    "commuter-tips/two-wheeler-vs-carpool.html",
    """
<h2>Two-wheeler vs carpool — choose by scenario</h2>
<table>
<thead><tr><th>Scenario</th><th>Often better</th></tr></thead>
<tbody>
<tr><td>Short hop, dry weather, alone</td><td>Two-wheeler</td></tr>
<tr><td>Long corridor, office group</td><td>Carpool</td></tr>
<tr><td>Monsoon / heavy bag days</td><td>Carpool</td></tr>
<tr><td>Erratic late nights</td><td>Depends — prioritise safety partners</td></tr>
</tbody>
</table>
<p>Many people keep both options: bike for flexibility, Rydo seat share for expensive weekdays.</p>
""",
    [
        ("Can moto seats be shared on Rydo?", "Rydo supports ride-type choices including moto where appropriate — follow local safety laws and helmets."),
        ("Insurance concerns?", "Vehicle owners should know their policy; riders should still verify matches."),
        ("Cost comparison tip?", "Include parking and fatigue, not only petrol receipts."),
    ],
)

# ---- Travel guides ----
register(
    "travel-guides/airport-transfer-carpool.html",
    """
<h2>Airport transfers without taxi surge</h2>
<p>Early flights and late landings are perfect for pre-agreed private seat share — if luggage and terminal details are crystal clear.</p>
<h2>Checklist</h2>
<ul>
<li>Terminal + door landmark</li>
<li>Flight time + buffer for security queues</li>
<li>Luggage count and size</li>
<li>OTP + live tracking</li>
<li>Fuel/toll share agreed in chat</li>
</ul>
<p>City airport notes appear inside each <a href="../city-guides/index.html">city guide</a>.</p>
""",
    [
        ("What if the flight is delayed?", "Update chat immediately; agree waiting rules or cancel fairly."),
        ("Max luggage?", "State limits before confirm — do not surprise the captain at the kerb."),
        ("Is this a taxi replacement?", "No — it is private travellers sharing a ride they arrange together."),
    ],
)

register(
    "travel-guides/festival-travel-carpool.html",
    """
<h2>Festival weeks need earlier matching</h2>
<p>Diwali, Holi, Eid, Navratri and regional festivals spike highway demand. Last-minute solo driving is expensive and exhausting.</p>
<ol>
<li>Lock partners 3–7 days ahead</li>
<li>Agree night-driving rules</li>
<li>Split tolls transparently</li>
<li>Plan food/fuel stops</li>
<li>Keep emergency contacts ready</li>
</ol>
<p>See <a href="../travel-guides/highway-carpool-india.html">highway carpool</a> and <a href="../travel-guides/long-distance-seat-share-checklist.html">long-distance checklist</a>.</p>
""",
    [
        ("Should we drive overnight?", "Only with alert drivers and rotation; never force drowsy driving."),
        ("Kids on festival trips?", "Only with explicit consent and appropriate seating."),
        ("How to price fuel share?", "Distance-based split of fuel + tolls is simplest."),
    ],
)

register(
    "travel-guides/long-distance-seat-share-checklist.html",
    """
<h2>Long-distance seat share checklist</h2>
<ul>
<li>Full route + breaks agreed</li>
<li>Driver rotation plan if overnight</li>
<li>Vehicle condition (tyres, lights, AC)</li>
<li>Documents and emergency numbers</li>
<li>Luggage map (who sits where)</li>
<li>OTP at start; tracking for the journey</li>
<li>Clear cancel/refund-style fuel fairness if plans break</li>
</ul>
""",
    [
        ("Minimum notice?", "For highways, earlier is safer — 48 hours+ preferred."),
        ("What if someone cancels last minute?", "Message early; partial contribution norms should be pre-agreed for long trips."),
        ("Night buses vs carpool?", "Compare cost, sleep quality, and safety partners — see our comparison guide."),
    ],
)

register(
    "travel-guides/luggage-tips-shared-rides.html",
    """
<h2>Luggage etiquette for shared vehicles</h2>
<p>Most friction on shared trips is baggage, not personality. Solve it in chat before pickup.</p>
<ul>
<li>State suitcase count and cabin bag sizes</li>
<li>Soft bags nest better than hard giants</li>
<li>Keep a small personal bag at your seat</li>
<li>Do not block rear visibility</li>
<li>Label bags for multi-drop trips</li>
</ul>
""",
    [
        ("Can I bring a bicycle or large carton?", "Only with captain consent and space confirmation."),
        ("Airport trolley to car?", "Help load quickly; do not block terminal lanes."),
        ("Smelly food or wet umbrellas?", "Seal food; shake umbrellas outside — cabin comfort matters."),
    ],
)

register(
    "travel-guides/night-bus-vs-carpool.html",
    """
<h2>Night bus vs carpool — honest comparison</h2>
<table>
<thead><tr><th>Factor</th><th>Night bus</th><th>Carpool</th></tr></thead>
<tbody>
<tr><td>Cost</td><td>Fixed ticket</td><td>Shared fuel/toll</td></tr>
<tr><td>Flexibility</td><td>Depot timings</td><td>Door-to-door possible</td></tr>
<tr><td>Sleep</td><td>Varies by operator</td><td>Depends on seats/driver care</td></tr>
<tr><td>Safety tools</td><td>Operator process</td><td>OTP, GPS, known partners</td></tr>
</tbody>
</table>
<p>Choose based on corridor, group size, and whether you already trust the travellers.</p>
""",
    [
        ("When is bus better?", "When you are solo, want a fixed ticket, and the depot is convenient."),
        ("When is carpool better?", "Small groups, odd origins/destinations, or trusted recurring partners."),
        ("Can I mix modes?", "Yes — bus one way, carpool return is common on weekends."),
    ],
)

register(
    "travel-guides/pilgrimage-route-carpool.html",
    """
<h2>Pilgrimage and faith-route seat share</h2>
<p>Ayodhya, Tirupati, Shirdi, Vaishno Devi approaches and similar corridors see seasonal spikes. Shared private vehicles can reduce cost and chaos when planned respectfully.</p>
<ul>
<li>Agree dress/stop expectations if relevant to the group</li>
<li>Plan parking far from core temple crush when advised</li>
<li>Keep elderly travellers’ comfort in mind (AC, breaks)</li>
<li>Use OTP + tracking on unfamiliar highway segments</li>
</ul>
""",
    [
        ("Is bargaining over fuel OK?", "Be transparent and fair; pilgrimage stress is high enough without money arguments."),
        ("Night arrival tips?", "Pre-book or pre-agree stay; do not improvise in crowded alleys at midnight."),
        ("Family groups?", "Clarify seats for elders/children before confirming."),
    ],
)

register(
    "travel-guides/weekend-trip-fuel-share.html",
    """
<h2>Weekend trips with fair fuel share</h2>
<p>Hill getaways and hometown visits work well when money talk happens before the highway entry.</p>
<ol>
<li>Estimate fuel + tolls roughly</li>
<li>Divide by occupied seats</li>
<li>Decide who pays FASTag and how to settle UPI</li>
<li>List stops and return window</li>
</ol>
<p>Use <a href="../cost-calculators/index.html">calculators</a> for a reality check.</p>
""",
    [
        ("What if we take detours for sightseeing?", "Recalculate share or rotate treat stops fairly."),
        ("Music and AC fights?", "Set norms at the start — see etiquette guide."),
        ("Solo captain with three riders?", "Still voluntary cost share — not a commercial tour price."),
    ],
)

# ---- Sustainability ----
register(
    "sustainability/carpool-carbon-footprint.html",
    """
<h2>Empty seats are wasted carbon</h2>
<p>Every solo car on a duplicated office corridor burns fuel for seats that could have carried people. Seat share raises occupancy and cuts per-person emissions on trips that are happening anyway.</p>
<h2>Personal footprint levers</h2>
<ul>
<li>Share 3–5 commute days weekly</li>
<li>Combine errands</li>
<li>Avoid cold-start micro-trips when walking works</li>
<li>Maintain the vehicle if you captain</li>
</ul>
<p>Continue with the <a href="../sustainability/green-commute-challenge.html">30-day challenge</a>.</p>
""",
    [
        ("Is carpool greener than metro?", "Metro can win on dense corridors; carpool wins when it replaces multiple private cars on the same road."),
        ("Do I need perfect tracking?", "Simple weekly shared-day counts already show progress."),
        ("What about EVs?", "EVs help; empty EV seats still waste road space — share them too."),
    ],
)

register(
    "sustainability/fewer-cars-better-cities.html",
    """
<h2>Cities need fewer redundant car trips</h2>
<p>Road widening never finishes if occupancy stays near one. Cultural habits — Favourites-based seat share, staggered timing, hybrid transit — scale better than concrete alone.</p>
<ul>
<li>Higher occupancy per vehicle</li>
<li>Less circling for parking</li>
<li>Quieter peaks when many people shift 15 minutes</li>
</ul>
<p>Read <a href="../blog/traffic-problem-in-indian-cities.html">traffic problems in Indian cities</a>.</p>
""",
    [
        ("Can one person matter?", "Yes — corridors improve when many individuals adopt the same habit."),
        ("Is this anti-car?", "No — it is anti-empty-seat inefficiency."),
        ("Policy vs apps?", "Both matter; apps help coordination today."),
    ],
)

register(
    "sustainability/green-commute-challenge.html",
    """
<h2>How to run the 30-day challenge properly</h2>
<p>Treat it like a simple experiment with notes — not a guilt contest.</p>
<ol>
<li>Week 1: baseline costs and solo days</li>
<li>Week 2: at least two shared weekdays</li>
<li>Week 3: replace two micro-trips with walking where safe</li>
<li>Week 4: lock Favourites + recurring windows</li>
</ol>
<p>Log fuel money saved and shared-day count. Then keep the habit in month two.</p>
""",
    [
        ("What if I miss a week?", "Restart without drama — consistency beats streaks."),
        ("Can teams do this together?", "Yes — office cohorts on one corridor are ideal."),
        ("Where do I calculate savings?", "Use Rydo’s <a href='../cost-calculators/index.html'>cost calculators</a>."),
    ],
)

register(
    "sustainability/reduce-air-pollution-commute.html",
    """
<h2>Commute choices and local air quality</h2>
<p>Idling in peak congestion concentrates pollution where people walk and wait. Higher occupancy and fewer duplicated trips help your corridor’s air over time.</p>
<ul>
<li>Share seats on the worst peak days</li>
<li>Maintain engines and tyres</li>
<li>Avoid unnecessary revs in standstill traffic</li>
<li>Support walking/transit hybrids for short hops</li>
</ul>
""",
    [
        ("Does one carpool change AQI?", "One trip is small; thousands of shared seats on the same belt matter."),
        ("Masks on pollution days?", "Personal protection still helps even as you reduce emissions."),
        ("WFO vs WFH?", "Hybrid weeks plus shared office days is a practical mix."),
    ],
)

register(
    "sustainability/sustainable-transportation-guide.html",
    """
<h2>Sustainable transport menu for Indian commuters</h2>
<ol>
<li>Walk / cycle micro-trips</li>
<li>Metro/bus for dense corridors</li>
<li>Carpool / seat share for awkward office-park legs</li>
<li>Solo vehicle only when necessary</li>
</ol>
<p>Rydo focuses on the third lever: coordinating private travellers who already share a route.</p>
""",
    [
        ("Is sustainability only for big cities?", "No — any corridor with duplicated solo trips benefits."),
        ("How to start today?", "Download Rydo, post one recurring route, share two days this week."),
        ("Where to learn safety?", "See the <a href='../safety-guides/index.html'>safety guides hub</a>."),
    ],
)

# ---- Blog expansions for thinner posts ----
register(
    "blog/captain-getting-started.html",
    """
<h2>Captain onboarding beyond the basics</h2>
<p>Great captains are predictable: clear windows, clean vehicles, fair fuel talk, and zero OTP skipping.</p>
<ul>
<li>Publish landmarks riders actually recognise</li>
<li>State seat count and luggage policy</li>
<li>Keep a short etiquette note for new riders</li>
<li>Favourite reliable people quickly</li>
</ul>
""",
    [
        ("Do I need a commercial permit?", "Rydo is for private seat share / cost sharing — not running a taxi business."),
        ("How to price fuel share?", "Simple distance or per-seat contribution agreed upfront."),
        ("What if riders are late?", "Define a 5-minute rule in chat and stick to it kindly."),
    ],
)

register(
    "blog/carpool-etiquette.html",
    """
<h2>Etiquette keeps groups alive for months</h2>
<ul>
<li>Punctuality within the agreed window</li>
<li>Hygiene and reasonable volume</li>
<li>No surprise detours</li>
<li>Transparent money</li>
<li>Early cancel messages</li>
</ul>
""",
    [
        ("Food in the car?", "Ask first; avoid strong smells."),
        ("Calls on speaker?", "Prefer earphones and short calls."),
        ("AC wars?", "Agree a default; be flexible on extreme days."),
    ],
)

register(
    "blog/fuel-share-vs-taxi.html",
    """
<h2>Fuel share vs taxi — different products</h2>
<p>Taxis sell transport as a service with commercial fares. Rydo coordinates private travellers sharing a route and contributing to costs.</p>
<table>
<thead><tr><th></th><th>Taxi / cab</th><th>Rydo seat share</th></tr></thead>
<tbody>
<tr><td>Pricing</td><td>Commercial fare / surge</td><td>Voluntary fuel/toll share</td></tr>
<tr><td>Intent</td><td>Hire a ride</td><td>Fill empty seats on an existing trip</td></tr>
<tr><td>Safety tools</td><td>Operator dependent</td><td>OTP, GPS, Favourites</td></tr>
</tbody>
</table>
""",
    [
        ("Can captains profit like cabs?", "No — the model is cost sharing for private trips."),
        ("When is a taxi better?", "Urgent unplanned hops with no matched partner."),
        ("Is fuel share legal goodwill?", "Participants should keep contributions reasonable and transparent; Rydo is not a taxi marketplace."),
    ],
)

register(
    "blog/how-rydo-works.html",
    """
<h2>Mental model of Rydo</h2>
<p>Think <strong>route coordination</strong>, not cab dispatch. Riders search corridors; captains accept compatible seat requests; OTP starts the trusted trip; GPS keeps everyone oriented; receipts help records.</p>
<ol>
<li>Download on Google Play</li>
<li>Choose Rider or Captain mode</li>
<li>Set route + window</li>
<li>Match → OTP → travel → complete</li>
</ol>
""",
    [
        ("Is iOS available?", "Android is available now on Google Play; check the listing for updates."),
        ("Does Rydo set fares?", "No commercial surge fares — voluntary share fuel cost."),
        ("Support?", "Email pktiwari110487@gmail.com or call +91 9026317151."),
    ],
)

register(
    "blog/monsoon-commute-tips.html",
    """
<h2>Extra monsoon tactics</h2>
<ul>
<li>Waterproof phone pouch</li>
<li>Backup landmark list</li>
<li>Earlier departure band</li>
<li>Honest cancel culture</li>
</ul>
<p>Pair with <a href="../safety-guides/rainy-weather-travel-safety.html">rain safety</a>.</p>
""",
    [
        ("Office expects presence in floods?", "Communicate early with both office and carpool group."),
        ("Electronics protection?", "Dry bags beat hope."),
        ("Shoes?", "Keep a spare pair at work in heavy season."),
    ],
)

register(
    "blog/student-commute-guide.html",
    """
<h2>Students and shared travel</h2>
<p>College belts often have identical timetables — perfect for seat share if groups stay disciplined.</p>
<ul>
<li>Match lecture days, not random hours</li>
<li>Split fuel fairly even on small budgets</li>
<li>Use OTP habits early</li>
<li>Avoid overcrowding beyond legal/safe seats</li>
</ul>
""",
    [
        ("Can students be captains?", "If they legally drive and follow private cost-share norms."),
        ("Exam week changes?", "Update the group chat early every day."),
        ("Parents’ concerns?", "Share live tracking and Favourites practices."),
    ],
)

register(
    "blog/traffic-problem-in-indian-cities.html",
    """
<h2>Why traffic feels unsolvable — and what individuals can still do</h2>
<p>Supply of road space grows slower than vehicles. Demand management (timing, occupancy, transit hybrids) is the realistic personal toolkit.</p>
<ul>
<li>Raise occupancy via carpool</li>
<li>Shift peak by 15–30 minutes</li>
<li>Use metro/bus where density wins</li>
<li>Cut pointless micro-drives</li>
</ul>
""",
    [
        ("Will one carpool fix my city?", "No — but it fixes your cost and contributes to corridor occupancy culture."),
        ("Are flyovers enough?", "They help locally; habits determine whether new capacity fills with empty seats again."),
        ("What should offices do?", "Encourage staggered timing and corridor-based carpool groups."),
    ],
)

register(
    "blog/trip-receipts-explained.html",
    """
<h2>Why trip receipts matter</h2>
<p>PDF/trip records help expense discussions, disputes, and personal budgeting — even when contributions are voluntary.</p>
<ul>
<li>Confirm distance/time after completion</li>
<li>Keep monthly folders for fuel share tracking</li>
<li>Use numbers when renegotiating weekly contributions</li>
</ul>
""",
    [
        ("Are receipts invoices?", "They are trip records — not commercial taxi invoices."),
        ("Lost a receipt?", "Check in-app history or contact support if needed."),
        ("Office reimbursement?", "Ask your employer; policies vary."),
    ],
)

register(
    "blog/work-from-office-commute-planning.html",
    """
<h2>Hybrid WFO planning</h2>
<p>When only some weekdays are in-office, carpool groups need sharper calendars.</p>
<ol>
<li>Publish office days every Sunday</li>
<li>Keep a stand-by Favourite</li>
<li>Do not ghost the group on sudden WFH</li>
<li>Recalculate monthly costs for hybrid patterns</li>
</ol>
""",
    [
        ("Two office days enough to carpool?", "Yes — still saves fuel vs two solo drives."),
        ("Different teammates different days?", "Maintain two small Favourites lists."),
        ("Manager changed the roster?", "Notify partners as soon as you know."),
    ],
)

register(
    "blog/benefits-of-ride-sharing.html",
    """
<h2>Second-order benefits people underestimate</h2>
<ul>
<li>Lower parking stress</li>
<li>Built-in punctuality culture</li>
<li>Social accountability on sleepy mornings</li>
<li>Better monthly money visibility</li>
</ul>
""",
    [
        ("Is privacy reduced?", "You share a cabin with chosen partners — Favourites keep it familiar."),
        ("What if I like driving alone?", "Share only on the most expensive days."),
        ("Health angle?", "Less solo stress and optional last-mile walking help some people."),
    ],
)

register(
    "blog/best-travel-apps-for-commuters.html",
    """
<h2>How to build a commuter app stack</h2>
<ol>
<li>Maps + live traffic</li>
<li>Transit apps for metro/bus</li>
<li>Rydo for seat share coordination</li>
<li>UPI for quick fuel-share settlement</li>
<li>Notes/calendar for recurring windows</li>
</ol>
""",
    [
        ("Do I need many apps?", "No — maps + Rydo + UPI covers most shared-commute needs."),
        ("Why not only WhatsApp groups?", "Apps add OTP, tracking, and structured matching beyond chat chaos."),
        ("Offline mode?", "Download offline maps for highway segments."),
    ],
)

register(
    "blog/complete-guide-to-carpooling.html",
    """
<h2>Advanced carpool playbook</h2>
<ul>
<li>Score partners on punctuality privately</li>
<li>Keep a rainy-day backup Landmark B</li>
<li>Review fuel share monthly when prices move</li>
<li>Separate weekday commute groups from weekend trip groups</li>
</ul>
""",
    [
        ("How many people max?", "Never exceed safe legal seating."),
        ("Can companies organise official groups?", "Yes — corridor cohorts work well."),
        ("Where to learn Rydo flows?", "See <a href='../blog/how-rydo-works.html'>How Rydo works</a>."),
    ],
)

register(
    "blog/how-to-find-carpool-partners.html",
    """
<h2>Partner discovery channels that work</h2>
<ol>
<li>Rydo route matching</li>
<li>Office floor / team channels</li>
<li>Society WhatsApp (with caution)</li>
<li>College classmates with same timetable</li>
</ol>
<p>Convert chats into Favourites inside Rydo so OTP and tracking stay consistent.</p>
""",
    [
        ("Cold matching scary?", "Start daytime, short corridor, OTP on."),
        ("What profile helps?", "Clear photo, stable route text, polite chat."),
        ("Dealing with flakes?", "Keep two Favourites; do not rely on one person."),
    ],
)

register(
    "travel-guides/highway-carpool-india.html",
    """
<h2>Highway seat share — advanced tips</h2>
<ul>
<li>Pre-decide FASTag payer and settlement</li>
<li>Rotate drivers on overnight runs</li>
<li>Pack water and basic medicine</li>
<li>Avoid unknown late-night shortcuts</li>
</ul>
""",
    [
        ("Ideal group size?", "Enough to split costs without overcrowding."),
        ("Toll disputes?", "Screenshot tolls and settle via UPI same day."),
        ("Police stops?", "Carry required documents; be polite and factual."),
    ],
)

register(
    "commuter-tips/how-to-save-money-on-daily-travel.html",
    """
<h2>Keep savings visible</h2>
<p>People quit good habits when benefits are invisible. Track shared days and rupees monthly.</p>
<ul>
<li>Screenshot calculator results once a month</li>
<li>Compare against fuel wallet spends</li>
<li>Adjust windows when prices spike</li>
</ul>
""",
    [
        ("Biggest lever?", "Raising occupancy on your longest corridor."),
        ("Smallest lever worth doing?", "Cutting one micro-trip errand loop per week."),
        ("Family cars?", "Still share seats on school/office overlaps when schedules match."),
    ],
)


HUB_INTROS = {
    "guides/index.html": """
{MARKER}
<div class="article-body" style="margin-top:28px;">
<h2>Why Rydo publishes commute guides</h2>
<p>Google-friendly guides only help if they are also practically useful. This hub gathers calculators, city playbooks, safety checklists, and carpool explainers so Indian riders and captains can make better weekday decisions — then coordinate those trips on <strong>Rydo</strong>.</p>
<h2>Start here by goal</h2>
<ul>
<li><strong>Save money:</strong> <a href="../cost-calculators/index.html">Cost calculators</a> + <a href="../commuter-tips/how-to-save-money-on-daily-travel.html">savings tips</a></li>
<li><strong>Travel safer:</strong> <a href="../safety-guides/index.html">Safety guides</a></li>
<li><strong>Match your city:</strong> <a href="../city-guides/index.html">City guides</a></li>
<li><strong>Understand the product:</strong> <a href="../blog/how-rydo-works.html">How Rydo works</a></li>
</ul>
<p>Rydo is route-based carpool &amp; seat share — not a taxi. OTP verification, live GPS, and Favourites help private travellers coordinate recurring corridors across India.</p>
</div>
{/MARKER}
""".replace("{MARKER}", MARKER_START).replace("{/MARKER}", MARKER_END),
}


def strip_old_expansion(text: str) -> str:
    if MARKER_START in text and MARKER_END in text:
        return re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            "",
            text,
            flags=re.S,
        )
    return text


def inject_before_lead(text: str, html: str) -> str:
    text = strip_old_expansion(text)
    if LEAD in text:
        return text.replace(LEAD, html + "\n" + LEAD, 1)
    # fallback: before lead-box
    if '<div class="lead-box">' in text:
        return text.replace('<div class="lead-box">', html + '\n<div class="lead-box">', 1)
    # hubs: before footer
    if "<footer" in text:
        return text.replace("<footer", html + "\n<footer", 1)
    return text


def upsert_faq_jsonld(text: str, faqs: list[tuple[str, str]]) -> str:
    # Remove prior SEO-EXPANDED FAQ scripts? Keep existing FAQPage if present; append ours with marker comment
    snippet = "\n<!-- SEO-FAQ-v2 -->\n" + faq_jsonld(faqs) + "\n"
    if "<!-- SEO-FAQ-v2 -->" in text:
        text = re.sub(r"<!-- SEO-FAQ-v2 -->.*?</script>\s*", "", text, flags=re.S)
    text = text.replace("</head>", snippet + "</head>", 1)
    return text


def bump_dates(text: str) -> str:
    text = re.sub(r'"dateModified":\s*"[0-9-]+"', f'"dateModified": "{TODAY}"', text)
    text = re.sub(
        r"<lastmod>[0-9-]+</lastmod>",
        f"<lastmod>{TODAY}</lastmod>",
        text,
    )
    return text


def expand_file(path: Path) -> bool:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    text = path.read_text(encoding="utf-8")
    changed = False

    slug = path.stem
    if path.parent.name == "city-guides" and slug in CITY:
        faqs = CITY[slug]["faqs"] + [
            (
                f"How do I start carpooling in {CITY[slug]['city']} with Rydo?",
                "Download Rydo on Google Play, create a Rider or Captain profile, publish your recurring route and time window, verify with OTP, and favourite reliable partners.",
            ),
            (
                "What costs are shared?",
                "Participants typically agree a voluntary fuel and toll contribution in advance. Rydo is not a taxi and does not set commercial fares.",
            ),
        ]
        html = city_block(slug, CITY[slug])
        text2 = inject_before_lead(text, html)
        text2 = upsert_faq_jsonld(text2, faqs)
        text2 = bump_dates(text2)
        if text2 != text:
            path.write_text(text2, encoding="utf-8")
            return True
        return False

    if rel in PAGE_BLOCKS:
        body, faqs = PAGE_BLOCKS[rel]
        # extend green-commute self-link weirdness already handled
        html = block("", body, faqs)
        # block() already wraps body; remove empty title usage
        html = f"{MARKER_START}\n{body}\n<h2>Frequently asked questions</h2>\n{faq_html(faqs)}\n{MARKER_END}\n"
        text2 = inject_before_lead(text, html)
        text2 = upsert_faq_jsonld(text2, faqs)
        text2 = bump_dates(text2)
        if text2 != text:
            path.write_text(text2, encoding="utf-8")
            return True
        return False

    return False


def expand_hubs():
    # Add longer intros to category hubs if missing
    hubs = {
        "city-guides/index.html": (
            "City-by-city commute playbooks",
            "Each city guide covers corridors, peak hours, parking pressure, landmarks for chat, and how to match faster on Rydo. Start with your metro, then open the cost calculator to quantify savings.",
        ),
        "safety-guides/index.html": (
            "Safety is a system",
            "OTP, live GPS, Favourites, emergency contacts, and night/monsoon habits work together. Read the guides once, then practise the same checklist every trip.",
        ),
        "commuter-tips/index.html": (
            "Daily habits that cut commute cost",
            "These tips focus on money, time, health, and peak-hour tactics for Indian office corridors — designed to pair with Rydo seat share.",
        ),
        "travel-guides/index.html": (
            "Beyond the daily office run",
            "Airport transfers, festivals, highways, pilgrimage routes, and weekend fuel-share trips need clearer checklists than weekday hops.",
        ),
        "sustainability/index.html": (
            "Lower emissions by filling empty seats",
            "Sustainable commuting is not only metro evangelism — it is raising occupancy on trips already happening across Indian cities.",
        ),
        "blog/index.html": (
            "Guides and explainers for riders & captains",
            "From carpool basics to receipts, etiquette, traffic, and monsoon planning — practical articles for people using Rydo in India.",
        ),
        "guides/index.html": (
            "All Rydo resources in one place",
            "Browse calculators, city guides, safety checklists, commuter tips, travel guides, sustainability pieces, and the blog. Then download Rydo to match your corridor.",
        ),
        "cost-calculators/index.html": (
            "Turn guesswork into numbers",
            "Use the calculators to estimate daily/yearly solo commute cost, fuel-price impact, and per-seat share — then compare with recurring carpool days on Rydo.",
        ),
    }
    count = 0
    for rel, (h2, p) in hubs.items():
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if MARKER_START in text:
            continue
        html = f"""
{MARKER_START}
<div class="article-body" style="margin:28px auto;">
<h2>{h2}</h2>
<p>{p}</p>
<p>Rydo is India’s route-based <strong>carpool &amp; seat share</strong> app for private travellers — OTP safety, live GPS, Favourites, and transparent fuel-cost sharing. Not a taxi.</p>
<ul>
<li><a href="https://play.google.com/store/apps/details?id=com.godrive.rideshare" target="_blank" rel="noopener noreferrer">Download on Google Play</a></li>
<li>Support: <a href="mailto:pktiwari110487@gmail.com">pktiwari110487@gmail.com</a> · <a href="tel:+919026317151">+91 9026317151</a></li>
</ul>
</div>
{MARKER_END}
"""
        # insert before footer
        if "<footer" in text:
            text = text.replace("<footer", html + "\n<footer", 1)
            text = bump_dates(text)
            path.write_text(text, encoding="utf-8")
            count += 1
    return count


def expand_homepage():
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if MARKER_START in text:
        return False
    html = f"""
{MARKER_START}
<section class="how" id="seo-commute-india" style="padding-top:20px;">
  <div class="container">
    <h2 class="section-title">Carpool &amp; seat share for Indian corridors</h2>
    <p class="section-sub">Rydo helps private riders and captains coordinate recurring routes — office belts, college runs, airport transfers, and weekend highway shares — with OTP verification and live GPS.</p>
    <div class="feat-grid">
      <div class="feat-card">
        <h3>Not a taxi</h3>
        <p>Share voluntary fuel and toll costs on trips you are already taking. No commercial surge pricing model.</p>
      </div>
      <div class="feat-card">
        <h3>Built for repetition</h3>
        <p>Favourites, stable windows, and clear landmarks beat one-off matching for real monthly savings.</p>
      </div>
      <div class="feat-card">
        <h3>Learn, then match</h3>
        <p>Use our <a href="city-guides/index.html">city guides</a>, <a href="safety-guides/index.html">safety guides</a>, and <a href="cost-calculators/index.html">calculators</a> before you ride.</p>
      </div>
    </div>
    <div class="faq" style="margin-top:28px;">
      <details><summary>Is Rydo available on Android?</summary><p>Yes — download from Google Play: com.godrive.rideshare.</p></details>
      <details><summary>How is this different from cab apps?</summary><p>Cab apps sell transport as a service. Rydo coordinates private seat share with voluntary cost sharing.</p></details>
      <details><summary>Is OTP mandatory?</summary><p>OTP verification is a core safety step before trip start — do not skip it.</p></details>
      <details><summary>Which cities?</summary><p>Guides cover major Indian metros and corridors; matching works wherever riders and captains share a route.</p></details>
    </div>
  </div>
</section>
{MARKER_END}
"""
    # insert before resources or contact
    needle = '<section class="features" id="resources"'
    if needle in text:
        text = text.replace(needle, html + "\n    " + needle, 1)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if "google" in path.name:
            continue
        if expand_file(path):
            updated.append(str(path.relative_to(ROOT)))
    hubs = expand_hubs()
    home = expand_homepage()
    # sitemap dates
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        sm.write_text(bump_dates(sm.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Updated articles: {len(updated)}")
    for u in updated:
        print(" -", u)
    print(f"Hubs expanded: {hubs}")
    print(f"Homepage expanded: {home}")


if __name__ == "__main__":
    main()
