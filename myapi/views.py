from sre_constants import LITERAL
from typing import Literal
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import PhoneBookSerializer
from .models import PhoneBook

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


#API
class PhonebookViews(APIView):
    @swagger_auto_schema(operation_description='POST /api/ - to add phonetitle to phonebook\n JSON body:\n{\n"name": [String name],\n"phone": [String phone_number],\n"email": [String email],\n"title": [String title]\n}', 
    responses={200: 'Contact added successfully', 400: 'Operation error'}, tags=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of your contact'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone of your contact'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of your contact'),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of your contact'),
        }, required=['name', 'phone', 'email', 'title']
    ))
    def post(self, request):
        serializer = PhoneBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="GET /api/ - to get all phonetitles from phonebook\nGET /api/{id} - to get concrete phonetitle by ID from phonebook", responses={200: 'Contact found', 400: 'Contact not found'}, tags=['GET'])
    def get(self, request, id=None):
        if id is None:
            items = PhoneBook.objects.all()
            serializer = PhoneBookSerializer(items, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                
    @swagger_auto_schema(operation_description="DELETE /api/ - to delete all phonetitles from phonebook\nDELETE /api/{id} - to delete concrete phonetitle by ID from phonebook", responses={200: 'Contact(-s) deleted successfully', 400: 'Contact not found'}, tags=['DELETE'])
    def delete(self, request, id=None):
        if id is None:
            items = PhoneBook.objects.all()
            items.delete()
            return Response({"status": "success", "data": "Items Deleted"}, status=status.HTTP_200_OK)


class PhonebookIDViews(APIView):
    @swagger_auto_schema(operation_description="GET /api/ - to get all phonetitles from phonebook\nGET /api/{id} - to get concrete phonetitle by ID from phonebook", responses={200: 'Contact found', 400: 'Contact not found'}, tags=['GET'])
    def get(self, request, id=None):
        if id:
            item = get_object_or_404(PhoneBook, id=id)
            serializer = PhoneBookSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="DELETE /api/ - to delete all phonetitles from phonebook\nDELETE /api/{id} - to delete concrete phonetitle by ID from phonebook", responses={200: 'Contact(-s) deleted successfully', 400: 'Contact not found'}, tags=['DELETE'])
    def delete(self, request, id=None):
        if id:
            item = get_object_or_404(PhoneBook, id=id)
            item.delete()
            return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="PATCH /api/{id} - to patch concrete phonetitle by ID from phonebook", responses={200: 'Contact changed successfully', 204: 'Contact not found', 400: 'Bad Request'},
     tags=['PATCH'], 
     request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of your contact'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone of your contact'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of your contact'),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of your contact'),
        }, required=['name', 'phone', 'email', 'title']
        )
    )
    def patch(self, request, id):
        item = PhoneBook.objects.get(id=id)
        serializer = PhoneBookSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_204_NO_CONTENT)


#Front-client
@csrf_exempt
def createView(request):
    return render(request, 'create.html')


@csrf_exempt
def store(request):
    phonebook = PhoneBook()
    phonebook.name = request.POST.get('name')
    phonebook.email = request.POST.get('email')
    phonebook.phone = request.POST.get('phone')
    phonebook.title = request.POST.get('title')
    phonebook.save()
    messages.success(request, "PhoneTitle Added Successfully")
    return redirect('/create')

@csrf_exempt
def index(request):
    phonebook = PhoneBook.objects.all()
    return render(request, 'index.html',{'phonebook':phonebook})


@csrf_exempt
def viewPT(request, pk):
    phonebook = PhoneBook.objects.get(id = pk)
    return render(request, 'view.html',{'phonebook':phonebook})


@csrf_exempt
def deletePT(request, pk):
    phonebook = PhoneBook.objects.get(id = pk)
    phonebook.delete()
    messages.success(request, "PhoneTitle Deleted Successfully")
    return redirect('/index')


@csrf_exempt
def updatePT(request, pk):
    phonebook = PhoneBook.objects.get(id = pk)
    return render(request,'update.html',{'phonebook':phonebook})

@csrf_exempt
def update(request,pk):
    print('in')
    phonebook = PhoneBook.objects.get(id = pk)
    phonebook.name = request.POST.get('name')
    phonebook.email = request.POST.get('email')
    phonebook.mobile = request.POST.get('mobile')
    phonebook.title = request.POST.get('title')
    phonebook.save()
    messages.success(request, "PhoneTitle Update Successfully")
    return redirect('/index')
