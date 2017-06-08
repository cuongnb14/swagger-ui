from django.utils.translation import ugettext as _
from rest_framework import serializers
from . import models


class InfoSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField()
    termsOfService = serializers.CharField(source='terms_of_service')

    def get_contact(self, info):
        return {'email': info.contact_email}

    class Meta:
        model = models.Info
        exclude = ('contact_email', 'document', 'terms_of_service')


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        exclude = ('id', 'schema', 'parent')
        depth = 1


class SchemaSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    required = serializers.SerializerMethodField()

    def get_required(self, instance):
        result = []
        properties = instance.property_set.all()
        for property in properties:
            if property.required:
                result.append(property.name)
        if result:
            return result
        return None

    def get_properties(self, instance):
        properties = instance.property_set.all()
        serializer = PropertySerializer(properties, many=True)
        result = {}
        for property in serializer.data:
            name = property["name"]
            del property["name"]
            del property["required"]
            result[name] = property
        return result

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


class ResponseSerializer(serializers.ModelSerializer):
    schema = serializers.SerializerMethodField()

    def get_schema(self, instance):
        return {"$ref": "#/definitions/{}".format(instance.schema.name)}

    class Meta:
        model = models.Response
        exclude = ('id', 'path')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        exclude = ('id', 'document')


class PathSerializer(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()
    responses = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, path):
        tags = path.tags.all()
        serializer = TagSerializer(tags, many=True)
        return [tag["name"] for tag in serializer.data]

    def get_responses(self, path):
        responses = path.response_set.all()
        serializer = ResponseSerializer(responses, many=True)
        result = {}
        for response in serializer.data:
            code = response["http_code"]
            del response["http_code"]
            result[code] = response
        return result

    def get_parameters(self, path):
        path_schema = path.pathschema_set.all()
        schemas_serializer = PathSchemaSerializer(path_schema, many=True)
        for schema in schemas_serializer.data:
            schema['in'] = schema['at']
            del schema['at']

        parameters_serializer = ParameterSerializer(path.parameters, many=True)
        return schemas_serializer.data + parameters_serializer.data

    class Meta:
        model = models.Path
        exclude = ('id', 'document', 'schemas')


class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Security
        exclude = ('document',)


class DocumentSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    info = InfoSerializer()
    basePath = serializers.CharField(source='base_path')
    paths = serializers.SerializerMethodField()
    securityDefinitions = serializers.SerializerMethodField()
    definitions = serializers.SerializerMethodField()

    def get_tags(self, doc):
        tags = doc.tag_set.all()
        serializer = TagSerializer(tags, many=True)
        return serializer.data

    def get_definitions(self, doc):
        schemas = doc.schema_set.all()
        serializer = SchemaSerializer(schemas, many=True)
        result = {}
        for schema in serializer.data:
            name = schema["name"]
            del schema["name"]
            result[name] = schema
        return result

    def get_paths(self, doc):
        paths = doc.path_set.all()
        serializer = PathSerializer(paths, many=True)
        result = {}
        for path in serializer.data:
            url = path['path']
            method = path['method']
            del path['path']
            del path['method']
            if url not in result:
                result[url] = {}
            result[url][method] = path
        return result

    def get_securityDefinitions(self, doc):
        try:
            serializer = SecuritySerializer(doc.security)
            data = serializer.data.copy()
            key = data["key"]
            data["in"] = serializer.data["at"]
            del data["key"]
            del data["at"]
            print(data)
            return {key: data}
        except Exception:
            return None

    class Meta:
        model = models.Document
        exclude = ('id', 'base_path', 'name')
