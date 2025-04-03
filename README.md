## About
The purpose of this repository is to give a starting point and some code examples in Python on what can be done using [Harvesters](https://github.com/genicam/harvesters/) during integration with a [Ranger/Ruler device](https://www.sick.com/se/en/catalog/products/machine-vision-and-identification/machine-vision/ranger3/c/g448354).

Since our GenIStream API does not have Python support, we recommend Harvesters using for integration using Python and a Ranger/Ruler device.

### Version
Currently tested with Harvesters 1.4.2 and Python 3.11.1.

### CTI-file
Get the CTI-file from the SDK, it is located at: `"GenTL producer/x64-release/SICKGigEVisionTL.cti"`. This file is the one you want to load into Harvesters.

## Import an existing icon-image (dat-file)
If you instead want to use existing images saved to disk you can have a look at this article at the support portal (need login):
https://support.sick.com/sick-knowledgebase/article/?code=KA-07788
