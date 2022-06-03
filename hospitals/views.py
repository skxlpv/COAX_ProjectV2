from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from hospitals.models import Hospitals
from hospitals.serializers import HospitalSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospitals.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]