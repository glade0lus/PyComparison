from skimage.measure import compare_ssim as ssim
import cv2
import os

class ImageCompare:
    def __init__(self, path):
        if not os.path.exists("./_cache/"):
            os.mkdir("./_cache/")
        self.path = path
        self.ImageA = self.Get_cache_image(path)
        self.h, self.w = self.ImageA.shape[:2]
        self.dimension = self.h/float(self.w)
    def Compare(self, path):
        if path != self.path:
            ImageB = self.Get_cache_image(path)
            h, w = ImageB.shape[:2]
            dimension = h/float(w)
            if self.dimension == dimension:
                ImageB = cv2.resize(ImageB, (self.w,self.h))
                sim = ssim(self.ImageA, ImageB, multichannel=True)
                with open('comparison_list', "a") as file:
                    file.write("%s\n%s\nSSIM: %.2f\n\n"%(self.path, path, sim))
    def Walk(self, path):
        for directory, dirnames, filenames in os.walk(path):
            if "_cache" in directory:
                continue
            self.Check_cache_path(directory)
            for _file in filenames:
                if _file.split(".")[-1] in ["png", "jpg", "jpeg", "bmp"]:
                    self.Compare("%s/%s"%(directory, _file))
    def Get_new_size(self, w, h):
        if w > h:
            return 64, int(64*h/float(w))
        elif h > w:
            return int(64*w/float(h)), 64
        else:
            return 64, 64
    def Check_cache_path(self, path):
        cache_path = "./_cache/"
        for folder in path.split("/")[1:]:
            cache_path = "%s/%s/"%(cache_path, folder)
            if not os.path.exists(cache_path):
                os.mkdir(cache_path)
    def Get_cache_image(self, path):
        cache_file = "./_cache/"+os.path.normpath(path)
        if not os.path.isfile(cache_file):
            img = cv2.imread(path)
            h, w = img.shape[:2]
            img = cv2.resize(img, self.Get_new_size(w, h))
            cv2.imwrite(cache_file, img)
            return img
        else:
            return cv2.imread(cache_file)

if __name__ == "__main__":
    path = "./"
    
    for directory, dirnames, filenames in os.walk(path):
        if "_cache" in directory:
            continue
        for _file in filenames:
            if _file.split(".")[-1] in ["png", "jpg", "jpeg", "bmp"]:
                Image = ImageCompare("%s/%s"%(directory, _file))
                Image.Walk(path)