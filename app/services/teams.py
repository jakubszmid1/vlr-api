from typing import Tuple
from config.constants import VLR_URL, Status
from bs4 import BeautifulSoup, Tag
from services.vlr_client import VlrClient
from services.utils import cleanup_text, safe_int, agents_from_composition_div


async def vlr_team_compositions(client: VlrClient,
                                team_id: str,
                                event_id: str = "all",
                                from_date: str = None,
                                to_date: str = None) -> dict:
    url = f"{VLR_URL}/team/stats/{team_id}"

    params = {
        k: v for k, v in {
            "event_id": event_id,
            "from_date": from_date,
            "to_date": to_date
        }.items() if v is not None
    }

    html = await client.soupify(url, params=params)

    table_body = html.select_one("table.wf-table.mod-team-maps > tbody")
    team_name, team_code = get_team_name(html)

    map_data = {}
    # tr's without class are map rows, others contain metadata in HTML comments
    for map_row in table_body.find_all("tr", class_=False):
        map_name = ""
        agent_divs = parse_team_compositions_from_map_row(map_row)

        # Map has not been played / no compositions data
        if len(agent_divs) == 0:
            continue

        if not map_name:
            map_name = cleanup_text(agent_divs[0]["data-map"])

        all_compositions_data = []
        for composition_div in agent_divs:
            compositions_data = {}

            compositions_data["times_played"] = times_map_played_from_composition_div(composition_div)
            compositions_data["agents"] = agents_from_composition_div(composition_div)
            all_compositions_data.append(compositions_data)

        all_compositions_data.sort(key=lambda x: x["times_played"], reverse=True)

        map_stats = {
            "compositions": all_compositions_data
        }

        map_data[map_name] = map_stats

    data = {
        "team_id": team_id,
        "team_name": team_name,
        "team_code": team_code,
        "maps": map_data
    }

    return {"status": Status.OK, "compositions": data}


def times_map_played_from_composition_div(composition_div: Tag) -> int:
    # Context is small.. there are 2 spans, one empty with no style "", one containing times played
    def is_inline(style): return style and all(
        [s in style for s in ["inline", "display"]])  # <-- bruh
    times_played_span = composition_div.find("span", style=lambda s: is_inline(s)).text
    return safe_int(cleanup_text(times_played_span))


def parse_team_compositions_from_map_row(map_row: Tag) -> Tag:
    tds = map_row.find_all("td")
    all_comps = tds[-1].find("div")
    return all_comps.find_all("div", class_="agent-comp-agg mod-first", recursive=False)

def get_team_name(html: BeautifulSoup) -> Tuple[str, str]:
    div = html.select_one("div.team-header")
    team_name = div.select_one("h1.wf-title")
    team_name_code = div.select_one("h2.wf-title.team-header-tag")

    return (
        cleanup_text(team_name.get_text(), to_lower=False),
        cleanup_text(team_name_code.get_text(), to_lower=False)
    )