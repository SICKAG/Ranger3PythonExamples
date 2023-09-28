
Currently our Genistrem API does not have Python support. So we recommend using https://github.com/genicam/harvesters/ for integration using Python and a Ranger/Ruler device (https://www.sick.com/se/sv/vision/3d-visionssensor/ranger3/c/g448354). The purpose of this repository is to give a starting point and some examples what can be done using Harvesters during integration with a Ranger/Ruler device.

## Installation

### Harvesters
Currently tested with Harvesters 1.4.2

### CTI-file
Get the CTI-file from the SDK, it is located at: `"GenTL producer/x64-release/SICKGigEVisionTL.cti"`
This file is the one you want to load into Harvesters.