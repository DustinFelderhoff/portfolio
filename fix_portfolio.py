"""Final humanizer cleanup + narrative rewrite + visual evidence."""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ===== STEP 1: Fix grammatical artifacts from em dash replacement =====
fixes = [
    # About section artifacts
    ('Not a bullet-point bio. the short version of what drives me.',
     "Not a bullet-point bio. Here's the short version."),
    ("I've been a product manager for 13 years. SaaS, AI, enterprise.",
     "I've been a product manager for 13 years across SaaS, AI, and enterprise."),
    ("his grandmother's voice when he's older. the way she told a story",
     "his grandmother's voice when he's older. Not just the words on a screen, but how she told a story."),
    
    # Lesson box artifacts - lowercase after period
    ('transparency. never just better code',
     'transparency, never just better code'),
    ('Verification is not optional. it\'s the architecture.',
     "Verification is not optional. It's the architecture."),
    ('do. it was what each agent', 'do. It was what each agent'),
    ("couldn't do. it was what each agent",
     "couldn't do. It was what each agent"),
    ("couldn't do. Blocking the wrong tools", "couldn't do. Blocking the wrong tools"),  # already correct
    
    # Process section artifacts
    ('sub-agent personas. researcher, implementer, architect, operator. each with its own',
     'sub-agent personas: researcher, implementer, architect, operator, each with its own'),
    ('started fresh. repeating the same mistakes',
     'started fresh, repeating the same mistakes'),
    ('refactoring. trimmed verbose descriptions',
     'refactoring that trimmed verbose descriptions'),
    ('memory decay. built a retention-class',
     'memory decay, building a retention-class'),
    ('guardrails. 4 silent checks run before',
     'guardrails: 4 silent checks run before every tool call'),
    ('orchestration. the routing system described above',
     'orchestration, which is the routing system described above'),
    ('classification problems. if you know what to keep',
     'classification problems. If you know what to keep'),
    
    # Challenge section artifacts
    ('ChatGPT had just launched. unproven in enterprise',
     'ChatGPT had just launched, unproven in enterprise'),
    ('LLM deployments. no playbook existed',
     'LLM deployments, and no playbook existed'),
    ('wasn\'t the technology. it was iterating on the human workflow',
     "wasn't the technology. It was iterating on the human workflow"),
    
    # Outcome artifacts
    ('Data leakage. fully private',
     'Data leakage, fully private'),
    ('problem. the wasted',
     'problem: the wasted'),
    ('the most valuable components. not the scoring engine',
     'the most valuable components, not the scoring engine'),
    ('behind on. not just JD keywords',
     'behind on, not just JD keywords'),
    
    # Lessons section artifacts
    ('thrash loop. try X, fail, try Y, fail, try Z.',
     'thrash loop: try X, fail, try Y, fail, try Z.'),
    ('most commonly skipped step. because',
     'most commonly skipped step, because'),
    ('most commonly skipped step. because it\'s overhead, because trust is faster, because the child usually works. Until it doesn\'t.',
     "most commonly skipped step, because it's overhead and trust is faster and usually the child works fine. Until it doesn't."),
    
    # Closing section
    ('healthcare and agentic AI. helping people',
     'healthcare and agentic AI, helping people'),
    
    # Lesson 6 title fix
    ('6. Verify everything, including your own sub-agents : not even for sub-agents',
     '6. Verify everything, including your own sub-agents'),
    
    # Section desc
    ('Not a bullet-point bio.', "Not a bullet-point bio. Here's"),
    
    # Bad artifact in about
    ("13 years. SaaS, AI,", "13 years across SaaS, AI,"),
]

for old, new in fixes:
    if old in html:
        html = html.replace(old, new)
        print(f'  FIXED: {old[:50]}...')
    else:
        # Try case-insensitive
        lower_idx = html.lower().find(old.lower()[:30])
        if lower_idx >= 0:
            print(f'  PARTIAL near {lower_idx}: ...{html[lower_idx:lower_idx+60]}...')
        else:
            print(f'  NOT FOUND: {old[:40]}...')

# ===== STEP 2: Fix the "Data leakage. fully private" that appears elsewhere
# Make sure we got all the lowecase-starting sentences
html = re.sub(r'\. ([a-z])', lambda m: '. ' + m.group(1).upper(), html)

# Fix ". the" -> ". The" but NOT inside HTML tags
# Do this carefully
html = re.sub(r'>\. the ', '>. The ', html)
html = re.sub(r'>\. it ', '>. It ', html)
html = re.sub(r'>\. was', '>. Was', html)
# Fix remaining lowercase starts after periods in visible text
html = html.replace('. the ', '. The ')
html = html.replace('. it was ', '. It was ')
html = html.replace('. not just ', '. Not just ')
html = html.replace('. no playbook', '. No playbook')

# Fix double spaces
html = html.replace('  ', ' ')

# ===== STEP 3: Add project repo links =====
# Story Sundays section - add link
story_link = '<div class="project-subtitle"><a href="https://github.com/DustinFelderhoff" target="_blank" style="color:var(--accent);">Source on GitHub →</a></div>'
# Actually, let me add links to the tech list areas instead
html = html.replace(
    '<li>TDD Pipeline</li>\n        </ul>',
    '<li>TDD Pipeline</li>\n        </ul>\n        <p style="margin-top:12px;font-size:13px;color:var(--text-tertiary);">Private repo. Architecture documented in TTD pipeline.</p>'
)

# Sub-agent - link to Hermes docs
html = html.replace(
    '<li>Handoff Contracts</li>\n        </ul>',
    '<li>Handoff Contracts</li>\n        </ul>\n        <p style="margin-top:12px;font-size:13px;color:var(--text-tertiary);"><a href="https://hermes-agent.nousresearch.com/docs" target="_blank" style="color:var(--accent);">Hermes Agent documentation →</a></p>'
)

# Job pipeline - live link
html = html.replace(
    '<li>Gmail API</li>\n        </ul>',
    '<li>Gmail API</li>\n        </ul>\n        <p style="margin-top:12px;font-size:13px;color:var(--text-tertiary);"><a href="https://career-ops.org" target="_blank" style="color:var(--accent);">Live: career-ops.org →</a> · <a href="https://github.com/DustinFelderhoff/career-ops" target="_blank" style="color:var(--accent);">GitHub →</a></p>'
)

# System architecture - hermes repo link
html = html.replace(
    '<li>Retention Classification</li>\n        </ul>',
    '<li>Retention Classification</li>\n        </ul>\n        <p style="margin-top:12px;font-size:13px;color:var(--text-tertiary);"><a href="https://github.com/DustinFelderhoff/hermes-agent-self-evolution" target="_blank" style="color:var(--accent);">GitHub →</a></p>'
)

# ===== STEP 4: Rewrite project subtitles for varied structure =====
# Story Sundays - keep the personal-led structure. The lessons already work.
# Just change the subtitle to be less formal
html = html.replace(
    'Local-first AI family storytelling platform · React 19 + Vite 8 + Cloudflare Workers + Supabase',
    'A full-stack storytelling platform for my son and his grandparents. React 19, Cloudflare Workers, Supabase.'
)

# Sub-agent - technical focus
html = html.replace(
    'Production-grade multi-agent orchestration with 4 specialized personas, routing logic, and fail-fast boundaries',
    'Four agent personas, strict handoff contracts, and a routing system that enforces boundaries.'
)

# Invoice parser - failure story focus
html = html.replace(
    'First ChatGPT enterprise workflow in 2022 · Python + Prompt Engineering',
    'The one that taught me trust matters more than technology. ChatGPT + Python in an enterprise audit in 2022.'
)

# System architecture - audit focus
html = html.replace(
    'Four-pillar optimization of a production agent runtime · 65 tools, 26 toolsets',
    'Tool schema refactoring, context compression, guardrails, and orchestration. A system-level audit.'
)

# Job pipeline - pipeline flow focus
html = html.replace(
    'End-to-end agentic pipeline: discovery → scoring → deep research → voice-captured submission',
    'Discovery through voice-gated generation. 120+ jobs/hour, per-company research, zero AI tells.'
)

# ===== STEP 5: Fix the remaining "production-grade" in subtitles =====
html = html.replace('Production-grade ', '')

# ===== STEP 6: Write =====
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone! Written to index.html')
