import os

from configobj import ConfigObj

from utils.tfrecord_creator import TfRecordWriter

config = ConfigObj(os.path.join("..", "config.ini"))

CLASS_ID_MAP_JSON_PATH = os.path.join(config["CLASS_ID_MAP_JSON_FILE"])

SAMPLE_IMG_DIR = os.path.join(config["TRAINING_IMAGE_FOLDER"])
TFRECORD_OUTPUT_PATH = os.path.join(config["TFRECORD_OUTPUT_FOLDER"])

cwd = os.getcwd()
print(cwd)

# tfCreator = TfRecordCreator(os.path.join(cwd, "sample.xml"))

tfWriter = TfRecordWriter(CLASS_ID_MAP_JSON_PATH, SAMPLE_IMG_DIR, TFRECORD_OUTPUT_PATH)
tfWriter.write_tfrecord()
