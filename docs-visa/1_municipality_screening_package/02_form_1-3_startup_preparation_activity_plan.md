# 02 - Form 1-3: Startup Preparation Activity Plan (Draft Skeleton)

Use this as a writing skeleton before transferring content into the official Form 1-3 template.

## 0) Document Controls
- [ ] Version: `v0.1 / v0.2 / final`
- [ ] Last updated: `YYYY-MM-DD`
- [ ] Primary owner: `Name`
- [ ] Linked evidence folder: `path`

## Visa-Oriented Plan Skeleton

Use the following structure when drafting the visa-facing startup plan. The goal is to prove that the business can realistically be established and operated in Japan.

### 1) Applicant profile

This explains who you are, what your role is, and why you are qualified.

For this case, include:
- CTO role
- PhD in economics/finance
- 10+ years software experience
- startup engineering background
- technical work in finance / VC context
- specific relevance to MPC wallets, cryptography, escrow, and commerce infrastructure

Draft prompts:
- Applicant name:
- Role in the business:
- Academic background:
- Technical background:
- Startup experience:
- Why this background is relevant to the proposed business:

### 2) Business overview

This is the heart of the plan.

You need to explain:
- what the company builds
- who pays for it
- what problem it solves
- why the solution is better than current alternatives
- why the business can generate revenue

For this startup, frame it as:
- embedded wallet infrastructure for ecommerce
- smart-contract escrow
- logistics and shipping oracle integrations
- stablecoin FX / settlement support
- lower lock-in through migration toward self-hosting
- secure passkey / Face ID native checkout and wallet flows
- merchant-focused JPY / USD / EUR settlement and on-ramp / off-ramp tooling

Draft prompts:
- Product / service summary:
- Customer problem:
- Proposed solution:
- Why existing alternatives are insufficient:
- Why this business can make money:

### 3) Market and customers

You need to identify:
- the target customers
- the market segment
- why they need this now
- why they would buy from you

For this startup, likely customer groups are:
- marketplaces
- cross-border ecommerce platforms
- merchant infrastructure providers
- operators needing order-specific escrow and programmable settlement
- merchants sourcing goods in Japan and selling internationally in USD or EUR
- merchants selling higher-value goods that benefit from escrow and real-time shipment tracking

Draft prompts:
- Primary customer segment:
- Secondary customer segment:
- Urgency of the problem:
- Buying decision maker:
- Why these customers would adopt this product:

### 4) Competitive differentiation

The plan should show why this is not a generic clone.

State clearly:
- competitors like `Privy` and `Dynamic` handle embedded wallets
- the differentiation is not generic wallet onboarding
- the focus is ecommerce-specific workflows
- the second differentiator is migration / self-hosting path and lower lock-in
- the product is effectively a stablecoin-native Shopify toolkit for cross-border commerce

Japan-specific pain points that may be worth solving:
- FX spread and settlement friction for merchants who source in JPY but sell internationally in USD or EUR
- high fees and slow reconciliation on traditional card-based cross-border payments
- chargebacks on international card payments even when the merchant has already shipped goods
- landed-cost uncertainty, import duty surprises, and parcel refusals that turn into costly refunds or reverse logistics
- customs and export-document coordination for small merchants without internal trade-ops systems
- proof-of-shipment, proof-of-delivery, and condition / authenticity disputes for higher-value goods
- slow payout timing for merchants that need working capital to reorder inventory from Japanese suppliers
- fragmented coordination across merchant, logistics provider, escrow logic, and refund / dispute handling

Draft prompts:
- Main competitors:
- What they do well:
- What they do not focus on:
- Why this company is different:
- Why the differentiation matters commercially:

### 5) Founder role and team structure

You need to explain who is doing what.

For this strategy, state:
- cofounder is CEO and handles sales / operations / business development
- founder is CTO and handles technical architecture, MPC wallet infrastructure, applied cryptography, and implementation
- external support can include accountant, legal, scrivener, and contractors if needed

Draft prompts:
- CEO responsibilities:
- CTO responsibilities:
- External advisors / service providers:
- Planned hires or contractors:

### 6) Revenue model

You need to explain how money comes in.

For this case, include:
- B2B SaaS subscription
- usage-based wallet / MAU / transaction pricing
- escrow fees
- optional logistics-oracle managed-service revenue

Reference:
- [wallet_financial_model_assumptions.md](/Users/pta/Dev/web2/tatchi-financials/data/wallet_financial_model_assumptions.md)

Draft prompts:
- Base subscription model:
- Usage-based pricing:
- Escrow revenue:
- Logistics / oracle revenue:
- Revenue expansion path over 12 to 24 months:

### 7) Budget and cash flow

This section should show:
- available funds
- expected costs
- expected revenue
- how long the business can operate

This needs to answer:
- can the business survive the startup period?
- can it fund business setup in Japan?
- can it become a viable company?

For this case, include:
- available capital and liquid assets
- startup costs
- monthly operating costs
- runway
- year-one revenue assumptions from the spreadsheet model

Draft prompts:
- Founder funds available:
- Additional liquid assets:
- One-time setup costs:
- Monthly burn:
- Year-one revenue estimate:
- Runway estimate:

### 8) 12-month roadmap

This should show month-by-month or phase-by-phase progress.

Typical milestones:
- company formation
- product MVP
- first pilots
- first paying customers
- partnerships
- compliance setup
- office / operating setup
- revenue milestones

Draft prompts:
- Month 1-3 milestones:
- Month 4-6 milestones:
- Month 7-9 milestones:
- Month 10-12 milestones:
- KPI targets for each phase:

### 9) Reason business can succeed in Tokyo / Japan

This section should explain:
- why Tokyo is the right base
- why the market exists here
- why the product is relevant to Japan and cross-border trade
- what partnerships / ecosystem advantages Tokyo gives

For this case, the working narrative is:
- the company is focused on exporting high-quality Japanese goods to international buyers with quicker settlement, lower payment friction, fewer chargebacks, and more controlled refunds
- Japan has a strong base of artisanal, specialty, and quality-focused merchants whose products are attractive to overseas buyers
- many of these merchants and platforms can benefit from better cross-border settlement, escrow, and post-purchase logistics tooling
- Tokyo provides access to exporters, logistics operators, fintech and compliance advisors, and cross-border trade partners
- Tokyo is also a strong base for emerging regulated digital-asset infrastructure, including new yen stablecoin projects and enterprise blockchain settlement initiatives

Draft prompts:
- Why Tokyo:
- Why Japan:
- Relevance to cross-border commerce:
- Strategic local partnerships or ecosystem advantages:
- Cross-border merchant pain points addressed by the product:

### 10) Evidence and attachments

Every major claim should be backed by something.

Expected evidence types:
- resume
- degrees
- work history
- GitHub / OSS
- bank statements
- lease / residence proof
- customer discussions or LOIs if available
- financial model outputs

Draft prompts:
- Evidence for qualifications:
- Evidence for technical track record:
- Evidence for funds:
- Evidence for residence:
- Evidence for demand / customer interest:
- Evidence for financial assumptions:

## 1) Applicant and Startup Basics
1. Applicant name: ``
2. Nationality: ``
3. Proposed company name (if decided): ``
4. Business category/industry: ``
5. Planned office location in Tokyo: ``
6. Planned incorporation timing: `YYYY-MM`

## 2) Business Summary (One Page)
1. Problem statement:
   - Current pain point: Ecommerce operators that want to add onchain payments, escrow, and post-purchase automation still have to stitch together wallet infrastructure, custody decisions, dispute handling, logistics status data, and cross-border settlement workflows.
   - Who is affected: Marketplace operators, high-trust ecommerce merchants, cross-border commerce platforms, and logistics-linked commerce businesses that need order-specific payment controls rather than a generic wallet.
   - Why existing options are insufficient: Generic embedded-wallet providers solve login and wallet creation, but they do not primarily optimize for transaction-scoped escrow, shipping and delivery attestation, stablecoin FX settlement logic, or a migration path toward self-hosted wallet infrastructure.
2. Solution summary:
   - Product/service: An embedded-wallet and wallet-orchestration platform for ecommerce that supports stablecoin-based escrow, logistics-linked oracle events, and settlement flows designed around real order lifecycles, with secure passkey and Face ID native wallet experiences.
   - Core value proposition: Help commerce platforms and merchants launch wallet-based escrow and settlement faster, with a clearer path from managed embedded wallets to a self-hosted or lower lock-in setup as the customer matures.
   - Key differentiator: The product is positioned around three specific advantages: a migration-friendly wallet architecture with an upgrade path toward self-hosting, verticalized ecommerce modules such as smart-contract escrow and logistics/shipping tracking oracles, and cross-border merchant tooling for JPY sourcing with USD/EUR sales and stablecoin settlement.
   - Risk model advantage: By combining passkey- and biometric-authenticated wallet flows with stablecoin settlement, the product reduces merchant exposure to traditional card-not-present fraud and unauthorized-use chargeback patterns. The platform then focuses dispute handling on genuine commerce issues such as damaged goods, non-conforming items, shipping failures, authenticity concerns, and refund allocation. In this way, payment fraud risk and product dispute risk are treated as separate operational problems rather than being forced into a single card chargeback framework.
3. Why now:
   - Market/technology/regulatory timing: Stablecoin settlement, embedded wallets, and programmable commerce workflows are becoming easier to deploy together. Merchants and platforms increasingly want programmable payment control without building their own wallet stack from scratch.
4. Why Japan/Tokyo:
   - Local market reason: Tokyo is a strong base for cross-border commerce, logistics, enterprise software sales, and partnership development with marketplaces, trading businesses, exporters, and fintech-adjacent operators. The business is specifically focused on helping merchants export high-quality Japanese goods to international buyers with quicker settlement, lower payment friction, fewer chargebacks, and more controlled refunds.
   - Ecosystem/supply chain/talent reason: Tokyo offers access to startup support, legal/accounting professionals, engineering talent, and enterprise customers relevant to regulated fintech and commerce infrastructure, while Japan's reputation for high-quality goods supports export-oriented merchant use cases. Tokyo is also a natural base for working with logistics, customs, and payments partners involved in cross-border trade.

## 3) Product/Service Detail
1. Product scope (MVP -> next versions):
2. Main features:
3. Delivery model (SaaS/service/hybrid):
4. Development and operations setup:
5. IP or know-how (if any):

## 4) Target Customers and Market
1. Primary customer segment:
   - Customer profile: Ecommerce platforms, marketplaces, merchant software operators, and export-oriented merchants that need embedded wallets plus order-linked escrow and settlement workflows.
   - Geography: Japan-first commercial base with broader cross-border use cases in Asia, North America, and Europe.
   - Buying decision maker: Founder, CTO, Head of Payments, or GM of commerce operations.
2. Secondary segment (optional):
   - Secondary segment: Logistics-enabled commerce operators, inspection-based marketplaces, and merchants selling higher-value goods that benefit from shipping-event attestations and dispute-aware settlement.
3. Market size estimate:
   - TAM: Broad embedded-wallet and wallet infrastructure demand across fintech and digital commerce.
   - SAM: Commerce platforms specifically needing escrow, logistics-linked payment events, stablecoin settlement workflows, and merchant tooling for sourcing in JPY while selling internationally in USD or EUR.
   - SOM (12 months): Based on the current projection model, the initial operating target is to ramp from `6` developer organizations in month 1 to `18` developer organizations by month 12, with paying organizations increasing from `4` to `13`.
4. Evidence of demand:
   - Interviews: To be filled with founder pipeline evidence.
   - Pilot users: Draft commercial model assumes first-year traction consistent with the spreadsheet ramp from `1,125` MAU in month 1 to `5,135` MAU by month 12.
   - LOIs/partnership discussions: To be added as supporting evidence in the package if available.
   - Market context: METI's FY2024 E-Commerce Market Survey reports continued growth in cross-border EC between Japan, the U.S., and China, and JETRO continues to operate export-support programs and buyer-matching channels for Japanese companies seeking overseas sales.

## 5) Competitive Landscape
1. Main competitors/alternatives:
   - Main reference competitors are `Privy` and `Dynamic`, plus internal in-house wallet builds and generic payment orchestration vendors.
2. Comparison table:
   | Area | Generic embedded wallet providers | Proposed business |
   | --- | --- | --- |
   | Wallet onboarding | Strong | Strong |
   | Commerce-specific escrow flows | Limited / not core focus | Core focus |
   | Logistics and shipping oracle linkage | Usually custom work | Productized add-on |
   | Stablecoin FX workflow support | Partial / implementation-dependent | Core vertical feature |
   | Cross-border JPY sourcing to USD/EUR sales workflows | Not core focus | Core merchant use case |
   | Passkey / Face ID native commerce wallet UX | General wallet UX | Optimized for checkout and commerce flows |
   | Upgrade path to self-hosting | Often weaker or more custom | Deliberate product design goal |
   | Lock-in sensitivity for customers | Higher concern | Lower-lock-in positioning |
3. Defensible advantage:
   - Defensible advantage comes from product direction rather than generic wallet access alone: transaction-scoped escrow design, logistics-linked settlement automation, merchant-friendly FX and settlement flows for Japan export commerce, and an architecture that lets customers start managed and move toward self-hosting as they scale.
   - Another key differentiator is that passkey and biometric-authenticated wallet flows create stronger proof of user authorization than traditional card checkout, while stablecoin settlement avoids a large class of card-network chargeback mechanics. This allows the product to reduce fraud-driven reversals while preserving structured dispute handling for real commerce issues.
4. Main risks and mitigation:
   - Risk: Larger wallet vendors can add adjacent features.
   - Mitigation: Focus on the ecommerce-specific workflow layer and operational integration, not only wallet creation.
   - Risk: Customers may move slowly on regulated stablecoin use cases.
   - Mitigation: Start with narrowly scoped platform customers and keep legal/compliance structure conservative.
   - Risk: Integration complexity can slow sales.
   - Mitigation: Offer opinionated escrow and logistics modules with clear API boundaries.
   - Risk: Cross-border merchants still face logistics, customs, and refund complexity outside the payment layer.
   - Mitigation: Focus on programmatic settlement triggers, shipment-event attestations, and dispute tooling that reduce those frictions rather than claiming to replace the entire trade stack.
   - Japan export pain points this product can address:
   - FX spread and settlement friction for merchants who source inventory and pay suppliers in JPY but sell internationally in USD or EUR.
   - High card-processing costs and chargeback exposure on international ecommerce transactions.
   - Slow reconciliation and payout timing, which creates working-capital pressure for merchants reordering goods from Japanese suppliers.
   - Proof-of-shipment, proof-of-delivery, and authenticity or condition disputes for higher-value goods.
   - Reverse-logistics and refund complexity when international buyers reject parcels after customs duties, shipping delays, or delivery issues.
   - Documentary and operational burden around export proof, shipping records, and tax treatment for cross-border transactions.
   - Refund and chargeback pain points this product can address:
   - In standard card flows, merchants often face both unauthorized-use payment disputes and genuine product disputes through the same blunt chargeback process.
   - In this model, payment authorization risk is reduced by the wallet plus stablecoin design, while product, fulfillment, and logistics disputes are handled through escrow, shipment evidence, and structured dispute resolution.

## 6) Revenue Model and Go-To-Market
1. Pricing model:
   - Plan/pricing tiers: Current draft model uses a base developer subscription of `$79` per paying organization per month, plus MAU-linked pricing. Year-one modeled customers stay within the `starter` tier at `$50` per paying organization per month for MAU pricing.
   - Contract type: B2B SaaS subscription plus usage-based fees and optional managed-service revenue for logistics-linked escrow workflows.
2. Revenue drivers:
   - Number of customers: Model assumes ramp from `4` paying organizations in month 1 to `13` paying organizations by month 12.
   - Average contract value: Base first-year SaaS ARPU is modest because customers are early-stage and remain in the starter pricing band during year one.
   - Conversion assumptions: The model assumes `70%` of developer organizations convert into paying organizations.
   - Merchant value proposition: Refunds become programmable value transfers rather than card-network reversal events. This can reduce refund transaction friction and support more flexible outcomes such as seller-paid, buyer-paid, or shared-cost allocation for return shipping, inspection, restocking, or other dispute-related costs.
3. Sales channels:
   - Direct sales: Founder-led outreach to marketplaces, merchant platforms, export-oriented merchants, and commerce infrastructure operators.
   - Partner channel: Legal, integration, logistics, and cross-border commerce partners that can refer customers needing escrow or shipping-linked settlement workflows.
   - Online acquisition: Content, developer documentation, demos, and targeted fintech/ecommerce distribution.
   - Ecosystem angle: Tokyo-based partnerships with exporters, logistics providers, customs brokers, and regulated stablecoin or settlement infrastructure providers can accelerate adoption.
4. Month 1-12 sales targets:
   - New leads/month: Initial target `20-30` relevant outbound and referral conversations per month.
   - Qualified leads/month: Initial target `5-8`.
   - Closed customers/month: Model implies approximately `1` net new paying organization per month on average, with stronger conversion in later months as product proof improves.
   - Additional service expansion: A logistics managed-service layer is assumed to begin in month 10, generating first-year additional revenue of about `$1,738.56` on top of base wallet revenue.
   - Commercial messaging: fewer fraud-driven reversals, better dispute granularity, lower merchant risk, and more controlled refund logic for cross-border commerce.

## 7) 12-Month Execution Plan
Use concrete monthly milestones.

| Month | Product Milestone | Business Milestone | Legal/Admin Milestone | KPI Target |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |
| 7 |  |  |  |  |
| 8 |  |  |  |  |
| 9 |  |  |  |  |
| 10 |  |  |  |  |
| 11 |  |  |  |  |
| 12 |  |  |  |  |

## 8) Team and Roles
1. Founder role and responsibilities:
   - Founder/CTO leads technical architecture, applied cryptography, MPC wallet infrastructure, wallet security, and product implementation in Japan.
2. Co-founder(s) or key hires (if any):
   - Current operating assumption is a lean year-one team of `3` people total, aligned with the model.
   - Suggested structure for the draft plan:
   - Cofounder / CEO: sales, operations, partnerships, customer development, and business execution.
   - Founder / CTO: wallet orchestration, applied cryptography, backend systems, and smart-contract integration.
   - Engineer or technical operator: frontend/integration work, implementation support, and customer onboarding.
3. External support (accountant, legal, scrivener, etc.):
   - External accountant or tax advisor in Japan.
   - Legal counsel for company formation, commercial terms, and fintech compliance review.
   - Administrative scrivener or equivalent visa/corporate filing support as needed.
4. Hiring plan (if any):
   - Role: Technical and implementation support.
   - Start month: During year 1 as customer pipeline validates.
   - Cost estimate: To be finalized based on Japan hiring or contractor structure.

## 9) Financial Plan (JPY)
1. Startup costs (one-time):
   - Draft note: The source financial model is in USD. For visa-plan drafting, convert to JPY using a single internal planning FX assumption before filing the official form.
   - Working planning FX assumption for this draft: `JPY 150 = USD 1`.
   - Registration/incorporation: Model includes one-time setup cost of `$500`, approximately `JPY 75,000` under the working draft FX assumption.
   - Equipment/software: To be supplemented with founder-specific hardware and setup costs if not already owned.
   - Professional services: Add Japan legal, accounting, incorporation, and visa support costs as separate line items in the final form.
2. Monthly operating costs:
   - Office/housing: To be added from actual Tokyo residence and office plan.
   - Payroll: Not yet separated in the synthetic model and should be added in the official plan based on actual founder salary and any local hires.
   - Tools/infrastructure: Year-one modeled technology and infrastructure expense totals `$38,560.30`, averaging about `$3,213.36` per month.
   - Marketing/sales: Year-one modeled sales and marketing expense totals `$45,600`, or `$3,800` per month.
   - G&A: Year-one modeled general and administrative expense totals `$2,012`, including one-time setup cost in month 1.
3. Funding source:
   - Personal funds: To be supported by bank evidence in the visa package.
   - External funding: Draft assumption is founder-funded initial setup, with optional future external capital after early customer validation.
4. Runway estimate:
   - Current available cash: To be replaced with actual bank evidence.
   - Monthly burn: Year-one modeled total operating expenses average about `$7,181` per month.
   - Months of runway: To be calculated after inserting real founder cash position and Japan-specific payroll/residence costs.
5. 12-month projection summary:
   - Revenue: Base wallet year-one revenue is modeled at `$115,831.36`. With the logistics add-on, year-one total revenue is modeled at `$117,569.92`.
   - Expenses: Year-one operating expenses are modeled at `$86,172.30`.
   - Net: Operating profit is modeled at `$29,659.06` on a base-wallet basis and `$31,333.00` with the logistics add-on.
   - Volume assumptions: Year-one modeled escrow volume totals about `$11.28M` across `3,489` transactions, with average monthly escrow fee revenue of about `$8,459.36`.

## 10) Compliance and Setup Plan
1. Entity setup path:
   - Entity type: Final entity choice to be confirmed with Japan legal and tax advisors. A standard Japan operating company structure will be selected based on visa, governance, and tax efficiency.
   - Registration sequence: Secure address, complete company formation, open bank account, execute accounting and tax registration, and complete immigration-related filings.
2. Banking/accounting/tax setup:
   - Open a Japan business bank account after incorporation.
   - Retain local accounting support for bookkeeping, tax filings, and consumption-tax review if applicable.
   - Maintain clear separation between founder funds, corporate funds, and any customer transaction flows.
3. Licenses/permits needed (if any):
   - Final licensing analysis is a required legal workstream before launch. The business plan should state that product rollout will be scoped to the legally supportable operating model confirmed by Japanese counsel.
   - The initial product design is intentionally narrow: stablecoin-only, transaction-scoped escrow tied to an underlying order, and no general-purpose open-loop wallet balances.
   - If any regulated payment, custody, exchange, or transfer activity is implicated, launch scope will be adjusted or delayed until the correct structure, partnerships, or registrations are in place.
   - The ecosystem for regulated yen-denominated stablecoin and tokenized settlement infrastructure in Japan is developing. For example, SBI Holdings and Startale Group announced `JPYSC`, a trust-bank-backed JPY stablecoin project targeted for 2026 launch, which supports the broader thesis that Tokyo is becoming a relevant base for regulated digital settlement infrastructure.
4. Data/privacy or sector-specific compliance (if any):
   - Prepare privacy policy, terms of service, and customer agreements for wallet and escrow workflows.
   - Implement KYC/AML, sanctions screening, transaction monitoring, and audit logging to the extent required by the final operating model.
   - Commission smart-contract and application security review before handling production customer value.

## 11) Evidence Mapping (Attach Proof)
Map each major claim to a document in the package.

| Claim | Evidence File Name | Folder | Ready (Y/N) |
| --- | --- | --- | --- |
| Market demand exists |  |  |  |
| Founder has relevant experience |  |  |  |
| Funds are sufficient |  |  |  |
| Tokyo residence plan is valid |  |  |  |
| Partnerships/customers in pipeline |  |  |  |

## 12) Consistency Check Before Finalizing
- [ ] Business activity wording matches Form 1-1
- [ ] Dates align with resume (Form 1-4)
- [ ] Address/location details align with residence proof
- [ ] Funding numbers align with bank evidence
- [ ] Timeline is realistic for Designated Activities period
- [ ] All amounts are in JPY

## 13) Finalization Checklist
- [ ] Draft completed
- [ ] Internal review done
- [ ] Numbers and dates verified
- [ ] Moved to official Form 1-3 document
- [ ] Final PDF exported and saved in this folder
