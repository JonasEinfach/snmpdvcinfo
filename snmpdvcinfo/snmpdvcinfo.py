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
def get_snmp(target, oids, credentials, port=SNMP_PORT, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):

    try:
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *construct_object_types(oids)
        )
        return snmp_fetch(handler, 1)[0]

    except:
        if DEBUG: # --> DEBUG
            # error = "Error in SNMP Get: Target:" + str(target) + " - OID:" + str(oids) + " - port:" + str(port)
            print(error)
        return 0
# ------------------------------------------------------------------------------
def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types
#------------------------------------------------------------------------------
def snmp_fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = snmp_cast(var_bind[1])
                result.append(items)
            else:
                if DEBUG: # --> DEBUG
                    print('Got SNMP error: {0}'.format(error_indication))
        except:
            if DEBUG: # --> DEBUG
                print("SNMP Error")
    return result
#------------------------------------------------------------------------------
def snmp_cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value
#------------------------------------------------------------------------------


#--------------- E N D   S C R I P T ---------------#
