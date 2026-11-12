

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
    price = page.locator(".price-info").inner_text()
    price = price.replace("\n", "").strip()

    return price