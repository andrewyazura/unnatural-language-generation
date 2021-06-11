def read_text(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()

    return text
