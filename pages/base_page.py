class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to(self, url: str) -> None:
        self.page.goto(url)
        print(f"Navigated to URL: {url}")
