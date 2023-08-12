# FeedFox

Generate RSS/ATOM feeds from web pages with FeedFox. Even those websites that load content via JavaScript are not an issue, thanks to the Playwright headless browser integration. Dynamically loaded content by JS can now be fetched with ease. While being inspired by [Feed me up, Scotty!](https://feed-me-up-scotty.vincenttunru.com/), FeedFox, implemented in Python, introduces further enhancements in usability.


## Features

- **Dynamic JS Content Support**: With Playwright at its core, FeedFox can easily fetch content from JS-intensive web pages.
- **Customizable Templates**: Adapt templates to your preference and crawl data in a manner that suits your needs.
- **Bundled Feeds**: Incorporate feeds into designated bundles, producing aggregated `all.rss` and `all.atom` feeds for every single bundle.
- **Automated Workflow**: Leveraging GitHub Actions, FeedFox automates feed generation and subsequently publishes on GitHub Pages.

## Quick Start

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/feedfox.git
    ```

2. **Define Your Templates and Feeds in `config.yaml`**


3. **Fire Up FeedFox**

    ```Python
    python app.py
    ```

4. **Navigate to the `public` directory to view the generated feeds.**


## Configuration
TBD

## Contribute
TBD

## License
FeedFox is under the MIT License.

## Acknowledgments
- A nod to [Feed me up, Scotty!](https://feed-me-up-scotty.vincenttunru.com/) for the inspiration.
- Gratitude to every contributor who's shaping FeedFox.
