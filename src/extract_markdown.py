def extract_title(markdown):
    lines = markdown.split("\n")
    header = ""
    for line in lines:
        if line.startswith("# "):
            header = line[2:].strip()
            return header
    raise Exception ("No h1 header found")