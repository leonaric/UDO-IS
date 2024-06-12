import math
num = 23487

def toBinary(number):
    binary = ""
    divnum = number
    while divnum > 1:
        toadd = math.remainder(divnum, 2)
        binary += str(int(abs(toadd)))
        if toadd != 0:
            divnum = (divnum/2) - 0.5
        else:
            divnum = (divnum/2)
    return binary

def toDecimal(binary):
    number = 0
    divbin = binary
    for i in range(len(divbin)):
        val = int(divbin[i]) * (2**i)
        number += val
    return number


realbinary = toBinary(num)
realnum = toDecimal(realbinary)

print(f"{num}\n{realbinary}\n{realnum}")
print(len(realbinary))