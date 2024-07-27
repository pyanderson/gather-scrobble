import asyncio
import logging

from gather_client_ws import GatherClient
from tabulate import tabulate

from gather_scrobble.config import (
    get_credentials,
    get_lastfm_client,
    get_spotify_client,
    logger,
)


async def gather_heartbeat(client):
    await client.client_heartbeat()


async def test_gather_connection(
    credentials, space_id, log_level=logging.ERROR
):
    client = GatherClient(
        credentials.gather_api_key, space_id, log_level=log_level
    )
    await client.run(gather_heartbeat)


def test_configuration(space_id, log_level=logging.ERROR):
    credentials = get_credentials()
    result = []
    print("Testing connection with Gather...")
    try:
        asyncio.get_event_loop().run_until_complete(
            test_gather_connection(credentials, space_id, log_level)
        )
        result.append(["Gather", True])
        print("Success")
    except Exception:
        result.append(["Gather", False])
        print("Failed")
    print("Testing connection with last.fm...")
    try:
        lastfm = get_lastfm_client(credentials)
        logger.debug("Checking last.fm 'now playing'")
        lastfm.get_now_playing()
        logger.debug("last.fm 'now playing' is Working")
        result.append(["last.fm", True])
        print("Success")
    except Exception:
        result.append(["last.fm", False])
        print("Failed")

    print("Testing connection with Spotify...")
    try:
        spotify = get_spotify_client(credentials)
        logger.debug("Checking Spotify 'now playing'")
        spotify.current_user_playing_track()
        logger.debug("Spotify 'now playing' is Working")
        result.append(["Spotify", True])
        print("Success")
    except Exception:
        result.append(["Spotify", False])
        print("Failed")

    print()
    print(tabulate(result, ["Service", "Working?"], tablefmt="heavy_grid"))
