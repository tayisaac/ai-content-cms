> FORMAT REFERENCE. The Librarian writes <project>/learned/content-model.md in this shape.
> Generated files start with "Status: draft"; change to "Status: reviewed" once checked.

# Content model (neutral)

The page types and sections the team may use. Written in plain terms: no Storyblok
component or field names here (those go in `cms/cms-mapping.md`).

Agents use this to decide what a page must contain. The Page Architect may only create
page types listed here, and only with the sections listed for that type.

---

## Section types

Reusable building blocks, shared across page types.

| Section | Purpose | Key fields |
| --- | --- | --- |
| hero | Top-of-page headline and main visual | headline, subhead, image, cta |
| key-benefits | 3–6 short benefit points | items (title, text, icon) |
| rich-text | Free-form body copy | body |
| product-highlight | Feature one or more products | products, headline |
| offer-details | Promo mechanics: what, who, when | headline, body, start date, end date |
| faq | Questions and answers | items (question, answer) |
| cta-banner | Single call to action | headline, cta |
| store-locator-cta | Push to find a store / optician | headline, cta |
| terms | Legal terms and conditions | body |

TODO: add, rename or remove sections to match what your site actually has.

---

## Page type: promo-landing

- Purpose: time-limited campaign page
- Allowed folder: TODO (e.g. promotions)
- Required sections (in order): hero, key-benefits, offer-details, cta-banner, terms
- Optional sections: product-highlight, faq, store-locator-cta
- Required page fields: title, SEO title, meta description, slug, campaign start date, campaign end date
- Rules:
  - Exactly 1 hero, always first
  - terms always the last section
  - Offer end date must appear in hero or offer-details
- Agents may create from scratch: TODO yes / no

## Page type: product

- Purpose: one product or product range
- Allowed folder: TODO (e.g. products)
- Required sections (in order): hero, key-benefits, rich-text, store-locator-cta
- Optional sections: faq, product-highlight, cta-banner
- Required page fields: title, SEO title, meta description, slug, product name
- Rules:
  - TODO
- Agents may create from scratch: TODO yes / no

## Page type: article

- Purpose: educational / eye-health content
- Allowed folder: TODO (e.g. articles)
- Required sections (in order): hero, rich-text
- Optional sections: faq, cta-banner, product-highlight
- Required page fields: title, SEO title, meta description, slug, author, publish date
- Rules:
  - TODO (e.g. medical review needed before approval)
- Agents may create from scratch: TODO yes / no

TODO: add any other page types (store locator, about, careers...) or delete unused ones.
