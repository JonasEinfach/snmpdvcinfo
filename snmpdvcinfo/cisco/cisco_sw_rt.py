#!/usr/bin/python3

# -------------------------------------------------#
# Script Name: cisco_sw_rt.py                      #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 25.03.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#

# --------------- M O D U L E S ---------------#

import snmpdvcinfo

# --------------- S N M P   O I D   V A R I A B L E S ---------------#

OID_CISCO_MODEL_CAL = "1.3.6.1.2.1.47.1.1.1.1.13.1"
OID_CISCO_MODEL_NX = "1.3.6.1.2.1.47.1.1.1.1.13.10"
OID_CISCO_MODEL_C1000 = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_MODEL_C2960X = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_MODEL_C4900 = "1.3.6.1.2.1.47.1.1.1.1.13.1000"
OID_CISCO_MODEL_C3560 = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_MODEL_C4500_VSS = "1.3.6.1.2.1.47.1.1.1.1.13.2"
OID_CISCO_MODEL_C6807_VSS = "1.3.6.1.2.1.47.1.1.1.1.13.1000"

OID_CISCO_VERSION = "1.3.6.1.2.1.1.1.0"
OID_CISCO_VERSION_SW_4500 = "1.3.6.1.2.1.47.1.1.1.1.10.1000"
OID_CISCO_VERSION_SW_3650 = "1.3.6.1.2.1.47.1.1.1.1.10.1000"

OID_CISCO_SN = "1.3.6.1.2.1.47.1.1.1.1.11.1"
OID_CISCO_SN_SW_C3560 = "1.3.6.1.2.1.47.1.1.1.1.11.1001"
OID_CISCO_SN_SW_C2960X = "1.3.6.1.2.1.47.1.1.1.1.11.1001"
OID_CISCO_SN_SW_NX = "1.3.6.1.2.1.47.1.1.1.1.11.10"
OID_CISCO_SN_SW_C1000 = "1.3.6.1.2.1.47.1.1.1.1.11.1001"
OID_CISCO_SN_SW_C4500 = "1.3.6.1.2.1.47.1.1.1.1.11.1"
OID_CISCO_SN_SW_C4500_VSS_1 = "1.3.6.1.2.1.47.1.1.1.1.11.2"
OID_CISCO_SN_SW_C4500_VSS_2 = "1.3.6.1.2.1.47.1.1.1.1.11.500"
OID_CISCO_SN_SW_C4900 = ""
OID_CISCO_SN_SW_3650 = "1.3.6.1.2.1.47.1.1.1.1.11.1"
OID_CISCO_SN_SW_C6807_VSS_1 = "1.3.6.1.2.1.47.1.1.1.1.11.1000"
OID_CISCO_SN_SW_C6807_VSS_2 = "1.3.6.1.2.1.47.1.1.1.1.11.2000"
OID_CISCO_SN_SW_C6807 = "1.3.6.1.2.1.47.1.1.1.1.11.1"


# ------------------------------------------------------------------------------
def get_dvc_info_cisco_nx(ip,community_string): # --> get model and version for cisco nexus devices

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_NX], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_NX] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_NX]
    else: dvc_model="no_device_model"

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_NX], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_NX] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_sn = dvc_sn[OID_CISCO_SN_SW_NX]
    else: dvc_sn = "no_device_sn"
        
    dvc_vendor = "cisco"

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c4500(ip,community_string): # --> get model and version for cisco C4500 Switches / C4900
    
    dvc_vendor = "cisco"
    dvc_version = "no_device_version"
    dvc_sn = "no_device_sn"
    dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_SW_4500], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_SW_4500] != "": # --> check for snmp error
        dvc_version = dvc_version[OID_CISCO_VERSION_SW_4500]

    # --> get model for default C4500 standalone
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_CAL], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_CAL] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_CAL]
        
        # --> get sn for default C4500 standalone
        dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C4500], community_string)

        if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C4500] != "": # --> check for snmp error
            dvc_sn = dvc_sn[OID_CISCO_SN_SW_C4500] # --> extract Version aus Dict

    else: # --> get model for C4500 vss 
        
        dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_C4500_VSS], community_string)

        if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C4500_VSS] != "":   # --> check for snmp error
            dvc_model = dvc_model[OID_CISCO_MODEL_C4500_VSS]
            
            # --> get sn for vss 1 & 2
            dvc_sn_1 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C4500_VSS_1], community_string)
            dvc_sn_2 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C4500_VSS_2], community_string)
            
            if dvc_sn_1 != 0 and dvc_sn_1[OID_CISCO_SN_SW_C4500_VSS_1] != "": # --> check for snmp error
                dvc_sn_1 = dvc_sn_1[OID_CISCO_SN_SW_C4500_VSS_1] # --> extract SN aus Dict
                
            if dvc_sn_2 != 0 and dvc_sn_2[OID_CISCO_SN_SW_C4500_VSS_2] != "": # --> check for snmp error
                dvc_sn_2 = dvc_sn_2[OID_CISCO_SN_SW_C4500_VSS_2] # --> extract SN aus Dict
                dvc_sn = "VSS1:%s_VSS2:%s" %(dvc_sn_1,dvc_sn_2)
            
        else: # --> Special for WS-C4900
            dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_C4900], community_string)
            if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C4900] != "":   # --> check for snmp error
                dvc_model = dvc_model[OID_CISCO_MODEL_C4900]
                
            # --> get sn for default C4900
            dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN], community_string)

            if dvc_sn != 0 and dvc_sn[OID_CISCO_SN] != "": # --> check for snmp error
                # --> extract Version aus Dict
                dvc_sn = dvc_sn[OID_CISCO_SN]

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c1000(ip,community_string): # --> get model and version for cisco C1000 Switches

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_C1000], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C1000] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_C1000]
    else: dvc_model="no_device_model"

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C1000], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C1000] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_sn = dvc_sn[OID_CISCO_SN_SW_C1000]
    else: dvc_sn = "no_device_sn"

    dvc_vendor = "cisco"

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c2960x(ip,community_string): # --> get model and version for cisco C2960x Switches

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_C2960X], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C2960X] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_C2960X]
    else: dvc_model="no_device_model"

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C2960X], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C2960X] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_sn = dvc_sn[OID_CISCO_SN_SW_C2960X]
    else: dvc_sn = "no_device_sn"

    dvc_vendor = "cisco"

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c3560(ip,community_string): # --> get model and version for cisco C3560 Switches

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_C3560], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C3560] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_C3560]
    else: dvc_model="no_device_model"

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C3560], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C3560] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_sn = dvc_sn[OID_CISCO_SN_SW_C3560]
    else: dvc_sn = "no_device_sn"

    dvc_vendor = "cisco"

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c6807(ip,community_string): # --> get model and version for cisco C6807 Switches and VSS System

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_CAL], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_CAL] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_CAL]
        
        # --> get sn for standalone 6807
        dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C6807], community_string)

        if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C6807] != "": # --> check for snmp error
            # --> extract Version aus Dict
            dvc_sn = dvc_sn[OID_CISCO_SN_SW_C6807]
        else: dvc_sn = "no_device_sn"
        

    else:
        # --> get model for vss system
        dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_C6807_VSS], community_string)

        if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_C6807_VSS] != "":  # --> check for snmp error
            dvc_model = dvc_model[OID_CISCO_MODEL_C6807_VSS]
        
            # --> get sn for vss 1 & 2
            dvc_sn_1 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C6807_VSS_1], community_string)
            dvc_sn_2 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C6807_VSS_2], community_string)
            
            if dvc_sn_1 != 0 and dvc_sn_1[OID_CISCO_SN_SW_C6807_VSS_1] != "": # --> check for snmp error
                # --> extract SN aus Dict
                dvc_sn_1 = dvc_sn_1[OID_CISCO_SN_SW_C6807_VSS_1]
            else: dvc_sn = "no_device_sn"
                
            if dvc_sn_2 != 0 and dvc_sn_2[OID_CISCO_SN_SW_C6807_VSS_2] != "": # --> check for snmp error
                # --> extract SN aus Dict
                dvc_sn_2 = dvc_sn_2[OID_CISCO_SN_SW_C6807_VSS_2]
                dvc_sn = "VSS1:%s_VSS2:%s" %(dvc_sn_1,dvc_sn_2)
            else: dvc_sn = "no_device_sn"
        
        else:
            dvc_model="no_device_model"
            dvc_sn = "no_device_sn"
            
    dvc_vendor = "cisco"

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_default(ip,community_string): # --> get model, version and sn for cisco catalyst Switches / router --> default snmp getter

    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        dvc_version = dvc_version.lstrip()  # --> cut space at start
    else: dvc_version = "no_device_version"

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_CAL], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_CAL] != "":   # --> check for snmp error
        dvc_model = dvc_model[OID_CISCO_MODEL_CAL]
    else: dvc_model="no_device_model"

    # --> get sn for default 
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_sn = dvc_sn[OID_CISCO_SN]
    else: dvc_sn = "no_device_sn"
        
    if "C3650" in dvc_model: # --> special for C3650
        dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_SW_3650], community_string)
        if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_SW_3650] != "":  # --> check for snmp error
            dvc_version = dvc_version[OID_CISCO_VERSION_SW_3650]
        else: dvc_version = "no_device_version"
            
        # --> get sn for C3650
        dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_3650], community_string)

        if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_3650] != "": # --> check for snmp error
            # --> extract Version aus Dict
            dvc_sn = dvc_sn[OID_CISCO_SN_SW_3650]
        else: dvc_sn = "no_device_sn"

    dvc_vendor = "cisco"

    return "%s,%s,%s,%s" % (dvc_vendor,dvc_model,dvc_version,dvc_sn)
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
