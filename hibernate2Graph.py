import xml.etree.ElementTree as ET

outputFileName = 'outputGraphQL.graphqls'
inputFileName = 'mapping3.xml'

def retrieve_class_name(fully_qualified_name):
    qualified_name = fully_qualified_name.split('.')
    class_name = qualified_name[qualified_name.__len__() - 1]
    if qualified_name.__len__() == 1:
        return class_name.capitalize()
    else:
        return class_name


tree = ET.parse(inputFileName)
root = tree.getroot()
schema = {}
for child in root:
    if child.tag == 'class':
        hibernateClass = child
        className = retrieve_class_name( child.attrib['name'])
        classProperties = {}
        # print('Class: '+className)
        for element in hibernateClass:
            if element.tag == 'id':
                # print(element.attrib['name'], element.attrib['type'])
                classProperties[element.attrib['name']] = 'ID'
            elif element.tag == 'property':
                # print(element.attrib['name'], element.attrib['type'])
                classProperties[element.attrib['name']] = retrieve_class_name(element.attrib.get('type', 'String'))
            elif element.tag == 'one-to-one' or element.tag == 'many-to-one':
                # print(element.attrib['name'], element.attrib['type'])
                classProperties[element.attrib['name']] = retrieve_class_name(element.attrib['class'])
            elif element.tag == 'set' or element.tag == 'set' or element.tag == 'set' or element.tag == 'set' or element.tag == 'array':
                for prop in element:
                    if prop.tag == 'one-to-many':
                        # print(element.attrib['name'], element.attrib['type'])
                        classProperties[element.attrib['name']] = '['+retrieve_class_name(prop.attrib['class'])+']'
        schema[className] = classProperties
outputFile = open (outputFileName, "w");
gqlSchema = ""
for item in schema:
    gqlSchema += 'type '+item+' {\r\n'
    for prop in schema[item]:
        gqlSchema += prop+': '+schema[item][prop]+'\r\n'
    gqlSchema += '}\r\n'
outputFile.write(gqlSchema)
outputFile.close()


'''
    type Employee {
        id: ID
        firstName: String
        lastName: String
        salary: Int
    }
    type Department {
        id: ID
        deptName: String
        location: String
        type: Int
    }
'''

'''
one-to-one - single
many-to-one - single
one-to-many - collection
'''
