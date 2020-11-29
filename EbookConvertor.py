#!/usr/bin/env python
# coding: utf-8
import urllib
from selenium import webdriver
import base64
from PIL import Image
import os
import time
import argparse
import sys

def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Command line parser.")
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-u", "--url", help="Ebook URL on Rekhta/Hindwi.", required=True)
    requiredNamed.add_argument("-n", "--name", help="Your output file name. Don't include '.pdf' extension in your file name.", required=True)
    options = parser.parse_args(args)
    return options

options = getOptions()

def create_folder(path_name):
    if not os.path.exists(path_name):
        os.makedirs(path_name)

    return None

# EBOOK_LINK = 'https://www.rekhta.org/ebooks/muhajir-nama-munawwar-rana-ebooks-4/'
# EBOOK_LINK = 'https://www.rekhta.org/ebooks/aas-bashir-badr-ebooks-1'
# EBOOK_NAME = 'aas'
EBOOK_LINK = options.url
EBOOK_NAME = options.name

EBOOK_CONTENT_FOLDER =  os.path.join('./content', EBOOK_NAME)

BROWSER_SCREENSHOT_FOLDER = os.path.join(EBOOK_CONTENT_FOLDER, 'browser-screenshot')
SINGLE_PAGE_FOLDER =  os.path.join(EBOOK_CONTENT_FOLDER, 'single-page-screenshot')
PDF_FOLDER = os.path.join(EBOOK_CONTENT_FOLDER, 'pdf-file')

create_folder(EBOOK_CONTENT_FOLDER)
create_folder(BROWSER_SCREENSHOT_FOLDER)
create_folder(SINGLE_PAGE_FOLDER)
create_folder(PDF_FOLDER)

class EbookToPdfConvertor:
    def __init__(self, ebook_url, ebook_name):
        self.book_name = ebook_name
        self.ebook_url = ebook_url
        self.driver = self.create_driver();
        self.n_pages = int(self.driver.find_element_by_class_name('ebookTotalPageCount').text)

        self.z_fill = len(str(self.n_pages))

    def create_driver(self):
        driver = webdriver.Firefox()
        driver.get(self.ebook_url)
        return driver

    def click_next(self):
        self.driver.find_element_by_class_name("ebookprev").click()

    def simulate_image_capturing(self):
        count = 1
        i = 1

        while True:
            self.driver.execute_script("""
            console.log("hello");

            var element = document.querySelector(".navPopOvelay");
            var element2 = document.querySelector(".navPopupWrap");
            if (element)
                element.parentNode.removeChild(element);
            if(element2)
                element2.parentNode.removeChild(element2);
            """)

            browser_screenshot_path = os.path.join(BROWSER_SCREENSHOT_FOLDER, self.book_name + str(i).zfill(self.z_fill) +".png")
            self.driver.save_screenshot(browser_screenshot_path)

            canvas = self.driver.find_elements_by_css_selector("canvas")
            for ele in canvas[::-1]:
                crop_image_path = os.path.join(SINGLE_PAGE_FOLDER, self.book_name + str(count).zfill(self.z_fill) +".png")
                self.crop_image(browser_screenshot_path, ele.location, ele.size, crop_image_path)
                count +=1

                if count>self.n_pages:
                    break

            if count>self.n_pages:
                    break

            i+=1
            self.click_next()
            time.sleep(2)

        return None

    def crop_image(self, browser_screenshot_path, location, size, crop_image_path):
        x = location['x']
        y = location['y']
        height = location['y']+size['height']
        width = location['x']+size['width']

        imgOpen = Image.open(browser_screenshot_path)
        imgOpen = imgOpen.crop((int(x), int(y), int(width), int(height)))

        imgOpen.save(crop_image_path)

        return None

    def create_pdf(self):
        files = os.listdir(SINGLE_PAGE_FOLDER)
        files.sort()

        images = []

        for file_name in files:
            img = Image.open(os.path.join(SINGLE_PAGE_FOLDER, file_name))
            img = img.convert('RGB')
            images.append(img)

        self.imagelist_to_pdf(images, SINGLE_PAGE_FOLDER, os.path.join(PDF_FOLDER, EBOOK_NAME+'.pdf'))

    def create_pdf2(self, images):
        self.imagelist_to_pdf(images, SINGLE_PAGE_FOLDER, os.path.join(PDF_FOLDER, EBOOK_NAME+'.pdf'))

    def imagelist_to_pdf(self, images, imagelist_folder, pdf_filename):
        image1 = images[0]
        image1.save(pdf_filename, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])


if __name__ == "__main__":
    convertor = EbookToPdfConvertor(EBOOK_LINK, EBOOK_NAME)
    time.sleep(2)
    convertor.simulate_image_capturing()
    convertor.create_pdf()
