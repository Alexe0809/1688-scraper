import json
from playwright.sync_api import TimeoutError

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

def get_product_price(page):
    price_elements = page.locator(".price-info")
    count = price_elements.count()

    print(f"Price elements count: {count}")

    if count == 0:
        return None

    price = price_elements.first.inner_text()
    price = price.replace("\n", "").strip()

    return price


def colors_variants(page):
    colors = page.locator("button.sku-filter-button")

    colors_variants = {}

    for i in range(colors.count()):

        captcha = page.locator("iframe[src*='action=captcha']")

        if captcha.count() > 0:
            print("Verification appeared")
            break

        color_button = colors.nth(i)

        color_name = color_button.locator(".label-name").inner_text().strip()

        print(f"\nSelecting color: {color_name}")

        is_active = "active" in (color_button.get_attribute("class") or "")

        if not is_active:
            try:
                color_button.click(timeout=3000)
            except TimeoutError:
                print("Click blocked, verification likely appeared")
                break

            page.wait_for_timeout(1000)

        captcha = page.locator("iframe[src*='action=captcha']")

        if captcha.count() > 0:
            print("Verification appeared after color selection")
            break

        sizes = get_sizes(page)

        colors_variants[color_name] = sizes

    return colors_variants
        

# def get_product_variants(page):
#         ...

def get_product_weight(page):
    weight_elements = page.locator("td.field-value")

    for i in range(weight_elements.count()):
        value = weight_elements.nth(i).inner_text().strip()

        if value.isdigit():
            return value

    return None

def get_product_colors(page):
    colors = page.locator("button.sku-filter-button .label-name")

    result = []

    for i in range(colors.count()):
        color = colors.nth(i).inner_text().strip()
        result.append(color)

    return result

def get_sizes(page):
    size_items = page.locator(".expand-view-item")

    result = []

    for i in range(size_items.count()):
        item = size_items.nth(i)

        size = item.locator(".item-label").inner_text().strip()

        stock_element = item.locator("od-text[i18n='sku-stock']")
        stock_data = stock_element.get_attribute("data")

        stock = None

        if stock_data:
            stock = int(json.loads(stock_data)[0])

        result.append({
            "size": size,
            "stock": stock
        })

    return result