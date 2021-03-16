import xmltodict
import json


def xmlToJson(file):
    """ Convertir un archivo XML a JSON
    Parameters
    ----------
    file: xml
        archivo en formato xml
    Returns
    -------
    json
        objeto json convertido
    """
    file_obj = file  # Obtengo el objeto file
    # Leo el archivo y lo convierto en string
    file_str = str(file_obj.read().decode('utf-8'))
    # Obtengo un diccionario a partir del xml
    file_dict = xmltodict.parse(file_str)
    # Convierto el dict en una json string
    json_str = json.dumps(file_dict, indent=2)
    json_obj = json.loads(json_str)  # Convierto la json string en objeto json
    return json_obj
