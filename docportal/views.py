from datetime import datetime

from rest_framework import decorators, status, viewsets
from rest_framework.decorators import action
from django.http import JsonResponse
from docportal.serializers import (
    DocumentSerializer, ManufacturedUnitSerializer, DocumentPermissionSerializer,
    UserSerializer, UnitPermissionSerializer
)
from docportal.models import (
    DocumentModel, ManufacturedUnitModel, DocumentPermission, UnitPermission
)
from django.contrib.auth.models import User


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = DocumentModel.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        doc_type = request.data['doc_type']
        unit = request.data['unit']
        unit_instance = ManufacturedUnitModel.objects.get(pk=unit)
        d = DocumentModel(name=name, doc_type=doc_type, unit=unit_instance)
        d.save()
        return JsonResponse({'status': 'success'}, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=False)
    def add_access(self, request):
        user = request.data['user']
        document = request.data['document']
        user_object = User.objects.get(pk=user)
        document_object = DocumentModel.objects.get(pk=document)
        # TODO: Check for already existing relationship before adding another
        DocumentPermission.objects.create(
            viewer=user_object,
            document=document_object,
            notes="Access added through API add_access method, by user: {0}, at {1}".format(
                request.user.username, datetime.today()
            )
        )
        return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)


class ManufacturedUnitViewSet(viewsets.ModelViewSet):
    queryset = ManufacturedUnitModel.objects.all()
    serializer_class = ManufacturedUnitSerializer

    @action(methods=['PUT'], detail=False)
    def add_access(self, request):
        user = request.data['user']
        unit = request.data['unit']
        user_object = User.objects.get(pk=user)
        unit_object = ManufacturedUnitModel.objects.get(pk=unit)
        # TODO: Check for already existing relationship before adding another
        UnitPermission.objects.create(
            viewer=user_object,
            unit=unit_object,
            notes="Access added through API add_access method, by user: {0}, at {1}".format(
                request.user.username, datetime.today()
            )
        )
        return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)


class DocumentPermissionViewSet(viewsets.ModelViewSet):
    queryset = DocumentPermission.objects.all()
    serializer_class = DocumentPermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UnitPermissionViewSet(viewsets.ModelViewSet):
    queryset = UnitPermission.objects.all()
    serializer_class = UnitPermissionSerializer


@decorators.api_view(http_method_names=['GET'])
def test_access(request):
    # current_user_id = request.user.id
    test_access_for_user_id = request.query_params['user']
    document_id_requested = request.query_params['doc']
    document_to_check = DocumentModel.objects.get(pk=document_id_requested)

    # first check if user has direct access
    try:
        document_to_check.viewers.get(pk=test_access_for_user_id)
        return JsonResponse({}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        pass  # for now

    # then if not, check if the user has access to the unit as a whole
    unit_id_for_this_document = document_to_check.unit.id
    unit_object = ManufacturedUnitModel.objects.get(pk=unit_id_for_this_document)
    try:
        unit_object.viewers.get(pk=test_access_for_user_id)
        return JsonResponse({}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        pass  # for now

    # ok, they don't have access
    return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)
