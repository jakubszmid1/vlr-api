from typing import Tuple
from config.constants import VLR_URL
from bs4 import Tag, BeautifulSoup
from services.vlr_client import VlrClient
from services.utils import cleanup_text, agents_from_composition_div

async def vlr_get_match(
        client: VlrClient,
        match_id: str
) -> dict:
    url = f"{VLR_URL}/{match_id}"
    html = await client.soupify(url)
    # TODO: differentiate upcoming & completed matches
    # TODO: handle upcoming matches
    return get_completed_match(html)
    

def get_completed_match(html: BeautifulSoup) -> dict:
    teams_div = html.select_one("div.match-header-vs")
    team_1_name = get_team_name(teams_div, 1)
    team_2_name = get_team_name(teams_div, 2)
    scores = get_match_scores(teams_div, team_1_name, team_2_name)
    
    maps_div = html.select_one("div.vm-stats-container")
    map_stats_overall_div = maps_div.select_one("div.vm-stats-game.mod-active")
    map_stats_individual_divs = maps_div.select("div.vm-stats-game")
    map_stats = get_map_stats(map_stats_overall_div)

    return scores | map_stats

def get_map_stats(stats_div: Tag) -> dict:
    stat_tables = stats_div.select("table.wf-table-inset.mod-overview > tbody")
    all_team_stats = {}
    for idx, team_table in enumerate(stat_tables, start=1):
        player_rows = team_table.select("tr")
        all_players = []
        for row in player_rows:
            player_name = cleanup_text(
                row
                .select_one("td.mod-player > div > a > div.text-of")
                .get_text()
            )
            player_id = cleanup_text(
                row
                .select_one("td.mod-player > div > a")["href"]
                .split("/")[-2]
            )
            agents = agents_from_composition_div(
                row.select_one("td.mod-agents > div"),
            )
            rating, acs = get_player_ratings(row)

            all_players.append({
                "player_name": player_name,
                "player_id": player_id,
                "rating": rating,
                "acs": acs,
                "agents": agents,
            })
        all_team_stats[f"team_{idx}"] = all_players
    return {"stats": all_team_stats}


def get_player_ratings(player_row: Tag) -> Tuple[str, str]:
    return "", "" # TODO


def get_match_scores(teams_div: Tag, team_1_name: str, team_2_name: str):
    scores_div = (
        teams_div
        .select_one("div.match-header-vs-score")
        .select_one("div.match-header-vs-score")
        .select_one("div.js-spoiler")
    )

    scores_spans = scores_div.find_all("span")
    # if winner span first -> team 1 won & vice versa
    if "match-header-vs-score-winner" in scores_spans[0]["class"]:
        winner, loser = team_1_name, team_2_name
        winner_score = cleanup_text(scores_spans[0].get_text())
        loser_score = cleanup_text(scores_spans[2].get_text())
    else:
        winner, loser = team_2_name, team_1_name
        winner_score = cleanup_text(scores_spans[2].get_text())
        loser_score = cleanup_text(scores_spans[0].get_text())

    return {
        "winner": winner,
        "loser": loser,
        "winner_score": winner_score,
        "loser_score": loser_score,
    }

def get_team_name(teams_div: Tag, team_num: int) -> str:
    """Get the name of a team from the teams div

    Args:
        teams_div (Tag): DIV containing teams and match scores
        team_num (int): Which team (1, 2), in left->right order on vlr

    Returns:
        str: Team name
    """
    team_name = (
        teams_div
        .select_one(f"a.match-header-link.mod-{team_num}")
        .select_one("div.wf-title-med")
        .get_text()
    )

    return cleanup_text(team_name)
