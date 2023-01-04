# -------------------------------------------------#
# Script Name: cisco_wlc.py                        #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 03.01.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#

# --------------- M O D U L E S ---------------#

import snmpdvcinfo

# --------------- S N M P   O I D   V A R I A B L E S ---------------#

# --> Cisco WLC C9800
OID_CISCO_MODEL_WLC_C9800 = "1.3.6.1.2.1.47.1.1.1.1.13.2"
OID_CISCO_VERSION_WLC_C9800 = "1.3.6.1.2.1.1.1.0"
OID_CISCO_SN_WLC_C9800 = "1.3.6.1.2.1.47.1.1.1.1.11.500"
OID_CISCO_HOSTNAME_WLC_C9800 = "1.3.6.1.2.1.1.5.0"

# --------------- F U N C T I O N S ---------------#

# ------------------------------------------------------------------------------
# CISCO WLC C9800
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c9800(ip,community_string): # --> get model and version for cisco wlc c9800
    
    final_dvc_vendor = "cisco"
    final_dvc_hostname = "no_device_hostname"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version for wlc c9800 
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_WLC_C9800], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_WLC_C9800] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_WLC_C9800]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model for wlc c9800 
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_WLC_C9800], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_WLC_C9800] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_WLC_C9800]

    # --> get sn for wlc c9800  
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_WLC_C9800], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_WLC_C9800] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_WLC_C9800]
    
    # --> get hostname for wlc c9800  
    dvc_hostname = snmpdvcinfo.get_snmp(ip, [OID_CISCO_HOSTNAME_WLC_C9800], community_string)

    if dvc_hostname != 0 and dvc_hostname[OID_CISCO_HOSTNAME_WLC_C9800] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_hostname = dvc_hostname[OID_CISCO_HOSTNAME_WLC_C9800]

    return "%s,%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_hostname,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
