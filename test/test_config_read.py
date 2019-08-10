import os

from configobj import ConfigObj

CONFIG_FILE_PATH = os.path.join("..", "config.ini")

config = ConfigObj(CONFIG_FILE_PATH)

print(config)
