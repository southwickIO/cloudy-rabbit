#!/bin/bash

# Array of ports to check
ports=(21 22 23 25 53 80 110 143 443 3389)

# Get the target URL or IP from the user
read -p "Enter a URL or IP address: " target

# Loop through each port and perform banner grabbing with nmap
for port in "${ports[@]}"; do
    # Run nmap to grab the banner for the port
    banner=$(nmap -sV -p $port --script=banner $target | grep -i "Service Info")
    if [ -n "$banner" ]; then
        # Banner found
        echo "Port $port: $banner"
    else
        # No banner found
        echo "Port $port: Not open"
    fi
    # Wait for 1 second before moving on to the next port
    sleep 1
done
