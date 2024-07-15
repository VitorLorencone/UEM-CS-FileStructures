import sys

PATHFILE = "Lists/List2/Ex1.txt"
try:
    file = open(PATHFILE, "a")
except:
    file = open(PATHFILE, "w")

c = sys.stdin.read(1)
while c != '\n':
    file.write(c)
    c = sys.stdin.read(1)
file.close()