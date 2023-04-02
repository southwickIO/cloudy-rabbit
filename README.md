# Cloudy Rabbit
> v. 20230401

> author: southwickio

<br>

## Overview
Simple reconnaissance and threat hunting toolbox.

## Description
This collection of standalone scripts was written with the intent to gather data for some specific cybersecurity and threat hunting use cases. These scripts are quick 'n' dirty and cover some standalone tasks I wasn't able to find in the wild or wanted to create my own. This repo is a toolbox that covers diverse areas of reconnaissance and is continuously under development as new scripts are added.

## Dependencies
1. Python (>=3.10.6)
2. Ubuntu (>=20.04) or relevant distro.
3. scapy (`sudo pip3 install scapy`). Used for tipid.py and must be installed as sudo for tipid.py to work.

## Scripts

 0. **Menu** (main.py) - Must be run as sudo. This is the main script of the program.
 1. **Fetch Comments** (fc.py) - This script fetches all HTML comments from a site specified by the user and outputs to STDOUT and ./comments.txt. This can be used from a cybersecurity standpoint as a way to look for any developer comments that made it to production that shouldn't have; such as passwords, keys, or other proprietary information.
 2. **Get Logs** (gl.sh) - This script outputs all `.log` files on a \*nix machine. Potential cybersecurity use cases include tracking down a specific log, what applications are running on the machine, and modification dates for DFIR. Run as sudo for different results.
 3. **Track IP-IDs** (tipid.py) - Must be run as sudo. Analyze the IP-IDs of an IP address to determine order of IDs. Different patterns can help determine exploits or corroborate any idle network scan (with a zombie) that only scans for sequential IP-IDs. This was based on the paper *A closer look at IP-ID behavior in the Wild* by Flavia Salutari, Danilo Cicalese, and Dario J. Rossi.
 4. **Count Host Command** (ch.sh) - Must be run as sudo. Runs the host command N times and counts unique occurences across different geographical regions. This can assist an analyst in finding anomalous data and help further map an external network.   

## Installation and Runtime
##### Note: There is no error handling for any script
1. `git clone github.com/southwickIO/cloudy-rabbit`
2. `cd cloudy-rabbit/`
3. `chmod -R u+x cloudy-rabbit/`
4. Run any script with the prefix `./`. For example: `./fc.py` or `./gl.sh` or run the menu `./main.py`

## Todo
- [ ] create a menu (main.py) for the application
- [ ] create a script (nmap ip-options) or scapy that detects source routing
- [ ] create a script that tells if packets are being fragmented or not. Fragmentation is a way to potentially bypass IDS.
- [ ] Banner grabber using the same dns switing mechanisn from ch.sh
- [ ] script that detect iis lockdown tool, apache mod headers, and apache2.conf serversignature/server token settings. This could detect false or off banners
- [ ] simple proxy creator script
- [ ] http tunelling detection script. See ../res/Detecting HTTP tunneling.
- [ ] detect outbound ssh traffic script
- [ ] simple custom vpn script
- [ ] IP spoofing detection script. See ../res/detecting ip spoofing and the other one
- [ ] bogon detection script
- [ ] routing tables enumeration script
- [ ] port 53, 445, 161-162, 389, 135, 137-139 enumeration script. make it quiet.
- [ ] sysinternals wrapper and menu (?exploratory; might be its own project)
- [ ] sysinternals detector script
- [ ] System Call Table explorer/detector for linux
- [ ] File metadata explorer
- [ ] Hidden Form Items Finder for websites 
- [ ] tunnel check script: ack tunneling, icmp tunneling, ssh tunneling
- [ ] source routing check

- [ ] Add error handling to scripts
- [x] Add an output folder check to scripts