from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from crm.models import Employee
from rest_framework import serializers
from rest_framework import authentication,permissions
#serializers for converting query set to native type and vice versa

class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee
        # exclude=("id",)
        fields="__all__"

# Create your views here.
class EmployeesView(ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        #deserialisation(query set to native type)
        serializer=EmployeeSerializer(qs,many=True)

        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs,many=False)
        return Response(data=serializer.data)
        # return Response(data={"result":"specific employee"})
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no data matching found")
        

class EmployeeViewsetView(ModelViewSet):
    serializer_class=EmployeeSerializer
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]        