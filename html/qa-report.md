# HTML plan document — browser verification

## Deliverable
Nine linked chapters under `.omo/plans/html/`, complete rewritten Markdown plan, downloadable exhaustive operation inventory and original OpenAPI schema. This verifies the document surface only; future product implementation is not claimed.

## Actual checks on the final generated revision
- Playwright opened all nine pages at 1920, 1280, 768 and 375 pixels after the full-width revision: 36 page/viewport combinations.
- Desktop reading workspace has no max-width: measured 1,696px beside the 224px rail on a 1,920px viewport, and 1,056px on a 1,280px viewport. Main workspace reaches the right viewport edge.
- Tablet/mobile chapter picker navigated to the selected chapter; the long wrapped chapter menu is not shown when JS enables the picker.
- Each had one H1; no unresolved local section anchors, duplicate DOM IDs, rendered template placeholders, or document-level horizontal overflow.
- Desktop full-page screenshots and tablet/mobile viewport screenshots captured for every page.
- Source-operation register contains exactly 1,382 table rows; expanding the Assistants group worked without causing page overflow.
- Section search displayed the empty state for a non-match; clearing restored all sections.
- Clicked real chapter link and local section link: both navigated correctly.
- All nine chapter URLs and three portable source downloads returned HTTP 200.
- Two official reference links returned HTTP 200: FastMCP OpenAPI integration and official MCP Apps build documentation.
- No page JavaScript errors were captured. Tailwind's CDN emits its standard production-use warning; this is a static plan artifact, and all necessary reading/layout styles are also inline.
- No-JavaScript / blocked-CDN mobile test preserved all 12 server-page sections, all nine navigation links, readable 32px heading, and no root overflow.

## Fixed during actual browser QA
- Tailwind preflight initially reduced heading sizes: specificity corrected in shared document styles.
- Slash-separated identifiers caused mobile overflow on inventory/roadmap/full specification: content wrapping fixed; all page/viewport checks re-run and screenshots re-captured after the fix.
- Preview initially requested a missing favicon: self-contained SVG favicon added.
- Relative Markdown downloads initially pointed outside the served bundle: portable source copy and links fixed.
- User-requested full-screen layout: removed centered main/prose caps, reduced navigation rail, widened reference tables and replaced mobile wrapped navigation with a native picker. All nine pages were captured again at four viewport widths.

## Independent review limitation
Read-only reviewer launch returned an authentication error. No independent visual/content approval or Lighthouse result is claimed. This report is direct browser and source verification, not the dual-review completion gate. The limitation is also disclosed in the Transparency chapter.

## Content audit
- Server/OpenAPI configuration and native four-tool chaining are documented.
- Native Client capabilities, facilitator runtime and assistant-to-widget compatibility blocker are documented.
- Native GenerativeUI lifecycle, action chaining, official AppBridge and design-token mapping are documented.
- Communications including fax/email/video/external meetings, AI voice/inference/training/RAG, and storage have concrete source operation examples plus exhaustive source schema/register.
- Build order, parallel lanes, 27 tasks, 4 final verifiers, dependencies, test commands and evidence are preserved in complete-plan chapter.
- All artifacts are planning documentation; no production server/client/app code was created by this run.
