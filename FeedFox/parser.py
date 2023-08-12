import logging
from bs4 import BeautifulSoup
from .feedentry import FeedEntry

logger = logging.getLogger(__name__)


class Parser(object):
    entry_attributes = ["title", "link", "content", "description", "updated_time"]

    def __init__(self, entry=None, **kwargs):
        super(Parser, self).__init__()
        logger.debug("Created new Parser object")

        self.entry = entry
        self.wait_for = kwargs.get("wait_for", None)
        logger.debug(f"Set entry to {self.entry}")
        logger.debug(f"Set wait_for to {self.wait_for}")

        for attr in self.entry_attributes:
            setattr(self, attr, kwargs.get(attr, None))
            logger.debug(f"Set {attr} to {getattr(self, attr)}")

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        entries = []
        if self.entry is not None:
            # assume the attribute selector are based on the entry
            for tag in soup.css.select(self.entry):
                entry = FeedEntry()
                for attr in self.entry_attributes:
                    if getattr(self, attr) is not None:
                        attr_tag = tag.select_one(getattr(self, attr))
                        setattr(entry, attr, attr_tag)
                entries.append(entry)
        else:
            # assume the attribute selector are based on the document
            n_entries = len(soup.css.select(self.title))
            entries = [FeedEntry() for _ in range(n_entries)]
            for attr in self.entry_attributes:
                if getattr(self, attr) is not None:
                    attr_tags = soup.css.select(getattr(self, attr))
                    if len(attr_tags) != len(entries):
                        raise ValueError(
                            f"Number of {attr} tags does not match number of entries."
                        )
                    for i, tag in enumerate(attr_tags):
                        setattr(entries[i], attr, tag)
        return entries
