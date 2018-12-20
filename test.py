import hashlib

m=hashlib.md5()
m.update(bytes('8a216da866f71d04016706e25f6605d537bdff1a56564f4fa31cdcaf295bfdc320181113095137',encoding="utf-8"))
print(m.hexdigest().upper())