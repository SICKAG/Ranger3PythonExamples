from pathlib import Path
from harvesters.core import Harvester

import ranger3_common

"""
Script created for demo purpose, to demonstrate how we can read the log from
a Ranger or Ruler device using Harvesters.
"""

OUTPUT_FOLDER = "c:/tmp/ranger3_demo"
CTI_FILE_PATH = "SICKGigEVisionTL.cti"


def main():
    # Create the Harvester instance
    h = Harvester()
    # Load the cti-file
    h.add_file(CTI_FILE_PATH)
    # Update Harvester, this will update the list of devices
    h.update()

    # Connect to the first device.
    with h.create(0) as ia:
        node_map = ia.remote_device.node_map

        # Read the current_log from the device
        currentLog = ranger3_common.read_file(node_map=node_map,
                                              filename='CurrentLog')
        file_path = OUTPUT_FOLDER + '/current-log.txt'
        Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
        # Save the current log to disk
        with open(file_path, 'wb') as f:
            # force file overwrite
            f.write(currentLog)
        print(f"Wrote File current-log.txt to {file_path}")


if __name__ == "__main__":
    # execute only if run as a script
    main()
