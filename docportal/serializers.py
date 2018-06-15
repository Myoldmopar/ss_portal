from rest_framework import serializers
from docportal.models import DocumentModel, ManufacturedUnitModel, DocumentPermission, UnitPermission
from django.contrib.auth.models import User


class DocumentSerializer(serializers.ModelSerializer):
    doc_type = serializers.CharField(source='get_doc_type_display')

    class Meta:
        model = DocumentModel
        fields = '__all__'


class ManufacturedUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturedUnitModel
        fields = '__all__'


class DocumentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentPermission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UnitPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPermission
        fields = '__all__'
