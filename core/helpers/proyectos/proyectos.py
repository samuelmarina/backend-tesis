from firebase_admin import db


def addNewProject(data):
    """ Agregar un nuevo proyecto a la base de
    datos del usuario
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
