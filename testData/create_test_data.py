import os

os.makedirs("test_data", exist_ok=True)

with open("testData/Python-logo-notext.svg.png", "rb") as img:
    data = img.read()

with open("testData/binary.bin", "wb") as f:
    f.write(data)
