#!/usr/bin/env python3

import os
import re
import sys

BASE_IEEE80211_DIR = '/sys/class/ieee80211/'

# Gather all 802.11 PHY device directory paths
#
# All files in the '/sys/class/ieee80211/' directory are directories,
# each corresponding to a different wireless radio on the system
phy_names = os.listdir(path=BASE_IEEE80211_DIR)

if len(phy_names) == 0:
    print('No WiFi radios detected', file=sys.stderr)
    exit(1)

phys_data = {}
for phy_name in phy_names:
    this_phy_data = {
        'name': phy_name,
        'device_dir': BASE_IEEE80211_DIR + phy_name + '/device/',
        'net_ifs': [],
        'pci_bus': None,
    }
    phys_data[phy_name] = this_phy_data

# Query 'net/' and 'device/' directory subdirectory "driver/" for
# network interfaces using the radio and the PCI bus of the radio, respectively.
#
# The network interfaces using a radio will appear like this, for example:
# '/sys/class/ieee80211/phy0/device/net/wlan0'
#
# The PCI bus of the radio will appear like this, for example:
# '/sys/class/ieee80211/phy0/device/driver/0000:03:00.0'
pci_bus_pattern = re.compile('^[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+.[0-9a-fA-F]')
for phy_name in phys_data:
    phy_data = phys_data[phy_name]

    # Get network interfaces
    phy_data['net_ifs'] = os.listdir(path=phy_data['device_dir'] + 'net/')
    
    # Get PCI bus
    driver_files = os.listdir(path=phy_data['device_dir'] + 'driver/')
    for file_name in driver_files:
        if re.search(pci_bus_pattern, file_name):
            phy_data['pci_bus'] = file_name
            break

# Print out data gathered
print('Found the following WiFi radios:\n')
for phy_name in phys_data:
    phy_data = phys_data[phy_name]

    pci_bus = phy_data['pci_bus'] if phy_data['pci_bus'] else 'NOT FOUND'

    net_ifs_str = ''
    for net_if in phy_data['net_ifs']:
        net_ifs_str = net_if

    print('Name:                 %s' % (phy_name))
    print('PCI Bus:              %s' % (pci_bus))
    print('Network Interface(s): %s' % (net_ifs_str))
    print()