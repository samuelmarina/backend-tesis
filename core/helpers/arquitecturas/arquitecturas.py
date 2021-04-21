from firebase_admin import db
from ...graphManager.manager import manageFiles
from rest_framework.response import Response


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
    try:
        manageFiles(files, nodes, edges, node_set, edge_set)
    except:
        return Response(status=409)
    else:
        if not nodes:
            return Response(data=None, status=406)
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
        try:
            architectures = addNewArchitecture(elements, new_arch, index, uid)
            return Response(data=architectures)
        except:
            return Response(data=None, status=500)


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


def handleDeleteArchitecture(data):
    """ Manejar la eliminación de una arquitectura de
    un proyecto de la base de datos del usuario

    Parameters
    ----------
    data: dict
        diccionario con la información de la solicitud

    Returns
    -------
    list
        lista actualizada con todas las arquitecturas del usuario
    """
    uid = data['user_id']
    project_index = data['project_index']
    arch_index = int(data['arch_index'])
    url = '/users/' + uid + '/projects/' + str(project_index)
    try:
        architectures = deleteArchitecture(url, arch_index)
        return Response(architectures)
    except:
        return Response(data=None, status=500)


def deleteArchitecture(url, archIndex):
    """ Eliminar una arquitectura de la base de datos
    del usuario

    Parameters
    ----------
    url: str
        dirección de la base de datos
    archIndex: int
        índice de la arquitectura

    Returns
    -------
    list
        lista actualizada con todas las arquitecturas del usuario
    """
    arch_ref = db.reference(url + '/architectures')
    arch_arr = arch_ref.get()
    arch_arr.pop(archIndex)
    project_ref = db.reference(url)
    project_ref.update({
        'architectures': arch_arr
    })
    return arch_arr


def handleEditArchitecture(data):
    """ Manejar la edición del nombre de una arquitectura
    de la base de datos del usuario

    Parameters
    ----------
    data: dict
        diccionario con la información de la solicitud

    Returns
    -------
    list
        lista actualizada con todas las arquitecturas del usuario
    """
    uid = data['user_id']
    project_index = data['project_index']
    arch_index = int(data['arch_index'])
    new_arch_name = data['arch_name']
    url = '/users/' + uid + '/projects/' + str(project_index)
    try:
        architectures = editArchitecture(url, arch_index, new_arch_name)
        return Response(data=architectures)
    except:
        return Response(data=None, status=500)


def editArchitecture(url, archIndex, archName):
    """ Editar el nombre de una arquitecturas de la 
    base de datos del usuario 

    Parameters
    ----------
    url: str
        dirección de la base de datos
    archIndex: int
        índice de la arquitectura
    archName: str
        nuevo nombre de la arquitectura

    Returns
    -------
    list
        lista actualizada con todas las arquitecturas del usuario
    """
    arch_ref = db.reference(url + '/architectures')
    arch_arr = arch_ref.get()
    arch_arr[archIndex]['name'] = archName
    project_ref = db.reference(url)
    project_ref.update({
        'architectures': arch_arr
    })
    return arch_arr
