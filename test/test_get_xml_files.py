import glob
import os

from configobj import ConfigObj

config = ConfigObj(os.path.join("..", "config.ini"))

SAMPLE_IMG_DIR = os.path.join(config["TRAINING_IMAGE_FOLDER"])
TFRECORD_OUTPUT_PATH = os.path.join(config["TFRECORD_OUTPUT_FOLDER"])

os.chdir(SAMPLE_IMG_DIR)
for file in glob.glob("*.xml"):
    print(file)

# Get list of all the xml files
