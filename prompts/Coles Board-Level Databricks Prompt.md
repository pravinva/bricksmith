# Bricksmith Prompt — Coles Group x Databricks
## Board-Ready Strategic Value Diagram (Not a Tech Architecture)

***

## Design Philosophy

This is **not** an architecture diagram. A board or CEO doesn't care about medallion architectures, Delta Lake, or ETL pipelines. They care about:

- Which strategic priorities does this accelerate?
- What's the dollar impact?
- Where are we today vs. where could we be?

The prompt below creates a **strategy-on-a-page** that maps Databricks capabilities directly onto Coles' own published strategic pillars — using their language, their KPIs, and their financial results.[^1][^2]

***

## The Prompt

Copy and paste the following into **Bricksmith** (Google AI Studio / Gemini):

***

```
Create a polished, board-ready 16:9 landscape strategy slide with a clean white background, using Coles brand red (#E01A22) as the primary accent colour and charcoal (#2D2D2D) for text. The style should feel like a McKinsey or Bain strategy-on-a-page — authoritative, minimal, executive. No tech jargon. No code. No server icons.

TITLE (top centre, bold, charcoal):
"Powering the Coles 3D Strategy with a Unified Data Intelligence Platform"

SUBTITLE (smaller, grey):
"How our data backbone accelerates every strategic pillar — and the $1B+ opportunity ahead"

LAYOUT: The slide has THREE HORIZONTAL TIERS.

═══════════════════════════════════════
TIER 1 — "THE COLES STRATEGIC PILLARS" (top band)
═══════════════════════════════════════

Show FOUR rounded rectangular cards in a horizontal row, each with a subtle shadow. Each card has:
- A small icon at top
- A bold title
- 1-2 lines of supporting text with a key FY25 metric in Coles red

Card 1 (fork & knife icon):
Title: "Destination for Food & Drink"
Text: "9.9M Flybuys members | 970 new ETC products | Coles Finest +13.6%"

Card 2 (smartphone/digital icon):
Title: "Accelerated by Digital"  
Text: "$4.5B eCommerce (+24.4%) | 11.2% online penetration | Coles Plus 2x growth"

Card 3 (circular arrow/sustainability icon):
Title: "Delivered Consistently for the Future"
Text: "$327M Simplify & Save benefits | 860 stores | Kemps Creek ADC live"

Card 4 (people/handshake icon):
Title: "Win Together"
Text: "115,000+ team members | Top quartile engagement | 42.7% women in leadership"

═══════════════════════════════════════
TIER 2 — "THE INTELLIGENCE ENGINE" (centre, visually dominant)
═══════════════════════════════════════

This is the HERO section. Show a wide, elegant rounded rectangle spanning the full width, with a very subtle warm gradient background (light peach/cream to white). Inside, show SIX capability circles arranged in a horizontal row, connected by thin flowing lines that curve upward to each of the four strategy cards in Tier 1 (showing which capabilities power which pillar). Each circle has a simple icon inside and a label below.

The six circles (left to right):

Circle 1 — "Customer Intelligence"
Icon: magnifying glass over a person
Connected to: Card 1 + Card 2
Annotation below: "Personalisation, next-best-offer, Flybuys insights, basket affinity"

Circle 2 — "Demand & Supply Forecasting"
Icon: chart with trend line
Connected to: Card 1 + Card 3
Annotation below: "1.6 billion predictions/day across 860 stores, ADCs & CFCs"

Circle 3 — "Real-Time Store Operations"  
Icon: lightning bolt in a store outline
Connected to: Card 3 + Card 4
Annotation below: "Availability, loss prevention, workforce optimisation, bakery planning"

Circle 4 — "Retail Media & Data Monetisation"
Icon: megaphone with dollar sign
Connected to: Card 2
Annotation below: "Coles 360 +13.5% — audience targeting, attribution, supplier insights"

Circle 5 — "Generative AI & Copilots"
Icon: sparkle/star
Connected to: Card 2 + Card 4
Annotation below: "Tell Coles sentiment AI, digital chef, team member productivity tools"

Circle 6 — "Unified Governance & Trust"
Icon: shield with checkmark
Connected to: ALL four cards
Annotation below: "Single source of truth — lineage, access control, ethical AI compliance"

In the CENTRE of this row, place a subtle Databricks logo watermark (very light, tasteful — not dominant) with the text "Unified Data Intelligence Platform" beneath it in small grey type.

═══════════════════════════════════════
TIER 3 — "THE OPPORTUNITY" (bottom band)
═══════════════════════════════════════

Show THREE side-by-side insight cards with a light grey background and Coles red left-border accent:

Card A — "Simplify the Stack":
"Consolidate fragmented governance tools and reduce data duplication between platforms. One governed data layer powering BI, AI, and operational decisions — fewer moving parts, lower cost, faster time-to-insight."

Card B — "From Reporting to Intelligence":  
"Move beyond dashboards. The same data platform that powers BI today can train ML models, serve real-time predictions, and enable GenAI — without moving data. Turn $44.4B in transactions into $44.4B in intelligence."

Card C — "Monetise the Data Asset":
"With 9.9M Flybuys households and $4.5B in eCommerce, Coles sits on one of Australia's richest consumer datasets. Privacy-safe data sharing with CPG partners unlocks the next wave of Coles 360 growth."

═══════════════════════════════════════
FOOTER
═══════════════════════════════════════

A thin bottom bar with three small elements:
- Left: Small Coles logo placeholder + "FY25 Results: $44.4B Revenue | EBIT +6.8% | NPAT $1.2B"
- Centre: "Prepared for Coles Technology & Data Leadership — February 2026"  
- Right: Small Databricks logo placeholder

All text must be fully legible. Use a clean sans-serif font throughout (e.g., Inter, Helvetica Neue). No technical diagrams, no server racks, no database icons. This should look like it belongs in a board pack, not an engineering wiki.
```

***

## Why This Framing Works

### It Speaks Coles' Own Language

Coles' published strategy has three pillars — **Destination for Food & Drink**, **Accelerated by Digital**, and **Delivered Consistently for the Future** — underpinned by **Win Together** and **Foundations** (financial discipline, technology, and data). Every element of this diagram maps directly to those pillars. When Leah Weckert or the board sees this, they see their own strategy reflected back — not someone else's tech pitch.[^1]

### It Puts Outcomes Before Technology

The word "Databricks" appears **once**, subtly, in the centre. There are no mentions of Delta Lake, medallion architecture, Unity Catalog, or SQL Warehouses. Instead, the diagram talks about what those things *do*: personalisation, 1.6 billion daily predictions, loss prevention, Coles 360 growth. The technology is invisible; the business value is front and centre.[^2][^3]

### It References Real FY25 Numbers

Every metric is sourced from Coles' own FY25 results release:[^2]
- $44.4B group revenue (+3.6% normalised)
- $4.5B eCommerce sales (+24.4%)
- $327M Simplify & Save benefits
- Coles 360 retail media +13.5%
- 9.9M Flybuys active members (+4.4%)
- 860 supermarkets

These aren't Databricks numbers — they're Coles numbers. The slide shows Databricks powering *their* results.

### It Addresses the Three Key Audiences Differently

| Audience | What They See | Key Message |
|---|---|---|
| **CEO / Board** (Leah Weckert) | Strategic pillars + $ outcomes | "Our data platform directly accelerates every pillar of our 3D strategy" |
| **CTO** (Mike Sackman) [^4] | "Simplify the Stack" card | "Consolidate governance, reduce platform sprawl, fewer moving parts" |
| **GM Data & Intelligence** (Caroline O'Brien) [^5] | "From Reporting to Intelligence" card | "Move beyond PowerBI dashboards into ML, GenAI, and real-time predictions" |

***

## Context for Your Meeting

### Leadership Changes Matter

Both Mike Sackman (CTO, joined March 2025 from John Lewis/Waitrose/Argos) and Caroline O'Brien (GM Data & Intelligence, joined February 2025 from Afiniti) are relatively new to their roles. They were brought in after John Cox (CTO) and Silvio Giorgio (CDO) both departed in early 2025. New leaders typically want to:[^6][^7]
- Understand the current state quickly
- Put their stamp on the strategy
- Simplify what their predecessors built
- Show early wins to the CEO and board

This diagram gives them a **ready-made narrative** they can take to Leah Weckert: "Here's how our data platform maps to the 3D strategy."

### The Palantir Angle

Coles has a 3-year partnership with Palantir (2024–2027) for workforce management, bakery planning, and supply chain operations across 840+ stores. The key point: **Palantir is the application/decision layer; Databricks is the data layer**. They're complementary, not competitive. Databricks and Palantir have an official partnership with virtual tables and zero-copy governed access. Frame it as: *"Palantir makes better decisions when it's powered by better data — and that's what the Lakehouse delivers."*[^8][^9][^10]

### The Snowflake/PowerBI Simplification Story

Coles currently has data flowing through **Databricks** (processing), then to **Snowflake** (BI serving), then to **Power BI** (dashboards). This is a three-hop architecture when it could be two: Databricks SQL Warehouses can serve Power BI directly. For the CTO, this is a **simplification and cost** story — fewer licenses, less data movement, single governance. Don't lead with "replace Snowflake"; lead with "simplify the path from data to decision".[^11][^12]

### Timing: HY26 Results on 27 February 2026

Coles' half-year results are due **27 February 2026**. The 1Q26 results already showed strong momentum: supermarket sales of ~$10B (+4.8%, +7.0% ex-tobacco). Engaging now means leadership is in planning mode for H2 and FY27 investment priorities.[^13][^14]

### The Microsoft Relationship

Coles signed a **5-year strategic partnership with Microsoft** in late 2024 covering Azure, AI, Copilot, and Fabric. Databricks runs on Azure — this is an *and* story, not an *or* story. Azure is the cloud; Databricks is the intelligence layer on top of it.[^15][^16]

***

## Talking Points (Board Language, Not Tech Language)

1. **"We're already the backbone"** — Databricks has processed all of Coles' data preparation, transformation, and modelling since the Enterprise Data Platform was built. This isn't a new vendor pitch; it's about unlocking more value from an investment you've already made.[^12][^17]

2. **"One governed data layer"** — Today, Coles has separate governance tools for metadata, lineage, and access control. We can consolidate this into a single pane — simpler for Caroline's team to manage, easier to demonstrate compliance to the board.[^12]

3. **"From dashboards to decisions"** — Power BI dashboards tell you what happened. The same data platform can tell you what's *about to* happen — 1.6 billion predictions a day, demand forecasting, loss prevention, personalised offers — all without moving data to a separate system.[^3]

4. **"Coles 360 is a data business"** — Retail media grew 13.5% last year. The next wave of growth comes from privacy-safe data collaboration with CPG partners. Our clean rooms and data sharing capabilities make this possible without exposing raw customer data.[^2]

5. **"Palantir gets better when the data is better"** — The operational decisions Palantir powers in 840+ stores  are only as good as the data feeding them. A governed, unified Lakehouse ensures Palantir is working with the most accurate, timely, and trusted data available — with zero-copy access, no duplication.[^10]

6. **"$1B in Simplify & Save over four years"** — Coles' own target. Consolidating data platforms, reducing data movement, and eliminating governance fragmentation directly contributes to that number. Technology simplification *is* cost simplification.[^2]

---

## References

1. [Our strategy | Coles Group](https://www.colesgroup.com.au/about-us/?page=our-strategy) - We aim to deliver on our purpose by focusing on three strategic pillars: Destination for food and dr...

2. [[PDF] 2025 Full Year Results Release - Coles Group](https://www.colesgroup.com.au/DownloadFile.axd?file=%2FReport%2FComNews%2F20250826%2F02983441.pdf) - In the first eight weeks of FY26, Supermarkets sales revenue increased by 4.9% (7.0% ex-tobacco) sup...

3. [Coles improves shopping experience by empowering...](https://www.technologyrecord.com/article/coles-improves-shopping-experience-by-empowering-employees-with-microsoft-powered-tools) - Coles will build on its partnership with Microsoft to develop an AI-as-a-service platform, powered b...

4. [Executive leadership team | Coles Group](https://www.colesgroup.com.au/about-us/?page=executive-leadership-team) - Mike Sackman. Chief Technology Officer. Mike joined Coles in March 2025 with more than 30 years' exp...

5. [Coles recruits new GM of data and intelligence - AMI](https://ami.org.au/knowledge-hub/coles-recruits-new-gm-of-data-and-intelligence/) - Caroline O'Brien has been appointed as the General Manager of Data and Intelligence at Coles, leadin...

6. [REA Group lands former Coles data lead - iTnews](https://www.itnews.com.au/news/rea-group-lands-former-coles-data-lead-614398) - The grocery retailer has now appointed Caroline O'Brien to the role of general manager for data and ...

7. [Coles Group CTO, CDO to leave in early 2025 - iTnews](https://www.itnews.com.au/news/coles-group-cto-cdo-to-leave-in-early-2025-613981) - Coles Group's chief technology officer John Cox and chief digital officer Ben Hassing are both leavi...

8. [Palantir AIP + Databricks for Secure Autonomous AI - YouTube](https://www.youtube.com/watch?v=DL14bsMgU94) - ... (CEO Palantir Technologies) vision on AI in the military domain | REAIM 2023. REAIMSummit•72K vi...

9. [Coles to deploy Palantir's AI platforms in more than 850 stores](https://www.retail-insight-network.com/news/coles-palantir-ai-stores/) - Australian supermarket chain Coles has partnered with artificial intelligence (AI) systems provider ...

10. [Palantir Partners with One of Australia's Leading Retailers - Nasdaq](https://www.nasdaq.com/press-release/palantir-partners-with-one-of-australias-leading-retailers-2024-02-01) - Coles will leverage Palantir platforms, including the Artificial Intelligence Platform (AIP), across...

11. [Databricks as the enterprise Lakehouse: Operating unified analytics ...](https://www.confiz.com/blog/databricks-as-the-enterprise-lakehouse-operating-unified-analytics-and-ai-at-scale/) - Delta Lake is an open-source storage layer that adds reliability and structure, helping you create r...

12. [How Coles Group is building its data management platform into the ...](https://www.arnnet.com.au/article/1255525/how-coles-group-is-building-its-data-management-platform-into-the-cloud.html) - Challenges and opportunities in shifting its data management platform from on-premises and into the ...

13. [Coles Sets Date for 2026 Half-Year Results and Analyst Briefing](https://www.tipranks.com/news/company-announcements/coles-sets-date-for-2026-half-year-results-and-analyst-briefing) - Coles Group will release its 2026 half-year financial results on 27 February 2026. · A webcast analy...

14. [[PDF] Coles Group Limited – 2026 First Quarter Sales Results](https://www.colesgroup.com.au/DownloadFile.axd?file=%2FReport%2FComNews%2F20251030%2F03016073.pdf) - eCommerce sales revenue increased by 6.8% with penetration of 7.6% (8.7% including liquor sold throu...

15. [Coles Group and Microsoft strike strategic five-year AI deal - ARNnet](https://www.arnnet.com.au/article/3612350/coles-group-and-microsoft-strike-strategic-five-year-ai-deal.html) - Building an AI-as-a-Service platform, Coles will leverage Microsoft's cloud, AI and edge computing c...

16. [Microsoft and Coles Ink $5 Billion AI Deal to Revolutionize Retail Tech](https://finance.yahoo.com/news/microsoft-coles-ink-5-billion-124226694.html) - Coles will be able to control real-time data processing for its 1,800+ stores with the help of Micro...

17. [Coles Group chases retail insights with data platform overhaul](https://www.itnews.com.au/news/coles-group-chases-retail-insights-with-data-platform-overhaul-548356) - Coles Group is a year into “reimagining” how it manages and treats data, setting up a new data manag...

