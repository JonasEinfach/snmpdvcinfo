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

OID_GENERAL_DEVICE_INFO = "1.3.6.1.2.1.1.1"
OID_GENERAL_DEVICE_INFO_2 = "1.3.6.1.2.1.1.1.0"

# ------------------------------------------------------------------------------
def get_dvc_info(ip,community_string):

    vendor = ""
    dvc_info = snmpdvcinfo.get_snmp(ip, [OID_GENERAL_DEVICE_INFO], community_string)

    if dvc_info != 0 and dvc_info[OID_GENERAL_DEVICE_INFO] != "": # --> check for snmp error --> every device should have a sys description string
        dvc_info = dvc_info[OID_GENERAL_DEVICE_INFO]

        vendor = get_vendor(dvc_info) # --> get vendor

    else:
        dvc_info = snmpdvcinfo.get_snmp(ip, [OID_GENERAL_DEVICE_INFO_2], community_string)

        if dvc_info != 0 and dvc_info[OID_GENERAL_DEVICE_INFO_2] != "": # --> check for snmp error --> every device should have a sys description string
            dvc_info = dvc_info[OID_GENERAL_DEVICE_INFO_2]

            vendor = get_vendor(dvc_info) # --> get vendor

    if "Cisco" in vendor:
        return snmpdvcinfo.get_cisco_main(ip,community_string)
    else:
        return "none,none"
# ------------------------------------------------------------------------------
def get_vendor(dvc_info):

    if "Cisco" in dvc_info:
        return "Cisco"

    return "no_vendor_info"
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
