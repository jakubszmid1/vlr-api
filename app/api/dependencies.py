from services.vlr_client import VlrClient


async def get_api_client(session=None):
    client = VlrClient(session)
    try:
        yield client
    finally:
        await client.close()
