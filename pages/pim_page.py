from tamash_playwright import expect

from .base_page import BasePage


class PIMPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header_pim = page.get_by_role("heading", name="PIM").describe("PIM Header in PIM Page")
        self.lnk_add_employee = page.get_by_role("link", name="Add Employee").describe("Add Employee Link in PIM Page")

    def verify_pim_header(self) -> None:
        expect(self.header_pim).to_be_visible()
        print("PIM Header is visible in PIM Page")

    def click_add_employee_link(self) -> None:
        self.lnk_add_employee.click()
        print("Add Employee Link clicked in PIM Page")
