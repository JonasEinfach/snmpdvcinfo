#!/usr/bin/python3

# -------------------------------------------------#
# Script Name: main.py                             #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 25.03.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#


# --------------- M O D U L E S ---------------#

import snmpdvcinfo

# --------------- G L O B A L   V A R I A B L E S ---------------#

DEBUG = False

# --------------- S N M P   O I D   V A R I A B L E S ---------------#

OID_GENERAL_DEVICE_INFO = ["1.3.6.1.2.1.1.1","1.3.6.1.2.1.1.1.0","1.3.6.1.2.1.47.1.1.1.1.12.1"] # --> Cisco, Cisco, Forti

# ------------------------------------------------------------------------------
def get_dvc_info(ip,community_string):

    for OID in OID_GENERAL_DEVICE_INFO:

        vendor = ""
        dvc_info = snmpdvcinfo.get_snmp(ip, [OID], community_string)

        if dvc_info != 0 and dvc_info[OID] != "": # --> check for snmp error --> every device should have a sys description string
            dvc_info = dvc_info[OID]

            vendor = get_vendor(dvc_info) # --> get vendor
            if not "no_vendor_info" in vendor:
                break


    if   "Cisco"    in vendor:  return build_dict(snmpdvcinfo.get_cisco_main(ip,community_string))
    elif "Fortinet" in vendor:  return build_dict(snmpdvcinfo.get_fortinet_main(ip,community_string))
    else:                       return build_dict("none,none,none,none,none")
# ------------------------------------------------------------------------------
def get_vendor(dvc_info):

    if "Cisco" in dvc_info: return "Cisco"
    elif "Fortinet" in dvc_info: return "Fortinet"

    return "no_vendor_info"
# ------------------------------------------------------------------------------
def build_dict(dvc_info_return):

    values = dvc_info_return.split(",")
    dvc_dict = {'dvc_vendor' : values[0], 'dvc_hostname' : values[1], 'dvc_model' : values[2], 'dvc_version' : values[3], 'dvc_sn' : values[4]}
    
    return dvc_dict
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
