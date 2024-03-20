import glob, os, pathlib, hashlib, shutil, time, sys
from datetime import datetime

source = sys.argv[3] #"source"
replica = sys.argv[4] #"replica"
logfile = sys.argv[2] #"log.txt"

listSource = {}
listReplica = {}

timeNext = 0
timeIncrease = float(sys.argv[1])


def deleteElement(path):  
    elementType = "NONE"
    if os.path.isfile(path):
        elementType = "FILE"

    if os.path.isdir(path):
        elementType = "DIRECTORY"

    f = open(logfile, "a")
    f.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + "DELETE (" + elementType + "): " + str(path) + "\n")
    f.close() 
    
    print("DELETING: " + path + " (" + elementType + ")")

    if os.path.isfile(path):
        os.remove(path)

    if os.path.isdir(path):
        shutil.rmtree(path)

def copyElement(src, dest):  
    elementType = "NONE"
    if os.path.isfile(src):
        elementType = "FILE"

    if os.path.isdir(src):
        elementType = "DIRECTORY"

    f = open(logfile, "a")
    f.write("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + "COPY (" + elementType + "): " + src + " to " + dest + "\n")
    f.close() 
    
    print("COPYING: " + src + " to " + dest + " (" + elementType + ")")

    
    if os.path.isfile(src):
        shutil.copy(src, dest)


    if os.path.isdir(src):
        shutil.copytree(src, dest)

def hash_file(path):
    if os.path.isdir(path):
        return 0
       
    h = hashlib.sha1()

    with open(path,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()

def sync():
    # print(os.listdir("./source"))
    # print(os.scandir("./source"))
    global listSource
    global listReplica

    # listSource = list(pathlib.Path(source).glob("*"))\
    
    listSource = list(pathlib.Path(source).rglob("*")) #list(pathlib.Path(source).glob("*"))
    listReplica = list(pathlib.Path(replica).rglob("*"))  #list(pathlib.Path(replica).glob("*"))

    # delete unique files from replica folder
    for element in listReplica:
        if(os.path.exists(element)):
            element2 = source + str(element)[len(replica):]

            if(os.path.exists(element2) == False or hash_file(element2) != hash_file(element)):

                deleteElement(str(element))

    for element in listSource:
        if os.path.exists(element):
            element2 = replica + str(element)[len(source):]

            if(os.path.exists(element2) == False):
                
                copyElement(str(element), str(element2))
             
            elif hash_file(element) != hash_file(element2):
                deleteElement(str(element2))
                copyElement(str(element), str(element2))
                
        
# TODO
# arguments -timedelay, -logfile path

while True:
    if(time.time() >= timeNext):
        #print("yes")
        timeNext = time.time() + timeIncrease
        sync()
