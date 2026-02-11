# Nano Banana Pro Prompt — Coles Group x Databricks Architecture Diagram

## Context & Briefing

Below is a ready-to-use **Nano Banana Pro** prompt for generating a professional architecture diagram. It is designed to be presented to **Mike Sackman** (CTO, Coles Group — joined March 2025 from John Lewis/Waitrose/Argos)  and **Caroline O'Brien** (GM Data & Intelligence, Coles Group — joined February 2025 from Afiniti where she was CDO/Head of Product).[^1][^2][^3]

> **Note on CTO**: Coles' current CTO is **Mike Sackman**, not John Cox. Cox departed in early 2025. You may want to confirm the CTO you're meeting with, as the user's original query referenced a "CTO of Coles" generically.[^4]

***

## The Prompt

Copy and paste the following into Nano Banana Pro (Google AI Studio / Gemini API):

***

```
Create a polished, professional enterprise architecture diagram in a clean modern flat-design style, using a dark navy (#0B1D3A) background with white text, Coles brand red (#E01A22) accent lines, and Databricks orange (#FF3621) highlight elements. The diagram should be 16:9 landscape format, high resolution, suitable for an executive briefing slide.

Title at the top in bold white sans-serif: "Coles Group — Unified Data Intelligence Platform powered by Databricks"
Subtitle below in smaller text: "From Lakehouse Foundation to Enterprise AI | Prepared for Coles Technology Leadership"

The diagram should show a LEFT-TO-RIGHT data flow architecture with FIVE clearly labeled vertical columns/zones:

ZONE 1 — "DATA SOURCES" (left edge):
Show icons and labels for these Coles data sources stacked vertically:
- "850+ Stores · POS · IoT" (with a store icon)
- "Intelligent Edge Backbone (Azure Stack HCI)" (with an edge computing icon)
- "Supply Chain · ADCs (Witron) · CFCs (Ocado)" (with a warehouse/logistics icon)
- "Flybuys · 10M+ Members" (with a loyalty card icon)
- "eCommerce · $4.5B · App & Web" (with a mobile/web icon)
- "Coles 360 · Retail Media" (with an ad/media icon)
- "Workforce · Rostering · Shifts" (with a people icon)

ZONE 2 — "INGESTION & STREAMING" (second column):
Show a vertical pipeline with:
- "Azure Event Hubs" 
- "Azure Data Factory"
- "Oracle Golden Gate (Legacy Migration)"
- "Structured Streaming (Real-Time)"
Connected by flowing arrow lines from Zone 1

ZONE 3 — "DATABRICKS LAKEHOUSE PLATFORM" (center, largest zone, highlighted with a subtle Databricks orange glow border):
This is the CORE and should be visually dominant. Show it as a large rounded rectangle containing:

TOP LAYER — labeled "Unity Catalog — Unified Governance":
- "Data Lineage · Access Control · Audit · Compliance"
- "Replaces: Amundsen / Apache Atlas / JanusGraph"
- Show a shield/lock icon

MIDDLE LAYER — show the Medallion Architecture as three horizontal connected boxes:
- Bronze box: "Raw / Landing (Delta Lake)"  
- Silver box: "Curated / Conformed"
- Gold box: "Business-Ready / Feature Store"

BOTTOM LAYER — show four side-by-side capability blocks:
- "Databricks SQL Warehouses — BI Serving at Scale" (with a chart icon)
- "MLflow + Mosaic AI — 1.6B Daily Predictions, Demand Planning, Loss Prevention" (with a brain/AI icon)
- "Delta Live Tables — Automated ETL Pipelines" (with a gear/pipeline icon)
- "Real-Time Streaming — Store Events, Pricing, Availability" (with a lightning bolt icon)

At the bottom of Zone 3, show a small integration callout:
- "Delta Sharing — Open Data Exchange with Suppliers & Partners"

ZONE 4 — "APPLICATION & DECISION LAYER" (fourth column):
Show three distinct blocks stacked vertically, connected from Zone 3:

Block A — "Palantir Foundry & AIP" with a Palantir-style hexagonal icon:
- Sub-labels: "Workforce Optimization · Bakery Planning · Supply Chain Ops"
- "Virtual Tables ↔ Unity Catalog (zero-copy)" in a small annotation
- Note: "Ontology-powered Operational AI across 840+ stores"

Block B — "Power BI + Microsoft Fabric" with a Power BI icon:
- Sub-labels: "Executive Dashboards · Store Manager Insights · Self-Service BI"
- "Direct Query to Databricks SQL Warehouses" in a small annotation

Block C — "AI Applications" with a sparkle/AI icon:
- Sub-labels: "Azure OpenAI · Copilot Agents · Tell Coles (Sentiment AI)"
- "Personalisation Engine · Digital Chef · Coles 360 Targeting"

ZONE 5 — "BUSINESS OUTCOMES" (right edge):
Show a vertical list of outcome badges/cards in Coles red:
- "$44.4B Revenue · 4.3% Volume Growth"
- "$4.5B eCommerce · +24.4% Growth"  
- "1.6B Predictions/Day Across 850+ Stores"
- "$327M Simplify & Save Benefits (FY25)"
- "Coles 360 Retail Media +13.5%"
- "Real-Time C-Suite to Shelf-Edge Decisions"

BOTTOM ANNOTATION BAR (spanning full width):
A thin bar at the bottom with three callouts in white text:
- Left: "TODAY: Delta Lakehouse is already the backbone — Databricks processes all data preparation, transformation & modeling"
- Center: "OPPORTUNITY: Consolidate governance (Unity Catalog), reduce Snowflake BI cost (Databricks SQL), unify AI/ML (Mosaic AI)"
- Right: "PARTNERSHIP: Databricks ↔ Palantir native integration enables zero-copy governed access from Lakehouse to Foundry"

Ensure all text is FULLY LEGIBLE, using clean sans-serif fonts. Use subtle connector arrows between zones to show data flow. The overall look should feel like a McKinsey or Bain strategy slide — authoritative, clean, data-rich but not cluttered.
```

***

## Why This Architecture Resonates with Coles

### They Already Have the Delta Lakehouse Foundation

Coles has been running Databricks as its **central processing technology** since at least 2020, when the Enterprise Data Platform (EDP) was built on Azure. Databricks handles all data preparation, transformation, and modeling on top of Azure Data Lake Storage Gen2 with Delta Lake. Former CTO John Cox confirmed in his departure post that Coles built a "fully cloud native data platform" with "hot-swappable models and automated governance". This is the bedrock — Databricks isn't a net-new sale; it's about **expanding an existing footprint**.[^5][^6][^7]

### The Snowflake/PowerBI Layer Is Just BI — Databricks SQL Can Do This

Coles currently uses **Power BI** for executive dashboards and store-level insights, with data flowing through Snowflake for BI serving. However, **Databricks SQL Warehouses** can serve Power BI directly via DirectQuery or Import, eliminating the need for a separate Snowflake serving layer. Power BI connects natively to Databricks SQL endpoints. This is a cost-consolidation and simplification story — fewer moving parts, single governance model, no data copying between Lakehouse and Snowflake.[^8][^9]

### Palantir Is the App Layer — And Databricks Has a Native Integration

Coles signed a 3-year partnership with Palantir in early 2024 for workforce management, bakery planning, supply chain ops, and operational AI across 840+ stores, processing 10 billion+ rows of data. The key message: **Databricks and Palantir have an official partnership** with Virtual Tables providing zero-copy governed access from the Lakehouse to Foundry, and Unity Catalog integration for governance. This means the Lakehouse data that Databricks already processes can flow directly into Palantir's operational decision layer without duplication.[^10][^11][^12]

### Unity Catalog Replaces Fragmented Governance

Coles historically used **Amundsen + Apache Atlas + JanusGraph** for metadata, lineage, and data discovery. Unity Catalog unifies all of this — access control, lineage, audit, data discovery — in a single pane across all Databricks workloads. For Caroline O'Brien, whose mandate includes "delivery of our data governance strategy" and "embedding our ethical AI framework", this is directly relevant.[^2][^13][^6]

### AI/ML Beyond BI — The Real Growth Story

Coles makes **1.6 billion predictions per day** across stores for demand planning, availability, and loss prevention. They use Azure OpenAI for generative AI, Copilot agents, and the "Tell Coles" customer sentiment system. The growth pitch is:[^14][^9]
- **Mosaic AI** on Databricks for unified model training, serving, and monitoring
- **MLflow** for experiment tracking and model registry across all ML workloads
- **Feature Store** in Unity Catalog for shared features across demand, personalization, and pricing models
- **Databricks Model Serving** for real-time inference at the edge, integrated back to the IEB

### Coles 360 Retail Media — A Data Monetization Play

Coles 360 retail media revenue grew **13.5% in FY25**. This is fundamentally a data business — audience segmentation, attribution, supplier insights. Databricks' clean rooms and Delta Sharing enable privacy-safe data collaboration with CPG advertisers, unlocking further revenue from the Lakehouse data they already govern.[^15]

### Key Financial Context to Reference

| Metric | Value | Source |
|---|---|---|
| FY25 Group Revenue | $44.4B (+3.6%) | [^16] |
| FY25 eCommerce Sales | $4.5B (+24.4%) | [^15] |
| FY25 EBITDA Growth | +10.7% | [^17] |
| FY25 Simplify & Save Benefits | $327M | [^16] |
| Coles 360 Media Growth | +13.5% | [^15] |
| 1Q26 Supermarket Sales | $9.97B (+4.8%, +7.0% ex-tobacco) | [^18] |
| Flybuys Members | ~10M+ households (~80% of AU) | Annual Report |
| Stores | 850+ supermarkets | [^12] |
| Daily Predictions | 1.6 billion | [^9] |
| Microsoft Partnership | 5-year strategic deal (2024) | [^14] |
| Palantir Partnership | 3-year (2024-2027) | [^12] |

### 1H26 Results — Coming 27 February 2026

Coles' HY26 results are scheduled for **27 February 2026**. The 1Q26 results already showed strong momentum with supermarket sales of ~$10B for the quarter (+7.0% ex-tobacco). This timing context is useful — you're engaging just ahead of their half-year results, when leadership is thinking about strategic technology investments for H2 and FY27 planning.[^19][^20][^18]

***

## Talking Points for the Meeting

1. **"You already bet on us"** — Databricks has been the processing engine behind the EDP since 2020. This isn't a new platform; it's about unlocking more value from an investment already made.

2. **"Simplify the stack"** — Unity Catalog replaces the Amundsen/Atlas/JanusGraph governance patchwork. Databricks SQL can serve PowerBI directly, reducing Snowflake dependency and data movement. Fewer copies = lower cost, better governance.

3. **"Databricks + Palantir is a designed integration"** — Virtual Tables and Unity Catalog integration mean the Lakehouse data flows directly into Foundry/AIP without ETL or duplication. This is the reference architecture bp and DoD are already using.[^10]

4. **"AI beyond dashboards"** — Caroline's mandate is to accelerate ML, computer vision, and ethical AI. Mosaic AI + MLflow + Feature Store on Databricks provides a unified ML platform for the 1.6B daily predictions, GenAI apps, and future computer vision workloads — all governed by Unity Catalog.[^2]

5. **"Data as a revenue stream"** — Coles 360 is a fast-growing retail media business. Delta Sharing and Databricks Clean Rooms enable privacy-safe data collaboration with CPG partners — turning the Lakehouse into a monetizable asset.

6. **"Mike's playbook"** — CTO Mike Sackman comes from UK retail (John Lewis, Waitrose, Argos) where Databricks Lakehouses are well-established patterns. He understands this architecture and the value of platform consolidation.[^3]

---

## References

1. [Coles recruits new GM of data and intelligence - AMI](https://ami.org.au/knowledge-hub/coles-recruits-new-gm-of-data-and-intelligence/) - Caroline O'Brien has been appointed as the General Manager of Data and Intelligence at Coles, leadin...

2. [REA Group lands former Coles data lead - iTnews](https://www.itnews.com.au/news/rea-group-lands-former-coles-data-lead-614398) - The grocery retailer has now appointed Caroline O'Brien to the role of general manager for data and ...

3. [Executive leadership team | Coles Group](https://www.colesgroup.com.au/about-us/?page=executive-leadership-team) - Mike Sackman. Chief Technology Officer. Mike joined Coles in March 2025 with more than 30 years' exp...

4. [Coles Group CTO, CDO to leave in early 2025 - iTnews](https://www.itnews.com.au/news/coles-group-cto-cdo-to-leave-in-early-2025-613981) - Coles Group's chief technology officer John Cox and chief digital officer Ben Hassing are both leavi...

5. [Leaving CTO role at Coles, pursuing writing and consulting - LinkedIn](https://www.linkedin.com/posts/john-cox-4477497_after-my-longest-time-in-a-role-ever-i-will-activity-7301390547766628352-Mq4T) - I will be finishing up as CTO at Coles at the end of this month (I will be staying on at the Flybuys...

6. [How Coles Group is building its data management platform into the ...](https://www.arnnet.com.au/article/1255525/how-coles-group-is-building-its-data-management-platform-into-the-cloud.html) - Challenges and opportunities in shifting its data management platform from on-premises and into the ...

7. [Coles Group chases retail insights with data platform overhaul](https://www.itnews.com.au/news/coles-group-chases-retail-insights-with-data-platform-overhaul-548356) - Coles Group is a year into “reimagining” how it manages and treats data, setting up a new data manag...

8. [Databricks as the enterprise Lakehouse: Operating unified analytics ...](https://www.confiz.com/blog/databricks-as-the-enterprise-lakehouse-operating-unified-analytics-and-ai-at-scale/) - Delta Lake is an open-source storage layer that adds reliability and structure, helping you create r...

9. [Coles improves shopping experience by empowering...](https://www.technologyrecord.com/article/coles-improves-shopping-experience-by-empowering-employees-with-microsoft-powered-tools) - Coles will build on its partnership with Microsoft to develop an AI-as-a-service platform, powered b...

10. [Palantir AIP + Databricks for Secure Autonomous AI - YouTube](https://www.youtube.com/watch?v=DL14bsMgU94) - ... (CEO Palantir Technologies) vision on AI in the military domain | REAIM 2023. REAIMSummit•72K vi...

11. [Coles to deploy Palantir's AI platforms in more than 850 stores](https://www.retail-insight-network.com/news/coles-palantir-ai-stores/) - Australian supermarket chain Coles has partnered with artificial intelligence (AI) systems provider ...

12. [Palantir Partners with One of Australia's Leading Retailers - Nasdaq](https://www.nasdaq.com/press-release/palantir-partners-with-one-of-australias-leading-retailers-2024-02-01) - Coles will leverage Palantir platforms, including the Artificial Intelligence Platform (AIP), across...

13. [What is a data lakehouse? - Azure Databricks | Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/) - This article describes the lakehouse architectural pattern and what you can do with it on Azure Data...

14. [Coles Group and Microsoft strike strategic five-year AI deal - ARNnet](https://www.arnnet.com.au/article/3612350/coles-group-and-microsoft-strike-strategic-five-year-ai-deal.html) - Building an AI-as-a-Service platform, Coles will leverage Microsoft's cloud, AI and edge computing c...

15. [[PDF] 2025 Full Year Results Release - Coles Group](https://www.colesgroup.com.au/DownloadFile.axd?file=%2FReport%2FComNews%2F20250826%2F02983441.pdf) - In the first eight weeks of FY26, Supermarkets sales revenue increased by 4.9% (7.0% ex-tobacco) sup...

16. [Coles Group Reports Strong 2025 Financial Results with Strategic ...](https://www.theglobeandmail.com/investing/markets/stocks/CLEGF/pressreleases/34407440/coles-group-reports-strong-2025-financial-results-with-strategic-growth/) - Coles Group Limited announced its 2025 full-year results, highlighting a 3.6% increase in group sale...

17. [Coles Group Ltd (CLEGF) (FY25) Earnings Call Highlights](https://finance.yahoo.com/news/coles-group-ltd-clegf-fy25-070334231.html) - Group Sales Revenue: Increased by 3.6% to $44.4 billion. · Underlying EBITDA: Increased by 10.7%. · ...

18. [[PDF] Coles Group Limited – 2026 First Quarter Sales Results](https://www.colesgroup.com.au/DownloadFile.axd?file=%2FReport%2FComNews%2F20251030%2F03016073.pdf) - eCommerce sales revenue increased by 6.8% with penetration of 7.6% (8.7% including liquor sold throu...

19. [Key investor dates | Coles Group](https://www.colesgroup.com.au/investors/?page=key-investor-dates) - HY26 results. 27 February 2026, Add to Calendar. 3Q26. 1 May 2026, Add to Calendar. Dates are subjec...

20. [Reporting Season - CommSec](https://www.commsec.com.au/market-news/reporting-season.html) - February 2026 reporting season is here. Market analysts Steven Daghlian and Laura Besarati give insi...

