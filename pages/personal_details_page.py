from tamash_playwright import expect

from .base_page import BasePage


class PersonalDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header_personal_details = page.get_by_role("heading", name="Personal Details").describe(
            "Personal Details Header in Personal Details Page"
        )

    def verify_personal_details_header(self) -> None:
        expect(self.header_personal_details).to_be_visible(timeout=10000)
        print("Personal Details Header is visible in Personal Details Page")
