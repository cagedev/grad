import lxml.html
import urllib
from urlparse import urljoin
import re
import os
from PIL import Image
import os.path
import sys

class gallery():
    def __init__(self, gal_url,
                 gal_type = "IMG_EMBED",
                 ddir = ".",
                 iuf = "(jpg|png)",
                 minsize=(320,240) ):
        if ddir == ".":
            try:
                self.download_directory = gal_url.split('/')[-1]
            except IndexError:
                print Exception
                self.download_directory = ddir
        self.gallery_url = gal_url
        self.gallery_type = gal_type # HTML_LINKS | IMG_LINKS | IMG_EMBED
        self.image_urls = []
        self.image_url_filter = iuf
        self.downloaded_images = []
        self.minsize = minsize

    def populate_image_list(self):
        if self.gallery_type == "IMG_EMBED":
            tree = lxml.html.parse(self.gallery_url)
            self.image_urls = tree.xpath("//img/@src")
        if self.gallery_type == "IMG_LINKS":
            tree = lxml.html.parse(self.gallery_url)
            self.image_urls = tree.xpath("//a/@href")

    def clean_image_urls(self):
        clean_urls = []
        for url in self.image_urls:
            clean_urls.append(urljoin(self.gallery_url, url))
        self.image_urls = clean_urls

    def filter_image_urls(self):
        filtered_urls = []
        for url in self.image_urls:
            pattern = re.compile(self.image_url_filter)
            if not pattern.search(url) == None:
                filtered_urls.append(url)
        self.image_urls = filtered_urls

    def check_download_dir(self):
        if not os.path.exists(self.download_directory):
            print "[Warning]:",self.download_directory,"No such directory."
            print "  Creating", self.download_directory,"...",
            try:
                os.makedirs(self.download_directory)
            except WindowsError:
                print "[WindowsError]"
                self.download_directory = self.download_directory.split('?')[-1]
                self.check_download_dir()
            except IOError:
                print "Failed!"
            else:
                print "Succes!"
    
    def download_images(self):
        for url in self.image_urls:
            img_file = self.download_directory+"/"+url.split('/')[-1]
            try:
                print "Downloading",url, "to",img_file,"...",
                urllib.urlretrieve(url,
                               self.download_directory+"/"+url.split('/')[-1] )
            except IOError:
                print "[IOError] Failed!"
            else:
                print "Success!"
                self.downloaded_images.append( img_file )

    def clean_downloaded_images(self):
        for img_file in self.downloaded_images:
            try:
                img = Image.open(img_file)
                isz = img.size
                del img
                #print isz, "" ,isz[0]*isz[1]
                if (isz[0]*isz[1] < self.minsize[0]*self.minsize[1]):
                    print "Image",img_file,"too small. Removing...",
                    try:
                        os.remove(img_file)
                    except IOError:
                        print "Error!"
                    else:
                        print "Succes!"
            except IOError:
                print "[IOError]: No such file?"

    def do(self):
        self.populate_image_list()
        ##self.clean_image_urls()
        self.filter_image_urls()
        self.check_download_dir()
        self.download_images()
        print self.downloaded_images
        print self.clean_downloaded_images()


def main():
   
    l = ['']
         
    for u in l:
        gallery( u, gal_type = "IMG_LINKS", minsize=(480,320), ).do()
    return 1

if __name__ == "__main__":
    sys.exit(main())


