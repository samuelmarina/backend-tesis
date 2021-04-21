from firebase_admin import db
from rest_framework.response import Response


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
    try:
        projects_ref = db.reference(url + '/projects')
        projects = projects_ref.get()
        projects.append({
            'name': project_name,
        })
        user_ref = db.reference(url)
        user_ref.update({
            'projects': projects
        })
        return Response(data=projects)
    except:
        return Response(status=500)


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
    return removeProject(url, project_index)


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
    try:
        projects_ref = db.reference(url + '/projects')
        projects_arr = projects_ref.get()
        projects_arr.pop(index)
        user_ref = db.reference(url)
        user_ref.update({
            'projects': projects_arr
        })
        return Response(data=projects_arr)
    except:
        return Response(status=500)


def handleEditProject(data):
    """ Manejar la edición de un proyecto en la
    base de datos

    Parameters
    ----------
    data: json
        diccionario con toda la información de la solicitud

    Returns
    -------
    list
        lista actualizada de todos los proyectos del usuario
    """
    uid = data['user_id']
    user_id = data['user_id']
    project_index = int(data['project_index'])
    project_new_name = data['project_name']
    url = '/users/' + str(uid)
    return editProject(url, project_index, project_new_name)


def editProject(url, projectIndex, projectName):
    """ Editar el nombre de un proyecto en la base
    de datos

    Parameters
    ----------
    url: str
        dirección de la base de datos
    projectIndex: int
        índice del proyecto
    projectName: str
        nuevo nombre del proyecto

    Returns
    -------
    list
        lista actualizada de todos los proyectos del usuario
    """
    try:
        projects_ref = db.reference(url + '/projects/')
        projects = projects_ref.get()
        projects[projectIndex]['name'] = projectName
        user_ref = db.reference(url)
        user_ref.update({
            'projects': projects
        })
        return Response(data=projects)
    except:
        return Response(status=500)
