from playwright.sync_api import sync_playwright, TimeoutError


def get_product_title(page):
    h1_elements = page.locator("h1")
    count = h1_elements.count()

    print(f"H1 count: {count}")

    for i in range(count):
        text = h1_elements.nth(i).inner_text().strip()

        print(f"H1 {i}: {text}")

        if len(text) > 20:
            return text

    return None


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

        input("Press Enter...")

        browser.close()

        return title