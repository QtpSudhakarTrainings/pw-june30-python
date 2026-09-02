from tamash_playwright import expect

from .base_page import BasePage


class AddEmployeePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header_add_employee = page.get_by_role("heading", name="Add Employee").describe(
            "Add Employee Header in Add Employee Page"
        )
        self.txt_first_name = page.get_by_placeholder("First Name").describe("First Name Textbox in Add Employee Page")
        # Intentionally broken placeholder ("Last Name1") to demonstrate self-healing recovery.
        self.txt_last_name = page.get_by_role("textbox", name="Last Name").describe("Last Name Textbox in Add Employee Page")
        self.btn_save = page.get_by_role("button", name="Save").describe("Save Button in Add Employee Page")
        self.txt_employee_id = page.locator('//label[text()="Employee Id"]/../..//input').describe(
            "Employee Id Textbox in Add Employee Page"
        )

    def verify_add_employee_header(self) -> None:
        expect(self.header_add_employee).to_be_visible()
        print("Add Employee Header is visible in Add Employee Page")

    def enter_first_name(self, first_name: str) -> None:
        self.txt_first_name.fill(first_name)
        print(f"First Name Entered: {first_name}")

    def enter_last_name(self, last_name: str) -> None:
        self.txt_last_name.fill(last_name)
        print(f"Last Name Entered: {last_name}")

    def click_save(self) -> None:
        self.btn_save.click()
        print("Save button clicked in Add Employee Page")

    def get_employee_id(self) -> str:
        employee_id = self.txt_employee_id.input_value()
        print(f"Employee Id is: {employee_id}")
        return employee_id

    def set_employee_id(self, employee_id: str) -> None:
        self.txt_employee_id.fill(employee_id)
        print(f"Employee Id set to: {employee_id}")
