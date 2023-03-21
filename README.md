# Cloudy Rabbit
> v. 20230321

> author: southwickio

<br>

## Overview
Simple reconnaissance and threat hunting toolbox.

## Description
This collection of scripts was written with the intent to gather data for cybersecurity and threat hunting use cases. These scripts are quick 'n' dirty and cover some standalone tasks I wasn't able to find in the wild. This repo is continuously under development as new scripts are added.

## Dependencies
1. Python (>=3.10.6)
2. *nix machine

## Scripts

 1. **Fetch Comments** (fc.py) - This script fetches all HTML comments from a site specified by the user and outputs to STDOUT and ./comments.txt. This can be used from a cybersecurity standpoint as a way to look for any developer comments that made it to production that shouldn't have; such as passwords, keys, or other proprietary information.
 2. **Get Logs** (gl.sh) - This script outputs all `.log` files on a *nix machine. Potential cybersecurity use cases include tracking down a specific log, what applications are running on the machine, and modification dates for DFIR. Run as sudo for different results.

## Installation and Runtime
1. `git clone github.com/southwickIO/cloudy-rabbit`
2. `cd cloudy-rabbit/`
3. `chmod -R u+x cloudy-rabbit/`
4. Run any script with the prefix `./`. For example: `./fc.py` or `./gl.sh`