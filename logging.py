
f = open("log.txt","w+")

def log(*value):
    for i in value:
        string = str(i)
        print(string)
        f.write(string)