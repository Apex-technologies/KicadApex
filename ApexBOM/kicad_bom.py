
def main(DataFile):
    import xml.etree.ElementTree as ET
    import re
    
    try :
        XMLFile = open(DataFile)
    except :
        print("\nError: Can't open file :\n" + str(DataFile) + "\n")
        exit()

    # Acquisition du Root du fichier XML
    tree = ET.parse(XMLFile)
    root = tree.getroot()

    # Récupération des Tags XML dans N dictionnaires contenus dans un 1 grand dictionnaire
        
    Components = []
    Iter = 1
    for comp in root[1]:
        component = {}
        component["name"] = comp.get("ref")
        component["comments"] = ""
        component["tolerance"] = ""
        component["manufacturer"] = ""
        component["manufacturer_ref"] = ""
        component["distributor"] = ""
        component["distributor_ref"] = ""
        for param in comp:
            if re.findall("value", param.tag) != []:
                component["designation"] = param.text
            if re.findall("footprint", param.tag) != []:
                try:
                    fp = param.text.split(":")[1]
                except:
                    fp = param.text
                component["footprint"] = fp
            if re.findall("fields", param.tag) != []:
                for fields in param:
                    if re.findall("voltage", fields.get("name").lower()) != []:
                        component["comments"] = fields.text
                    if re.findall("power", fields.get("name").lower()) != []:
                        component["comments"] = fields.text
                    if re.findall("tolerance", fields.get("name").lower()) != []:
                        component["tolerance"] = fields.text
                    if re.findall("manufacturer", fields.get("name").lower()) != []:
                        component["manufacturer"] = fields.text
                    if re.findall("manufacturer_ref", fields.get("name").lower()) != []:
                        component["manufacturer_ref"] = fields.text
        Components.append(component)

    fcsv = open(os.path.splitext(DataFile)[0] + ".csv", mode='w')
    fcsv.write("Name" + ";" + "Reference" + ";" + "Footprint" + ";" + "Comments" + "\n")
    for c in Components:
        fcsv.write(c["name"] + ";" + c["designation"] + ";" + c["footprint"] + ";" + c["comments"] + "\n")
    fcsv.close()

if __name__ == "__main__":
    import os, sys

    if len(sys.argv) < 2:
        print("Error: Not enough arguments")
    else:
        for i in range(1, len(sys.argv)):
            main(sys.argv[i])

    
