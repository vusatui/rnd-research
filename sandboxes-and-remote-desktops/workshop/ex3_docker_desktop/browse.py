"""Headful Playwright внутри desktop-контейнера: видно в noVNC."""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=False)
    page = b.new_page()
    page.goto("https://news.ycombinator.com")
    titles = page.locator(".titleline > a").all_inner_texts()[:5]
    print("\n".join(titles))
    page.screenshot(path="/tmp/hn.png")
    page.wait_for_timeout(5000)
    b.close()
