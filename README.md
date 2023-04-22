# ZeroSpot
A tool to connect a Spotify account to a Spotify Connect device via command line on the local lan.

My issue was that when spotifyd (base on librespot) would reset, spotify forgets it and I'm unable to cast music to it with [spotcast](https://github.com/search?q=spotcast) from [Home Assistant](https://github.com/home-assistant). Also, I don't want to log in permanently with spotifyd to let others on the local net to use the device to play music.

The tool encrypts the given username and password and sends it to the Spotify Connect device. Other authentication options are not provided.





## Installation

Install zerospot with `pip`

```bash
  python3 -m pip install zerospot
```

    
## Usage/Examples
Read the help: `zeroconf -h`

 __a)__  From the command line:
```bash
zerospot <hostname-or-IP>:<port><path> --username my_username --password my_password
```
or

```bash
zerospot --host <hostname-or-IP> --port <port> --path <path> \
--username my_username --password my_password
```
 __b)__ Using a config file at a different location than `~/.config/zerospot/config.json`:

```bash
zerospot --config-file /path/to/config.json
```

 __c)__ or if you have a config file at the default location or environment variables set up simply use:

```bash
zerospot
```

Use it as a library
```python
from zerospot import ZeroSpot

uri = 'http://<hostname-or-IP>:<port><path>'  
username = 'my_username'
password = 'my_password'

zc = zerospot.ZeroSpot(uri, username, password)
zc.connect()
```

## Obtaining parameters from the Spotify Connect device

On Linux use:
```bash
avahi-browse --resolve _spotify-connect._tcp
```
and find the relevant fields: `hostname`, `port` and `CPath=...`

## Config file
It possible to configure the tool using a json file. Default location: ` ~/.config/zerospot/config.json`
Check `config.json.example` for format.
## Environment Variables

All of the parameters can be set via environment variables using `ZEROSPOT_<paramname>` convention. 

These are the following:

`ZEROSPOT_URI` `ZEROSPOT_HOST` `ZEROSPOT_PORT`  `ZEROSPOT_PATH` `ZEROSPOT_USERNAME` `ZEROSPOT_PASSWORD`

There's an option to use `FILE__ZEROSPOT_PASSWORD` to mark the location of a secret file that contains the password, perhaps to use it with Docker secrets.

The __command line parameters have priority__ over environment variables.
## Usage in Home Assistant without HACS

Copy or clone the git repository under `/config/custom_components/zerospot`

There's no way to expand secrets in shell command, so the simplest way is to just put the whole shell command in `secrets.yaml`:

```yaml
zs_cmd: /config/custom_components/zerospot/bin/zerospot <host>:<port> --username <username> --password <password>
```

and in `configuration.yaml` add:
```yaml
shell_command:
  zerospot: !secret zs_cmd 
```
## Usage with HACS

Link coming soon ...
## Roadmap

- Create pypi package out of this repo in order to use it in [HACS](https://github.com/hacs) integrations

- Create HACS integration

- Maybe support more types of login, but there are plenty of options to achieve this.


## Acknowledgements
Many thanks to  [TimotheeGerber](https://github.com/TimotheeGerber) whose work I used extensively and to the librespot and the librespot-python guys for the awesome work.
 - [Spotify-Connect by TimotheeGerber](https://github.com/TimotheeGerber/spotify-connect)
 - [librespot](https://github.com/librespot-org/librespot)
 - [librespot-python](https://github.com/kokarare1212/librespot-python)


## License

[MIT](https://choosealicense.com/licenses/mit/)

