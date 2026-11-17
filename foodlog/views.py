from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from foodlog.models import Foodlog
from rest_framework import authentication,permissions
from rest_framework.response import Response
from foodlog.serializer import FoodlogSerializer
from foodlog.permission import IsOwner
from datetime import datetime
from django.db.models import Sum

# Create your views here.
class FoodlogListCreateView(APIView):

    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
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

class FoodlogRetreiveUpdateDeleteView(APIView):

   #authentication_classes=[authentication.BasicAuthentication]
   authentication_classes=[authentication.TokenAuthentication]
   permission_classes=[IsOwner]

   def get(self,request,pk=None):

      qs=get_object_or_404(Foodlog,id=pk)
      self.check_object_permissions(request,qs)
      serializer_instance=FoodlogSerializer(qs)
      return Response(serializer_instance.data)

   def put(self,request,pk=None):

      instance=get_object_or_404(Foodlog,id=pk)
      self.check_object_permissions(request,instance)

      form_data=request.data
      serializer_instance=FoodlogSerializer(data=form_data,instance=instance)
      if serializer_instance.is_valid():
         serializer_instance.save()
         return Response(serializer_instance.data)
      else:
         return Response(serializer_instance.errors)

   def delete(self,request,pk=None):

      instance=get_object_or_404(Foodlog,id=pk)
      self.check_object_permissions(request,instance)

      instance.delete()
      return Response({"message" : "deleted"})


class FoodlogSummeryView(APIView):

   #authentication_classes=[authentication.BasicAuthentication]
   authentication_classes=[authentication.TokenAuthentication]
   permission_classes=[permissions.IsAuthenticated]

   def get(self,request):

      get_user_calorie=Foodlog.objects.filter(owner=request.user)

      response_data={
         "todays_total" : 0,
         "monthly_total" : 0
      }
      cur_date=datetime.today().date()
      todays_total_calorie=get_user_calorie.filter(created_at__date=cur_date).values("calorie").aggregate(total=Sum("calorie")).get("total")

      response_data["todays_total"]=todays_total_calorie

      cur_month=datetime.today().month
      cur_year=datetime.today().year

      monthly_total_calorie=get_user_calorie.filter(created_at__month=cur_month,created_at__year=cur_year).values("calorie").aggregate(total=Sum("calorie")).get("total")

      response_data["monthly_total"]=monthly_total_calorie

      return Response(response_data)

