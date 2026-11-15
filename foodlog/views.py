from django.shortcuts import render
from rest_framework.views import APIView
from foodlog.models import Foodlog
from rest_framework import authentication,permissions
from rest_framework.response import Response
from foodlog.serializer import FoodlogSerializer

# Create your views here.
class FoodlogListCreateView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
     
     auth_user=request.user
     qs=Foodlog.objects.filter(owner=auth_user)
     serializer_instance=FoodlogSerializer(qs,many=True)
     return Response(serializer_instance.data)


    def post(self,request):

       form_data=request.data
       auth_user=request.user
       serializer_instance=FoodlogSerializer(data=form_data)
       if serializer_instance.is_valid():
          serializer_instance.save(owner=auth_user)
          return Response(serializer_instance.data)
       else:
          return Response(serializer_instance.errors)
