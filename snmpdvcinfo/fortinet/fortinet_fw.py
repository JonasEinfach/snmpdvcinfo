# -------------------------------------------------#
# Script Name: fortinet_fw.py                      #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 25.03.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#

# --------------- M O D U L E S ---------------#

import snmpdvcinfo

# --------------- S N M P   O I D   V A R I A B L E S ---------------#

# --> Fortinet Default
OID_FORTINET_MODEL = "1.3.6.1.2.1.47.1.1.1.1.7.1"
OID_FORTINET_VERSION = "1.3.6.1.2.1.47.1.1.1.1.10.1"
OID_FORTINET_SN = "1.3.6.1.2.1.47.1.1.1.1.11.1"
OID_FORTINET_HOSTNAME = "1.3.6.1.2.1.1.5.0"

# ------------------------------------------------------------------------------
def get_dvc_info_fortinet_default(ip,community_string): # --> get model and version for fortinet devices --> default snmp getter
    
    final_dvc_vendor = "fortinet"
    final_dvc_hostname = "no_device_hostname"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_FORTINET_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_FORTINET_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_FORTINET_VERSION]
        dvc_version = dvc_version.split(" ")  # --> separate at blank
        dvc_version = dvc_version[1]  # --> take 2 peace in dict --> normally the version by fortinet snmp
        final_dvc_version = dvc_version.replace(",", "_")  # --> replace "," to "_"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_FORTINET_MODEL], community_string)

    if dvc_model != 0 and dvc_model[OID_FORTINET_MODEL] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_FORTINET_MODEL]
    
    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_FORTINET_SN], community_string)

    if dvc_sn != 0 and dvc_sn[OID_FORTINET_SN] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_FORTINET_SN]
    
    # --> get hostname for default 
    dvc_hostname = snmpdvcinfo.get_snmp(ip, [OID_FORTINET_HOSTNAME], community_string)

    if dvc_hostname != 0 and dvc_hostname[OID_FORTINET_HOSTNAME] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_hostname = dvc_hostname[OID_FORTINET_HOSTNAME]   
    

    return "%s,%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_hostname,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
