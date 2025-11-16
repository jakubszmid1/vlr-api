from fastapi import APIRouter, Depends, Query
from typing import Optional

from api.dependencies import get_api_client
from config.constants import EventRegion, EventTier
from services.vlr_client import VlrClient

from services.teams import vlr_team_compositions
from services.events import vlr_get_events
from services.rankings import vlr_get_rankings
from services.matches import vlr_get_match

from schemas.teams import VLRTeamCompositionsResponse
from schemas.events import VLREventsResponse

router = APIRouter(tags=["scraper"])


@router.get("/team/compositions", response_model=VLRTeamCompositionsResponse)
async def team_compositions(
    team_id: str = Query(
        ...,
        description="VLR ID of the team to fetch data for"
    ),
    event_id: str = Query(
        "all",
        description="VLR ID of the event"
    ),
    from_date: Optional[str] = Query(
        None,
        description="(Optional) Start date for filtering matches (YYYY-MM-DD)"
    ),
    to_date: Optional[str] = Query(
        None,
        description="(Optional) End date for filtering matches (YYYY-MM-DD)"
    ),
    client: VlrClient = Depends(get_api_client),
):
    return await vlr_team_compositions(
        client=client,
        team_id=team_id,
        event_id=event_id,
        from_date=from_date,
        to_date=to_date
    )


@router.get("/events", response_model=VLREventsResponse)
async def get_events(
    completed: bool = Query(
        True,
        description="Whether to fetch completed events (true) or upcoming events (false)"
    ),
    page: int = Query(
        1,
        description="Page number for pagination"
    ),
    event_name_filter: Optional[str] = Query(
        None,
        description="(Optional) Filter events by name containing this string "
                    "(case-insensitive)"
    ),
    region: Optional[EventRegion] = Query(
        EventRegion.ALL,
        description="(Optional) Region filter for events."
    ),
    event_tier: Optional[EventTier] = Query(
        EventTier.ALL,
        description="Tier filter for events."
    ),
    client: VlrClient = Depends(get_api_client),
):
    return await vlr_get_events(
        client=client,
        completed=completed,
        page=page,
        region=region,
        event_tier=event_tier,
        event_name_filter=event_name_filter
    )

@router.get("/rankings")
async def get_rankings(
    region: str = Query(
        ...,
        description="Region code for rankings"
    ),
    client: VlrClient = Depends(get_api_client),
):
    return await vlr_get_rankings(
        client=client,
        region=region
    )

@router.get("/match")
async def get_match(
    match_id: str = Query(
        ...,
        description="The VLR match ID of this match"
    ),
    client: VlrClient = Depends(get_api_client)
):
    return await vlr_get_match(
        client=client,
        match_id=match_id
    )