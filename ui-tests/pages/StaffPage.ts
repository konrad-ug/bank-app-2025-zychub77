import { expect, Page } from '@playwright/test';

export class StaffPage {
  constructor(private readonly page: Page) {}

  async searchByLastName(lastName: string): Promise<void> {
    const inputs = await this.page.$$(
      'input[type="search"], input[type="text"]'
    );
    for (const input of inputs) {
      if (await input.isVisible()) {
        await input.fill(lastName);
        return;
      }
    }
    throw new Error('Visible search input not found on staff page.');
  }

  async expectEmployeeLinkVisible(name: string): Promise<void> {
    await expect(this.page.getByRole('link', { name: new RegExp(name, 'i') })).toBeVisible();
  }

  async openEmployee(name: string): Promise<void> {
    await this.page.getByRole('link', { name: new RegExp(name, 'i') }).click();
  }

  async expectEmployeeInInstitute(instituteName: string, employeeName: string): Promise<void> {
    const institute = this.page.getByRole('link', { name: new RegExp(instituteName, 'i') }).first();
    await expect(institute).toBeVisible();
    await expect(this.page.getByText(new RegExp(employeeName, 'i'))).toBeVisible();
  }
}
