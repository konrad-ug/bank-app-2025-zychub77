import { expect, Page } from '@playwright/test';

export class EmployeeProfilePage {
  constructor(private readonly page: Page) {}

  async expectRoomNumber(roomText: string): Promise<void> {
    await expect(this.page.getByText(roomText, { exact: false })).toBeVisible();
  }
}
