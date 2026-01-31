import { test } from '@playwright/test';
import { HomePage } from '../pages/HomePage';
import { EmployeesPage } from '../pages/EmployeesPage';
import { StaffPage } from '../pages/StaffPage';

test('Instytut Fizyki Doświadczalnej employs mgr Anna Baran', async ({ page }) => {
  const home = new HomePage(page);
  const employees = new EmployeesPage(page);
  const staff = new StaffPage(page);

  await home.goto();
  await home.openEmployees();
  await employees.openStaffList();
  await staff.expectEmployeeInInstitute('Instytut Fizyki Doświadczalnej', 'mgr Anna Baran');
});
