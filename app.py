import os

from configobj import ConfigObj

from utils.tfrecord_creator import TfRecordWriter

CONFIG_PATH = os.path.join("config.ini")

config = ConfigObj(CONFIG_PATH)

training_img_folder = config["TRAINING_IMAGE_FOLDER"]
tfrecord_output_folder = config["TFRECORD_OUTPUT_FOLDER"]
class_id_map_json_file = config["CLASS_ID_MAP_JSON_FILE"]

test_partition_percent = float(config["TEST_PARTITION_PERCENTAGE"])
val_partition_percent = float(config["VAL_PARTITION_PERCENTAGE"])
train_partition_percent = float(config["TRAIN_PARTITION_PERCENTAGE"])


def get_path(file_path):
    if file_path[0] == ".":
        # thats a relative path
        return os.path.join(os.getcwd(), file_path)
    else:
        # return absolute path
        return os.path.join(file_path)


SAMPLE_IMG_DIR = os.path.join(get_path(training_img_folder))

TFRECORD_OUTPUT_PATH = os.path.join(get_path(tfrecord_output_folder))
if not os.path.isdir(TFRECORD_OUTPUT_PATH):
    os.mkdir(TFRECORD_OUTPUT_PATH)

CLASS_ID_JSON_PATH = os.path.join(get_path(class_id_map_json_file))
if not os.path.isfile(CLASS_ID_JSON_PATH):
    sample = {"bv_label": 1}
    raise ("class map json file does not exist. Make one like ", str(sample))

os.chdir(SAMPLE_IMG_DIR)
record_writer = TfRecordWriter(CLASS_ID_JSON_PATH, SAMPLE_IMG_DIR, TFRECORD_OUTPUT_PATH, test_partition_percent,
                               val_partition_percent, train_partition_percent)
record_writer.write_tfrecord()
