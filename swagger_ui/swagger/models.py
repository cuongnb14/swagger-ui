from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=45)
    swagger = models.CharField(max_length=45)
    base_path = models.CharField(max_length=255)


class Info(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    version = models.CharField(max_length=45)
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    terms_of_service = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)


class Security(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    key = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    at = models.CharField(max_length=45)


class Schema(models.Model):
    name = models.CharField(max_length=45)
    type = models.CharField(max_length=45)


class Property(models.Model):
    name = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    example = models.CharField(max_length=45, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class Parameter(models.Model):
    key = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    at = models.CharField(max_length=45)
    description = models.TextField(null=True)
    type = models.CharField(max_length=45)
    required = models.BooleanField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class Path(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=45)
    summary = models.CharField(max_length=255)
    description = models.TextField(null=True)

    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class PathSchema(models.Model):
    at = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    description = models.TextField(null=True)
    required = models.BooleanField()

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    path = models.ForeignKey(Path, models.CASCADE)


class PathParameter(models.Model):
    path = models.ForeignKey(Path, models.CASCADE)
    parameter = models.ForeignKey(Parameter, models.CASCADE)


class PathTag(models.Model):
    path = models.ForeignKey(Path, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)
