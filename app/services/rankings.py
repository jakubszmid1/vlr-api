from config.constants import VLR_URL
from bs4 import Tag, Comment
from services.vlr_client import VlrClient
from services.utils import cleanup_text

async def vlr_get_rankings(
        client: VlrClient,
        region: str,
) -> dict:
    url = f"{VLR_URL}/rankings/{region}"
    html = await client.soupify(url)

    rankings_table = html.select_one("div.mod-scroll")
    team_tags = rankings_table.select("div.rank-item.wf-card")
    # return {"test": str(team_tags)}
    data = []
    for team in team_tags:
        rank = cleanup_text(team.select_one("div.rank-item-rank-num").text)
        team_info = team.select_one("a.rank-item-team")
        team_id = team_info["href"].split("/")[-2]
        # find div with class ge-text
        team_name = get_team_name(team_info)
        team_country = cleanup_text(
            team_info.select_one("div.rank-item-team-country").get_text()
        )
        data.append({"rank": rank, "team_name": team_name, "team_country": team_country, "team_id": team_id})
    
    return {"rankings": data}

def get_team_name(team_info: Tag) -> str:
    name = ''.join(
        text for text in
        team_info
        .select_one("div.ge-text")
        .find_all(string=True, recursive=False)
        # ? Team name div contains comments that serve no purpose
        if not isinstance(text, Comment)
    )
    return cleanup_text(name, to_lower=False)