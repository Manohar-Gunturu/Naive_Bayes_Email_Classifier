
file_handle = None

def open_trace(filename):
    global file_handle
    if file_handle is not None:
        file_handle.close()
    try:
        file_handle = open(filename, "w")
    except IOError:
        print("File not found or path is incorrect")


def write(line):
    if file_handle is not None:
        file_handle.write(line+"\n")

def close():
    if file_handle is not None:
        file_handle.close()