# JTW OnStepX Configuration Files
You will find here the configuration files to build images for your mount.
## Folder Contents

**Debug_image**: builds an image that resets the nvram (reset to factory defaults) and enables debugs. Use this image to help troubleshoot a problem and for support reasons only.

**Manticore_retrofit**: base configuration files for the manticore controller, use these as a base for your own OnStepX mount

**Tridents**: These are the configuration files for the Trident series of mounts, these include the P75, GTR and GTS
**For mounts with encoders:**
*Config-GTR-24b.h* applies to the P75 and GTR / GTS mounts with 24 bit encoders
*Config-GTR-24b.h* applies to the GTR mounts with 26 bit encoders
*Config-P75-23b.h* applies to the P75 mounts with 23 bit encoders
**For mounts without encoders:**
*Config-GTR-Homing.h* applies to GTR / GTS mounts
*Config-P75.h* applies to the P75 base mount

## Compiling OnStepX
Instructions for compiling OnStepX - https://onstep.groups.io/g/main/wiki/32776
