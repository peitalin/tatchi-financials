# Exporter Roadmap

This roadmap is designed to make us a real exporter first so we can test our wallet, ecommerce tooling, and the AT Protocol + UCP stack against actual cross-border commerce.

## 1. Choose a Narrow Export Wedge and Define the First Catalog

Start with a category that is easy to source, easy to ship, and low-dispute. Japanese tea is the strongest first wedge because it is lightweight, has a long shelf life, and is easier to operationalize than alcohol, fragile drinks, or heavily regulated goods.

Details:

- Focus V1 on processed Japanese tea: matcha, sencha, hojicha, and genmaicha.
- Keep the catalog intentionally small: 8-12 SKUs maximum.
- Build around bundles instead of low-value single-item orders.
- Start with a simple structure:
  - Starter set
  - Premium set
  - Daily-drinker set
  - Gift set
  - A few refill SKUs
- Optimize for operational clarity rather than assortment breadth.
- Choose products that let us test checkout, fulfillment, tracking, disputes, and repeat purchases with minimal customs complexity.

Outcome:

- A focused first catalog that supports export operations and protocol testing without unnecessary category risk.

## 2. Set Up the Exporter Operating Entity and Merchant Stack in Japan

We need a legal and operational base that can buy inventory, issue invoices, receive payments, and ship commercial orders internationally. This store should become the first reference merchant for the broader protocol.

Details:

- Decide whether to use an existing entity or create a new operating entity.
- Set up the business accounts and internal controls required for:
  - Inventory purchases
  - Commercial invoicing
  - International shipping
  - Refund handling
  - Tax and bookkeeping
- Create a clean bookkeeping structure so each shipment has a traceable paper trail.
- Set up the merchant stack:
  - Storefront
  - Order management
  - Customer support inbox
  - Label and invoice generation
  - Accounting tags and reporting
- Treat this merchant implementation as the canonical operator model for our future protocol integrations.

Outcome:

- A functioning exporter entity and an operational merchant stack capable of processing real international orders.

## 3. Build a Reliable Sourcing, Packaging, and Authenticity Workflow

We need supply consistency and a packaging system that can later integrate with wallet flows, escrow, shipment proofs, and tamper-evident verification.

Details:

- Find 2-3 repeatable suppliers rather than relying on one-off sourcing.
- For tea suppliers, prioritize:
  - Consistent lots
  - Product metadata
  - Reliable replenishment
  - Clear resale rights
- Standardize packaging early:
  - Outer mailer
  - Inner presentation
  - Product inserts
  - Seal placement
- Use tamper-evident seals with a unique serial or QR code.
- Tie each seal ID to the order record.
- Add a pack-out proof step:
  - Photograph the packed order
  - Capture the visible seal ID
  - Store this record for later verification and dispute handling
- Define the authenticity record for each product:
  - Origin
  - Producer
  - Lot date
  - Pack date

Outcome:

- A repeatable sourcing and fulfillment preparation workflow that supports authenticity claims and future protocol-native proofs.

## 4. Handle Export and Import Compliance Before Scaling

Compliance is part of the product. We should solve it early enough that our first shipments generate clean operational data instead of ambiguous failures.

Details:

- Create a compliance sheet for each product including:
  - Product description
  - Ingredients or materials
  - HS code
  - Declared value basis
  - Destination restrictions
  - Required supporting documentation
- For food exports, map the destination-country requirements before sale.
- For U.S. food shipments, account for FDA-related requirements such as prior notice and any facility registration exposure in the supply chain.
- Limit the number of launch destinations to 1-3 countries we understand well.
- Build country-specific shipping and customs playbooks instead of pretending V1 is global.
- Assume U.S. shipping will require more deliberate handling, including courier-first planning and real customs treatment.
- Avoid categories with early-stage IP, customs, or licensing complexity until the export process is stable.

Outcome:

- A controlled compliance model for the first export markets, reducing failed shipments and unclear legal exposure.

## 5. Design the Fulfillment and Export Operations Loop

The export business only becomes real when we can execute a deterministic order-to-delivery process and turn each shipment into structured operational events.

Details:

- Define the exact post-purchase sequence:
  - Order paid
  - Pick and pack
  - Seal assigned
  - Commercial invoice generated
  - Shipping label purchased
  - Courier handoff
  - Tracking ingested
  - Delivery confirmed
  - Dispute window opened or closed
- Standardize customs descriptions and invoice wording for each product type.
- Use couriers first to maximize reliability while we learn.
- Record the core shipment state transitions in a structured way so they can later map into protocol-level states.
- Suggested event model:
  - `order_paid`
  - `seal_applied`
  - `shipment_created`
  - `exported`
  - `in_transit`
  - `delivered`
  - `dispute_opened`
  - `released`
- Use this loop to validate not just logistics, but also where escrow state transitions should happen.

Outcome:

- A repeatable exporter operations loop that can later be encoded into wallet, escrow, and logistics specs.

## 6. Use Our Own Store to Test Wallet, Ecommerce Tooling, AT Protocol, and UCP in Layers

We should not launch all protocol ideas at once. The correct approach is to use a working store as the live testbed and then layer protocol capabilities incrementally.

Details:

- Start with a storefront that can actually sell and ship products.
- Add the wallet flow as an optional payment path rather than forcing stablecoin-only checkout at the start.
- Define the core commerce specs we want to validate:
  - Listing
  - Offer
  - Order intent
  - Payment
  - Escrow state
  - Shipment proof
  - Review
  - Seal verification
- Use AT Protocol for:
  - Merchant identity
  - Listing distribution
  - Feed-native discovery
  - Reputation portability
- Use UCP-style structures and flows for:
  - Machine-readable offers
  - Checkout interoperability
  - Agent-mediated commerce
- Keep sensitive order and payment state off the public social layer.
- Use blockchain components specifically where they add value:
  - Escrow
  - Stablecoin settlement
  - Auditable state changes

Outcome:

- A layered testbed where the exporter business validates the wallet, ecommerce tooling, AT integration, UCP alignment, and escrow design.

## 7. Run a Tightly Scoped Pilot and Convert the Results Into Protocol Design

The first milestone is not launching a broad marketplace. The first milestone is successfully exporting a controlled batch of real orders and using that data to shape the system.

Details:

- Set an initial pilot target of 20-50 real international orders.
- Recruit buyers across a small number of countries rather than distributing too widely.
- Observe and document every meaningful failure mode:
  - Checkout abandonment
  - Wallet confusion
  - Customs delays
  - Seal issues
  - Address failures
  - Delivery disputes
  - Refund requests
- Measure actual unit economics:
  - Product cost
  - Packaging cost
  - Shipping cost
  - Duties-related friction
  - Support time
  - Refund loss
- Review what the operational data says about the protocol design:
  - If trust in sellers matters most, improve merchant identity and reputation signals.
  - If logistics ambiguity drives disputes, improve shipment proof and escrow release logic.
  - If bundle economics dominate, refine the storefront and listing model.
- Use the exporter operation as the test harness for protocol revisions instead of designing the protocol in isolation.

Outcome:

- Real-world exporter data that informs the next version of the wallet, storefront stack, AT-based discovery, UCP execution model, and escrow logic.

## Strategic Goal

By following these seven steps, we become a real exporter first and use that operation as the reference implementation for a broader commerce protocol. The exporter business is not separate from the protocol effort. It is the environment that generates the operational truth needed to design the wallet, ecommerce tooling, AT Protocol integration, UCP compatibility, and trust layer correctly.
