## What it does
This project creates TfRecord files from LabelImg XML files and split them into sets of three:
1. Test
2. Val
3. Train

.. based on the partition percentage defined in config file.

It also creats a prototxt file from json mapping file label_id_map.json and put one in output folder for each set.

### Note
This project expects image files and their annotations to be in same folder for now.