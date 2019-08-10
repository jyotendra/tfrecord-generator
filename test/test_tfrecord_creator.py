import os

from utils.tfrecord_creator import TfRecordCreator

cwd = os.getcwd()
print(cwd)

tfCreator = TfRecordCreator(os.path.join(cwd, "sample.xml"))
print(tfCreator.create_img_tfrecord())
