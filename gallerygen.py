import jinja2
import Image
import os, sys
import shutil

def shrunkname(name, size):
    # Fails on file names that have more than 1 dot...
    return name.replace(".",str(size)+".")
    

def shrink(image, size=1920):
    im = Image.open(image)
    if im.size[0] > size:
        newname = shrunkname(image, size)
        im.thumbnail((size,size), Image.ANTIALIAS)
        im.save(newname, "JPEG")
        return newname
    else:
        return image
                


def get_class(num):
    # might be tidier done with a dict?
    if num == 1:
        return "one"
    elif num == 2:
        return "two"
    elif num == 3:
        return "three"
    else:
        return "more"

MAX_WIDTH = 1920 # probably wide enough
class Row:
    def __init__(self, imgs):
        self.cl = get_class(len(imgs))
        self.imgs = [(shrink(img, MAX_WIDTH/len(imgs)), img)
                     for img in imgs]
def main():
    #get image list
    with open(sys.argv[1]) as listf:
        lines = listf.readlines()
    lines = [line.split(",") for line in lines]
    lines = [[img.strip() for img in line] for line in lines]
    #prep images
    rows = [Row(line) for line in lines]
    #render page
    tl = jinja2.FileSystemLoader(searchpath=os.path.dirname(sys.argv[0]))
    tEnv = jinja2.Environment(loader=tl)
    template = tEnv.get_template("gallery.html")
    if len(sys.argv) > 2:
        title = sys.argv[2]
    else:
        title = "Gallery"
    page = template.render({'title':title,
                            'rows':rows})
    if len(sys.argv) > 3:
        out_name = sys.argv[3]
    else:
        out_name = "gallery.html"
    with open(out_name, "w") as outf:
        outf.write(page)
    # copy stylesheet 
    shutil.copy(os.path.join(os.path.dirname(sys.argv[0]),
                             "image.css"),
                ".")
                
    print "Done."

if __name__=="__main__":
    main()
    
