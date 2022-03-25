# snmpdvcinfo - SNMP Device Information
--> Script for fetching Network Device Information via SNMP (Model, Version)  <br />
--> Cisco support <br />
--> Fortinet Firewall support <br />
<br />
<br />
## Actual supported devices:
-> Cisco: <br />
--> Cisco Nexus <br />
--> Cisco Catalyst 2960X <br />
--> Cisco Catalyst 3650 <br />
--> Cisco Catalyst 3560 <br />
--> Cisco Catalyst 4500 <br />
--> Cisco Catalyst 1000 <br />
--> Cisco Catalyst 4900 <br />
--> Cisco Catalyst 9000 <br />
--> Cisco Catalyst 6807 Standalone <br />
--> Cisco Catalyst 6807 VSS <br />
<br />
-> Fortinet: <br />
--> Fortinet 3000D<br />
<br />
## Usage Examples:
\>>> import snmpdvcinfo <br />
\>>>snmpdvcinfo.get_dvc_info("10.10.10.10","YOUR_SNMP-V2_COMMUNITY_STRING")  <br />
'C6807XL','Version 15.6(1)SY7' <br />
