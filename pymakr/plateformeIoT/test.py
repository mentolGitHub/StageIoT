import struct

floatlist = [5000001.2125496, 3.4, 5.6, 7.8, 9.0]
intlist = [int(x) for x in floatlist]
buf = struct.pack('%sf' % len(floatlist), *floatlist)
#ajouter un entier à la fin
buf += struct.pack('%si' % len(intlist), *intlist)
print(buf)

# unpack
n = len(floatlist)
m = len(intlist)
floatlist = list(struct.unpack('%sf' % n, buf[:4*n]))
intlist = list(struct.unpack('%si' % m, buf[4*n:]))
print(floatlist)
print(intlist)
