from django.db import models
from django.contrib.auth.models import User


class ManufacturedUnitModel(models.Model):
    name = models.CharField(max_length=100)
    viewers = models.ManyToManyField(User, through='UnitPermission')


class DocumentModel(models.Model):
    name = models.CharField(max_length=100)

    class DocTypeChoices(object):
        Manual = '00'
        ProgressPhoto = '01'
        TestResults = '02'
    DOC_TYPES = (
        (DocTypeChoices.Manual, 'UserManual'),
        (DocTypeChoices.ProgressPhoto, 'ProgressPhotos'),
        (DocTypeChoices.TestResults, 'TestingResults'),
    )
    doc_type = models.CharField(max_length=10, choices=DOC_TYPES, default=DocTypeChoices.Manual)

    unit = models.ForeignKey(ManufacturedUnitModel, null=True, on_delete=models.CASCADE)
    viewers = models.ManyToManyField(User, through='DocumentPermission')
    file = models.FileField(upload_to="docs", null=True)

    def __str__(self):
        return self.name


class DocumentPermission(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(DocumentModel, on_delete=models.CASCADE)
    notes = models.TextField()


class UnitPermission(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(ManufacturedUnitModel, on_delete=models.CASCADE)
    notes = models.TextField()
