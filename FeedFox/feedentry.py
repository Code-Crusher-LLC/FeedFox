import logging
import dateparser
from dateparser.search import search_dates
from bs4 import BeautifulSoup, element
from feedgen.entry import FeedEntry as Entry

logger = logging.getLogger(__name__)


class FeedEntry(object):
    def __init__(self) -> None:
        super(FeedEntry, self).__init__()
        self._entry = Entry()
        logger.debug("Created new FeedEntry object")

        self._entry.title("Untitled")
        self._entry.id(dateparser.parse("now").astimezone().isoformat())
        self._entry.updated(dateparser.parse("now").astimezone())
        # logger.debug(f"Set entry title to {self._entry.title()}")
        # logger.debug(f"Set entry id to {self._entry.id()}")
        # logger.debug(f"Set entry updated to {self._entry.updated()}")

    @property
    def entry(self):
        return self._entry

    @property
    def title(self):
        return self._entry.title()

    @title.setter
    def title(self, value):
        if isinstance(value, BeautifulSoup) or isinstance(value, element.Tag):
            value = " ".join(value.stripped_strings)
        if isinstance(value, str) and value != "":
            self._entry.title(value)
        else:
            self._entry.title("Untitled")
            logger.warning(f"Title is empty or type of {type(value)}, set to Untitled")
        logger.debug(f"Set entry title to {self._entry.title()}")

    @property
    def link(self):
        return self._entry.link()

    @link.setter
    def link(self, value):
        if isinstance(value, BeautifulSoup) or isinstance(value, element.Tag):
            if value.has_attr("href") and value["href"]:
                self._entry.link(link={"href": value["href"]})
                self._entry.id(value["href"])
            else:
                self._entry.link(link={"href": ""})
        elif isinstance(value, str):
            self._entry.link(link={"href": value})
            self._entry.id(value)
        else:
            self._entry.link(link={"href": ""})
        logger.debug(f"Set entry link to {self._entry.link()}")
        logger.debug(f"Set entry id to {self._entry.id()}")

    @property
    def content(self):
        return self._entry.content()

    @content.setter
    def content(self, value):
        if isinstance(value, BeautifulSoup) or isinstance(value, element.Tag):
            # self._entry.content(" ".join(value.stripped_strings))
            self._entry.content(value.prettify())
        else:
            self._entry.content(value)
        logger.debug(f"Set entry content to {self._entry.content()}")

    @property
    def description(self):
        return self._entry.description()

    @description.setter
    def description(self, value):
        if isinstance(value, BeautifulSoup) or isinstance(value, element.Tag):
            self._entry.description(" ".join(value.stripped_strings))
        else:
            self._entry.description(value)
        logger.debug(f"Set entry description to {self._entry.description()}")

    @property
    def updated_time(self):
        return self._entry.published()

    @updated_time.setter
    def updated_time(self, value):
        if isinstance(value, BeautifulSoup) or isinstance(value, element.Tag):
            value = " ".join(value.stripped_strings)
        if isinstance(value, str) and value != "":
            if search_dates(value):
                value = search_dates(value)[0][1].astimezone()
            else:
                value = dateparser.parse("now").astimezone()
        self._entry.updated(value)
        self._entry.published(value)
        logger.debug(f"Set entry published time to {self._entry.published()}")
        logger.debug(f"Set entry updated time to {self._entry.updated()}")
