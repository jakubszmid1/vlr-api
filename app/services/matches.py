from config.constants import VLR_URL
from bs4 import Tag, Comment
from services.vlr_client import VlrClient
from services.utils import cleanup_text

async def vlr_get_match(
        client: VlrClient,
        match_id: str
) -> dict:
    url = f"{VLR_URL}/{match_id}"
    html = await client.soupify(url)

    teams_div = html.select_one("div.match-header-vs")
    team_1_name = get_team_name(teams_div, 1)
    team_2_name = get_team_name(teams_div, 2)

    scores_div = (
        teams_div
        .select_one("div.match-header-vs-score")
        .select_one("div.match-header-vs-score")
        .select_one("div.js-spoiler")
    )

    scores_spans = scores_div.find_all("span")

    # if winner span first -> team 1 won & vice versa
    if "match-header-vs-score-winner" in scores_spans[0]["class"]:
        winner = team_1_name
    else:
        winner = team_2_name

    team_1_score = cleanup_text(scores_spans[0].get_text())
    team_2_score = cleanup_text(scores_spans[2].get_text())

    return {
        "team_1": team_1_name,
        "team_2": team_2_name,
        "winner": winner,
        "team_1_stats": {
            "players": None,
            "score": team_1_score,
        },
        "team_2_stats": {
            "players": None,
            "score": team_2_score,
        },
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
