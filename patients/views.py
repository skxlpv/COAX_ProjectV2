from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from patients.models import Patient
from patients.serializers import PatientSerializer


class PatientViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    """
     list:
     Get list of articles

     ### Here user get list of articles from hospital, where user belong

     create:
     Create article

     ### Create new article, by giving text, excerpt, text and category. Author and hospital will be taken automatically
     # User must have permission "isWriter"

     read:
     Get article

     ### Get detailed information about specific article by {id}.
     #### You should belong to the hospital, where this article is

     update:
     Update article

     ### User must be original author of article

     partial_update:
     Partially update article

     ### User must be original author of article

     delete:
     Delete article

     ### Delete article, if user is the author of article

     """

    permission_classes = (IsAuthenticated,)
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def get_queryset(self):
        queryset = Patient.objects.all()
        doctor = self.request.query_params.get('doctor')
        if doctor is not None:
            queryset = queryset.filter(doctor__first_name__startswith=doctor) | \
                       queryset.filter(doctor__last_name__startswith=doctor)
        return queryset
