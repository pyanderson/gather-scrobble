import asyncio
import logging
from contextlib import suppress

from docopt import docopt

from gather_scrobble.config import logger
from gather_scrobble.info import show_info
from gather_scrobble.scrobble import start
from gather_scrobble.test import test_configuration


def main():
    """Gather Scrobble v0.1.1
    Usage:
        gather-scrobble start <space_id> [--source SOURCE] [--emojis EMOJIS] [--verbose]
        gather-scrobble info
        gather-scrobble test <space_id> [--verbose]

    Arguments:
        <space_id>          Gather space id.

    Options:
        -h --help           Show this screen.
        -s --source SOURCE  Scrobble source, if not defined the tool will try
                            all available sources configured.
                            Can be: lastfm, spotify, or any.
                            If 'any' it will use the first source configured in
                            the priority: lastfm -> spotify [default: any]
        -e --emojis EMOJIS  It is possible to customize the emojis, by setting
                            the list of emojis that will be chosen randomly,
                            and also you don't like emojis, you can set an
                            empty string here. [default: 🎼🎵🎶🎧📻🎷🎸🎹]
        -v --verbose        Enable verbose logging.

    """
    arguments = docopt(main.__doc__ or "", version="Gather Scrobble 0.1.1")
    log_level = logging.DEBUG if arguments.get("--verbose") else logging.ERROR
    logger.setLevel(log_level)
    for handler in logger.handlers:
        handler.setLevel(log_level)
    if arguments["start"]:
        if arguments["--source"] not in ["lastfm", "spotify", "any"]:
            raise Exception(f"Invalid source: {arguments['--source']}")
        with suppress(KeyboardInterrupt):
            asyncio.get_event_loop().run_until_complete(
                start(
                    arguments["<space_id>"],
                    arguments["--source"],
                    arguments["--emojis"],
                    log_level,
                )
            )
        print("bye")
    if arguments["info"]:
        show_info()
    if arguments["test"]:
        test_configuration(arguments["<space_id>"], log_level)
