from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import AnyUrl, Field, model_validator

from jsonstat_validator.models.base import JSONStatBaseModel
from jsonstat_validator.utils import JSONStatValidationError


class Link(JSONStatBaseModel):
    """Model for a link.

    It is used to provide a list of links related to a dataset or a dimension,
    sorted by relation.
    """

    type: str | None = Field(
        default=None,
        description=(
            "It describes the media type of the accompanying href. "
            "Not required when the resource referenced in the link "
            "is a JSON-stat resource."
        ),
    )
    # Required for proper links to external or JSON-stat resources
    href: AnyUrl = Field(description="It specifies a URL.")
    class_: Literal["dataset", "dimension", "collection"] | None = Field(
        default=None,
        alias="class",
        description=(
            "It describes the class of the resource referenced "
            "in the link. Not required when the resource referenced "
            "in the link is a JSON-stat resource."
        ),
    )
    label: str | None = Field(
        default=None,
        description=(
            "It provides a human-readable label for the link. "
            "Not required when the resource referenced in the link "
            "is a JSON-stat resource."
        ),
    )

    @model_validator(mode="after")
    def validate_link(self) -> Link:
        # Defensive; keeps error types consistent
        if self.href is None:
            raise JSONStatValidationError("Link objects must include an 'href'.")
        return self


class LinkRelationType(str, Enum):
    """Link relation types allowed in JSON-stat.

    This ID must be an IANA link relation name:
    https://www.iana.org/assignments/link-relations/link-relations.xhtml
    that describes the relation between the elements of the array and the parent of link.
    """

    ABOUT = "about"
    ALTERNATE = "alternate"
    APPENDIX = "appendix"
    ARCHIVES = "archives"
    AUTHOR = "author"
    BLOCKED_BY = "blocked-by"
    BOOKMARK = "bookmark"
    CANONICAL = "canonical"
    CHAPTER = "chapter"
    COLLECTION = "collection"
    CONTENTS = "contents"
    COPYRIGHT = "copyright"
    CREATE_FORM = "create-form"
    CURRENT = "current"
    DERIVED_FROM = "derivedfrom"
    DESCRIBED_BY = "describedby"
    DESCRIBES = "describes"
    DISCLOSURE = "disclosure"
    DNS_PREFETCH = "dns-prefetch"
    DUPLICATE = "duplicate"
    EDIT = "edit"
    EDIT_FORM = "edit-form"
    EDIT_MEDIA = "edit-media"
    ENCLOSURE = "enclosure"
    FIRST = "first"
    GLOSSARY = "glossary"
    HELP = "help"
    HOSTS = "hosts"
    HUB = "hub"
    ICON = "icon"
    INDEX = "index"
    ITEM = "item"
    LAST = "last"
    LATEST_VERSION = "latest-version"
    LICENSE = "license"
    LRDD = "lrdd"
    MEMENTO = "memento"
    MONITOR = "monitor"
    MONITOR_GROUP = "monitor-group"
    NEXT = "next"
    NEXT_ARCHIVE = "next-archive"
    NOFOLLOW = "nofollow"
    NOREFERRER = "noreferrer"
    ORIGINAL = "original"
    PAYMENT = "payment"
    PINGBACK = "pingback"
    PRECONNECT = "preconnect"
    PREDECESSOR_VERSION = "predecessor-version"
    PREFETCH = "prefetch"
    PRELOAD = "preload"
    PRERENDER = "prerender"
    PREV = "prev"
    PREVIEW = "preview"
    PREVIOUS = "previous"
    PREV_ARCHIVE = "prev-archive"
    PRIVACY_POLICY = "privacy-policy"
    PROFILE = "profile"
    RELATED = "related"
    REPLIES = "replies"
    SEARCH = "search"
    SECTION = "section"
    SELF = "self"
    SERVICE = "service"
    START = "start"
    STYLESHEET = "stylesheet"
    SUBSECTION = "subsection"
    SUCCESSOR_VERSION = "successor-version"
    TAG = "tag"
    TERMS_OF_SERVICE = "terms-of-service"
    TIMEGATE = "timegate"
    TIMEMAP = "timemap"
    TYPE = "type"
    UP = "up"
    VERSION_HISTORY = "version-history"
    VIA = "via"
    WEBMENTION = "webmention"
    WORKING_COPY = "working-copy"
    WORKING_COPY_OF = "working-copy-of"
