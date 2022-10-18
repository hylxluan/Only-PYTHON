def hashFile(path: str):
    from hashlib import sha256
    import re
    import os
    pathReplace = path.replace(os.sep, "/")
    assert os.path.exists(pathReplace)
    hashObj = sha256()
    filePaths = []
    if re.compile(r"^(.+/)(.+[.].+)?").match(pathReplace).group(2) is not None:
        with open(pathReplace, "rb") as absPath:
            while (data_abs := absPath.read(104876)):
                hashObj.update(data_abs)
            return hashObj.hexdigest()
    for root, dirs, files in os.walk(pathReplace):
        for filename in files:
            filePaths += [root + os.sep + filename]
            filePaths = sorted(filePaths)
    for k in filePaths:
        sizePaths = lambda x: x[len(pathReplace + os.sep):].encode()
        hashObj.update(len(sizePaths(k)).to_bytes(2, byteorder="big"))
        hashObj.update(sizePaths(k))
        hashObj.update(os.path.getsize(k).to_bytes(8, byteorder="big"))
        with open(k, "rb") as dirFiles:
            while (data := dirFiles.read(104876)):
                hashObj.update(data)
    return hashObj.hexdigest()
from sys import argv
print("Hash: ", hashFile(argv[1]))