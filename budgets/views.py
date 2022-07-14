from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BudgetSerializer
from .models import Budget
#from rest_framework import permissions
#from .permissions import IsOwner

#These codes on comment only works when linked with the authentication app
#when you want to complie this app then remove  the comment tags from the codes

class BudgetListAPIView(ListCreateAPIView):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    #permissions = (permissions.IsAuthenticated,)

    #def perform_create(self, serializer):
        #return serializer.save(owner=self.request.user) 
        

    #def get_queryset(self):
       # return self.queryset.filter(owner=self.request.user)

class BudgetDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    #permissions = (permissions.IsAuthenticated, IsOwner,)
    #lookup_field = 'id'

    #def perform_create(self, serializer):
        #return serializer.save(owner=self.request.user)

    #def get_queryset(self):
        #return self.queryset.filter(owner=self.request.user)