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

## Compiling and uploading OnStepX on linux

This chapter describes how to compile, and flash the firmware from scratch on a linux workstation.

### Preparation

Read the [https://onstep.groups.io/g/main/wiki/32776](Instructions for compiling OnStepX)
and prepare the environment as described.

---
**_NOTE:_**

As the 2.x.x version of the Arduino IDE can be slow, unreliable, and some menu items
referenced in the wiki could be missing completely on linux desktops, it is
recommended to use the latest > 1.8.x version.
---

* Clone the [https://github.com/hjd1964/OnStepX.git](OnStepX repository)
* Clone the [https://github.com/hjd1964/OnStepX-Plugins.git](OnStepX plugins repository)
* Choose and check out the latest release tag
* Apply the Manticore config files (Config.h, and Plugins.config.h)
* Optional: update the values in COnfig.h to match your mount configuration.
  If you skip this step, then later you will have to update it via the `SWS`
* Copy the `website` plugin into the OnStepX source tree, into the
  `src/plugins` directory
* Proceed as described in the instructions.
