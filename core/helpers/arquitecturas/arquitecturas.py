from firebase_admin import db
from ...graphManager.manager import manageFiles


def createArchitecture(data):
    """ Manejar la creación de una nueva arquitectura

    Parameters
    ----------
    data: dict
        diccionario con la información de la solicitud

    Returns
    -------
    list
        lista actualizada con todas las arquitecturas del usuario
    """
    uid = data['uid']
    name = data['name']
    index = data['index']
    files = dict(data)['file']
    nodes = []
    edges = []
    node_set = set()
    edge_set = set()
    manageFiles(files, nodes, edges, node_set, edge_set)
    elements = {
        'nodes': nodes,
        'edges': edges
    }
    new_arch = {
        'name': name,
        'versions': [
            {
                'name': name + ' - versión inicial',
                'elements': elements
            }
        ]
    }
    architectures = addNewArchitecture(elements, new_arch, index, uid)
    return architectures


def addNewArchitecture(elems, architecture, project_index, uid):
    """ Agregar una nueva arquitectura a la base de datos
    del usuario.

    Parameters
    ----------
    elems: dict
        diccionario con los elementos de la arquitectura
    architecture: dict
        diccionario con la información de la architectura
    project_index: int
        índice del proyecto
    uid: str
        ID del usuario

    Returns
    -------
    list
        lista actualizada con todas las arquitecturas del usuario
    """
    url = '/users/' + uid + '/projects/' + project_index
    arch_ref = db.reference(url + '/architectures')
    architectures = arch_ref.get()
    if architectures is None:
        architectures = []
    architectures.append(architecture)
    project_ref = db.reference(url)
    project_ref.update({
        'architectures': architectures
    })
    return architectures
