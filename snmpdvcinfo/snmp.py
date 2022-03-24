#!/usr/bin/python3

# -------------------------------------------------#
# Script Name: snmp.py                             #
# -------------------------------------------------#
# Script Author: Jonas Einfach                     #
# Creation Date: 24.03.2022                        #
# -------------------------------------------------#

# --------------- S T A R T   S C R I P T ---------------#

# --------------- M O D U L E S ---------------#

from pysnmp import hlapi # --> snmp requests

# --------------- G L O B A L   V A R I A B L E S ---------------#

SNMP_PORT = "161"

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
