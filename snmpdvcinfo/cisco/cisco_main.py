#!/usr/bin/python3

# -------------------------------------------------#
# Script Name: cisco_main.py                       #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 24.03.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#

# ------------------------------------------------------------------------------
def get_cisco(ip,community_string):

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

#--------------- E N D   S C R I P T ---------------#