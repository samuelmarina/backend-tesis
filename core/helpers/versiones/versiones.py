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
