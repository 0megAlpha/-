import { test, expect } from '@playwright/test';

const canvasHealth = process.env.OPENHANDS_CANVAS_URL || 'http://172.17.0.1:8000/health';
const openHandsUi = process.env.OPENHANDS_UI_URL || 'http://172.17.0.1:13000/';

test('OpenHands Agent Canvas health endpoint', async ({ page }) => {
  const response = await page.goto(canvasHealth);
  expect(response?.status()).toBe(200);
  await expect(page.locator('body')).toContainText('ok');
});

test('OpenHands main UI responds', async ({ page }) => {
  const response = await page.goto(openHandsUi);
  expect(response?.status()).toBe(200);
  await expect(page).toHaveTitle(/OpenHands/);
});
