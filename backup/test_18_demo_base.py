# Python port of tests/18demoBase.spec.ts — exercises fixtures/base_fixtures.py (the port of
# fixtures/basetest.ts): independently-injected base_page/login_page/dashboard_page/
# user_credentials fixtures rather than TS's single test.extend() object.


def test_demo_using_base_fixtures(base_page, login_page, dashboard_page, user_credentials):
    base_page.navigate_to("https://vibetestq-osondemand.orangehrm.com/")
    login_page.enter_username(user_credentials["username"])
    login_page.enter_password(user_credentials["password"])
    login_page.click_login()

    dashboard_page.verify_dashboard_header()
