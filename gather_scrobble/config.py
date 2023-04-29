import logging
import os
import platform
from pathlib import Path
from typing import Optional, cast

import keyring
import pylast
import spotipy
from decouple import AutoConfig
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

from gather_scrobble.utils import get_logger

config = AutoConfig(os.getcwd())  # search for settings in the current dir
USE_CRYPTFILE = config("USE_CRYPTFILE", cast=bool, default=False)
CONFIG_FOLDER = "gather-scrobble"

logger = get_logger(
    "gather-scrobble", logging.DEBUG if USE_CRYPTFILE else logging.INFO
)


class Credentials:
    def __init__(
        self,
        gather_api_key: str,
        lastfm_api_key: Optional[str],
        lastfm_api_secret: Optional[str],
        lastfm_username: Optional[str],
        spotify_client_id: Optional[str],
        spotify_client_secret: Optional[str],
        spotify_client_redirect_uri: Optional[str],
    ) -> None:
        self.gather_api_key = gather_api_key
        self.lastfm_api_key = lastfm_api_key
        self.lastfm_api_secret = lastfm_api_secret
        self.lastfm_username = lastfm_username
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.spotify_client_redirect_uri = spotify_client_redirect_uri

    @property
    def has_lastfm(self) -> bool:
        return (
            self.lastfm_api_key is not None
            and self.lastfm_api_secret is not None
            and self.lastfm_username is not None
        )

    @property
    def has_spotify(self) -> bool:
        return (
            self.spotify_client_id is not None
            and self.spotify_client_secret is not None
            and self.spotify_client_redirect_uri is not None
        )

    @property
    def is_valid(self) -> bool:
        return self.has_lastfm or self.has_spotify


def _get_config_value(var_name: str) -> Optional[str]:
    keyring_value = keyring.get_password("gather-scrobble", var_name)
    env_var = config(var_name, default=None)
    return keyring_value or cast(Optional[str], env_var)


def get_credentials():
    if USE_CRYPTFILE:
        from keyrings.cryptfile.cryptfile import CryptFileKeyring

        kr = CryptFileKeyring()
        kr.keyring_key = config("KEYRING_CRYPTFILE_PASSWORD", default="secret")
        keyring.set_keyring(kr)
    gather_api_key = _get_config_value("GATHER_API_KEY")
    if gather_api_key is None or str(gather_api_key).strip() == "":
        raise Exception("Missing 'GATHER_API_KEY' value")
    lastfm_api_key = _get_config_value("LASTFM_API_KEY")
    lastfm_api_secret = _get_config_value("LASTFM_API_SECRET")
    lastfm_username = _get_config_value("LASTFM_USERNAME")
    spotify_client_id = _get_config_value("SPOTIFY_CLIENT_ID")
    spotify_client_secret = _get_config_value("SPOTIFY_CLIENT_SECRET")
    spotify_client_redirect_uri = _get_config_value(
        "SPOTIFY_CLIENT_REDIRECT_URI"
    )
    return Credentials(
        gather_api_key,
        lastfm_api_key,
        lastfm_api_secret,
        lastfm_username,
        spotify_client_id,
        spotify_client_secret,
        spotify_client_redirect_uri,
    )


def get_config_folder_path() -> Path:
    if "windows" in platform.system().lower():
        config_dir = Path(os.environ.get("APPDATA", "config"), CONFIG_FOLDER)
    else:
        config_dir = Path(
            os.environ.get("XDG_CONFIG_HOME", Path("~/.config").expanduser()),
            CONFIG_FOLDER,
        )
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_lastfm_session_key(network: pylast.LastFMNetwork) -> str:
    session_key_file = Path(
        get_config_folder_path(), f"lastfm_user_{network.username}"
    )
    if not session_key_file.exists():
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()

        print(f"Please authorize this script to access your account: {url}\n")
        import time
        import webbrowser

        webbrowser.open(url)

        while True:
            try:
                session_key = skg.get_web_auth_session_key(url)
                with open(session_key_file, "w") as f:
                    f.write(session_key)
                break
            except pylast.WSError:
                time.sleep(1)
    return session_key_file.read_text()


def get_lastfm_client(credentials: Credentials):
    if not credentials.has_lastfm:
        raise Exception("last.fm not configured.")
    network = pylast.LastFMNetwork(
        cast(str, credentials.lastfm_api_key),
        cast(str, credentials.lastfm_api_secret),
    )
    network.username = credentials.lastfm_username
    network.session_key = get_lastfm_session_key(network)
    return network.get_user(credentials.lastfm_username)


class CustomCacheHandler(CacheFileHandler):
    def __init__(self, cache_path=None, username=None):
        custom_cache_path = Path(get_config_folder_path(), "spotify.cache")
        super().__init__(custom_cache_path, username)


def get_spotify_client(credentials: Credentials):
    if not credentials.has_spotify:
        raise Exception("Spotify not configured.")

    auth_manager = SpotifyOAuth(
        credentials.spotify_client_id,
        credentials.spotify_client_secret,
        credentials.spotify_client_redirect_uri,
        scope=["user-read-currently-playing", "user-read-playback-state"],
        cache_handler=CustomCacheHandler(),
        open_browser=not USE_CRYPTFILE,
    )
    return spotipy.Spotify(auth_manager=auth_manager)
