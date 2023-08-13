import os
import sys
import shutil
import logging
import yaml
import tqdm
import dateparser
from feedgen.feed import FeedGenerator
from FeedFox.browser import Browser
from FeedFox.parser import Parser
from jinja2 import Environment, FileSystemLoader


public_base_path = "public"
if os.environ.get("GITHUB_ACTIONS_ENVIRONMENT", False):
    level = logging.INFO
else:
    level = logging.DEBUG
logging.basicConfig(
    level=level,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.debug("Starting FeedFox")


if __name__ == "__main__":
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    templates = {
        tname: Parser(**config["templates"][tname]) for tname in config["templates"]
    }
    default = config["default"]

    feeds = config["feeds"]

    browser = Browser()
    browser.start()
    bundles = {}
    for feed_id in tqdm.tqdm(feeds, desc="Fetching feeds"):
        feed = feeds[feed_id]
        logger.info(f"Processing feed: {feed_id} - {feed['title']}")

        if feed["bundle"] is None:
            feed["bundle"] = default["bundle"]
        if type(feed["bundle"]) == str:
            feed["bundle"] = [feed["bundle"]]

        paths = feed["bundle"]
        logger.debug(f"Feed {feed_id} will be bundled in {paths}")
        for path in paths:
            if path not in bundles:
                bundles[path] = FeedGenerator()
                logger.debug(f"Initialize feed to bundle {path}")
            path = os.path.join(public_base_path, path)
            if not os.path.exists(path):
                os.makedirs(path)

        fg = FeedGenerator()
        fg.id(feed_id)
        fg.title(feed.get("title", feed_id))
        fg.description(feed.get("description", default.get("description", feed_id)))
        fg.updated(dateparser.parse("now").astimezone())
        fg.image(url=feed.get("image", default.get("image", None)))
        if type(feed["link"]) == str:
            links = [feed["link"]]
            fg.link(href=feed["link"], rel="alternate")
        elif type(feed["link"]) == list:
            links = feed["link"]
            fg.link(href=feed["link"][0], rel="alternate")
        else:
            raise ValueError("Invalid feed link")
        if type(feed["template"]) == str:
            template = templates[feed["template"]]
        else:
            template = Parser(**feed["template"])

        timeout = feed.get("timeout", default.get("timeout", 30))
        for link in links:
            logger.info(f"Fetching {link}")
            try:
                html = browser.fetch(link, template.wait_for, timeout=timeout)
            except Exception as e:
                logger.error(f"Error while fetching {link}: {e}")
                logger.info("Skipping...")
                continue
            entries = template.parse(html)
            for entry in entries:
                fg.add_entry(entry.entry)
                for path in paths:
                    bundles[path].add_entry(entry.entry)

        for path in paths:
            path = os.path.join(public_base_path, path)
            fg.atom_file(os.path.join(path, f"{fg.id()}.atom"))
            fg.rss_file(os.path.join(path, f"{fg.id()}.rss"))

    for path in tqdm.tqdm(bundles, desc="Generating bundles"):
        logger.info(f"Generating bundle {path}")
        bundle = bundles[path]
        bundle.id(f"{path}-all")
        bundle.title(f"{path}")
        bundle.description(f"{path}")
        bundle.updated(dateparser.parse("now").astimezone())
        bundle.link(href=f"{path}/all.atom", rel="self")

        path = os.path.join(public_base_path, path)
        bundle.atom_file(os.path.join(path, "all.atom"))
        bundle.rss_file(os.path.join(path, "all.rss"))
    browser.stop()

    # Generate `index.html` files for bundles and feeds indexing
    bundles = {}
    for feed_id in tqdm.tqdm(feeds, desc="Generating index.html"):
        feed = feeds[feed_id]
        if feed["bundle"] is None:
            feed["bundle"] = default["bundle"]
        if type(feed["bundle"]) == str:
            feed["bundle"] = [feed["bundle"]]

        paths = feed["bundle"]
        for path in paths:
            if path not in bundles:
                bundles[path] = []
            bundles[path].append(
                {"href": os.path.join(path, f"{feed_id}.atom"), "title": feed["title"]}
            )

    for path in bundles:
        bundles[path].sort(key=lambda x: x["title"])
        bundles[path].insert(
            0, {"href": os.path.join(path, "all.atom"), "title": "All"}
        )

    env = Environment(loader=FileSystemLoader("web/templates"))
    template = env.get_template("index.html")

    with open("public/index.html", "w") as f:
        f.write(template.render(title="FeedFox RSS", bundles=bundles))

    if os.path.exists("public/static"):
        shutil.rmtree("public/static")
    shutil.copytree("web/static", "public/static")
