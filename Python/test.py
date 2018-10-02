import auth as au
import utilities as u

voting = ["JO"]

def doublicates(newM):
    return newM not in voting

print(doublicates("JO"))

i = 0
if not i:
    print(not i == 1)

print("token : ", au.token)


a = "Hallo Darkness my old friend, I've come to talk with you again"
b = u.checkspaces(a)
print(b)
