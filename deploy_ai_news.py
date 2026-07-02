#!/usr/bin/env python3
"""
Deploy a daily AI news briefing to the portfolio site at dustinfelderhoff.github.io/portfolio.

Usage: python deploy_ai_news.py [--weekly]
  Reads briefing content from stdin (markdown), generates:
    - ai-news/YYYY-MM-DD.html  (individual day page)
    - ai-news/index.html       (main page with latest + archive links)
  On Sunday with --weekly, also generates ai-news/weekly/YYYY-MM-DD.html

Requires: git origin at https://github.com/DustinFelderhoff/portfolio.git
"""

import sys, os, re, json, shutil, subprocess, datetime
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────
REPO = Path("/c/Users/dusti/portfolio-site")
if not REPO.exists():
    REPO = Path("C:/Users/dusti/portfolio-site")
AI_NEWS_DIR = REPO / "ai-news"
WEEKLY_DIR = AI_NEWS_DIR / "weekly"
TODAY = datetime.date.today()
IS_SUNDAY = TODAY.weekday() == 6  # 6 = Sunday

# ── template snippets (matches portfolio dark theme) ────────────────────────

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Dustin Felderhoff</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #08090a;
  --bg-card: #0f1011;
  --bg-elevated: #191a1b;
  --bg-subtle: rgba(255,255,255,0.03);
  --text-primary: #f7f8f8;
  --text-secondary: #d0d6e0;
  --text-tertiary: #8a8f98;
  --text-quaternary: #62666d;
  --border: rgba(255,255,255,0.08);
  --border-subtle: rgba(255,255,255,0.05);
  --accent: #7170ff;
  --accent-bg: #5e6ad2;
  --accent-hover: #828fff;
  --green: #10b981;
  --green-bg: rgba(16,185,129,0.1);
  --amber: #f59e0b;
  --amber-bg: rgba(245,158,11,0.1);
  --rose: #fb7185;
  --rose-bg: rgba(251,113,133,0.1);
  --cyan: #22d3ee;
  --cyan-bg: rgba(34,211,238,0.1);
  --font: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, monospace;
  --radius-sm: 4px;
  --radius: 8px;
  --radius-lg: 12px;
  --max-w: 960px;
  --nav-w: 200px;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: var(--font);
  background: var(--bg);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  font-feature-settings: 'cv01', 'ss03';
}}
.layout-wrap {{ display: flex; min-height: 100vh; }}
.sidebar {{
  position: fixed; top: 0; left: 0; width: var(--nav-w); height: 100vh;
  z-index: 100; background: var(--bg-card);
  border-right: 1px solid var(--border-subtle);
  display: flex; flex-direction: column; padding: 32px 20px;
}}
.sidebar .logo {{
  font-size: 15px; font-weight: 510; color: var(--text-primary);
  text-decoration: none; letter-spacing: -0.01em;
  margin-bottom: 40px; display: block;
}}
.sidebar .nav-links {{ list-style: none; display: flex; flex-direction: column; gap: 6px; flex: 1; }}
.sidebar .nav-links a {{
  display: block; padding: 8px 12px; font-size: 14px; font-weight: 510;
  color: var(--text-tertiary); text-decoration: none; border-radius: 6px;
  transition: background 0.12s, color 0.12s;
}}
.sidebar .nav-links a:hover {{ background: var(--bg-subtle); color: var(--text-primary); }}
.sidebar .nav-links a.active {{ color: var(--accent); background: rgba(113,112,255,0.06); }}
.sidebar .nav-cta {{
  background: var(--accent-bg); color: #fff; text-align: center;
  padding: 10px 14px; border-radius: 6px; font-size: 14px;
  font-weight: 500; text-decoration: none; display: block; transition: background 0.15s;
}}
.sidebar .nav-cta:hover {{ background: var(--accent-hover); }}
.main-content {{ margin-left: var(--nav-w); flex: 1; min-width: 0; }}
.container {{ max-width: var(--max-w); margin: 0 auto; padding: 0 24px; }}

@media (max-width: 768px) {{
  .sidebar {{ display: none; }}
  .main-content {{ margin-left: 0; padding-bottom: 72px; }}
  .bottom-nav {{
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 100;
    background: var(--bg-card); border-top: 1px solid var(--border);
    display: flex; justify-content: space-around; align-items: center;
    height: 64px; padding: 0 8px 8px; backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }}
  .bottom-nav a {{
    display: flex; flex-direction: column; align-items: center; gap: 2px;
    text-decoration: none; color: var(--text-quaternary); font-size: 10px;
    font-weight: 510; padding: 6px 4px; border-radius: 6px; min-width: 48px;
    transition: color 0.12s;
  }}
  .bottom-nav a .nav-icon {{ font-size: 20px; line-height: 1; }}
  .bottom-nav a:hover {{ color: var(--text-primary); }}
  .bottom-nav a.active {{ color: var(--accent); }}
}}
@media (min-width: 769px) {{ .bottom-nav {{ display: none; }} }}

.hero {{
  padding: 80px 0 48px; text-align: center; position: relative;
}}
.hero::before {{
  content: ''; position: absolute; top: -200px; left: 50%;
  transform: translateX(-50%); width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(113,112,255,0.06) 0%, transparent 70%);
  pointer-events: none;
}}
.hero h1 {{
  font-size: 38px; font-weight: 510; line-height: 1.08;
  letter-spacing: -0.836px; color: var(--text-primary);
  margin-bottom: 12px; position: relative;
}}
.hero .subtitle {{
  font-size: 15px; font-weight: 400; line-height: 1.6;
  color: var(--text-tertiary); max-width: 640px;
  margin: 0 auto; position: relative;
}}

section {{ padding: 40px 0; }}
section + section {{ border-top: 1px solid var(--border-subtle); }}

.news-section {{
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 28px; margin-bottom: 20px;
}}
.news-section:last-child {{ margin-bottom: 0; }}
.news-section h3 {{
  font-size: 18px; font-weight: 590; letter-spacing: -0.2px;
  color: var(--text-primary); margin-bottom: 6px;
}}
.news-section .meta {{
  font-size: 12px; color: var(--text-quaternary); margin-bottom: 12px;
  display: flex; gap: 12px; flex-wrap: wrap;
}}
.news-section .meta .bias {{
  display: inline-block; padding: 1px 8px; border-radius: 3px;
  font-size: 11px; font-weight: 500;
}}
.news-section .meta .bias-left {{ background: rgba(59,130,246,0.15); color: #93bbfc; }}
.news-section .meta .bias-center {{ background: rgba(107,114,128,0.15); color: #9ca3af; }}
.news-section .meta .bias-right {{ background: rgba(239,68,68,0.15); color: #fca5a5; }}
.news-section .meta .badge {{
  background: rgba(16,185,129,0.1); color: #34d399; padding: 1px 6px;
  border-radius: 3px; font-size: 11px;
}}
.news-section .meta .blindspot {{
  background: rgba(245,158,11,0.12); color: #fbbf24; padding: 1px 6px;
  border-radius: 3px; font-size: 11px;
}}
.news-section .summary {{
  font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 8px;
}}
.news-section .why-it-matters {{
  font-size: 13px; color: var(--text-tertiary); line-height: 1.6;
  border-left: 2px solid var(--accent); padding-left: 14px; margin-top: 8px;
}}
.news-section .why-label {{
  font-size: 11px; font-weight: 600; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px;
}}

.section-title {{
  font-size: 24px; font-weight: 590; letter-spacing: -0.36px;
  color: var(--text-primary); margin-bottom: 20px;
}}

.archive-list {{
  display: flex; flex-direction: column; gap: 8px;
}}
.archive-item {{
  display: flex; align-items: center; gap: 12px;
  padding: 10px 16px; background: var(--bg-card);
  border: 1px solid var(--border); border-radius: var(--radius);
  transition: border-color 0.12s;
}}
.archive-item:hover {{ border-color: var(--accent); }}
.archive-item .date {{
  font-size: 13px; font-weight: 500; color: var(--text-quaternary);
  min-width: 90px; font-family: var(--font-mono);
}}
.archive-item .title {{
  font-size: 14px; color: var(--text-secondary); text-decoration: none;
  flex: 1;
}}
.archive-item .title:hover {{ color: var(--accent); }}
.archive-item .label {{
  font-size: 10px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.5px; padding: 2px 8px; border-radius: 3px;
}}
.archive-item .label.weekly {{ background: rgba(16,185,129,0.1); color: #34d399; }}
.archive-item .label.daily {{ background: rgba(113,112,255,0.08); color: #828fff; }}

.closing {{
  text-align: center; max-width: 640px; margin: 0 auto; padding: 48px 0;
}}
.closing p {{ font-size: 14px; color: var(--text-tertiary); line-height: 1.7; }}

footer {{
  text-align: center; padding: 32px 0;
  border-top: 1px solid var(--border-subtle);
  font-size: 13px; color: var(--text-quaternary);
}}
footer a {{ color: var(--text-tertiary); text-decoration: none; }}
footer a:hover {{ color: var(--accent); }}

@media (max-width: 640px) {{
  .hero {{ padding: 48px 0 32px; }}
  .hero h1 {{ font-size: 26px; letter-spacing: -0.572px; }}
  section {{ padding: 28px 0; }}
  .news-section {{ padding: 20px; }}
  .archive-item {{ flex-wrap: wrap; gap: 6px; }}
  .archive-item .date {{ min-width: 0; }}
}}
</style>
</head>
<body>
<div class="layout-wrap">
<aside class="sidebar">
  <a href="index.html" class="logo">Dustin Felderhoff</a>
  <div class="nav-links">
   <a href="../about.html">About</a>
   <a href="../projects.html">Projects</a>
   <a href="../pm_ai_field_notes.html">PM + AI Field Notes</a>
   <a href="../ai-news/" class="active">AI News</a>
   <a href="../lessons.html">Lessons</a>
   <a href="../contact.html">Contact</a>
   <a href="../apply.html">Apply</a>
  </div>
  <a href="../resume.pdf" class="nav-cta" download>Resume</a>
</aside>
<nav class="bottom-nav">
  <a href="../about.html"><span class="nav-icon">&#9883;</span>About</a>
  <a href="../projects.html"><span class="nav-icon">&#9881;</span>Projects</a>
  <a href="../ai-news.html" class="active"><span class="nav-icon">&#128240;</span>AI News</a>
  <a href="../contact.html"><span class="nav-icon">&#9993;</span>Contact</a>
  <a href="../resume.pdf" download><span class="nav-icon">&#128196;</span>Resume</a>
</nav>
<div class="main-content">"""

FOOTER = """
</div> <!-- /main-content -->
</div> <!-- /layout-wrap -->
<footer>
 <div class="container">
  <p>Dustin Felderhoff, built with the same tools I write about.</p>
  <p style="margin-top:4px;"><a href="https://github.com/dustinfelderhoff/portfolio" target="_blank">github.com/dustinfelderhoff/portfolio</a></p>
 </div>
</footer>
</body>
</html>"""

# ── helpers ─────────────────────────────────────────────────────────────────

def fmt_date(d):
    return d.strftime("%B %d, %Y")

def fmt_iso(d):
    return d.strftime("%Y-%m-%d")

def makelink(path):
    """Turn relative path for ai-news/ pages into one for root vs subdir."""
    return path

def strip_markdown(text):
    """Light markdown-to-plaintext for meta descriptions."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    text = text.strip()
    return text[:200]

def parse_briefing(md_text):
    """
    Parse markdown briefing into structured sections.
    
    Expects sections with ## Headers and content like:
    **1. Story Title** (Articles count)
    > What happened: ...
    > Why it matters: ...
    Bias: Left X% Center Y% Right Z%
    """
    sections = []
    current = None
    buffer = ""
    
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detect story headers like "**1. Story Title**" or "### Story Title"
        story_match = re.match(r'\*\*(\d+[\.\)]?\s*.+?)\*\*', line)
        h3_match = re.match(r'^###\s+(.+)', line)
        
        if story_match or h3_match:
            if current:
                current['body'] = buffer.strip()
                sections.append(current)
            
            title = (story_match.group(1) if story_match else h3_match.group(1)).strip()
            current = {'title': title, 'body': '', 'bias': '', 'meta': '', 'source_count': ''}
            buffer = ""
        elif current and line.strip():
            buffer += line + '\n'
        elif not line.strip() and current:
            buffer += '\n'
        
        i += 1
    
    if current:
        current['body'] = buffer.strip()
        sections.append(current)
    
    # Post-process: extract bias and meta from body
    for s in sections:
        body = s['body']
        
        # Extract bias line
        bias_m = re.search(r'(Left|L)\s*(\d+)%\s*(Center|C)\s*(\d+)%\s*(Right|R)\s*(\d+)%', body)
        if bias_m:
            s['bias'] = {'L': bias_m.group(2), 'C': bias_m.group(4), 'R': bias_m.group(6)}
        
        # Extract blindspot
        blind_m = re.search(r'Blindspot:\s*(.*?)(?=\n\n|\Z)', body, re.DOTALL)
        if blind_m:
            s['blindspot'] = blind_m.group(1).strip()
        
        # Extract article count
        count_m = re.search(r'(\d+)\s*Articles?\s*•', body)
        if count_m:
            s['source_count'] = count_m.group(1)
        
        # Extract source quality
        qual_m = re.search(r'(\d+)%\s*of\s*sources\s*are\s*(Original\s*Reporting|High\s*Factuality)', body)
        if qual_m:
            s['quality'] = f"{qual_m.group(1)}% {qual_m.group(2)}"
    
    return sections


def render_story(s):
    """Render a news section HTML."""
    html = '<div class="news-section">\n'
    html += f'  <h3>{s["title"]}</h3>\n'
    
    meta_parts = []
    if s.get('source_count'):
        meta_parts.append(f'<span>{s["source_count"]} sources</span>')
    if s.get('bias'):
        b = s['bias']
        meta_parts.append(
            f'<span class="bias bias-left">L {b["L"]}%</span>'
            f'<span class="bias bias-center">C {b["C"]}%</span>'
            f'<span class="bias bias-right">R {b["R"]}%</span>'
        )
    if s.get('quality'):
        meta_parts.append(f'<span class="badge">{s["quality"]}</span>')
    if s.get('blindspot'):
        meta_parts.append(f'<span class="blindspot">Blindspot: {s["blindspot"]}</span>')
    
    if meta_parts:
        html += f'  <div class="meta">{" ".join(meta_parts)}</div>\n'
    
    body = s['body']
    # Strip metadata lines from body rendering
    body = re.sub(r'(Left|L)\s*\d+%\s*(Center|C)\s*\d+%\s*(Right|R)\s*\d+%', '', body)
    body = re.sub(r'Blindspot:.*?(\n\n|\Z)', '', body, flags=re.DOTALL)
    body = re.sub(r'\d+\s*Articles?\s*•.*?\n', '', body)
    body = re.sub(r'\d+%\s*of\s*sources\s*are\s*(Original Reporting|High Factuality)', '', body)
    body = re.sub(r'\*\*(\d+[\.\)]?\s*.+?)\*\*', '', body)
    body = re.sub(r'^###\s+.+$', '', body, flags=re.MULTILINE)
    body = body.strip()
    
    # Split into paragraphs
    paras = [p.strip() for p in body.split('\n\n') if p.strip()]
    for p in paras:
        p_formatted = p.replace('\n', ' ')
        if p_formatted.startswith('What happened:'):
            html += f'  <div class="summary">{p_formatted}</div>\n'
        elif p_formatted.startswith('Why it matters:') or p_formatted.startswith('Why it means:') or p_formatted.startswith('What it means:'):
            html += f'  <div class="why-it-matters"><div class="why-label">Why it matters</div>{p_formatted}</div>\n'
        elif p_formatted.startswith('The details:'):
            html += f'  <div class="summary">{p_formatted}</div>\n'
        elif p_formatted.startswith('The findings:'):
            html += f'  <div class="summary">{p_formatted}</div>\n'
        else:
            html += f'  <div class="summary">{p_formatted}</div>\n'
    
    html += '</div>\n'
    return html


def build_daily_page(date, date_label, briefing_text, is_weekly=False):
    """Generate full HTML for an individual day's briefing."""
    # Parse sections
    sections = parse_briefing(briefing_text)
    
    title = f"AI News - {date_label}"
    if is_weekly:
        title = f"AI News Weekly Recap - {date_label}"
    
    html = HEAD.format(title=title)
    
    # Hero
    html += f'<section class="hero">\n<div class="container">\n'
    if is_weekly:
        html += f'<h1>Weekly AI News Recap</h1>\n'
        html += f'<p class="subtitle">{date_label} — The week\'s top stories in AI, product management, and tech.</p>\n'
    else:
        html += f'<h1>Daily AI News</h1>\n'
        html += f'<p class="subtitle">{date_label}</p>\n'
    html += '</div>\n</section>\n'
    
    # News content
    html += '<section>\n<div class="container">\n'
    
    # Add the briefing intro text (before the sections)
    # Grab the first paragraph that isn't a section header
    lines = briefing_text.strip().split('\n')
    intro_lines = []
    for line in lines:
        if re.match(r'^##\s+PART|^###?\s', line) or re.match(r'^\*\*(\d+[\.\)]?\s*)', line):
            break
        intro_lines.append(line)
    intro = '\n'.join(intro_lines).strip()
    if intro:
        html += f'<p style="font-size: 14px; color: var(--text-tertiary); margin-bottom: 24px; line-height: 1.7;">{intro}</p>\n'
    
    if not sections:
        # No structured sections found, render as raw
        body_text = briefing_text
        # Strip intro
        if intro:
            body_text = briefing_text[len(intro):].strip()
        html += f'<div style="white-space: pre-wrap; font-size: 14px; color: var(--text-secondary); line-height: 1.8;">{body_text}</div>\n'
    else:
        for s in sections:
            html += render_story(s)
    
    html += '</div>\n</section>\n'
    
    # Archive links
    html += '<section>\n<div class="container">\n'
    html += '<h2 class="section-title">Previous Briefings</h2>\n'
    html += '<div class="archive-list">\n'
    
    # List recent days
    for i in range(1, 8):
        d = date - datetime.timedelta(days=i)
        iso = fmt_iso(d)
        fpath = f"{iso}.html"
        html += f'<a href="{fpath}" class="archive-item" style="text-decoration:none;">\n'
        html += f'  <span class="date">{iso}</span>\n'
        html += f'  <span class="title">{fmt_date(d)}</span>\n'
        html += f'  <span class="label daily">Daily</span>\n'
        html += '</a>\n'
    
    html += '</div>\n</div>\n</section>\n'
    
    html += FOOTER
    return html


def build_index_page(date, date_label, briefing_text):
    """Build the main ai-news.html page (latest briefing + archive)."""
    sections = parse_briefing(briefing_text)
    
    html = HEAD.format(title="Daily AI News")
    
    # Hero
    html += '<section class="hero">\n<div class="container">\n'
    html += '<h1>Daily AI News</h1>\n'
    html += f'<p class="subtitle">The latest AI, product management, and tech news — with bias breakdowns. Updated every morning. <a href="{fmt_iso(date)}.html" style="color:var(--accent);">Read today\'s full briefing &rarr;</a></p>\n'
    html += '</div>\n</section>\n'
    
    # Today's briefing summary
    html += '<section>\n<div class="container">\n'
    html += f'<h2 class="section-title">Latest — {date_label}</h2>\n'
    
    if sections:
        for s in sections[:4]:  # Show top 4
            html += render_story(s)
    else:
        body_text = briefing_text
        lines = briefing_text.strip().split('\n')
        intro_lines = []
        for line in lines:
            if re.match(r'^##\s+PART|^###?\s', line) or re.match(r'^\*\*(\d+[\.\)]?\s*)', line):
                break
            intro_lines.append(line)
        intro = '\n'.join(intro_lines).strip()
        if intro:
            body_text = briefing_text[len(intro):].strip()
        html += f'<div style="white-space: pre-wrap; font-size: 14px; color: var(--text-secondary); line-height: 1.8;">{body_text}</div>\n'
    
    html += f'<p style="margin-top: 20px;"><a href="{fmt_iso(date)}.html" style="color: var(--accent); font-size: 14px; font-weight: 500;">Read the full briefing &rarr;</a></p>\n'
    html += '</div>\n</section>\n'
    
    # Archive
    html += '<section>\n<div class="container">\n'
    html += '<h2 class="section-title">Previous Days</h2>\n'
    html += '<div class="archive-list">\n'
    
    for i in range(1, 8):
        d = date - datetime.timedelta(days=i)
        iso = fmt_iso(d)
        fpath = f"ai-news/{iso}.html"
        html += f'<a href="{fpath}" class="archive-item" style="text-decoration:none;">\n'
        html += f'  <span class="date">{iso}</span>\n'
        html += f'  <span class="title">{fmt_date(d)}</span>\n'
        html += f'  <span class="label daily">Daily</span>\n'
        html += '</a>\n'
    html += '</div>\n</div>\n</section>\n'
    
    # About section
    html += '<section class="closing">\n<div class="container">\n'
    html += '<p>This page is updated every morning at 5 AM MT with the latest AI news, product management developments, and tech trends — sourced from Ground News with bias breakdowns and supplemented with curated AI/PM stories.</p>\n'
    html += f'<p style="margin-top: 12px;">Sundays include a Weekly Recap with the most important stories from the past seven days.</p>\n'
    html += '</div>\n</section>\n'
    
    html += FOOTER
    return html


def write_page(path, html):
    """Write an HTML file, creating directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding='utf-8')
    print(f"  ✓ {path.relative_to(REPO)}")


def get_existing_dates():
    """Find existing daily briefing files in ai-news/ directory."""
    if not AI_NEWS_DIR.exists():
        return []
    files = sorted(AI_NEWS_DIR.glob("????-??-??.html"))
    dates = []
    for f in files:
        try:
            d = datetime.datetime.strptime(f.stem, "%Y-%m-%d").date()
            if d <= TODAY:
                dates.append(d)
        except ValueError:
            continue
    return dates


def git_push():
    """Commit and push changes to the portfolio repo."""
    os.chdir(str(REPO))
    
    # Check for changes
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("  No changes to commit.")
        return True
    
    # Stage all ai-news changes, and any nav-update changes
    subprocess.run(["git", "add", "-A"], check=False)
    
    # Commit
    msg = f"AI News: daily briefing for {fmt_iso(TODAY)}"
    result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Commit failed: {result.stderr.strip()}")
        return False
    print(f"  Committed: {msg}")
    
    # Push to main (remote's deployment branch)
    result = subprocess.run(["git", "push", "origin", "master:main"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Push to main failed: {result.stderr.strip()}")
        # Fallback: just push current branch
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Push failed: {result.stderr.strip()}")
            return False
    print(f"  Pushed to origin/main")
    return True


# ── main ────────────────────────────────────────────────────────────────────

def main():
    is_weekly = "--weekly" in sys.argv or IS_SUNDAY
    
    # Read briefing content from stdin
    briefing = sys.stdin.read().strip()
    if not briefing:
        print("ERROR: No briefing content on stdin")
        sys.exit(1)
    
    date_label = fmt_date(TODAY)
    iso = fmt_iso(TODAY)
    
    print(f"Deploying AI News for {date_label}...")
    
    # Ensure directories exist
    AI_NEWS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Write individual day page (ai-news/YYYY-MM-DD.html)
    day_html = build_daily_page(TODAY, date_label, briefing, is_weekly)
    day_path = AI_NEWS_DIR / f"{iso}.html"
    write_page(day_path, day_html)
    
    # 2. If Sunday, write weekly recap
    if is_weekly:
        WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
        weekly_html = build_daily_page(TODAY, date_label, briefing, is_weekly=True)
        weekly_path = WEEKLY_DIR / f"{iso}.html"
        write_page(weekly_path, weekly_html)
    
    # 3. Write/update main index page (ai-news/index.html)
    index_html = build_index_page(TODAY, date_label, briefing)
    index_path = AI_NEWS_DIR / "index.html"
    write_page(index_path, index_html)
    
    # 4. Git commit and push
    print("Pushing to GitHub Pages...")
    git_push()
    
    print(f"\nDone. Live at: https://dustinfelderhoff.github.io/portfolio/ai-news/")


if __name__ == "__main__":
    main()
