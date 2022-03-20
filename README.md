# snmpdvcinfo - SNMP Device Information
--> Script for fetching Device Information via SNMP (Model, Version)  <br />
--> Multivendor support (planned) <br />
<br />
<br />
## Actual supported devices:
--> Cisco Nexus <br />
--> Cisco Catalyst 2960X <br />
--> Cisco Catalyst 3650 <br />
--> Cisco Catalyst 3560 <br />
--> Cisco Catalyst 4500 <br />
--> Cisco Catalyst 1000 <br />
--> Cisco Catalyst 4900 <br />
--> Cisco Catalyst 9000 <br />
--> Cisco Catalyst 6807 <br />
<br />
<br />
## Usage Examples:
>>> import snmpdvcinfo
>>>snmpdvcinfo.get_dvc_info("10.10.10.10","YOUR_SNMP-V2_COMMUNITY_STRING") <br />
'C6807XL','Version 15.6(1)SY7'
