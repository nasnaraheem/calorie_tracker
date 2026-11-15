from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializer import UserSeralizer
from rest_framework.response import Response

# Create your views here.
class SignUpView(APIView):
     
     def post(self,request):
          form_data=request.data
          serializer_instance=UserSeralizer(data=form_data)

          if serializer_instance.is_valid():
               serializer_instance.save()
               return Response(serializer_instance.data)
          else:
               return Response(serializer_instance.errors)

