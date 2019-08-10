import glob
import json
import math
import os
import random
import xml.etree.ElementTree as ET

import tensorflow as tf

from utils import dataset_util
from utils.json_to_prototxt import ProtoWriter

image_formats = {"jpg": b"jpeg", "jpeg": b"jpeg", "png": b"png"}

'''
The class creates a tfRecord entry ... this does not include writing to file
'''


class TfRecordCreator:
    def __init__(self, xml_path, class_id_map, image_dir):
        self.tree = ET.parse(xml_path)
        self.class_id_map = class_id_map
        self.root = self.tree.getroot()
        self.image_dir = image_dir

    def create_img_tfrecord(self):
        file_name = self.root.find("filename").text
        file_format = file_name[-3:]
        file_path = os.path.join("..", self.image_dir, file_name)
        with tf.gfile.GFile(os.path.join(file_path), 'rb') as fid:
            encoded_jpg = fid.read()
        size = self.root.find("size")
        try:
            img_height = int(size.find("height").text)
        except ValueError:
            img_height = 0

        try:
            img_width = int(size.find("width").text)
        except ValueError:
            img_width = 0

        if not img_height or not img_width:
            return None

        file_name = str.encode(file_name)
        file_format = str.encode(file_format)

        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []

        classes_id = []
        classes_text = []
        encoded_image_data = None  # Encoded image bytes
        try:
            for object in self.root.findall("object"):
                object_class = object.find("name").text
                classes_text.append(str.encode(object_class))

                classes_id.append(int(self.class_id_map[object_class]))

                bndbox = object.find("bndbox")
                xmins.append(int(bndbox.find("xmin").text) / img_width)
                xmaxs.append(int(bndbox.find("xmax").text) / img_width)
                ymins.append(int(bndbox.find("ymin").text) / img_height)
                ymaxs.append(int(bndbox.find("ymax").text) / img_height)

        except Exception as e:
            print(e)

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': dataset_util.int64_feature(img_height),
            'image/width': dataset_util.int64_feature(img_width),
            'image/filename': dataset_util.bytes_feature(file_name),
            'image/source_id': dataset_util.bytes_feature(file_name),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature(file_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes_id)
        }))
        return tf_example


class TfRecordWriter:
    def __init__(self, class_id_json_path, sample_image_path, output_path, test_p=0, val_p=0.3, train_p=0.7):
        self.extension = ".xml"
        self.xml_files = []
        self.records = []
        self.sample_image_path = sample_image_path
        self.output_path = output_path
        self.get_files()
        self.class_id_json_path = class_id_json_path
        self.class_id_json = self.get_dict_from_json(self.class_id_json_path)

        # partition percent
        self.test_p = test_p
        self.val_p = val_p
        self.train_p = train_p

    def get_dict_from_json(self, class_id_json_path):
        with open(class_id_json_path) as json_file:
            data = json.load(json_file)
            return data

    def get_files(self):
        cwd = os.getcwd()
        os.chdir(self.sample_image_path)
        for file in glob.glob("*.xml"):
            self.xml_files.append(os.path.join(self.sample_image_path, file))
        os.chdir(cwd)

    def check_folder_or_create(self, output_path):
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        else:
            # if the folder is present remove sub files
            for the_file in os.listdir(output_path):
                file_path = os.path.join(output_path, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    pass

    def create_output_folders(self, sets):
        for set in sets:
            self.check_folder_or_create(os.path.join(self.output_path, set))

    def write_tfrecord_to_set(self, set_name, set_xml_list):
        if len(set_xml_list) == 0:
            return None
        writer = tf.python_io.TFRecordWriter(os.path.join(self.output_path, set_name, "output.tfrecord"))
        for file in set_xml_list:
            tf_record = TfRecordCreator(file, self.class_id_json, self.sample_image_path).create_img_tfrecord()
            if tf_record is None:
                continue
            writer.write(tf_record.SerializeToString())
            # self.records.append(tf_record)
        writer.close()
        self.write_prototxt(set_name)

    def write_tfrecord(self):
        sets = ['test', 'val', 'train']
        if not (self.train_p + self.val_p + self.test_p == float(1)):
            raise Exception("train_percent + val_percent + test_percent == 1")
        self.create_output_folders(sets)
        random.shuffle(self.xml_files)
        total_files = len(self.xml_files)

        self.write_tfrecord_to_set(sets[0], self.xml_files[0:math.floor(self.test_p * total_files)])
        self.write_tfrecord_to_set(sets[1],
                                   self.xml_files[math.floor(self.test_p * total_files):math.floor(self.val_p * total_files)])
        self.write_tfrecord_to_set(sets[2], self.xml_files[math.floor(self.val_p * total_files):])

    def write_prototxt(self, set_name):
        proto_file_path = os.path.join(self.output_path, set_name)
        # finally create the prototxt file to be used while training
        protowriter = ProtoWriter(self.class_id_json_path, proto_file_path)
        protowriter.write_prototxt()
