import time
from PIL import Image
from harvesters.core import Harvester


"""
Script created for demo purpose, to demonstrate what we can use Harvesters for
with a Ranger or Ruler device.
"""

OUTPUT_FOLDER = "c:/tmp/ranger3_demo_images"
BASE_FILE_NAME = "ranger3_demo"
CTI_FILE_PATH = "SICKGigEVisionTL.cti"


def save_image_to_disk(component, file_name):
    if component.data_format == 'Mono8':
        img_buffer = component.data.reshape(component.height, component.width)
        byte_buffer = img_buffer.tobytes()
        img = Image.new("L", img_buffer.T.shape)
        img.frombytes(byte_buffer)
        img.save(f"{OUTPUT_FOLDER}/{file_name}")
    elif component.data_format == 'Coord3D_C16':
        image_buffer = component.data.reshape(component.height, component.width)
        byte_buffer = image_buffer.tobytes()
        img3d = Image.new("I", image_buffer.T.shape)
        img3d.frombytes(byte_buffer, 'raw', "I;16")
        img3d.save(f"{OUTPUT_FOLDER}/{BASE_FILE_NAME}_3d.png")
    else:
        raise Exception(f"Cannot save image {file_name} to disk due to bad data format {component.data_format}")


def main():
    # Create the Harvester instance
    h = Harvester()
    # Load the cti-file
    h.add_file(CTI_FILE_PATH)
    # Update Harvester, this will update the list of devices
    h.update()

    # List available devices
    print("\n### Device List ###")
    print(h.device_info_list)
    print("### Device List ###\n")

    # Connect to the first device in the list
    # The following keys can be used to identify a device:
    # - list_index: item index of the list of :class:`DeviceInfo` objects.
    # - id_: Index of the device information list.
    # - vendor: Vendor name of the target device.
    # - model: Model name of the target device.
    # - tl_type: Transport layer type of the target device.
    # - user_defined_name: User defined name string of the target device.
    # - serial_number: Serial number string of the target device.
    # - version: Version number string of the target device.
    # Note: If list_index is specified that is always used and the other keys
    # are not used, otherwise a combination of the others shall be used to
    # specify an unique device
    with h.create(0) as ia:
        # Get the node map from the device
        node_map = ia.remote_device.node_map

        # Example of setting of parameters
        node_map.AcquisitionMode.value = 'SingleFrame'
        # Chunk mode needs to be disabled for older versions of Harvester
        # node_map.ChunkModeActive.value = False

        # Remember to first set the selector when setting values depending
        # on which selector is currently active.
        node_map.RegionSelector.value = 'Scan3dExtraction1'
        node_map.Height.value = 100
        node_map.RegionSelector.value = 'Region0'
        node_map.ExposureTime.value = 100
        node_map.RegionSelector.value = 'Region1'
        node_map.ExposureTime.value = 100

        # Capture 2D image
        # Set camera in 2D-mode
        node_map.DeviceScanType.value = 'Areascan'
        # Start the acquisition
        ia.start()
        # Fetch the buffers from the camera
        # Can be given more parameters, for example a timeout on how long to
        # wait for a new buffer.
        with ia.fetch() as buffer:
            # Save the 2D-image
            print("Saving 2D-image")
            save_image_to_disk(buffer.payload.components[0], f"{BASE_FILE_NAME}_2d.png")
        ia.stop()

        # Capture 3D image
        node_map.DeviceScanType.value = 'Linescan3D'
        ia.start()
        # Fetch data from the image
        with ia.fetch() as buffer:
            print("Saving 3D-images")
            # Save 3D image
            save_image_to_disk(buffer.payload.components[0], f"{BASE_FILE_NAME}_3d.png")
            # Save reflectance
            save_image_to_disk(buffer.payload.components[1], f"{BASE_FILE_NAME}_refl.png")
        ia.stop()


if __name__ == "__main__":
    # execute only if run as a script
    main()
