**JTW Trident Firmware**

Standardised firmware for the JTW Trident GTR v2, for earlier models of the GTR or P75 mounts please email us first to check. To download the firmware click the green '<> Code' button and select the 'Download ZIP' option. 

**Instructions**

This repository contains the firmware for all types of Trident mount. The Manticore has two processors, it's necessary to upload OnStepX to the primary processor & the SWS to the secondary processor. Be sure to upload the correct version for the mount. Unzip the entire folder for the uploader as it requires access to the contents of the /bin and /esptool directories. Flash the OnStepX firmware first and then the SWS firmware, following on-screen prompts. 

**Notes**

To keep current settings and only update the firmware do not tick the 'Erase flash before upload' button. In the event that the controller doesn't restart after the final step of flashing the SWS simply flash the OnStepX firmware again. 
