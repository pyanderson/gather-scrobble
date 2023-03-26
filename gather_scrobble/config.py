import os
import platform
from pathlib import Path
from typing import Optional

import keyring
import pylast
import spotipy
from decouple import config
from spotipy.oauth2 import SpotifyClientCredentials

CONFIG_FOLDER = "gather-scrobble"


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


def get_credentials():
    gather_api_key = keyring.get_password(
        "gather-scrobble", "GATHER_API_KEY"
    ) or config("GATHER_API_KEY", default=None)
    if gather_api_key is None or str(gather_api_key).strip() == "":
        raise Exception("Missing 'GATHER_API_KEY' value")
    lastfm_api_key = keyring.get_password(
        "gather-scrobble", "LASTFM_API_KEY"
    ) or config("LASTFM_API_KEY", default=None)
    lastfm_api_secret = keyring.get_password(
        "gather-scrobble", "LASTFM_API_SECRET"
    ) or config("LASTFM_API_SECRET", default=None)
    lastfm_username = keyring.get_password(
        "gather-scrobble", "LASTFM_USERNAME"
    ) or config("LASTFM_USERNAME", default=None)
    spotify_client_id = keyring.get_password(
        "gather-scrobble", "SPOTIFY_CLIENT_ID"
    ) or config("SPOTIFY_CLIENT_ID", default=None)
    spotify_client_secret = keyring.get_password(
        "gather-scrobble", "SPOTIFY_CLIENT_SECRET"
    ) or config("SPOTIFY_CLIENT_SECRET", default=None)
    spotify_client_redirect_uri = keyring.get_password(
        "gather-scrobble", "SPOTIFY_CLIENT_REDIRECT_URI"
    ) or config("SPOTIFY_CLIENT_REDIRECT_URI", default=None)
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
        credentials.lastfm_api_key, credentials.lastfm_api_secret
    )
    network.username = credentials.lastfm_username
    network.session_key = get_lastfm_session_key(network)
    return network.get_user(credentials.lastfm_username)


def get_spotify_client(credentials: Credentials):
    if not credentials.has_spotify:
        raise Exception("Spotify not configured.")
    from spotipy.oauth2 import SpotifyOAuth

    auth_manager = SpotifyOAuth(
        credentials.spotify_client_id,
        credentials.spotify_client_secret,
        credentials.spotify_client_redirect_uri,
        scope=["user-read-currently-playing", "user-read-playback-state"],
    )
    return spotipy.Spotify(auth_manager=auth_manager)
