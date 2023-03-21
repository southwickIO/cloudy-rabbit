# Cloudy Rabbit
> v. 20230321

> author: southwickio

<br>

## Overview
Simple reconnaissance and threat hunting toolbox.

## Description
This collection of standalone scripts was written with the intent to gather data for some specific cybersecurity and threat hunting use cases. These scripts are quick 'n' dirty and cover some standalone tasks I wasn't able to find in the wild. This repo is a toolbox that covers diverse areas of reconnaissance and is continuously under development as new scripts are added.

## Dependencies
1. Python (>=3.10.6)
2. \*nix machine
3. scapy (`sudo pip3 install scapy`). Used for tipid.py and must be installed as sudo for tipid.py to work.

## Scripts

 1. **Fetch Comments** (fc.py) - This script fetches all HTML comments from a site specified by the user and outputs to STDOUT and ./comments.txt. This can be used from a cybersecurity standpoint as a way to look for any developer comments that made it to production that shouldn't have; such as passwords, keys, or other proprietary information.
 2. **Get Logs** (gl.sh) - This script outputs all `.log` files on a \*nix machine. Potential cybersecurity use cases include tracking down a specific log, what applications are running on the machine, and modification dates for DFIR. Run as sudo for different results.
 3. **Track IP-IDs** (tipid.py) - Must be run as sudo. Analyze the IP-IDs of an IP address to determine order of IDs. Different patterns can help determine exploits or corroborate any idle network scan (with a zombie) that only scans for sequential IP-IDs. This was based on the paper *A closer look at IP-ID behavior in the Wild* by Flavia Salutari, Danilo Cicalese, and Dario J. Rossi.

## Installation and Runtime
##### Note: There is no error handling for any script
1. `git clone github.com/southwickIO/cloudy-rabbit`
2. `cd cloudy-rabbit/`
3. `chmod -R u+x cloudy-rabbit/`
4. Run any script with the prefix `./`. For example: `./fc.py` or `./gl.sh`

## Todo
- [ ] Add error handling to scripts