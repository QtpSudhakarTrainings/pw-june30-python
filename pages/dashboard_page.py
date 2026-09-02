from tamash_playwright import expect

from .base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header_dashboard = page.get_by_role("heading", name="Dashboard").describe("Dashboard Header in Dashboard Page")
        self.lnk_pim = page.get_by_role("link", name="PIM").describe("PIM Link in Dashboard Page")
        self.lnk_admin = page.get_by_role("link", name="Admin").describe("Admin Link in Dashboard Page")

    def verify_dashboard_header(self) -> None:
        expect(self.header_dashboard).to_be_visible()
        print("Dashboard Header is visible in Dashboard Page")

    def click_pim_link(self) -> None:
        self.lnk_pim.click()
        print("PIM Link clicked in Dashboard Page")

    def click_admin_link(self) -> None:
        self.lnk_admin.click()
        print("Admin Link clicked in Dashboard Page")
