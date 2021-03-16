from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt

from firebase_admin import credentials, db, initialize_app


cred = credentials.Certificate('./firebase-sdk.json')
initialize_app(cred, {
    'databaseURL': 'https://tesis-406cd-default-rtdb.firebaseio.com/',
})


class Login(APIView):
    def post(self, request, *args, **kwargs):
        """ Request to log in an user or create a new one
        Returns
        -------
        list
            a list of all the projects of the user
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
