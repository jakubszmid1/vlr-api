from config.constants import VLR_URL, REGION_CODE_MAP, EVENT_TIER_CODE_MAP, Status, EventRegion, EventTier
from bs4 import BeautifulSoup, ResultSet, Tag
from services.vlr_client import VlrClient
from services.utils import cleanup_text, safe_int, convert_date_format
from datetime import datetime


async def vlr_get_events(
        client: VlrClient,
        completed: bool = True,
        page: int = 1,
        region: EventRegion = EventRegion.ALL,
        event_tier: EventTier = EventTier.ALL,
        event_name_filter: str = None) -> dict:

    url = f"{VLR_URL}/events"
    params = {
        "page": page,
        "region": REGION_CODE_MAP[region],
        "tier": EVENT_TIER_CODE_MAP[event_tier]
    }
    html = await client.soupify(url, params=params)
    events_tag = get_events_list(html, completed)
    events = []
    for event_tag in events_tag:
        event_id = get_event_id_from_href(event_tag)
        date_start, date_end = get_event_dates(event_tag)
        event_name, prize_amount = get_inner_data_event(event_tag)

        if event_name_filter and event_name_filter.lower() not in event_name:
            continue

        events.append({
            "event_name": event_name,
            "date_start": date_start,
            "date_end": date_end,
            "prize_amount": prize_amount,
            "event_id": event_id,
        })

    return {"events": events}

def get_event_id_from_href(event_tag: Tag) -> str:
    href = event_tag['href']
    try:
        event_id = href.split("/")[-2]
        int(event_id)
        return event_id
    except (IndexError, ValueError):
        pass

    try:
        event_id = href.split("/")[-1]
        int(event_id)
        return event_id
    except (IndexError, ValueError):
        return "N/A"
    
def get_event_dates(event_tag: Tag):
    # mod-dates
    date_div = event_tag.select_one("div.mod-dates")
    # date is directly in the div, nested divs contain other data
    date_text = cleanup_text(date_div.contents[0].text) if date_div else "N/A"

    if "—" in date_text:
        date_start, date_end = date_text.split("—", 1)
        current_year = datetime.now().year
        date_start = convert_date_format(date_start.strip(), current_year)
        date_end = convert_date_format(date_end.strip(), current_year)
        return date_start, date_end
    else:
        return "N/A", "N/A"
    
def get_events_list(html: BeautifulSoup, completed: bool) -> ResultSet[Tag]:
    label_class = "mod-completed" if completed else "mod-upcoming"
    event_completed_tag = html.select_one(f"div.wf-label.{label_class}")
    events_container = event_completed_tag.find_parent("div")
    return events_container.select("a.wf-card.event-item")

def get_inner_data_event(event_tag: Tag):
    event_name = cleanup_text(event_tag.select_one("div.event-item-title").text)
    prize_amount_div = event_tag.select_one("div.mod-prize")
    # prize amount is directly in the div, nested divs contain other data
    prize_amount = cleanup_text(prize_amount_div.contents[0].text) if prize_amount_div else "N/A"
    return event_name, prize_amount
