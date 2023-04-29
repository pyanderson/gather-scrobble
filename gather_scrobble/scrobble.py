import asyncio
import logging
import queue
import random
import threading
from itertools import cycle
from sys import stdout as terminal
from time import sleep
from typing import Optional

from gather_client_ws import GatherClient

from gather_scrobble.config import (
    Credentials,
    get_credentials,
    get_lastfm_client,
    get_spotify_client,
    logger,
)

BARS = "𝄖𝄗𝄘𝄙𝄚𝄛"

PLAYING_ANIMATION = [
    [1, 2, 0, 1, 4],
    [2, 2, 0, 2, 4],
    [3, 2, 1, 3, 4],
    [4, 3, 1, 4, 4],
    [5, 3, 2, 5, 3],
    [0, 3, 2, 0, 3],
    [1, 4, 3, 1, 3],
    [2, 4, 3, 2, 3],
    [3, 4, 4, 3, 2],
    [4, 5, 4, 4, 2],
    [5, 5, 5, 5, 2],
    [0, 5, 5, 0, 2],
]

EMOJIS = ["🎼", "🎵", "🎶", "🎧", "📻", "🎷", "🪗", "🎸", "🎹", "🎺", "🎻", "🪕", "🥁", "🪘"]


def parse_source(credentials: Credentials, source: str) -> str:
    if source == "any":
        if credentials.has_lastfm:
            return "lastfm"
        return "spotify"
    return source


class ScrobbleClient:
    def __init__(
        self, credentials: Credentials, source: str, emojis: str
    ) -> None:
        self.credentials = credentials
        self.source = parse_source(credentials, source)
        self.emojis = [e for e in emojis] if emojis != "" else [""]
        self._lastfm = None
        self._spotify = None
        if self.source == "lastfm":
            self._lastfm = get_lastfm_client(self.credentials)
        else:
            self._spotify = get_spotify_client(self.credentials)

    def get_lastfm_now_playing(self) -> Optional[str]:
        if self._lastfm is None:
            return None
        track = self._lastfm.get_now_playing()
        if track is None:
            return None
        artist_name = (
            track.artist.get_name() if track.artist is not None else ""
        )
        return f"{track.get_title()} - {artist_name}"

    def get_spotify_now_playing(self) -> Optional[str]:
        if self._spotify is None:
            return None
        track = self._spotify.current_user_playing_track()
        if track is None:
            return None
        name = track.get("item", {}).get("name", "")
        artists = track.get("item", {}).get("artists", [])
        artist_name = artists[0].get("name") if len(artists) > 0 else ""
        if name.strip() == "" or artist_name.strip() == "":
            return None
        return f"{name} - {artist_name}"

    def get_now_playing(self) -> Optional[str]:
        if self.source == "lastfm":
            return self.get_lastfm_now_playing()
        return self.get_spotify_now_playing()


async def clear_status(client):
    await client.set_emoji_status("")
    await client.set_text_status("")


async def set_status(client, emoji: str, text: str):
    await client.set_emoji_status(emoji)
    await client.set_text_status(text)
    logger.debug("%s - %s", emoji, text)


async def scrobble(client, scrobble_client):
    q = queue.Queue()

    def show_now_playing():
        default_msg = "Nothing is playing now 😕"
        msg = ""
        for bars in cycle(PLAYING_ANIMATION):
            if q.qsize() > 0:
                msg = q.get()
            if msg.strip() == "":
                to_write = default_msg
            else:
                to_write = f"{msg} {''.join(BARS[index] for index in bars)}"
            # No show the playing now when running in docker
            # to avoid messing with the logs.
            if logger.level > logging.DEBUG:
                terminal.write(f"\033[2K\r{to_write}")
                terminal.flush()
            sleep(0.1)

    current_now_playing = None
    threading.Thread(target=show_now_playing, daemon=True).start()
    retry = 0
    logger.debug("application started")
    while True:
        try:
            now_playing = scrobble_client.get_now_playing()
            if now_playing is None:
                if current_now_playing is not None:
                    await clear_status(client)
                current_now_playing = None
            elif current_now_playing != now_playing:
                emoji = random.choice(scrobble_client.emojis)
                current_now_playing = now_playing
                await set_status(client, emoji, now_playing)
                if emoji:
                    q.put(f"{emoji} - {current_now_playing}")
                else:
                    q.put(f"{current_now_playing}")
            await asyncio.sleep(15)
            retry = 0
        except KeyboardInterrupt:
            break
        except Exception:
            # The retry will ensure the problem is not temporary
            retry += 1
            if retry >= 3:
                break
            await asyncio.sleep(2)


async def start(space_id, source, emojis):
    logger.debug("loading credentials")
    credentials = get_credentials()
    if not credentials.is_valid:
        raise Exception("At least one source needs to be configured.")
    scrobble_client = ScrobbleClient(credentials, source, emojis)
    client = GatherClient(
        credentials.gather_api_key, space_id, log_level=logging.ERROR
    )
    logger.debug("starting application")
    await client.run(scrobble, scrobble_client)
