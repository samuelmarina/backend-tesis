from firebase_admin import db


def addNewProject(data):
    """ Agregar un nuevo proyecto a la base de
    datos del usuario
    Parameters
    ----------
    data: json
        diccionario con toda la información de la solicitud

    Returns
    -------
    list
        una lista actualizada con todos los proyectos del usuario
    """
    user_id = str(data['user_id'])
    project_name = data['project_name']
    url = '/users/' + user_id
    projects_ref = db.reference(url + '/projects')
    projects = projects_ref.get()
    projects.append({
        'name': project_name,
    })
    user_ref = db.reference(url)
    user_ref.update({
        'projects': projects
    })
    return projects


def handleRemoveProject(data):
    """ Manejar la eliminación de un proyecto de 
    la base de datos del usuario

    Parameters
    ----------
    data: json
        diccionario con toda la información de la solicitud

    Returns
    -------
    list
        una lista actualizada con todos los proyectos del usuario
    """
    user_id = str(data['user_id'])
    project_index = int(data['project_index'])
    url = '/users/' + user_id
    projects = removeProject(url, project_index)
    return projects


def removeProject(url, index):
    """ Eliminar un proyecto de la base de
    datos del usuario

    Parameters
    ----------
    url: str
        dirección de la base de datos
    index: int
        índice del proyecto a eliminar

    Returns
    -------
    list
        lista actualizada de todos los proyectos del usuario
    """
    projects_ref = db.reference(url + '/projects')
    projects_arr = projects_ref.get()
    projects_arr.pop(index)
    user_ref = db.reference(url)
    user_ref.update({
        'projects': projects_arr
    })
    return projects_arr
