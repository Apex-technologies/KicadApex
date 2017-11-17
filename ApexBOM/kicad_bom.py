
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
    
    # Standard Fields
    StdFields = ["value", "footprint", "datasheet"]
    
    # Extra Fields
    XtraFields = ["package", "voltage", "power", "tolerance", "manufacturer", "p/n"]

    # Récupération des Tags XML dans N dictionnaires contenus dans un 1 grand dictionnaire
        
    Components = []
    Iter = 1
    for comp in root[1]:
        component = {}
        component["name"] = comp.get("ref")
        component["comments"] = ""
        component["tolerance"] = ""
        component["manufacturer"] = ""
        component["p/n"] = ""
        for param in comp:
            for field in StdFields:
                if re.findall(field, param.tag) != []:
                    component[field] = param.text
            if re.findall("footprint", param.tag) != []:
                try:
                    fp = param.text.split(":")[1]
                except:
                    fp = param.text
                component["footprint"] = fp
            if re.findall("fields", param.tag) != []:
                for pfield in param:
                    for field in XtraFields:
                        if re.findall(field, pfield.get(field).lower()) != []:
                            component[field] = pfield.text
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

    
