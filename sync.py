import glob, os, pathlib, hashlib, shutil, time

source = "source"
replica = "replica"

listSource = {}
listReplica = {}

timeNext = 0
timeIncrease = 10

def deleteElement(path):  
    elementType = "NONE"
    if os.path.isfile(path):
        elementType = "FILE"

    if os.path.isdir(path):
        elementType = "DIRECTORY"

    f = open("log.txt", "a")
    f.write("DELETE (" + elementType + "): " + str(path) + "\n")
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

    f = open("log.txt", "a")
    f.write("COPY (" + elementType + "): " + str(src) + "\n")
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
# log time
# timmingtime.time()

while True:
    if(time.time() >= timeNext):
        #print("yes")
        timeNext = time.time() + timeIncrease
        sync()
