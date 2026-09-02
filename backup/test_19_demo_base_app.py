# Python port of tests/19demoBaseApp.spec.ts — exercises fixtures/base_app_fixtures.py (the port
# of fixtures/baseAppTest.ts): the grouped App/AppData SimpleNamespace fixtures.


def test_demo_using_app_fixtures(App, AppData):
    App.base_page.navigate_to("https://vibetestq-osondemand.orangehrm.com/")
    App.login_page.enter_username(AppData.user_credentials["username"])
    App.login_page.enter_password(AppData.user_credentials["password"])
    App.login_page.click_login()

    App.dashboard_page.verify_dashboard_header()
