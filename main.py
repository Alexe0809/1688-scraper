from excel.reader import read_urls
from scraper.browser import open_browser

urls = read_urls('excel/import/input.xlsx')

print(urls)

open_browser(urls[0])