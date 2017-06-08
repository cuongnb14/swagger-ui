from django.utils.translation import ugettext as _
from rest_framework import serializers
from . import models


class InfoSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField()

    def get_contact(self, info):
        return {'email': info.contact_email}

    class Meta:
        model = models.Info
        exclude = ('contact_email', 'id', 'document')


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schema
        exclude = ('id', 'document')


class PathSchemaSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()

    def get_schema(self, instance):
        return {"$ref": "#/definitions/{}".format(instance.schema.name)}

    class Meta:
        model = models.PathSchema
        exclude = ('id', 'path')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parameter
        exclude = ('id', 'document')


class PathSerializer(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()

    def get_parameters(self, path):
        path_schema = path.pathschema_set.all()
        schemas_serializer = PathSchemaSerializer(path_schema, many=True)
        parameters_serializer = ParameterSerializer(path.parameters, many=True)
        return schemas_serializer.data + parameters_serializer.data

    class Meta:
        model = models.Path
        exclude = ('id', 'document', 'schemas')


class DocumentSerializer(serializers.ModelSerializer):
    info = InfoSerializer()
    basePath = serializers.CharField(source='base_path')
    path = serializers.SerializerMethodField()

    def get_path(self, doc):
        paths = doc.path_set.all()
        serializer = PathSerializer(paths, many=True)
        result = {}
        for path in serializer.data:
            url = path['path']
            del path['path']
            result[url] = path
        return result

    class Meta:
        model = models.Document
        exclude = ('id', 'base_path')
