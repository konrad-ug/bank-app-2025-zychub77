import { Page } from '@playwright/test';

export class HomePage {
  constructor(private readonly page: Page) {}

  async goto(): Promise<void> {
    await this.page.goto('/');
  }

  async openEmployees(): Promise<void> {
    const employeesLink = this.page.getByRole('link', { name: /Pracownicy/i });
    if (await employeesLink.count()) {
      await employeesLink.first().click();
      return;
    }
    await this.page.getByRole('button', { name: /Pracownicy/i }).click();
  }
}
