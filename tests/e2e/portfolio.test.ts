import { test, expect } from '@playwright/test';

test.describe('Portfolio — Navigation', () => {
  
  test('all sidebar nav links resolve without 404', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.waitForLoadState('networkidle');
    
    // Just verify the links exist with correct hrefs
    const links = page.locator('.nav-links a');
    await expect(links).toHaveCount(7);
    
    // Check each link's href attribute
    await expect(links.nth(0)).toHaveAttribute('href', '#about');
    await expect(links.nth(0)).toContainText('About');
    
    await expect(links.nth(1)).toHaveAttribute('href', '#projects');
    await expect(links.nth(1)).toContainText('Projects');
    
    await expect(links.nth(3)).toHaveAttribute('href', 'ai-news/');
    
    await expect(links.nth(4)).toHaveAttribute('href', '#lessons');
    await expect(links.nth(5)).toHaveAttribute('href', '#contact');
    await expect(links.nth(6)).toHaveAttribute('href', 'apply/');
  });

  test('hash nav scrolls to correct sections', async ({ page }) => {
    test.setTimeout(60000);
    // Use desktop viewport — sidebar is hidden on mobile (bottom-nav tested separately)
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.waitForLoadState('networkidle');

    // Click Projects nav link
    await page.locator('.nav-links a').filter({ hasText: 'Projects' }).click();
    await page.waitForTimeout(500);
    await expect(page.locator('#projects')).toBeInViewport();

    // Click Principles
    await page.locator('.nav-links a').filter({ hasText: 'Principles' }).click();
    await page.waitForTimeout(500);
    await expect(page.locator('#lessons')).toBeInViewport();

    // Click Contact
    await page.locator('.nav-links a').filter({ hasText: 'Contact' }).click();
    await page.waitForTimeout(500);
    await expect(page.locator('#contact')).toBeInViewport();
  });

  test('sidebar active link highlights on Projects scroll', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.waitForLoadState('networkidle');
    
    await page.locator('#projects').scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);
    
    const projectsLink = page.locator('.nav-links a').filter({ hasText: 'Projects' });
    await expect(projectsLink).toHaveClass(/active/);
  });
});

test.describe('Portfolio — Content', () => {

  test('all 5 Decision/The Call lines present', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.waitForLoadState('networkidle');
    await page.locator('#projects').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    
    await expect(page.locator('text=The Call')).toHaveCount(5);
  });

  test('no Here\'s Here\'s typo', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await expect(page.locator('body')).not.toContainText("Here's Here's");
  });

  test('no banned AI words', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await expect(page.locator('body')).not.toContainText('comprehensive');
    await expect(page.locator('body')).not.toContainText('leverage');
  });

  test('resume download link works', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await expect(page.locator('.nav-cta')).toHaveAttribute('href', 'resume.pdf');
    await expect(page.locator('.nav-cta')).toHaveAttribute('download', '');
  });

  test('hero contains name and tagline', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await expect(page.locator('.hero h1')).toContainText('I build tools');
    await expect(page.locator('.hero')).toContainText('Denver');
  });

  test('all 5 projects have metric cards', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.locator('#projects').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await expect(page.locator('.metrics-grid')).toHaveCount(5);
  });

  test('principles section has 4+ items', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.locator('#lessons').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    expect(await page.locator('.lesson-cross').count()).toBeGreaterThanOrEqual(4);
  });

  test('contact has email and LinkedIn', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await page.locator('#contact').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await expect(page.locator('#contact')).toContainText('dustin.felderhoff');
    await expect(page.locator('#contact a[href*="linkedin"]')).toBeVisible();
  });
});

test.describe('Portfolio — Mobile', () => {

  test.use({ viewport: { width: 375, height: 812 } });

  test('bottom nav visible on mobile', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await expect(page.locator('.bottom-nav')).toBeVisible();
  });

  test('bottom nav links navigate', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    
    await page.locator('.bottom-nav a').filter({ hasText: 'Projects' }).click();
    await page.waitForTimeout(500);
    await expect(page.locator('#projects')).toBeInViewport();
    
    await page.locator('.bottom-nav a').filter({ hasText: 'Principles' }).click();
    await page.waitForTimeout(500);
    await expect(page.locator('#lessons')).toBeInViewport();
  });

  test('bottom nav Apply link uses apply/', async ({ page }) => {
    await page.goto('https://dustinfelderhoff.github.io/portfolio/');
    await expect(page.locator('.bottom-nav a').filter({ hasText: 'Apply' })).toHaveAttribute('href', 'apply/');
  });
});

test.describe('Portfolio — External Pages', () => {

  test('PM+AI Field Notes loads without 404', async ({ page }) => {
    await page.goto('pm_ai_field_notes.html');
    await expect(page.locator('body')).not.toContainText('404');
  });

  test('AI News page loads without 404', async ({ page }) => {
    await page.goto('ai-news/');
    await expect(page.locator('body')).not.toContainText('404');
  });

  test('Apply page loads without 404', async ({ page }) => {
    await page.goto('apply/');
    await expect(page.locator('body')).not.toContainText('404');
  });
});
