import operator
import os
from PIL import Image

class SortCompare:
    def __init__(self, path):
        self.path = path
        self.Parse()
        self.Sort()
    def Parse(self):
        self.list = []
        with open(self.path, "r") as file:
            raw_file = file.readlines()
            for i in range(0, len(raw_file), 4):
                file1 = raw_file[i].replace("\n", "")
                file2 = raw_file[i+1].replace("\n", "")
                ssim = float(raw_file[i+2].split(": ")[-1])
                self.list.append([ssim, file1, file2])
    def Sort(self):
        self.list = sorted(self.list, key=operator.itemgetter(0))

if __name__ == "__main__":
    Sort = SortCompare("./comparison_list")
    for struct in reversed(Sort.list):
        try:
            if not (os.path.isfile(struct[1]) and os.path.isfile(struct[2])):
                continue
#            if struct[0] == 1.0:
#                if os.path.getsize(struct[1]) > os.path.getsize(struct[2]):
#                    os.remove(struct[2])
#                else:
#                    os.remove(struct[1])
            else:
                print struct[0]
                print "1. ", struct[1]
                print "2. ", struct[2]
                Image.open(struct[1]).show()
                Image.open(struct[2]).show()
                while True:
                    inpt = raw_input()
                    if inpt == "1":
                        os.remove(struct[2])
                        break
                    elif inpt == "2":
                        os.remove(struct[1])
                        break
                    elif inpt == "0":
                        break
        except (OSError, IOError), error:
            raw_input(error)
