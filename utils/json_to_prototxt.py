import json
import os
from string import Template

from configobj import ConfigObj

CONFIG_PATH = None


def set_config_path(path):
    CONFIG_PATH = path


config = ConfigObj(CONFIG_PATH)

# This line expects a json map file in root which shall have class_name mapped against id. Ex:
# {
#   "bv_dog": 1,
#   "bv_cat": 2
# }


template = Template('item {\n' \
                    '\tname: "$class_name"\n' \
                    '\tid: $class_id\n' \
                    '}')


class ProtoWriter:
    def __init__(self, json_path, output_path, template=template, json_data=None):
        self.json_path = json_path
        self.proto_output_path = os.path.join(output_path, "output.prototxt")
        self.template = template
        self.json_data = self.read_json_data()
        self.protodata = None
        self.create_protofile()

    def read_json_data(self):
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            json_data = data
        return json_data

    def create_protofile(self):
        # delete stale file
        try:
            os.remove(self.proto_output_path)
        except OSError:
            pass

        self.protodata = open(self.proto_output_path, 'wb')

    def write_prototxt(self):
        for item in self.json_data:
            item_template = self.template.substitute(class_name=item, class_id=self.json_data[item])
            item_template = item_template.encode()
            self.protodata.write(item_template)
            self.protodata.write("\n".encode())
        self.protodata.close()
