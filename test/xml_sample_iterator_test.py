import xml.etree.ElementTree as ET

tree = ET.parse('sample.xml')
root = tree.getroot()

# This should print
root_name = root.tag
assert root_name == "annotation"

# Nested iteration testing
size = root.find("size")
# print(size.find("width").text)
# print(size.find("height").text)

# iterate nested objects:
for object in root.findall("object"):
    name = object.find("name")
    # print(name)

image_name = root.find("filename").text
print(image_name[-3:])
