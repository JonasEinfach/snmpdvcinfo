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

# --> Cisco Default
OID_CISCO_MODEL_SW_CAL = "1.3.6.1.2.1.47.1.1.1.1.13.1"
OID_CISCO_VERSION_DEFAULT = "1.3.6.1.2.1.1.1.0"
OID_CISCO_SN_DEFAULT = "1.3.6.1.2.1.47.1.1.1.1.11.1"

# --> Cisco Nexus
OID_CISCO_MODEL_SW_NX = "1.3.6.1.2.1.47.1.1.1.1.13.10"
OID_CISCO_SN_SW_NX = "1.3.6.1.2.1.47.1.1.1.1.11.10"

# --> Cisco C1000
OID_CISCO_MODEL_SW_C1000 = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_SN_SW_C1000 = "1.3.6.1.2.1.47.1.1.1.1.11.1001"

# --> Cisco C2960X
OID_CISCO_MODEL_SW_C2960X = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_SN_SW_C2960X = "1.3.6.1.2.1.47.1.1.1.1.11.1001"

# --> Cisco C4500 & C4900
OID_CISCO_MODEL_SW_C4500_VSS = "1.3.6.1.2.1.47.1.1.1.1.13.2"
OID_CISCO_VERSION_SW_C4500 = "1.3.6.1.2.1.47.1.1.1.1.10.1000"
OID_CISCO_SN_SW_C4500 = "1.3.6.1.2.1.47.1.1.1.1.11.1"
OID_CISCO_SN_SW_C4500_VSS_1 = "1.3.6.1.2.1.47.1.1.1.1.11.2"
OID_CISCO_SN_SW_C4500_VSS_2 = "1.3.6.1.2.1.47.1.1.1.1.11.500"
OID_CISCO_MODEL_SW_C4900 = "1.3.6.1.2.1.47.1.1.1.1.13.1000"
OID_CISCO_SN_SW_C4900 = ""

# --> Cisco C3560
OID_CISCO_MODEL_SW_C3560 = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_SN_SW_C3560 = "1.3.6.1.2.1.47.1.1.1.1.11.1001"

# --> Cisco C2960C
OID_CISCO_MODEL_SW_C2960C = "1.3.6.1.2.1.47.1.1.1.1.2.1001"
OID_CISCO_SN_SW_C2960C = "1.3.6.1.2.1.47.1.1.1.1.11.1001"

# --> Cisco C6807
OID_CISCO_MODEL_SW_C6807_VSS = "1.3.6.1.2.1.47.1.1.1.1.13.1000"
OID_CISCO_SN_SW_C6807_VSS_1 = "1.3.6.1.2.1.47.1.1.1.1.11.1000"
OID_CISCO_SN_SW_C6807_VSS_2 = "1.3.6.1.2.1.47.1.1.1.1.11.2000"
OID_CISCO_SN_SW_C6807 = "1.3.6.1.2.1.47.1.1.1.1.11.1"

# --> Cisco C3650
OID_CISCO_VERSION_SW_C3650 = "1.3.6.1.2.1.47.1.1.1.1.10.1000"
OID_CISCO_SN_SW_C3650 = "1.3.6.1.2.1.47.1.1.1.1.11.1"

# --------------- F U N C T I O N S ---------------#

# ------------------------------------------------------------------------------
# CISCO NEXUS
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_nx(ip,community_string): # --> get model and version for cisco nexus devices
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_NX], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_NX] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_NX]

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_NX], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_NX] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_NX]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO C4500 Switches / C4900
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c4500(ip,community_string): # --> get model and version for cisco C4500 Switches / C4900
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_SW_C4500], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_SW_C4500] != "": # --> check for snmp error
        final_dvc_version = dvc_version[OID_CISCO_VERSION_SW_C4500]

    # --> get model for default C4500 standalone
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_CAL], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_CAL] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_CAL]
        
        # --> get sn for default C4500 standalone
        dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C4500], community_string)

        if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C4500] != "": # --> check for snmp error
            final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C4500] # --> extract Version aus Dict

    else: # --> get model for C4500 vss 
        
        dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C4500_VSS], community_string)

        if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C4500_VSS] != "":   # --> check for snmp error
            final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C4500_VSS]
            
            # --> get sn for vss 1 & 2
            dvc_sn_1 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C4500_VSS_1], community_string)
            dvc_sn_2 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C4500_VSS_2], community_string)
            
            if dvc_sn_1 != 0 and dvc_sn_1[OID_CISCO_SN_SW_C4500_VSS_1] != "": # --> check for snmp error
                dvc_sn_1 = dvc_sn_1[OID_CISCO_SN_SW_C4500_VSS_1] # --> extract SN aus Dict
                
            if dvc_sn_2 != 0 and dvc_sn_2[OID_CISCO_SN_SW_C4500_VSS_2] != "": # --> check for snmp error
                dvc_sn_2 = dvc_sn_2[OID_CISCO_SN_SW_C4500_VSS_2] # --> extract SN aus Dict
                final_dvc_sn = "VSS1:%s_VSS2:%s" %(dvc_sn_1,dvc_sn_2)
            
        else: # --> Special for WS-C4900
            dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C4900], community_string)
            if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C4900] != "":   # --> check for snmp error
                final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C4900]
                
            # --> get sn for default C4900
            dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_DEFAULT], community_string)

            if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_DEFAULT] != "": # --> check for snmp error
                # --> extract Version aus Dict
                final_dvc_sn = dvc_sn[OID_CISCO_SN_DEFAULT]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO C1000 Switches
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c1000(ip,community_string): # --> get model and version for cisco C1000 Switches
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C1000], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C1000] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C1000]

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C1000], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C1000] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C1000]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO C2960X Switches
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c2960x(ip,community_string): # --> get model and version for cisco C2960x Switches
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C2960X], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C2960X] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C2960X]

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C2960X], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C2960X] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C2960X]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO C3560 Switches
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c3560(ip,community_string): # --> get model and version for cisco C3560 Switches
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C3560], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C3560] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C3560]

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C3560], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C3560] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C3560]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO C2960C Switches
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c2960c(ip,community_string):
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C2960C], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C2960C] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C2960C]

    # --> get sn
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C2960C], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C2960C] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C2960C]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO C6807 & C6807 VSS Switches
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_c6807(ip,community_string): # --> get model and version for cisco C6807 Switches and VSS System
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_CAL], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_CAL] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_CAL]
        
        # --> get sn for standalone 6807
        dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C6807], community_string)

        if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C6807] != "": # --> check for snmp error
            # --> extract Version aus Dict
            final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C6807]

    else:
        # --> get model for vss system
        dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_C6807_VSS], community_string)

        if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_C6807_VSS] != "":  # --> check for snmp error
            final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_C6807_VSS]
        
            # --> get sn for vss 1 & 2
            dvc_sn_1 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C6807_VSS_1], community_string)
            dvc_sn_2 = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C6807_VSS_2], community_string)
            
            if dvc_sn_1 != 0 and dvc_sn_1[OID_CISCO_SN_SW_C6807_VSS_1] != "": # --> check for snmp error
                # --> extract SN aus Dict
                dvc_sn_1 = dvc_sn_1[OID_CISCO_SN_SW_C6807_VSS_1]
                
            if dvc_sn_2 != 0 and dvc_sn_2[OID_CISCO_SN_SW_C6807_VSS_2] != "": # --> check for snmp error
                # --> extract SN aus Dict
                dvc_sn_2 = dvc_sn_2[OID_CISCO_SN_SW_C6807_VSS_2]
                final_dvc_sn = "VSS1:%s_VSS2:%s" %(dvc_sn_1,dvc_sn_2)

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------
# CISCO Default Switches / Router
# ------------------------------------------------------------------------------
def get_dvc_info_cisco_default(ip,community_string): # --> get model, version and sn for cisco catalyst Switches / router --> default snmp getter
    
    final_dvc_vendor = "cisco"
    final_dvc_version = "no_device_version"
    final_dvc_sn = "no_device_sn"
    final_dvc_model="no_device_model"
    
    # --> get version
    dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_DEFAULT], community_string)

    if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        dvc_version = dvc_version[OID_CISCO_VERSION_DEFAULT]
        dvc_version = dvc_version.split(",")  # --> separate at comma
        dvc_version = dvc_version[2]  # --> take 3 peace in dict --> normally the version by cisco snmp
        final_dvc_version = dvc_version.lstrip()  # --> cut space at start

    # --> get model
    dvc_model = snmpdvcinfo.get_snmp(ip, [OID_CISCO_MODEL_SW_CAL], community_string)

    if dvc_model != 0 and dvc_model[OID_CISCO_MODEL_SW_CAL] != "":   # --> check for snmp error
        final_dvc_model = dvc_model[OID_CISCO_MODEL_SW_CAL]

    # --> get sn for default 
    dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_DEFAULT], community_string)

    if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_DEFAULT] != "": # --> check for snmp error
        # --> extract Version aus Dict
        final_dvc_sn = dvc_sn[OID_CISCO_SN_DEFAULT]
        
    if "C3650" in dvc_model: # --> special for C3650
        dvc_version = snmpdvcinfo.get_snmp(ip, [OID_CISCO_VERSION_SW_C3650], community_string)
        if dvc_version != 0 and dvc_version[OID_CISCO_VERSION_SW_C3650] != "":  # --> check for snmp error
            final_dvc_version = dvc_version[OID_CISCO_VERSION_SW_C3650]
            
        # --> get sn for C3650
        dvc_sn = snmpdvcinfo.get_snmp(ip, [OID_CISCO_SN_SW_C3650], community_string)

        if dvc_sn != 0 and dvc_sn[OID_CISCO_SN_SW_C3650] != "": # --> check for snmp error
            # --> extract Version aus Dict
            final_dvc_sn = dvc_sn[OID_CISCO_SN_SW_C3650]

    return "%s,%s,%s,%s" % (final_dvc_vendor,final_dvc_model,final_dvc_version,final_dvc_sn)
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
