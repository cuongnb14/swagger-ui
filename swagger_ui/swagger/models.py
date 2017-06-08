from django.db import models
from model_utils import Choices

METHOD = Choices('post', 'get', 'delete', 'put')
TYPE = Choices('string', 'integer', 'object', 'array')
HTTP_CODE = Choices((200, 'http_200', 200),
                    (202, 'http_202', 202),
                    (400, 'http_400', 400),
                    (401, 'http_401', 401),
                    (403, 'http_403', 403),
                    (404, 'http_404', 404))
AT = Choices('path', 'body')


class Document(models.Model):
    name = models.CharField(max_length=45)
    swagger = models.CharField(max_length=45, default='2.0')
    base_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Info(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True)
    version = models.CharField(max_length=45, default='1.0.0')
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    terms_of_service = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)


class Security(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True)
    key = models.CharField(max_length=45)
    type = models.CharField(choices=TYPE, default=TYPE.string, max_length=45)
    name = models.CharField(max_length=45)
    at = models.CharField(max_length=45)


class Schema(models.Model):
    name = models.CharField(max_length=45)
    type = models.CharField(choices=TYPE, default=TYPE.string, max_length=45)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=45)
    type = models.CharField(choices=TYPE, default=TYPE.string, max_length=45)
    required = models.BooleanField(default=False)
    example = models.CharField(max_length=45, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    key = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    at = models.CharField(choices=AT, default=AT.body, max_length=45)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=45)
    required = models.BooleanField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Path(models.Model):
    path = models.CharField(max_length=255)
    method = models.CharField(choices=METHOD, default=METHOD.get, max_length=45)
    summary = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    schemas = models.ManyToManyField(Schema, related_name='paths', through='PathSchema')
    parameters = models.ManyToManyField(Parameter, related_name='paths', through='PathParameter')

    def __str__(self):
        return '{} {}'.format(self.method, self.path)


class PathSchema(models.Model):
    at = models.CharField(choices=AT, default=AT.body, max_length=45)
    name = models.CharField(max_length=45)
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField()

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    path = models.ForeignKey(Path, models.CASCADE)

    def __str__(self):
        return self.name


class PathParameter(models.Model):
    path = models.ForeignKey(Path, models.CASCADE)
    parameter = models.ForeignKey(Parameter, models.CASCADE)


class PathTag(models.Model):
    path = models.ForeignKey(Path, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)


class Response(models.Model):
    http_code = models.IntegerField(choices=HTTP_CODE, default=HTTP_CODE.http_200)
    description = models.CharField(max_length=255)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
