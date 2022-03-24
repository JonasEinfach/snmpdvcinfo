#!/usr/bin/python3

# -------------------------------------------------#
# Script Name: snmpdvcinfo.py                      #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 10.06.2020                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#


# --------------- M O D U L E S ---------------#

from pysnmp import hlapi  # --> snmp requests

from snmpdvcinfo import cisco # --> import cisco get functions
from snmpdvcinfo import fortinet # --> import forti get functions

from .snmp import get_snmp # --> import global snmp engine


# --------------- G L O B A L   V A R I A B L E S ---------------#

DEBUG = False

# --------------- S N M P   O I D   V A R I A B L E S ---------------#

SNMP_PORT = "161"
OID_GENERAL_DEVICE_INFO = "1.3.6.1.2.1.1.1"
OID_GENERAL_DEVICE_INFO_2 = "1.3.6.1.2.1.1.1.0"

OID_CISCO_MODEL_CAL = "1.3.6.1.2.1.47.1.1.1.1.13.1"
OID_CISCO_MODEL_NX = "1.3.6.1.2.1.47.1.1.1.1.13.10"
OID_CISCO_MODEL_C1000 = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_MODEL_C2960X = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_MODEL_C4900 = "1.3.6.1.2.1.47.1.1.1.1.13.1000"
OID_CISCO_MODEL_C3560 = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_MODEL_C6807_VSS = "1.3.6.1.2.1.47.1.1.1.1.13.1000"

OID_CISCO_VERSION = "1.3.6.1.2.1.1.1.0"
OID_CISCO_VERSION_SW_4500 = "1.3.6.1.2.1.47.1.1.1.1.10.1000"
OID_CISCO_VERSION_SW_3650 = "1.3.6.1.2.1.47.1.1.1.1.10.1000"


# ------------------------------------------------------------------------------
def get_dvc_info(ip,community_string):

    vendor = ""
    dvc_info = get_snmp(ip, [OID_GENERAL_DEVICE_INFO], hlapi.CommunityData(community_string))

    if dvc_info != 0 and dvc_info[OID_GENERAL_DEVICE_INFO] != "": # --> check for snmp error --> every device should have a sys description string
        dvc_info = dvc_info[OID_GENERAL_DEVICE_INFO]

        vendor = get_vendor(dvc_info) # --> get vendor

    else:
        dvc_info = get_snmp(ip, [OID_GENERAL_DEVICE_INFO_2], hlapi.CommunityData(community_string))

        if dvc_info != 0 and dvc_info[OID_GENERAL_DEVICE_INFO_2] != "": # --> check for snmp error --> every device should have a sys description string
            dvc_info = dvc_info[OID_GENERAL_DEVICE_INFO_2]

            vendor = get_vendor(dvc_info) # --> get vendor

    if "Cisco" in vendor:
        return get_dvc_info_cisco(ip,community_string)
    else:
        return "none,none"
# ------------------------------------------------------------------------------
def get_dvc_info_cisco(ip,community_string):

    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        dvc_version = dvc_version[OID_CISCO_VERSION]

        if "NX-OS" in dvc_version: return get_dvc_info_cisco_nx(ip,community_string)
        elif "Catalyst 4500 L3 Switch" in dvc_version: return get_dvc_info_cisco_c4500(ip,community_string)
        elif "C1000" in dvc_version: return get_dvc_info_cisco_c1000(ip,community_string)
        elif "C2960X" in dvc_version: return get_dvc_info_cisco_c2960x(ip,community_string)
        elif "C3560" in dvc_version: return get_dvc_info_cisco_c3560(ip,community_string)
        elif "s6t64" in dvc_version: return get_dvc_info_cisco_c6807(ip,community_string)
        else: return get_dvc_info_cisco_default(ip,community_string)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_nx(ip,community_string): # --> get model and version for cisco nexus devices

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_NX], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_NX] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_NX]
    else: dvc_model="no_device_model"

    return "%s,%s" % (dvc_model,dvc_version)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c4500(ip,community_string): # --> get model and version for cisco C4500 Switches / C4900

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION_SW_4500], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_SW_4500] != "": # --> check for snmp error
        dvc_version = dvc_version[OID_CISCO_VERSION_SW_4500]
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_CAL], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_CAL] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_CAL]

    else: # --> Special for WS-C4900
        dvc_model = get_snmp(ip, [OID_CISCO_MODEL_C4900], hlapi.CommunityData(community_string))
        if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C4900] != "":   # --> check for snmp error
            dvc_model = dvc_model[OID_CISCO_MODEL_C4900]

        else: dvc_model="no_device_model"

    return "%s,%s" % (dvc_model,dvc_version)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c1000(ip,community_string): # --> get model and version for cisco C1000 Switches

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_C1000], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C1000] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_C1000]
    else: dvc_model="no_device_model"

    return "%s,%s" % (dvc_model,dvc_version)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c2960x(ip,community_string): # --> get model and version for cisco C2960x Switches

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_C2960X], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C2960X] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_C2960X]
    else: dvc_model="no_device_model"

    return "%s,%s" % (dvc_model,dvc_version)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c3560(ip,community_string): # --> get model and version for cisco C3560 Switches

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_C3560], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C3560] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_C3560]
    else: dvc_model="no_device_model"

    return "%s,%s" % (dvc_model,dvc_version)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c6807(ip,community_string): # --> get model and version for cisco C6807 Switches and VSS System

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_CAL], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_CAL] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_CAL]

    else:
        # --> get model for vss system
        dvc_model = get_snmp(ip, [OID_CISCO_MODEL_C6807_VSS], hlapi.CommunityData(community_string))

        if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C6807_VSS] != "":  # --> check for snmp error
            dvc_model = dvc_model[OID_CISCO_MODEL_C6807_VSS]
        else:
            dvc_model="no_device_model"

    return "%s,%s" % (dvc_model, dvc_version)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_default(ip,community_string): # --> get model and version for cisco catalyst Switches / router --> default snmp getter

    # --> get version
    dvc_version = get_snmp(ip, [OID_CISCO_VERSION], hlapi.CommunityData(community_string))

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = get_snmp(ip, [OID_CISCO_MODEL_CAL], hlapi.CommunityData(community_string))

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_CAL] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_CAL]
    else: dvc_model="no_device_model"

    if "C3650" in dvc_model: # --> special for C3650
        dvc_version = get_snmp(ip, [OID_CISCO_VERSION_SW_3650], hlapi.CommunityData(community_string))
        if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_SW_3650] != "":  # --> check for snmp error
            dvc_version = dvc_version[OID_CISCO_VERSION_SW_3650]
        else: dvc_version = "no_device_version"

    return "%s,%s" % (dvc_model,dvc_version)
# ------------------------------------------------------------------------------
def get_vendor(dvc_info):

    if "Cisco" in dvc_info:
        return "Cisco"

    return "no_vendor_info"
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
