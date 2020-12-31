
def findFiles(path, lst=[]):
    import os
    import logging as l

    if not os.path.exists(path):
        l.critical("Path " + path + " does not exist!")
        raise Exception()

    if path[len(path)-1] != "/":
        path += "/"

    for obj in os.listdir(path):
        if os.path.isdir(path + obj):
            findFiles(path+obj, lst)
            l.debug("Find dir" + obj)
        else:
            lst.append(path+obj)

    return(lst)

if __name__ == "__main__":
    print(findFiles("C:/dv/ML_crs/logsAndUnits/dataset/origin"))