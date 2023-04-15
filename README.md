# Cloudy Rabbit
> v. 20230415

> author: southwickio

<br>

## Overview
Simple reconnaissance and threat hunting toolbox. This project is meant to be run on Linux.

## Description
This collection of standalone scripts was written with the intent to gather data for some specific cybersecurity and threat hunting use cases. These scripts are quick 'n' dirty and cover some standalone tasks I wasn't able to find in the wild or wanted to create my own or wanted to learn about. This toolbox covers diverse areas of reconnaissance and the standalone scripts aren't related to each other outside of falling under the reconnaissance phase of an engagement.

## Dependencies
1. Python (>=3.8)
2. Ubuntu (>=20.04) or relevant distro.
3. scapy (`sudo pip3 install scapy`). Used in several scripts and must be installed as sudo for those scripts to work.
4. ifconfig (`sudo apt install net-tools`). Used in df.sh to request information from interfaces.
5. nmap (`sudo apt install nmap`). Used in several scripts for port scanning.
6. enum4linux (from https://github.com/CiscoCXSecurity/). Used in ep.sh to enumerate open ports that are passed to it.
7. smbclient (`sudo apt install smbclient`) Used in enum4linux for enumeration.

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
11. **Sniff for HTTP Tunneling** (st.py) - Must be run as sudo. This script looks for over a dozen different indicators of potential HTTP tunelling by running a check on each port 80 and 443 packet. Custom ports are also considered in the script.
12. **Detect IP Spoofing** (ip.py) - Must be run as sudo. This script looks for potential IP spoofing by crafting, and sending, a SYN/ACK packet that advertizes a window size of 0. No communications are possible with a window size of 0, so if a suspicious IP responds to that SYN/ACK, it is a good indication that the IP is being spoofed. The window size on packets from A to B indicate how much buffer space is available on A for receiving packets. So when B receives a packet with window size 1, it would tell B how many bytes it is allowed to send to A before getting a response.
13. **Detect Bogon Traffic** (db.py) - Must be run as sudo. This script looks for bogon traffic coming in from the internet. This is a huge sign of spoofing or something malicious. Bogon networks are IP addresses or ranges of IP addresses that have not been allocated or assigned to any organization or user, and thus are not supposed to be used in the public internet. They are typically blocked by network administrators to prevent traffic from those networks from entering or leaving the network.
14. **Enumerate Ports** (ep.sh) - This script checks if ports 53, 445, 161-162, 389, 135, 137-139 are open with nmap and then enum4linux performs simple enumeration. This is meant to have Microsoft targets.

## Todo
- [ ] System Call Table explorer/detector for linux (b)
- [ ] File metadata explorer (b)
- [ ] Hidden Form Items Finder for websites (p) 
- [ ] detect ack tunneling script (p)
- [ ] detect icmp tunneling script (p)
- [ ] create a script that detects virtual routing/hosting (b)

- [ ] create a menu item to run all scripts in main.py along with the option to do it for the same IP; another option to run internal scripts/external scripts
- [ ] check the scripts that ask for ip/url exclusively and consider a check for the other name to check for virtual routing/hosting