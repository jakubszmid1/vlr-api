from enum import Enum

VLR_URL = "https://www.vlr.gg"

API_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


class Status:
    OK = 200


class EventTier(str, Enum):
    ALL = "all"
    VCT = "vct"
    VCL = "vcl"
    TIER3 = "tier3"
    GAMECHANGERS = "gamechangers"
    COLLEGIATE = "collegiate"
    OFFSEASON = "offseason"


EVENT_TIER_CODE_MAP = {
    EventTier.ALL: "all",
    EventTier.VCT: "60",
    EventTier.VCL: "61",
    EventTier.TIER3: "62",
    EventTier.GAMECHANGERS: "63",
    EventTier.COLLEGIATE: "64",
    EventTier.OFFSEASON: "67",
}


class EventRegion(str, Enum):
    ALL = "all"
    AMERICAS = "americas"
    EMEA = "emea"
    PACIFIC = "pacific"
    CHINA = "china"


REGION_CODE_MAP = {
    EventRegion.ALL: "all",
    EventRegion.AMERICAS: "26",
    EventRegion.EMEA: "27",
    EventRegion.PACIFIC: "28",
    EventRegion.CHINA: "24",
}
