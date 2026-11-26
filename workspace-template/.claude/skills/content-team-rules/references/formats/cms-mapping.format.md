> FORMAT REFERENCE. The Librarian drafts <project>/cms/cms-mapping.md in this shape, from the catalogue; you review it with a developer.
> Generated files start with "Status: draft"; change to "Status: reviewed" once checked.

# CMS mapping: Storyblok

Translates the neutral content model (`learned/content-model.md`) into Storyblok.
Only the CMS Operator and Component Librarian use this file.



- Space: TODO (name / ID)
- Last checked against catalogue: TODO (date)

---

## Page types -> content types

| Neutral page type | Storyblok content type | Folder (full slug) | Notes |
| --- | --- | --- | --- |
| promo-landing | TODO e.g. page_promo | TODO e.g. sg/en/promotions/ | |
| product | TODO e.g. page_product | TODO | |
| article | TODO e.g. page_article | TODO | |

## Sections -> nestable blocks

| Neutral section | Storyblok block | Variant field / options | Allowed inside |
| --- | --- | --- | --- |
| hero | TODO e.g. hero_banner | TODO e.g. variant: image-left, full-bleed | body |
| key-benefits | TODO e.g. feature_grid | | body |
| rich-text | TODO e.g. rich_text_block | | body |
| product-highlight | TODO | | body |
| offer-details | TODO | | body |
| faq | TODO e.g. faq_list | | body |
| cta-banner | TODO | | body |
| store-locator-cta | TODO | | body |
| terms | TODO | | body |

## Field mapping per block

Format: neutral field -> Storyblok field key (field type, required?)

### hero -> TODO block name
- headline -> TODO e.g. title (text, required)
- subhead -> TODO e.g. subtitle (textarea)
- image -> TODO e.g. image (asset, required)
- cta -> TODO e.g. cta_link (multilink)

### key-benefits -> TODO block name
- items -> TODO e.g. items (bloks: feature_item, 3–6)
  - title -> TODO
  - text -> TODO
  - icon -> TODO

TODO: repeat for each block.

## Page-level fields

| Neutral field | Storyblok field | Type |
| --- | --- | --- |
| title | TODO (story name) | |
| SEO title / meta description | TODO e.g. seo (SEO plugin field) | plugin |
| slug | story slug | |
| sections | TODO e.g. body | bloks |
| campaign start / end date | TODO | datetime |

## Locales

- Strategy: TODO (folder-level e.g. sg/en/, sg/zh/ OR field-level translation)
- Languages: TODO (default first)
- How the Operator creates a translated version: TODO

## Conventions

- Drafts only: the Operator saves, never publishes
- Slug format: lowercase-hyphenated
- Asset folder for new images: TODO e.g. /campaigns/<year>/
- Tag to add on every story agents create or edit (keep existing tags): TODO e.g. "ai-draft"
