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
gather-scrobble --help
Gather Scrobble v0.1.1
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
        -v --verbose        Enable verbose logging.


```

#### Info

Before starting, check if you have configured the services:

```bash
gather-scrobble info
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
gather-scrobble test "aAa0aAaAaaA0Aaaa/Name"
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
gather-scrobble start "aAa0aAaAaaA0Aaaa/Name"
🎸 - Evil Papagali - Massacration 𝄛𝄙𝄘𝄛𝄙
```

#### Verbose

The `start` and `test` commands accept an optional flag `-v` or `--verbose` to show more detailed information about the execution:

```bash
[2024-07-27 13:29:24,850][DEBUG] Loading credentials
[2024-07-27 13:29:25,144][DEBUG] Starting application
[2024-07-27 13:29:25,769][INFO] Connected to wss://ip-00-000-00-000.sa-east-1-a.prod.aws.gather.town:443/
[2024-07-27 13:29:26,084][INFO] Connected as user a0000bC0DEFgjIjLmnoPqRSTuvxY
[2024-07-27 13:29:26,085][DEBUG] Receiving messages
[2024-07-27 13:29:26,086][DEBUG] Heartbeat sent
[2024-07-27 13:29:26,086][DEBUG] Application started
[2024-07-27 13:29:26,540][DEBUG] New Status: 📻 - Junior's Eyes - Black Sabbath
[2024-07-27 13:29:26,639][DEBUG] Message received: events {
  transactionStatus {
    txnId: 2550000000
    succeeded: true
  }
}
events {
  transactionStatus {
    txnId: 900000000
    succeeded: true
  }
}

^Cbye
```

## Docker

### Pull

```bash
docker pull pyanderson/gather-scrobble:0.1.1
```

### Docker Configuration

#### Keyring

The most common way to manage credentials in docker containers is through environment variables, but in this case, you can still use [keyring](https://github.com/jaraco/keyring), through the third-party [keyrings.cryptfile](https://github.com/frispete/keyrings.cryptfile), you will need to create a file with your credentials, mount a volume with the file in the path `/root/.local/share/python_keyring/cryptfile_pass.cfg` and set the `KEYRING_CRYPTFILE_PASSWORD` environment variable with the password that you used to create the file:

```bash
docker run -v $(echo $HOME)/.local/share/python_keyring/cryptfile_pass.csg:/root/.local/share/python_keyring/cryptfile_pass.cfg -e KEYRING_CRYPTFILE_PASSWORD=secret_password ...
```

#### Env File

Add your credentials to a .env file and use it with the --env-file option:

```bash
docker run --env-file /path/to/myfile.env ...
```

#### Cache

To avoid being asked to authorize the last.fm/Spotify application in every usage, you should mount a volume to save the gather-scrobble cache folder:

```bash
docker run -v /path/to/the/host/cache/folder:/root/.config
```

### Docker Usage

The docker container works as an executable, so you can use the same CLI command interface, for example, to test your configuration you can do this:

```bash
docker run --env-file /path/to/myfile.env -v /path/to/the/host/cache/folder:/root/.config -it pyanderson/gather-scrobble:0.1.1 test "aAa0aAaAaaA0Aaaa/Name"
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

#### Examples

Validate your credentials:

```bash
docker run -it --rm --name gather-scrobble --env-file /path/to/myfile.env -v /path/to/the/host/cache/folder:/root/.config pyanderson/gather-scrobble:0.1.1 test "aAa0aAaAaaA0Aaaa/Name"
Testing connection with Gather...
Success
Testing connection with last.fm...
Please authorize this script to access your account: https://www.last.fm/api/auth/?api_key=<api_key>
Success
Testing connection with Spotify...
Go to the following URL: https://accounts.spotify.com/authorize?client_id=<client_id>&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A9090&scope=user-read-currently-playing+user-read-playback-state
Enter the URL you were redirected to: http://127.0.0.1:9090/?code=<code>
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

Run gather-scrobble in background:

```bash
docker run -d --restart=always --name gather-scrobble --env-file /path/to/myfile.env -v /path/to/the/host/cache/folder:/root/.config pyanderson/gather-scrobble:0.1.1 start "aAa0aAaAaaA0Aaaa/Name"
cbe4b6c916d8e7977788462a447b8a6c9e526f46f5c9b85d7be5f843e7fd80dc
```

Check the logs:

```bash
docker logs -f gather-scrobble
[2023-04-29 15:39:30,637][DEBUG] loading credentials
[2023-04-29 15:39:31,427][DEBUG] starting application
[2023-04-29 15:39:32,925][DEBUG] application started
[2023-04-29 15:40:05,650][DEBUG] 🎼 - Madhouse - Anthrax
```

Stop:

```bash
docker rm -r gather-scrobble
gather-scrobble
```

### Docker Compose

Thanks to @chocoelho for the docker compose example.

compose.yaml:

```yaml
services:
  main:
    image: "pyanderson/gather-scrobble:0.1.1"
    command: start $${GATHER_SPACE_ID} -v
    restart: always
    env_file:
      - .env
    volumes:
      - .cache:/root/.config/gather-scrobble
```

Validate the credentials:

```bash
docker compose run --rm main test "aAa0aAaAaaA0Aaaa/Name"
```

Run in the detached mode:

```bash
docker compose up -d service
```

Logs:

```bash
docker compose logs service
```

### FAQ

- How to get the `space_id` value?
  First enter in the space you want to scrobble, the `space_id` will be in the URL after the `/app/`. E.g., in the URL "https://app.gather.town/app/aAa0aAaAaaA0Aaaa/Name" the `space_id` is `aAa0aAaAaaA0Aaaa/Name`.
