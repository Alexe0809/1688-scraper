from playwright.sync_api import sync_playwright, TimeoutError
from scraper.product import (
    get_product_title,
    get_product_price,
    get_product_weight,
    colors_variants,
    get_product_images
)
from pathlib import Path

USER_DATA_DIR = Path('userDataDir')

def is_verification_page(page):
    text = page.locator("body").inner_text().lower()

    return (
        "please drag the slider to verify" in text
        or "verify to ensure normal access" in text
    )

def open_browser(url: str):

    for attempt in range(1, 3):

        full_data = {}

        with sync_playwright() as p:

            context = p.chromium.launch_persistent_context(USER_DATA_DIR,
                headless=False,
                executable_path="/usr/bin/google-chrome",
            )

            page = context.new_page()

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

            if is_verification_page(page):
                print("Verification page detected")
            else:
                print("Normal product page")

            title = get_product_title(page)

            if title:
                print("\nProduct title:", title)
            else:
                print("\nProduct title not found")

            price = get_product_price(page)

            images = get_product_images(page)

            print(images)

            if price:
                print("\nProduct price:", price)
            else:
                print("\nProduct price not found")

            weight = get_product_weight(page)

            if weight:
                print("\nProduct weight:", weight)
            else:
                print("\nProduct weight not found")

            print("\nColors variants:")

            variants = colors_variants(page)
            print(variants)

            input("Press Enter...")

            full_data['title'] = title
            full_data['price'] = price
            full_data['weight'] = weight
            full_data['images'] = images
            full_data['variants'] = variants

            context.close()

        is_valid, error = check_full_data(full_data)

        if is_valid:

            return full_data

        print(f"Attempt {attempt} failed: {error}")

        return {
            "data": full_data,
            "error": error,
        }



def check_full_data(data):
    for key, value in data.items():
        if value is None:
            return False, key
    return True, None
    
    