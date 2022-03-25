#!/usr/bin/python3

# -------------------------------------------------#
# Script Name: fortinet_main.py                    #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 25.03.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#

# --------------- M O D U L E S ---------------#

import snmpdvcinfo

# --------------- S N M P   O I D   V A R I A B L E S ---------------#

#

# ------------------------------------------------------------------------------
def get_fortinet_main(ip,community_string):

    return snmpdvcinfo.get_dvc_info_fortinet_default(ip,community_string)
# ------------------------------------------------------------------------------

#--------------- E N D   S C R I P T ---------------#
