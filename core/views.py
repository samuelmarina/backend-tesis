from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt

from firebase_admin import credentials, db, initialize_app

from .helpers.proyectos.proyectos import addNewProject


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
        user_ref = db.reference('/users/' + user_id)
        user_ref.update({
            'name': user['name']
        })
        projects_ref = db.reference('/users/' + user_id + '/projects')
        return Response(projects_ref.get())


class Proyectos(APIView):
    def post(self, request, *args, **kwargs):
        """ Solicitud para agregar un nuevo nuevo proyecto
        a la base de datos del usuario
        Returns
        -------
        list
            una lista actualizada con todos los proyectos del usuario 
        """
        token = request.data['token']
        data = jwt.decode(token, 'secret', algorithms=["HS256"])
        projects = addNewProject(data)
        return Response(projects)
