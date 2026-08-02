# Portfolio Audit — t_d8617cd1

**Date:** 2026-08-02
**Scope:** index.html, projects.html, about.html, contact.html, lessons.html, pm_ai_field_notes.html, case-studies/, ai-news/
**Card:** t_d8617cd1 (Portfolio & LinkedIn Refresh)

---

## Summary

The portfolio is in strong shape. Six projects are framed with Problem → Process → Outcome (or Challenge → Process → Outcome), the hero has a clear "Open to Work" band with a connect button, and the resume is one click from every page. The audit found one dead relative path, a set of stale nav links in the generated ai-news pages, and two text-hygiene issues (space-dash-space patterns) that the humanizer gate flags. All were fixed.

## Broken Links

| # | Location | Issue | Fix |
|---|----------|-------|-----|
| 1 | `case-studies/next-best-prompt-engine.html` | "Back to Portfolio" links to `./` which resolves to `case-studies/` (no index.html there) | Changed to `../index.html` (both footer and top back-links) |
| 2 | `ai-news/*.html` (24 generated pages + weekly) | Sidebar nav links to `../apply.html` which does not exist | Removed Apply link from sidebar nav |
| 3 | `ai-news/*.html` bottom-nav | Links to `../ai-news.html` which does not exist | Changed to `../ai-news/` |
| 4 | `deploy_ai_news.py` | Nav template still emitted `../apply.html` and `../ai-news.html` | Updated HEAD + bottom-nav templates so regenerated pages stay correct |

Verified: all local hrefs on index, projects, about, contact, lessons, pm_ai_field_notes, and case-studies resolve to real files. All external links (LinkedIn, GitHub, career-ops.org, Hermes docs, storysundays.com) use full URLs.

## Mobile Rendering

- `style.css` has responsive breakpoints at 768px (bottom-nav replaces sidebar), 600px (about grid stacks), and 640px (hero/project scaling). These look correct.
- SVGs in projects use `viewBox` + `width:100%;max-width:720px`, so diagrams scale down cleanly on phones.
- Case study page collapses its 3-column grids to 1 column at 700px.
- Bottom-nav on index has 7 items; at 375px wide this is tight but usable (10px labels). Minor, not blocking.

## CTA Clarity

- **Hero:** "See the projects →" primary button + email ghost button + "Open to Work" band with a LinkedIn connect button. Strong.
- **Nav:** Resume download present on every page (sidebar + bottom-nav). Good.
- **Contact page:** email + LinkedIn buttons. Good.
- **Projects/about/lessons:** These rely on the persistent nav resume link. Acceptable since the resume is one click away everywhere.

## Text Hygiene (Humanizer Gate)

The BRD requires removing space-dash-space patterns from portfolio text. Found and fixed:

- `index.html` title `Dustin Felderhoff - Building...` → `Dustin Felderhoff: Building...`
- `index.html` Project 6 subtitle + problem text (2 em-dash-with-spaces)
- `projects.html` title + ` - ` separator between Live/GitHub links
- `about.html`, `contact.html`, `lessons.html` page titles (` — ` → ` : `)
- `pm_ai_field_notes.html` title + Next Best Prompt Engine heading + Context paragraph
- `case-studies/next-best-prompt-engine.html` title + 6 body instances

New content added (Currently Building section, About learning note, Project 6 lesson boxes, LinkedIn posts) was written humanizer-clean from the start: no space-dash-space, varied paragraph lengths, no GPT transitions.

Note: `ai-news/*.html` body text is machine-generated daily briefing content produced by `deploy_ai_news.py` from news feeds. It is not authored portfolio copy and gets regenerated from the source feed on each deploy. This BRD's humanizer gate covers authored portfolio text and LinkedIn posts; the ai-news briefings are a separate generated artifact. My changes to ai-news pages were nav-only (removing the dead `../apply.html` link and fixing `../ai-news.html` → `../ai-news/`).

## Prioritized Issue List

| Priority | Issue | Status |
|----------|-------|--------|
| P0 | Dead back-link on case study (404 on GitHub Pages) | Fixed |
| P0 | ai-news nav 404s (`../apply.html`, `../ai-news.html`) | Fixed |
| P1 | Space-dash-space AI tells across pages | Fixed |
| P1 | No "Currently Building" section showing live work | Added to index.html + projects.html |
| P2 | Project 6 had no Lesson Learned box | Added two (dual-track A/B, life event override) |
| P2 | About section did not reference continuous learning | Added Field Notes link |
| P3 | Bottom-nav 7 items on index is tight at 375px | Left as-is (works, minor) |

## Deliverables Completed

1. ✅ Audit with prioritized issue list
2. ✅ Top fixes implemented (dead links, nav 404s, humanizer tells)
3. ✅ PM + AI Field Notes lessons synced into Project 6 lesson boxes
4. ✅ "Currently Building" section on index.html + projects.html
5. ✅ 8 LinkedIn posts drafted and humanized (`.hermes/plans/linkedin-content-plan.md`)
6. ✅ All existing content preserved (no deletions of copy)
7. ✅ Case study link works end-to-end
8. ✅ Portfolio shows continuous iteration (Currently Building + Field Notes)
9. ✅ All portfolio text + posts pass humanizer gate
