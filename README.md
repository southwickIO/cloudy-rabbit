# Cloudy Rabbit
> v. 20230407

> author: southwickio

<br>

## Overview
Simple reconnaissance and threat hunting toolbox.

## Description
This collection of standalone scripts was written with the intent to gather data for some specific cybersecurity and threat hunting use cases. These scripts are quick 'n' dirty and cover some standalone tasks I wasn't able to find in the wild or wanted to create my own. This repo is a toolbox that covers diverse areas of reconnaissance and is continuously under development as new scripts are added.

## Dependencies
1. Python (>=3.8)
2. Ubuntu (>=20.04) or relevant distro.
3. scapy (`sudo pip3 install scapy`). Used for ti.py and must be installed as sudo for ti.py to work.
4. ifconfig (`sudo apt install net-tools`). Used for df.sh to request information from interfaces.
5. nmap (`sudo apt install nmap`). Used for bg.sh to scan some port services.

## Installation and Runtime
##### Note: There is no error handling. Please read each script header before use. 
1. `git clone github.com/southwickIO/cloudy-rabbit`
2. `cd cloudy-rabbit/`
3. `chmod -R u+x cloudy-rabbit/`
4. Run any script with the prefix `./`. For example: `./fc.py` or `./gl.sh` or run the menu `sudo ./main.py`

## Scripts
0. **Menu** (main.py) - Must be run as sudo. This is the main script of the program.
1. **Fetch Comments** (fc.py) - This script fetches all HTML comments from a site specified by the user and outputs to STDOUT and ./comments.txt. This can be used from a cybersecurity standpoint as a way to look for any developer comments that made it to production that shouldn't have; such as passwords, keys, or other proprietary information.
2. **Get Logs** (gl.sh) - This script outputs all `.log` files on a \*nix machine. Potential cybersecurity use cases include tracking down a specific log, what applications are running on the machine, and modification dates for DFIR. Run as sudo for different results.
3. **Track IP-IDs** (ti.py) - Must be run as sudo. Analyze the IP-IDs of an IP address to determine order of IDs. Different patterns can help determine exploits or corroborate any idle network scan (with a zombie) that only scans for sequential IP-IDs. This was based on the paper *A closer look at IP-ID behavior in the Wild* by Flavia Salutari, Danilo Cicalese, and Dario J. Rossi.
4. **Count Host Command** (ch.sh) - Must be run as sudo. Runs the host command N times and counts unique occurences across different geographical regions. This can assist an analyst in finding anomalous data and help further map an external network.
5. **Detect Source Routing** (ds.sh) - Must be run as sudo. Checks if source routing is turned on (security risk), offers to toggle source routing for user, and displays the users current routing table.
6. **Detect Network Packet Fragmentation** (df.sh) - Must be run as sudo. This script checks MTU size and listens to all interfaces for network packet fragmentation. Fragmentation is a lowish level indicator on it's own, but can help detect IDS evasion.
7. **Banner Grabber** (bg.sh) - Collects banners using nmap for some of the more popular ports.
8. **Detect IIS Lockdown Tool** (di.py) - This script checks a remote server to see if it is an IIS server. If so, a check is done for the IIS Lockdown Tool. The IIS Lockdown Tool is a security tool developed by Microsoft to help secure IIS web servers.
9. **Detect Mod_headers** (dm.py) - This script checks a remote server to see if it is an Apache Server. If so, a check is done for mod_headers. Apache mod_headers is a module for the Apache web server that allows you to modify HTTP request and response headers. This allows a network defender to obfuscate banners if wanted.
10. **Detect Apache ServerSignature/ServerTokens** (da.py) - This script checks the remote server to see if it is an Apache server. If it is, it checks for the "ServerSignature" and "ServerTokens" headers/directives. The "ServerSignature" directive controls whether the server includes a footer line containing the server version number and other information in error messages and directory listings. The "ServerTokens" directive controls the level of detail in the server response headers. A network defender can raise the sensitivity higher than the default to reduce the attack surface. This script checks if the network defender did that.

## Todo
- [o] simple proxy creator script (p/b)
- [ ] http tunelling detection script. See ../res/Detecting HTTP tunneling
- [ ] detect outbound ssh traffic script (b)
- [ ] simple custom vpn script (p/b)
- [ ] IP spoofing detection script. See ../res/detecting ip spoofing and the other one
- [ ] bogon detection script (b)
- [ ] port 53, 445, 161-162, 389, 135, 137-139 enumeration script. make it quiet (p)
- [ ] System Call Table explorer/detector for linux (b)
- [ ] File metadata explorer (p/b)
- [ ] Hidden Form Items Finder for websites (p) 
- [ ] tunnel check script: ack tunneling, icmp tunneling, ssh tunneling
- [ ] create a script that detects virtual routing/hosting
- [ ] create a menu item to run all scripts in main.py along with the option to do it for the same IP; another option to run internal scripts/external scripts
- [ ] check the scripts that ask for ip/url exclusively and consider a check for the other name to check for virtual routing/hosting
- [x] add an output folder check to scripts
- [x] create a menu (main.py) for the application
- [x] create a bash script that detects and toggles source routing
- [x] create a script that tells if packets are being fragmented or not
- [x] banner grabber for several ports at once
- [x] script that detects IIS lockdown tool
- [x] script that detects apache mod headers. This could detect false or off banners
- [x] script that detects and apache2.conf serversignature/server token settings