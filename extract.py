from pathlib import Path
import gzip

path_blacklist = Path("./blacklist.pickle.gz")
path_forward = Path("./forward-dictionary-model-v1.tar.gz")
path_inverse = Path("./inverse-dictionary-model-v1.tar.gz")

with gzip.open(path_blacklist, "rb") as f:
    # Write the contents of the file
    with open("blacklist.pickle", "wb") as f_out:
        f_out.write(f.read())

with gzip.open(path_forward, "rb") as f:
    # Write the contents of the file in a folder
    with open("forward-dictionary-model-v1", "wb") as f_out:
        f_out.write(f.read())

with gzip.open(path_inverse, "rb") as f:
    # Write the contents of the file
    with open("inverse-dictionary-model-v1", "wb") as f_out:
        f_out.write(f.read())