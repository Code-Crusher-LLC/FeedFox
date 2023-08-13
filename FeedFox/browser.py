from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


class AsyncBrowser(object):
    def __init__(self):
        self.playwright = None
        self.browser = None

    async def start(self, slow_mo=300):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(slow_mo=slow_mo)

    async def stop(self):
        await self.browser.close()
        await self.playwright.stop()

    async def fetch(self, url, wait_for_selector=None, pagination=None,
                    n_pages=1):
        if self.browser is None:
            await self.start()
        context = await self.browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        html = []
        for i in range(n_pages):
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector)
            else:
                await page.wait_for_load_state()
            html.append(await page.content())
            if i < n_pages - 1 and pagination:
                await page.locator(pagination).click()
        await context.close()

        if n_pages == 1:
            return html[0]
        else:
            return html


class Browser(object):
    def __init__(self):
        self.playwright = None
        self.browser = None

    def start(self, slow_mo=100):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(slow_mo=slow_mo)

    def stop(self):
        self.browser.close()
        self.playwright.stop()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def fetch(self, url, wait_for_selector=None, pagination=None,
              n_pages=1, timeout=30):
        context = self.browser.new_context()
        page = context.new_page()
        page.set_default_timeout(timeout * 1000)
        page.goto(url)
        html = []
        for i in range(n_pages):
            if wait_for_selector:
                page.wait_for_selector(wait_for_selector)
            else:
                page.wait_for_load_state()
            html.append(page.content())
            if i < n_pages - 1 and pagination:
                page.locator(pagination).click()
        context.close()

        if n_pages == 1:
            return html[0]
        else:
            return html
