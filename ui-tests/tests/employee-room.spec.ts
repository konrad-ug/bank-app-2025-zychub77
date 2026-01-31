import { test } from '@playwright/test';
import { HomePage } from '../pages/HomePage';
import { EmployeesPage } from '../pages/EmployeesPage';
import { StaffPage } from '../pages/StaffPage';
import { EmployeeProfilePage } from '../pages/EmployeeProfilePage';

test('UG employee room is displayed for mgr Konrad Sołtys', async ({ page }) => {
  const home = new HomePage(page);
  const employees = new EmployeesPage(page);
  const staff = new StaffPage(page);
  const profile = new EmployeeProfilePage(page);

  await home.goto();
  await home.openEmployees();
  await employees.openStaffList();
  await staff.searchByLastName('sołtys');
  await staff.expectEmployeeLinkVisible('mgr Konrad Sołtys');
  await staff.openEmployee('mgr Konrad Sołtys');
  await profile.expectRoomNumber('Nr pokoju: 4.19');
});
