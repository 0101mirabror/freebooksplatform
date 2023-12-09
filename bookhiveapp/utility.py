def get_file_size(file_size):
    if file_size < 1024:
        size_text = f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        size_text = f"{file_size / 1024:.2f} KB"
    elif file_size < 1024 * 1024 * 1024:
        size_text = f"{file_size / (1024 * 1024):.2f} MB"
    else:
        size_text = f"{file_size / (1024 * 1024 * 1024):.2f} GB"
    return size_text