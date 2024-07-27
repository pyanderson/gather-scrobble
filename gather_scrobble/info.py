from tabulate import tabulate

from gather_scrobble.config import get_credentials


def show_info():
    credentials = get_credentials()
    print("Gather Scrobble")
    print(
        tabulate(
            [
                ["last.fm", credentials.has_lastfm],
                ["Spotify", credentials.has_spotify],
            ],
            ["Service", "Configured"],
            tablefmt="heavy_grid",
        )
    )
