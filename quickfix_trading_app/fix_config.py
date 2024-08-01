import xml.etree.ElementTree as ET

def load_field_names(file_path):
    field_names = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Namespace handling
        ns = {'fix': 'http://www.fixprotocol.org/FIX4.4'}
        
        # Iterate over each <field> element
        for field in root.findall('.//field', ns):
            tag = field.get('number')
            name = field.get('name')
            if tag and name:
                field_names[tag] = name
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return field_names

# Load field names from FIX44.xml
FIELD_NAMES = load_field_names('appCode/spec/FIX44.xml')
