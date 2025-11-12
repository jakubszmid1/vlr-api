from fastapi import APIRouter, Depends, Query
from typing import Optional

from api.dependencies import get_api_client
from services.vlr_client import VlrClient

from services.teams import vlr_team_compositions
from services.events import vlr_get_events

from schemas.teams import VLRTeamCompositionsResponse

router = APIRouter(tags=["scraper"])


@router.get("/team/compositions", response_model=VLRTeamCompositionsResponse)
async def team_compositions(
    team_id: str = Query(..., description="VLR ID of the team to fetch data for"),
    event_id: str = Query("all", description="VLR ID of the event"),
    from_date: Optional[str] = Query(None, description="(Optional) Start date for filtering matches (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="(Optional) End date for filtering matches (YYYY-MM-DD)"),
    client: VlrClient = Depends(get_api_client),
):
    return await vlr_team_compositions(
        client=client,
        team_id=team_id,
        event_id=event_id,
        from_date=from_date,
        to_date=to_date
    )

@router.get("/events")
async def get_events(
    completed: bool = Query(True, description="Whether to fetch completed events (true) or upcoming events (false)"),
    page: int = Query(1, description="Page number for pagination"),
    event_name_filter: Optional[str] = Query(None, description="(Optional) Filter events by name containing this string (case-insensitive)"),
    client: VlrClient = Depends(get_api_client),
):
    return await vlr_get_events(
        client=client,
        completed=completed,
        page=page,
        event_name_filter=event_name_filter
    )
