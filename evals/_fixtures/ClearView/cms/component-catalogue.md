Status: reviewed

# Component catalogue

> Eval fixture. ClearView Optics is a fictional brand.

- Generated: 2026-11-01
- Source: Storyblok space "ClearView SG – Production" (fictional)

## Hero (hero)
- Purpose: top of page; holds the page's only H1
- Used in page types: promotion, article, product
- Fields: headline – text – required – max 70 chars; subhead – text – optional – max 160 chars; image – asset – required; cta – link – optional
- Variants: none
- Can contain / allowed inside: page body only, first position

## Rich text (rich_text)
- Purpose: body copy with H2/H3 headings, lists and links
- Used in page types: promotion, article, product
- Fields: body – richtext – required
- Variants: none
- Can contain / allowed inside: page body

## FAQ (faq)
- Purpose: question and answer list
- Used in page types: promotion, article, product
- Fields: heading – text – required; items – list of {question – text – required, answer – text – required} – max 8
- Variants: none
- Can contain / allowed inside: page body

## Call to action block (cta_block)
- Purpose: closing call to action
- Used in page types: promotion, article, product
- Fields: heading – text – required; button_label – text – required (approved CTAs only); button_link – link – required
- Variants: none
- Can contain / allowed inside: page body

## Disclaimer (disclaimer)
- Purpose: legal and medical disclaimers
- Used in page types: promotion, article
- Fields: text – text – required
- Variants: none
- Can contain / allowed inside: page body, last position
