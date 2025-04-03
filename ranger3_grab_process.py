from harvesters.core import Harvester
import numpy as np
import matplotlib.pyplot as plt
import os


def reshape_component(component, type=np.uint16):
    h, w = component.height, component.width
    image = component.data.reshape(h, w)

    return np.array(image, dtype=type)


def get_components(buffer):
    """
    Extracts the components from the buffer and reshapes them into numpy arrays.
    :param buffer: The buffer containing the components.
    :return: A dictionary containing the reshaped components.
    """

    # The following keys can be used to identify a component:
    # 3300: Region ID
    # 3301: Component ID

    # Region ID:
    # 11: Extraction region 1
    # 16: Dual Exposure Extraction region
    # 12: Extraction region 2
    # 13: Extraction region 3
    # 14: Extraction region 4
    # 15: Extraction region 5
    # 17: Extraction White
    # 18: Extraction Color

    # Component ID:
    # 1: Intensity (2D)
    # 4: Range
    # 5: Reflectance
    # 7: Scatter
    components = {}
    for component in buffer.payload.components:
        region_id = component._part.get_info_int64(3300)
        component_id = component._part.get_info_int64(3301)

        if region_id == 11:  # Extraction region 1
            if components.get("Scan3dExtraction1") is None:
                components["Scan3dExtraction1"] = {}
            if component_id == 4:  # Ranger
                components["Scan3dExtraction1"]["Range"] = reshape_component(component, np.uint16)
            elif component_id == 5:  # Reflectance
                components["Scan3dExtraction1"]["Reflectance"] = reshape_component(component)
            elif component_id == 7:  # Scatter
                components["Scan3dExtraction1"]["Scatter"] = reshape_component(component)
            else:
                print("Unknown component ID: ", component_id)
        else:
            print("Unknown region ID: ", region_id)

    return components


def main():
    # Create the Harvester instance
    h = Harvester()

    # Load the cti-file
    cti_path = os.path.join(os.path.dirname(__file__), "SICKGigEVisionTL.cti")
    h.add_file(cti_path, check_existence=True, check_validity=True)

    # Update Harvester, this will update the list of devices
    h.update()
    print("Found devices: ", [(device.user_defined_name, device.serial_number) for device in h.device_info_list])

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
    with h.create({"user_defined_name": "ZPM03"}) as ia:

        node_map = ia.remote_device.node_map

        # Set to 3d mode
        node_map.DeviceScanType.value = 'Linescan3D'

        # Start the acquisition
        ia.start()

        # Fetch data from the image
        print("===== Waiting for image =====")
        with ia.fetch() as buffer:
            print("===== Image Aquired =====")
            components = get_components(buffer)
            region1_range = components["Scan3dExtraction1"]["Range"]
            region1_reflectance = components["Scan3dExtraction1"]["Reflectance"]
            region1_scatter = components["Scan3dExtraction1"]["Scatter"]

        ia.stop()

        print("===== Camera Stopped =====")

        # Save the data to numpy files
        np.save("data/region1_range", region1_range)
        np.save("data/region1_reflectance", region1_reflectance)
        np.save("data/region1_scatter", region1_scatter)

        print(region1_reflectance)
        plt.subplot(2, 1, 1)
        plt.imshow(region1_reflectance, interpolation='none')
        plt.subplot(2, 1, 2)
        plt.imshow(region1_range, interpolation='none')
        plt.show()


if __name__ == "__main__":
    main()
