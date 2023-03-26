import asyncio
import logging

from gather_client_ws import GatherClient
from tabulate import tabulate

from gather_scrobble.config import (
    get_credentials,
    get_lastfm_client,
    get_spotify_client,
)


async def gather_heartbeat(client):
    await client.client_heartbeat()


async def test_gather_connection(credentials, space_id):
    client = GatherClient(
        credentials.gather_api_key, space_id, log_level=logging.ERROR
    )
    await client.run(gather_heartbeat)


def test_configuration(space_id):
    credentials = get_credentials()
    result = []
    print("Testing connection with Gather...")
    try:
        asyncio.get_event_loop().run_until_complete(
            test_gather_connection(credentials, space_id)
        )
        result.append(["Gather", True])
        print("Success")
    except Exception:
        result.append(["Gather", False])
        print("Failed")
    print("Testing connection with last.fm...")
    try:
        lastfm = get_lastfm_client(credentials)
        lastfm.get_now_playing()
        result.append(["last.fm", True])
        print("Success")
    except Exception:
        result.append(["last.fm", False])
        print("Failed")

    print("Testing connection with Spotify...")
    try:
        spotify = get_spotify_client(credentials)
        spotify.current_user_playing_track()
        result.append(["Spotify", True])
        print("Success")
    except Exception:
        result.append(["Spotify", False])
        print("Failed")

    print()
    print(tabulate(result, ["Service", "Working?"], tablefmt="heavy_grid"))
