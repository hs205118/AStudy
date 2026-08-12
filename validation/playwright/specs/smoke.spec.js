const {test,expect}=require('@playwright/test');
test('UI-001 Chromium launches',async({page})=>{await page.goto('about:blank');expect(await page.title()).toBe('')});
test('UI-002 Health opens',async({page})=>{const r=await page.goto('/health');expect(r.status()).toBe(200)});
test('UI-003 Swagger opens',async({page})=>{await page.goto('/docs');await expect(page).toHaveTitle(/Swagger UI/)});
