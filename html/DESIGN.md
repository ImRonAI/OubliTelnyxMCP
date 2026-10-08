# Oubliai implementation dossier — document design

## 0. Reference and constraints
Base reference: writing-html-design-docs/skeleton.html, adapted into a multipage reading system. This is a plan artifact, not product UI implementation. No generated imagery, React setup, or new product dependency is required. Research/agent completion receipts from the earlier attempt are unavailable; no independent-review claim is made from them.

## 1. Direction
Dark editorial technical dossier. Quiet emerald accents mark navigation and verified primitives; amber marks compatibility gates. Content is the focal point, with generous reading measure and stable cross-page navigation, not a marketing landing page.

## 2. Tokens
Background #070809; sidebar #0c0d11; surfaces #101218; raised #15171f; border #262a36; body #c4c8d6; primary text #e6e8ef; muted #9aa0b4; accent #34d399; amber #fcd34d. Inter/system body, Outfit/system display, JetBrains Mono/ui-monospace code. Body 16px/1.8; h1 clamp 32–48px; h2 27px; h3 20px; mono 12–13px. 4px base grid; reading measure 76ch, wider tables scroll inside containers.

## 3. Layout
Nine linked HTML chapters. Sidebar 224px on desktop; the main workspace uses all remaining viewport width, with no centered max-width or narrow prose cap. Under 900px a compact native chapter picker replaces the wrapped nine-link menu when JavaScript is available; no-script chapter links remain usable. Chapter title, concise lead, facts strip, local contents and detailed semantic sections. Wide inventories/tables use the available workspace. A complete-plan page reproduces every source-plan section.

## 4. Reusable primitives
Chapter navigation active state; section eyebrow; callout (verified/proposed/gate); card; table wrapper; inline code; code block; next/previous links; search input for section filtering; print stylesheet. Links have clear hover and keyboard focus. No decorative continuous animation. Reduced motion disables smooth scroll.

## 5. Accessibility and offline
Skip link, landmarks, headings, descriptive titles, persistent link labels, high contrast, semantic tables, no hidden critical content. Every chapter works without JS and without CDN styles/fonts through inline fallback CSS. Print expands content and removes navigation. Content search may hide sections only after explicit input; clear restores all.

## 6. QA
Open every chapter at desktop and mobile, check links/anchors, tables and code overflow, keyboard navigation and search/clear. Browser screenshots are evidence of the document only, not evidence that the planned Telnyx product works. Do not claim Lighthouse/independent review unless actually run.
