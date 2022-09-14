from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import PhoneBookSerializer
from .models import PhoneBook


#API

class PhonebookViews(APIView):
    def post(self, request):
        serializer = PhoneBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            item = get_object_or_404(PhoneBook, id=id)
            serializer = PhoneBookSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = PhoneBook.objects.all()
        serializer = PhoneBookSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                
    
    def delete(self, request, id=None):
        if id:
            item = get_object_or_404(PhoneBook, id=id)
            item.delete()
            return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)

        items = PhoneBook.objects.all()
        items.delete()
        return Response({"status": "success", "data": "Items Deleted"}, status=status.HTTP_200_OK)



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
