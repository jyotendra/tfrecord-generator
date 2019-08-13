from PIL import Image
import xml.etree.ElementTree as ET
import os

MAX_WIDTH = 600
MAX_HEIGHT = 600
MAX_PIXELS = MAX_WIDTH * MAX_HEIGHT


def resize_image(img_path, xml_path):
    img = Image.open(img_path)
    folder_path, image_base_name = os.path.split(img_path)
    width, height = img.size
    if MAX_PIXELS < (width * height) :
        h_ratio = float(MAX_HEIGHT / height)
        w_ratio = float(MAX_WIDTH / width)
        ratio = min(h_ratio, w_ratio) or 1
        new_height = int(height * ratio)
        new_width = int(width * ratio)

        print("resizing image from width: ", width, "to width: ", new_width,
              "and from height: ", height, "to new height: ", new_height)

        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for object in root.findall("object"):
            object_class = object.find("name").text
            bndbox = object.find("bndbox")

            xmin = bndbox.find("xmin")
            xmin.text = str(int(float(xmin.text) * ratio))

            xmax = bndbox.find("xmax")
            xmax.text = str(int(float(xmax.text) * ratio))

            ymin = bndbox.find("ymin")
            ymin.text = str(int(float(ymin.text) * ratio))

            ymax = bndbox.find("ymax")
            ymax.text = str(int(float(ymax.text) * ratio))

        current_img_extension = img_path[-3:]

        # if  current_img_extension != "jpg":
        #     # convert image to jpg
        #     rgb_im = img.convert('RGB')
        #     image_base_without_ext = image_base_name.split(".")[0]
        #     new_file_path = os.path.join(folder_path, image_base_without_ext+ ".jpg")
        #     rgb_im.save(new_file_path)
        #     file_name = root.find("filename")
        #     file_name.text = str(new_file_path)

        # else:
        #     img.save(img_path)
        img.save(img_path)
        tree.write(xml_path)

if __name__ == "__main__":
    pass
