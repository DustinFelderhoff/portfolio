# Next Best Prompt Engine — Product Development Case Study

> **Context:** Personal project (Story Sundays — family story-sharing app)
> **Role:** Product Owner / Product Manager
> **Outcome:** Iterative algorithm design from MVP → research → hybrid A/B architecture based on user feedback

## The Problem

A family story-sharing app sends one prompt per day to each family member (e.g., "What's your favorite memory of Grandma?"). The initial MVP used a basic algorithm: exclude seen prompts, balance categories, prioritize personal prompts from family members. Users reported prompts felt repetitive and didn't account for real life events.

## The Process

### Phase 1: User Feedback
User identified several gaps:
- No life event triggers (birthdays, new family members, anniversaries)
- No re-engagement for inactive users
- No A/B testing to validate which algorithm works better
- Different generations may prefer different recommendation approaches

### Phase 2: Industry Research
Researched recommendation algorithms from major platforms:
- **Netflix** — Multi-layer personalization (75% of watched content from recommendations)
- **Duolingo** — Half-Life Regression + Thompson Sampling for lesson sequencing
- **Anki/SuperMemo** — SM-2 spaced repetition algorithm, FSRS (three memory states)
- **Pinterest** — Pixie random-walk recommendation
- **Competitors** — StoryWorth, 1000 Questions, Remento, Life Stories

### Phase 3: Algorithm Design
Designed three candidate algorithms:

| Option | Approach | Key Insight |
|---|---|---|
| A: EOSRS | Weighted scoring | Blends SRS skip cooldown + emotional valence + specificity |
| B: Thompson Sampling | Bayesian bandit | Learns per-category answer rates, auto-explores |
| C: Per-User Calibration | Personalized weights | Adapts per user behavior |

### Phase 4: User Feedback → Pivot
User rejected the "choose one" framing and proposed combining A + B:

**Final Architecture — Hybrid A+B with Life Event Override:**
1. **Layer 1:** Life Event Override (birthdays, new members, milestones, re-engagement) — runs first, if triggered serves immediately
2. **Layer 2:** Dual-Track A/B — users randomly assigned to EOSRS or Thompson Sampling; answer rates compared weekly
3. **Layer 3:** MVP fallback (category balance) — safety net

## Key Decisions

| Decision | Rationale |
|---|---|
| Zero ongoing LLM cost | All layers use SQL queries + in-memory scoring |
| Life events as override layer | Prevents algorithm from ignoring real-world signals |
| A/B both tracks | Different generations may prefer different approaches — let data decide |
| Sources cited in BRD | Every BRD includes academic/industry references |

## Deliverable

An interactive HTML presentation showing the full algorithm architecture, research findings, competitor analysis, and risk table. Used as a stakeholder communication tool during review cycles.

## Skills Demonstrated
- Product strategy & roadmap iteration
- User research & feedback incorporation
- Technical algorithm design
- Competitive analysis
- Stakeholder communication (HTML presentations)
- Data-driven decision making (A/B testing approach)
