# Gather Scrobble

Inspired by [gathertown/mod-spotify-as-status](https://github.com/gathertown/mod-spotify-as-status).

Scrobble your `last.fm` or `Spotify` activity to the `Gather` status.

![gather-scrobble](https://github.com/pyanderson/gather-scrobble/blob/main/images/gather-scrobble-at-terminal.gif)

![gather-status](https://github.com/pyanderson/gather-scrobble/blob/main/images/gather-status.png)

## Installation

```bash
pip install gather-scrobble
```

As this library has a CLI, you may have permissions issues when installing, so try it with the `--user` flag:

```bash
pip install gather-scrobble --user
```

## Documentation
### Configuration
It's necessary to configure the following credentials:

#### Gather Credentials
Access [Gather API keis](https://app.gather.town/apikeys) to get your `API_KEY`.

#### last.fm Credentials
**If you will scrobble from last.fm.**

Create a [last.fm API account](https://www.last.fm/api/account/create) to get your `API_KEY` and `API_SECRET`.

#### Spotify Credentials
**If you will scrobble from Spotify.**

Access your [Spotify account dashboard](https://developer.spotify.com/dashboard/applications) and create a new app (in case you don't have one or do not want to use an existing one). And get your `CLIENT_ID` and `CLIENT_SECRET`.

Also add a redirect URI in the `Edit Settings`. Suggested value: `http://127.0.0.1:9090`.

The spotispy will instantiate a server to receive the access token. More info [here](https://spotipy.readthedocs.io/en/2.22.1/#redirect-uri).


You can configure your credentials in 4 ways and with respective priorities:

#### keyring (recommended)

```bash
keyring set gather-scrobble GATHER_API_KEY
keyring set gather-scrobble LASTFM_API_KEY
keyring set gather-scrobble LASTFM_API_SECRET
keyring set gather-scrobble LASTFM_USERNAME
keyring set gather-scrobble SPOTIFY_CLIENT_ID
keyring set gather-scrobble SPOTIFY_CLIENT_SECRET
keyring set gather-scrobble SPOTIFY_CLIENT_REDIRECT_URI
```

#### environment variables

```bash
export GATHER_API_KEY=<GATHER_API_KEY>
export LASTFM_API_KEY=<LASTFM_API_KEY>
export LASTFM_API_SECRET=<LASTFM_API_SECRET>
export LASTFM_USERNAME=<LASTFM_USERNAME>
export SPOTIFY_CLIENT_ID=<SPOTIFY_CLIENT_ID>
export SPOTIFY_CLIENT_SECRET=<SPOTIFY_CLIENT_SECRET>
export SPOTIFY_CLIENT_REDIRECT_URI=<SPOTIFY_CLIENT_REDIRECT_URI>
```

#### .ini file

```ini
[settings]
GATHER_API_KEY=<GATHER_API_KEY>
LASTFM_API_KEY=<LASTFM_API_KEY>
LASTFM_API_SECRET=<LASTFM_API_SECRET>
LASTFM_USERNAME=<LASTFM_USERNAME>
SPOTIFY_CLIENT_ID=<SPOTIFY_CLIENT_ID>
SPOTIFY_CLIENT_SECRET=<SPOTIFY_CLIENT_SECRET>
SPOTIFY_CLIENT_REDIRECT_URI=<SPOTIFY_CLIENT_REDIRECT_URI>
```

#### .env file

```dotenv
GATHER_API_KEY=<GATHER_API_KEY>
LASTFM_API_KEY=<LASTFM_API_KEY>
LASTFM_API_SECRET=<LASTFM_API_SECRET>
LASTFM_USERNAME=<LASTFM_USERNAME>
SPOTIFY_CLIENT_ID=<SPOTIFY_CLIENT_ID>
SPOTIFY_CLIENT_SECRET=<SPOTIFY_CLIENT_SECRET>
SPOTIFY_CLIENT_REDIRECT_URI=<SPOTIFY_CLIENT_REDIRECT_URI>
```

### Usage

#### Help

```bash
$ gather-scrobble --help
Gather Scrobble v0.0.1
    Usage:
        gather-scrobble start <space_id> [--source SOURCE] [--emojis EMOJIS]
        gather-scrobble info
        gather-scrobble test <space_id>

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

    
```

#### Info
Before starting, check if you have configured the services:

```bash
$ gather-scrobble info
Gather Scrobble
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Service   ┃ Configured   ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━━━━┫
┃ Gather    ┃ True         ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━━━━┫
┃ last.fm   ┃ True         ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━━━━┫
┃ Spotify   ┃ False        ┃
┗━━━━━━━━━━━┻━━━━━━━━━━━━━━┛
```

#### Test
And test your configuration:

```bash
$ gather-scrobble test "aAa0aAaAaaA0Aaaa/Name"
Testing connection with Gather...
Success
Testing connection with last.fm...
Success
Testing connection with Spotify...
Success

┏━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Service   ┃ Working?   ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━━┫
┃ Gather    ┃ True       ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━━┫
┃ last.fm   ┃ True       ┃
┣━━━━━━━━━━━╋━━━━━━━━━━━━┫
┃ Spotify   ┃ True       ┃
┗━━━━━━━━━━━┻━━━━━━━━━━━━┛
```

#### Start
The first time you scrobble for any of the sources, the user will be asked to authorize your application to access data from the respective scrobble sources.

```bash
$ gather-scrobble start "aAa0aAaAaaA0Aaaa/Name"
🎸 - Evil Papagali - Massacration 𝄛𝄙𝄘𝄛𝄙
```

### FAQ

- How to get the `space_id` value?
First enter in the space you want to scrobble, the `space_id` will be in the URL after the `/app/`. E.g., in the URL "https://app.gather.town/app/aAa0aAaAaaA0Aaaa/Name" the `space_id` is `aAa0aAaAaaA0Aaaa/Name`.
