from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt

from firebase_admin import credentials, db, initialize_app

from .helpers.proyectos.proyectos import addNewProject, handleRemoveProject, handleEditProject
from .helpers.arquitecturas.arquitecturas import createArchitecture, handleDeleteArchitecture, handleEditArchitecture
from .helpers.versiones.versiones import createNewVersion, handleDeleteVersion, handleEditVersion
from .helpers.elementos.elementos import createElements


cred = credentials.Certificate('./firebase-sdk.json')
initialize_app(cred, {
    'databaseURL': 'https://tesis-406cd-default-rtdb.firebaseio.com/',
})


class Login(APIView):
    def post(self, request, *args, **kwargs):
        """ Solicitud para inicio de sesión de un usuario o 
        crear uno nuevo
        Returns
        -------
        list
            una lista con todos los proyectos del usuario
        """
        token = request.data['token']
        user = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = str(user['userid'])
        try:
            user_ref = db.reference('/users/' + user_id)
            user_ref.update({
                'name': user['name']
            })
            projects_ref = db.reference('/users/' + user_id + '/projects')
            return Response(projects_ref.get())
        except:
            return Response(status=500)


class Proyectos(APIView):
    def post(self, request, *args, **kwargs):
        """ Solicitud para agregar un nuevo proyecto
        a la base de datos del usuario
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario 
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return addNewProject(data)

    def delete(self, request, *args, **kwargs):
        """ Solicitud para eliminar un proyecto
        de la base de datos del usuario
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario 
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return handleRemoveProject(data)

    def put(self, request, *args, **kwargs):
        """ Solicitud para editar el nombre de un
        proyecto en la base de datos
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        projects = handleEditProject(data)
        return Response(projects)


class Arquitecturas(APIView):
    def post(self, request, *args, **kwargs):
        """ Solicitud para agregar una nueva arquitectura
        a la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las arquitecturas de un
            proyecto del usuario
        """
        data = request.data
        return createArchitecture(data)

    def delete(self, request, *args, **kwargs):
        """ Solicitud para eliminar una arquitectura de un 
        proyecto de la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las arquitecturas de un
            proyecto del usuario
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return handleDeleteArchitecture(data)

    def put(self, request, *args, **kwargs):
        """ Solicitud para editar el nombre de una arquitecturas
        de la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las arquitecturas de un
            proyecto del usuario
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return handleEditArchitecture(data)


class Versiones(APIView):
    def post(self, request, *args, **kwargs):
        """ Solicitud para agregar una nueva versión
        a la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las versiones de
            una arquitectura del usuario
        """
        data = request.data
        return createNewVersion(data)

    def delete(self, request, *args, **kwargs):
        """ Solicitud para eliminar una versión de la
        base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las versiones de
            una arquitectura del usuario
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return handleDeleteVersion(data)

    def put(self, request, *args, **kwargs):
        """ Solicitud para editar el nombre de una versión
        de la base de datos del usuario

        Returns
        -------
        list
            una lista actualizada con todas las versiones de
            una arquitectura del usuario
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        return handleEditVersion(data)


class Elementos(APIView):
    def post(self, request, *args, **kwargs):
        """ Solicitud para agregar elementos a la base
        de datos del usuario
        Returns
        -------
        list
            lista actualizada con todos los elementos de una
            versión del usuario
        """
        data = request.data
        elems = createElements(data)
        return Response(elems)
