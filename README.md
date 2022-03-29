# snmpdvcinfo - SNMP Device Information
--> Script for fetching Network Device Information via SNMP (Model, Version, SN)  <br />
--> Cisco support <br />
--> Fortinet Firewall support <br />
<br />
<br />
## Actual supported devices:
-> Cisco: <br />
--> Cisco Nexus <br />
--> Cisco Catalyst 2960X <br />
--> Cisco Catalyst 2960CG <br />
--> Cisco Catalyst 3650 <br />
--> Cisco Catalyst 3560 <br />
--> Cisco Catalyst 4500 Standalone<br />
--> Cisco Catalyst 4500 VSS<br />
--> Cisco Catalyst 1000 <br />
--> Cisco Catalyst 4900 <br />
--> Cisco Catalyst 9000 <br />
--> Cisco Catalyst 6807 Standalone <br />
--> Cisco Catalyst 6807 VSS <br />
<br />
-> Fortinet: --> actual no SN support<br />
--> Fortinet 3000D<br />
--> Fortinet 1500D<br />
--> Fortinet 600E<br />
--> Fortinet 500E<br />
--> Fortinet 300E<br />
<br />
## Usage Examples:
\>>> import snmpdvcinfo <br />
\>>>snmpdvcinfo.get_dvc_info("10.10.10.10","YOUR_SNMP-V2_COMMUNITY_STRING")  <br />
'cisco,C6807XL,Version 15.6(1)SY7,ABSCSJWHD' <br />
<br />
\>>>snmpdvcinfo.get_dvc_info("10.10.10.11","YOUR_SNMP-V2_COMMUNITY_STRING")  <br />
'fortinet,FGT_1500D,v7.8.1,ABSCSJWHX'
<br />
## Error Examples:
<br />
No SNMP Connection possible:<br />
'none,none,none,none'<br />
<br />
Cisco vendor detected but the device isn't supported:<br />
'cisco,no_device_model,no_device_version,no_device_sn'<br />

