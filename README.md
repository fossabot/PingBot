# PingBot
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fchitang233%2FPingBot.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fchitang233%2FPingBot?ref=badge_shield)


A simple Telegram bot to ping a server over ICMP or TCP protocol.

## Installation

First, you need to install these packages:

- Python 3.6+
- Python pip
- [zhengxiaowai/tcping](https://github.com/zhengxiaowai/tcping)

Then, clone the repo and install the python packages:

```shell
git clone git@github.com:chitang233/PingBot.git
cd PingBot
pip install -r requirements.txt
```

Finally, edit `main.py`

- `API_TOKEN` - Your Telegram Bot token.(Get it from [@BotFather](https://t.me/BotFather))
- `PROXY_URL` - Optional. Your proxy URL. Support HTTP and SOCKS5. *e.g. `http://host:port`, `socks5://host:port`*
- `SHOW_PUBLIC_IP` - Show your machine's public IP address in `/start` command if set to `True`. Default is `False`.

## Usage

```shell
python main.py
```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fchitang233%2FPingBot.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fchitang233%2FPingBot?ref=badge_large)