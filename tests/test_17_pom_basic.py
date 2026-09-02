import random

from pages.add_employee_page import AddEmployeePage
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.personal_details_page import PersonalDetailsPage
from pages.pim_page import PIMPage

# exercising the LoginPagetxt_password and AddEmployeePage.txt_last_name intentionally-broken placeholder as a real
# self-healing recovery.

def test_orange_hrm_add_employee(page):
    base_page = BasePage(page)
    base_page.navigate_to("https://vibetestq-osondemand.orangehrm.com/")

    login_page = LoginPage(page)
    login_page.enter_username("testadmin")
    login_page.enter_password("Vibetestq@123#")
    login_page.click_login()

    dashboard_page = DashboardPage(page)
    dashboard_page.verify_dashboard_header()
    dashboard_page.click_pim_link()

    pim_page = PIMPage(page)
    pim_page.verify_pim_header()
    pim_page.click_add_employee_link()

    add_employee_page = AddEmployeePage(page)
    add_employee_page.verify_add_employee_header()
    add_employee_page.enter_first_name("John")
    add_employee_page.enter_last_name("Doe")

    random_number = random.randint(2000, 5000)
    add_employee_page.set_employee_id(str(random_number))
    add_employee_page.click_save()

    personal_details_page = PersonalDetailsPage(page)
    personal_details_page.verify_personal_details_header()
