from firebase_admin import db


def createNewVersion(data):
    """ Manejar la creación de una nueva versión

    Parameters
    ----------
    data: dict
        diccionario con la información de la solicitud

    Returns
    -------
    list
        lista actualizada con todas las versiones de una 
        arquitectura del usuario
    """
    uid = data['uid']
    version_name = data['version_name']
    ver_index = data['ver_index']
    arc_index = data['arc_index']
    project_index = data['project_index']
    url = '/users/' + uid + '/projects/' + \
        project_index + '/architectures/' + arc_index
    version_ref = db.reference(url + '/versions/' + ver_index)
    version = version_ref.get()
    version['name'] = version_name
    versions_arr_ref = db.reference(url + '/versions/')
    versions_array = versions_arr_ref.get()
    versions_array.append(version)
    arch_ref = db.reference(url)
    arch_ref.update({
        'versions': versions_array
    })
    return versions_array


def handleDeleteVersion(data):
    """ Manejar la eliminación de una versión de la
    base de datos del usuario

    Parameters
    ----------
    data: dict
        diccionario con la información de la solicitud

    Returns
    -------
    list
        lista actualizada con todas las versiones de una 
        arquitectura del usuario
    """
    uid = data['user_id']
    ver_index = int(data['ver_index'])
    arc_index = str(data['arc_index'])
    project_index = str(data['project_index'])
    url = '/users/' + uid + '/projects/' + \
        project_index + '/architectures/' + arc_index
    versions = deleteVersion(url, ver_index)
    return versions


def deleteVersion(url, verIndex):
    """ Eliminar una versión de la base de datos
    del usuario

    Parameters
    ----------
    url: str
        dirección de la base de datos
    verIndex: int
        índice de la versión

    Returns
    -------
    list
        lista actualizada con todas las versiones de una 
        arquitectura del usuario
    """
    version_ref = db.reference(url + '/versions/')
    versions_arr = version_ref.get()
    versions_arr.pop(verIndex)
    arc_ref = db.reference(url)
    arc_ref.update({
        'versions': versions_arr
    })
    return versions_arr
