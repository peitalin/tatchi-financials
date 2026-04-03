# Wallet Infrastructure Comparison

## Market View

As of **April 2, 2026**, the wallet infrastructure market breaks into three adjacent categories:

- **Privy** is sold primarily as developer-friendly embedded wallet onboarding with MAU-based pricing.
- **Dynamic** is also sold primarily around embedded wallet UX and MAU-based monetization, with additional server wallet usage pricing.
- **Turnkey** is sold primarily as signing infrastructure with usage-based pricing tied to signatures.

Our current spreadsheet model sits between these categories. It combines a developer subscription, per-org MAU pricing, and metered transaction pricing in [assumptions.py](/Users/pta/Dev/web2/tatchi-financials/pipeline/assumptions.py#L59) and [wallet_projection_revenues.py](/Users/pta/Dev/web2/tatchi-financials/pipeline/wallet_projection_revenues.py#L313). That makes us cheaper than Privy and Dynamic on early paid tiers, but not clearly better than Turnkey on raw signing economics. In other words, we are currently priced as a hybrid, while the incumbents are positioned more cleanly.

The strategic risk is straightforward: generic wallet infrastructure is already crowded. We should not position ourselves as another embedded wallet SDK or generic wallet backend.

## Competitor Snapshot

| Provider | Primary product story | Pricing model | Relative strength | Relative weakness vs us |
| --- | --- | --- | --- | --- |
| Privy | Embedded wallets and onboarding | MAU-priced | Strong developer UX and consumer onboarding | Less differentiated around escrow, controlled money movement, and custody portability |
| Dynamic | Embedded wallets and wallet UX | MAU-priced plus server wallet usage | Strong UX and broad wallet product surface | Less differentiated around programmable escrow and sovereignty |
| Turnkey | Signing infrastructure | Signature-priced | Clean signing-infra story and usage pricing | Narrower product story around signing rather than escrow workflows |
| Tatchi | Threshold wallet + stablecoin escrow + recovery workflows | Should be workflow- and value-based | Can tie pricing directly to money movement and controlled operations | Must avoid looking like a generic wallet vendor with a confusing hybrid pricing model |

## Positioning

The primary differentiator should be:

- **programmable stablecoin escrow + threshold signing + recovery workflows**

The secondary differentiator should be:

- **open, auditable, and migratable custody infrastructure**

Put directly:

- Privy and Dynamic sell **wallet onboarding**
- Turnkey sells **signing infrastructure**
- We should sell **programmable stablecoin escrow and controlled money movement**

This is the sharper narrative:

- stablecoin escrow infrastructure rather than generic wallet plumbing
- threshold signing for both Ed25519 and ECDSA with operational recovery paths
- developer-facing money movement workflows: escrow, release conditions, disputes, treasury controls, policy approvals, recovery, and auditability
- commercial alignment to economic value created: money moved, escrow events, signatures, recoveries, and active transacting wallets

That is a stronger market position than trying to compete feature-for-feature on login UX or generic wallet provisioning.

## Open Core And Migration

Open source by itself is not enough. The stronger message is **no vendor lock-in with a credible migration path**.

The value proposition is:

- **No vendor lock-in**
- **Self-hosting path for regulated or security-sensitive customers**
- **Custody and security posture can migrate in-house over time**
- **Open SDKs and core relay/signing infrastructure are auditable**

That matters because Privy, Dynamic, and Turnkey are primarily sold as managed infrastructure. If we offer a credible path from **hosted -> hybrid -> self-hosted**, that gives buyers something the others generally do not emphasize as strongly.

The migration story is credible because we have:

- clear export and import paths for keys, policies, wallet state, and recovery configs
- deployment docs for self-hosting
- no hidden proprietary dependency in the critical path
- SDK and relay interfaces that remain stable across hosted and self-hosted modes
- passkey migration support using **ROR** so existing registered passkeys can continue working under the customer-controlled domain
- support for customer domains fronted to our infrastructure from day one, reducing future passkey migration friction because the relying-party domain does not need to change

The positioning should be:

**“Start managed, migrate to self-hosted when you need more control.”**

That is stronger than just saying “we are open source.”

## Custody Model

The custody story should stay high-level and precise.

In managed mode, the correct claim is not cryptographic non-custody. The defensible claim is **strong operational assurance**:

- key material is derived or handled only inside attested infrastructure
- sensitive root material is sealed inside TEE or HSM boundaries
- derivation and export operations are gated by quorum approval
- security-sensitive actions are covered by immutable audit trails
- customers can bring their own domain and recovery configuration
- customers can later migrate to a fresh customer-controlled root when they need stronger custody separation

That framing matters. It avoids overclaiming while still giving customers a credible control and migration story.

## Pricing Implications

The current MAU-heavy model is not the cleanest fit for the product we want to sell.

If our differentiation is controlled money movement rather than generic wallet onboarding, the pricing model should move closer to:

- low platform fee for developer organizations
- included signatures or active transacting wallets
- metered **signature pricing**
- metered **recovery / policy / approval / webhook / compliance workflow events**
- take rate on **escrow volume** where we are providing escrow value

This would sharpen the economic narrative:

- cheaper than Privy and Dynamic for teams that do not want to pay primarily for passive MAUs
- competitive with Turnkey on signing only if we lower signature pricing materially
- higher-value than all three when customers need escrow operations, policy controls, and recovery workflows

The main weakness in the current model is not just price level. It is that the pricing story still looks too generic relative to the product we want to build.

## Conclusion

The cleanest strategic position is:

**Tatchi is a threshold wallet and programmable stablecoin escrow platform for fintech and marketplace money movement.**

The company should not present itself as wallet infrastructure for everyone. The more precise positioning is:

- primary: **money movement workflows**
- secondary: **sovereignty and migration**

That combination is strong:

- **Turnkey** is strong on signing infrastructure
- **Privy** and **Dynamic** are strong on developer UX
- We can differentiate on **money movement workflows + sovereignty**
