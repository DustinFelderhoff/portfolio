import { test, expect } from '@playwright/test';

const URL = '/';

test.describe('Portfolio — Navigation', () => {
  
  test('all sidebar nav links resolve without 404', async ({ page }) => {
    const links = [
      { href: '#about', label: 'About' },
      { href: '#projects', label: 'Projects' },
      { href: 'pm_ai_field_notes.html', label: 'PM + AI Field Notes' },
      { href: 'ai-news/', label: 'AI News' },
      { href: '#lessons', label: 'Lessons' },
      { href: '#contact', label: 'Contact' },
      { href: 'apply/', label: 'Apply' },
    ];

    await page.goto(URL);
    
    for (const link of links) {
      const nav = page.locator('.sidebar .nav-links a', { hasText: link.label });
      await expect(nav).toBeVisible();
      
      // Click and verify no 404
      const resp = page.waitForResponse(r => 
        r.url().includes(link.href.replace('#', '')) || r.url().includes(link.href), 
        { timeout: 5000 }
      ).catch(() => null); // hash nav doesn't trigger network
      
      await nav.click();
      
      // For page navigations, check for 404
      if (!link.href.startsWith('#')) {
        await page.waitForLoadState('domcontentloaded');
        await expect(page.locator('body')).not.toContainText('404');
        await expect(page.locator('body')).not.toContainText('Page not found');
      }
    }
  });

  test('hash nav scrolls to correct sections', async ({ page }) => {
    await page.goto(URL);
    
    const sections = ['about', 'projects', 'lessons', 'contact'];
    
    for (const section of sections) {
      await page.locator('.sidebar .nav-links a', { hasText: new RegExp(section, 'i') }).click();
      await page.waitForTimeout(300);
      
      // Verify the section is visible
      const el = page.locator(`#${section}`);
      await expect(el).toBeVisible();
      
      // Verify it's approximately at the top
      const box = await el.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.y).toBeLessThan(400); // Should be in upper portion of viewport
    }
  });

  test('sidebar active link highlights on scroll', async ({ page }) => {
    await page.goto(URL);
    
    // Scroll to projects section
    await page.locator('#projects').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    
    const projectsLink = page.locator('.sidebar .nav-links a', { hasText: 'Projects' });
    await expect(projectsLink).toHaveClass(/active/);
  });
});

test.describe('Portfolio — Content', () => {

  test('all 5 Decision/The Call lines present', async ({ page }) => {
    await page.goto(URL);
    await page.locator('#projects').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    
    const decisionLabels = page.locator('.case-label strong', { hasText: 'The Call' });
    await expect(decisionLabels).toHaveCount(5);
  });

  test('no "Here\'s Here\'s" typo', async ({ page }) => {
    await page.goto(URL);
    const body = await page.locator('body').textContent();
    expect(body).not.toContain("Here's Here's");
  });

  test('no banned AI words in body text', async ({ page }) => {
    await page.goto(URL);
    const body = await page.locator('body').textContent();
    const banned = ['comprehensive', 'leverage', 'seamless', 'delve', 'tapestry', 'vibrant'];
    for (const word of banned) {
      expect(body).not.toContain(word);
    }
  });

  test('resume download link works', async ({ page }) => {
    await page.goto(URL);
    
    const resumeLink = page.locator('.sidebar .nav-cta', { hasText: 'Resume' });
    await expect(resumeLink).toBeVisible();
    await expect(resumeLink).toHaveAttribute('href', 'resume.pdf');
    await expect(resumeLink).toHaveAttribute('download', '');
  });

  test('hero contains name and tagline', async ({ page }) => {
    await page.goto(URL);
    await expect(page.locator('.hero h1')).toContainText('I build tools');
    await expect(page.locator('.hero')).toContainText('Dustin');
    await expect(page.locator('.hero')).toContainText('Denver');
  });

  test('all projects have metrics', async ({ page }) => {
    await page.goto(URL);
    await page.locator('#projects').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    
    // Each project should have metric cards
    const metrics = page.locator('.metrics-grid');
    await expect(metrics).toHaveCount(5);
  });

  test('lessons section has content', async ({ page }) => {
    await page.goto(URL);
    await page.locator('#lessons').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    
    const lessons = page.locator('.lesson-cross');
    expect(await lessons.count()).toBeGreaterThanOrEqual(4);
  });

  test('contact section has email and LinkedIn', async ({ page }) => {
    await page.goto(URL);
    await page.locator('#contact').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    
    await expect(page.locator('#contact')).toContainText('dustin.felderhoff');
    await expect(page.locator('#contact a[href*="linkedin"]')).toBeVisible();
  });
});

test.describe('Portfolio — Mobile', () => {

  test('bottom nav visible on mobile viewport', async ({ page }) => {
    await page.goto(URL);
    await expect(page.locator('.bottom-nav')).toBeVisible();
  });

  test('bottom nav links navigate correctly', async ({ page }) => {
    await page.goto(URL);
    
    // Click Projects in bottom nav
    await page.locator('.bottom-nav a', { hasText: 'Projects' }).click();
    await page.waitForTimeout(300);
    await expect(page.locator('#projects')).toBeVisible();
    
    // Click Lessons
    await page.locator('.bottom-nav a', { hasText: 'Lessons' }).click();
    await page.waitForTimeout(300);
    await expect(page.locator('#lessons')).toBeVisible();
  });

  test('bottom nav Apply link works', async ({ page }) => {
    await page.goto(URL);
    
    const applyLink = page.locator('.bottom-nav a', { hasText: 'Apply' });
    await expect(applyLink).toHaveAttribute('href', 'apply/');
  });
});

test.describe('Portfolio — External Pages', () => {

  test('PM+AI Field Notes page loads', async ({ page }) => {
    await page.goto('pm_ai_field_notes.html');
    await expect(page.locator('body')).not.toContainText('404');
  });

  test('AI News page loads', async ({ page }) => {
    await page.goto('ai-news/');
    await expect(page.locator('body')).not.toContainText('404');
  });

  test('Apply page loads', async ({ page }) => {
    await page.goto('apply/');
    await expect(page.locator('body')).not.toContainText('404');
  });
});
