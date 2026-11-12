from playwright.sync_api import sync_playwright, TimeoutError
from scraper.product import get_product_title, get_product_price


def open_browser(url: str):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            executable_path="/usr/bin/google-chrome",
        )

        page = browser.new_page()

        print("Opening:", url)

        try:
            page.goto(
                url,
                wait_until="commit",
                timeout=15000
            )

            print("Commit received")

        except TimeoutError:
            print("Navigation timeout")

        page.wait_for_timeout(5000)

        title = get_product_title(page)

        if title:
            print("\nProduct title:", title)
        else:
            print("\nProduct title not found")

        price = get_product_price(page)

        if price:
            print("\nProduct price:", price)
        else:
            print("\nProduct price not found")

        input("Press Enter...")



        browser.close()

        return title