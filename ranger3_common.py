import time


def print_verbose(msg, verbosity: int, verbosity_level: int = 2):
    """
    Print a message if the verbosity level is high enough.
    :param msg: The message to print
    :param verbosity: The current verbosity level
    :param verbosity_level: The verbosity level required to print the message
    """
    if verbosity >= verbosity_level:
        print(msg)


def read_file(node_map, filename, verbosity=1):
    """
    Read a file from the device.
    :param node_map: The node map of the device
    :param filename: The name of the file to read
    :param verbosity: The verbosity level
    :return: The file contents as a byte array
    """
    node_map.FileSelector.value = filename
    node_map.FileOpenMode.value = 'Read'
    node_map.FileOperationSelector.value = 'Open'
    node_map.FileOperationExecute.execute()

    print_verbose(node_map.FileSelector.value, verbosity)
    print_verbose(node_map.FileOperationStatus.value, verbosity)
    print_verbose(node_map.FileSize.value, verbosity)

    offset = 0
    time.sleep(1)
    result = b''
    hunk_size = 4096
    while offset < node_map.FileSize.value:
        print_verbose(f"Offset = {offset}", verbosity)
        node_map.FileOperationSelector.value = 'Read'
        node_map.FileAccessOffset.value = offset
        node_map.FileAccessLength.value = hunk_size
        node_map.FileOperationExecute.execute()
        time.sleep(1)
        print_verbose(f"length = {node_map.FileAccessLength.value}", verbosity)
        hunk = node_map.FileAccessBuffer.get(node_map.FileOperationResult.value)
        print_verbose(f"hunk = {hunk}", verbosity)
        result += hunk
        offset += hunk_size
    time.sleep(1)
    node_map.FileOperationSelector.value = 'Close'
    node_map.FileOperationExecute.execute()
    time.sleep(1)
    return result


def write_file(node_map, filename, buffer, verbosity=1):
    """
    Write a file to the device.
    :param node_map: The node map of the device
    :param filename: The name of the file to write
    :param buffer: The data to write
    :param verbosity: The verbosity level
    """
    node_map.FileSelector.value = filename
    node_map.FileOpenMode.value = 'Write'
    node_map.FileOperationSelector.value = 'Open'
    node_map.FileOperationExecute.execute()
    print_verbose(f"Writing file: {node_map.FileSelector.value}", verbosity)
    print_verbose(node_map.FileOperationStatus.value, verbosity)

    if not len(buffer) % 4 == 0:
        # Pad to multiple of 4
        b = bytearray(buffer)
        b.extend(bytearray(4 - (len(buffer) % 4)))
        buffer = bytes(b)
    offset = 0
    hunk_size = 4096
    time.sleep(1)
    while offset < len(buffer):
        node_map.FileOperationSelector.value = 'Write'

        node_map.FileAccessOffset.value = offset
        remaining_byte_count = len(buffer) - offset
        bytes_to_write = min(hunk_size, remaining_byte_count)
        print_verbose(f"Offset={offset}", verbosity)
        print_verbose(f"Will write {bytes_to_write} bytes", verbosity)

        node_map.FileAccessLength.value = bytes_to_write
        node_map.FileAccessBuffer.set(buffer[offset: offset + bytes_to_write])
        print_verbose(f"access buffer = {node_map.FileAccessBuffer.get(bytes_to_write)}", verbosity)
        node_map.FileOperationExecute.execute()
        # time.sleep(1)
        offset += node_map.FileAccessLength.value
        if offset % (len(buffer) / 10) < hunk_size:
            print_verbose(f"File transfer progress: {int(100 * offset / len(buffer))}%",
                          verbosity, 1)

    time.sleep(1)
    node_map.FileOperationSelector.value = 'Close'
    node_map.FileOperationExecute.execute()
    time.sleep(1)
