import { Page } from '@playwright/test';

export class EmployeesPage {
  constructor(private readonly page: Page) {}

  async openStaffList(): Promise<void> {
    await this.page.goto('/pracownicy/sklad-osobowy');
  }
}
