#PATHFILE = "Practice/Files/People.txt"
#file = open(PATHFILE, 'r')
#while c := file.read(1):
#    print(c)
#file.close()
#
import sys

PATHFILE = "Lists/List2/Files/Ex1.txt"
try:
    file = open(PATHFILE, "a")
except:
    file = open(PATHFILE, "w")

c = sys.stdin.read(1)
while c != '\n':
    file.write(c)
    c = sys.stdin.read(1)
file.close()