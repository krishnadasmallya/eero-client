# Eero Client - Starter client for Eero API Interactions

[comment]: <> (![GitHub Workflow Status]&#40;https://img.shields.io/github/workflow/status/krishnadasmallya/eero-client/Python&#41;)

[comment]: <> ([![Coverage Status]&#40;https://coveralls.io/repos/github/krishnadasmallya/eero-client/badge.svg&#41;]&#40;https://coveralls.io/github/krishnadasmallya/eero-client&#41;)

Having seen 343max/eero-client's excellent starter project, I wanted extend the same to add api for network insights. This project is a fork of bruskiza/eero-client since I saw more recent updates after 343max/eero-client, the initial project.

This is still a simple client lib extended from eero(https://pypi.org/project/eero/) to access information about your eero home network. Reused major part from the original project and added few more api calls for network usage and speedtest

Right now it support the following features:
- login/login verification
- user_token refreshing
- account (all information about an account, most importantly a list of your networks)
- networks (information about a particular network)
- devices (a list of devices connected to a network)
- reboot
- data_usage_last_5_min_breakdown (network usage breakdown by device/profile/eeros)
- speedtest (invoke and get speedtest from eero)

The API should be easy to extend from here if you miss something. There are a lot of URLs in the response json that will help you explore the API further.

There is a sample client that you might use for your experiments. On first launch it will ask you for the phone number you used to create your eero account. Afterwards you've been asked for the verfication code that you got via SMS. From here on you are logged in - running the command again will dump a ton of information about your network(s).

# Usage:

After cloning: 

```
workstation: eero-client $ virtualenv ve
workstation: eero-client $ . ve/bin/activate
(ve) workstation: eero-client $ pip install -r requirements.txt
(ve) workstation: eero-client $ ./sample.py
Usage: sample.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  device    Prints out the information for a specific device
  devices   Show all the devices connected to your network
  eeros     Shows all the eeros on your network
  log       TODO: Not implemented
  login     Login to eero API
  networks  Shows available networks.
  reboot    Reboot an eero
  summary   Summary of your network (This contains the most information)
(ve) workstation:eero-client $ 
```