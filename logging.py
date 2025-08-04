
f = open("log.txt","w+")

def log(*value):
    string = ''
    for i in value:
        string += str(i)
        
    print(string)
    f.write(string)