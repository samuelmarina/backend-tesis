from firebase_admin import db
from ...graphManager.manager import getEdgeIds, getNodeIds, manageFiles
from rest_framework.response import Response


def createElements(data):
    """ Manejar la creación de nuevos elementos

    Parameters
    ----------
    data: dict
        diccionario con la información de la solicitud

    Returns
    -------
    dict
        versión con los elementos actualizados
    """
    uid = data['user_id']
    ver_index = data['ver_index']
    arc_index = data['arc_index']
    project_index = data['project_index']
    files = dict(data)['file']
    url = '/users/' + uid + '/projects/' + project_index + \
        '/architectures/' + arc_index + '/versions/' + ver_index
    try:
        ver_data = getNodesAndEdges(url)
    except:
        return Response(status=500)
    else:
        try:
            manageFiles(files, ver_data['nodes'], ver_data['edges'],
                        ver_data['node_set'], ver_data['edge_set'])
        except:
            return Response(status=409)
        else:
            elements = {
                'nodes': ver_data['nodes'],
                'edges': ver_data['edges']
            }
            try:
                new_elems = addNewElements(url, elements)
                return Response(data=new_elems)
            except:
                return Response(status=500)


def getNodesAndEdges(url):
    """ Obtener los arreglos y sets de los nodos y 
    las aristas de una versión

    Parameters
    ----------
    url: str
        dirección de la base de datos

    Returns
    -------
    dict
        diccionario con los arreglos y sets
    """
    elems_ref = db.reference(url + '/elements')
    elements = elems_ref.get()
    nodes = elements['nodes']
    edges = []
    if 'edges' in elements:
        edges = elements['edges']
    node_set = getNodeIds(nodes)
    edge_set = getEdgeIds(edges)
    return {
        'nodes': nodes,
        'edges': edges,
        'node_set': node_set,
        'edge_set': edge_set
    }


def addNewElements(url, elems):
    """ Agregar nuevos elementos a una arquitectura de 
    la base de datos del usuario

    Parameters
    ----------
    url: str
        dirección de la base de datos
    elems: dict
        diccionario con los nodos y aristas

    Returns
    -------
    dict
        versión con los elementos actualizados
    """
    ver_ref = db.reference(url)
    ver_ref.update({
        'elements': elems
    })
    return ver_ref.get()
