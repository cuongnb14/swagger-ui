from django.contrib import admin

from . import models


class InfoInline(admin.StackedInline):
    model = models.Info
    extra = 1


class PathInline(admin.StackedInline):
    model = models.Path
    extra = 1


class SecurityInline(admin.StackedInline):
    model = models.Security
    extra = 1


class ResponseInline(admin.StackedInline):
    model = models.Response
    extra = 1


class PathParameterInline(admin.StackedInline):
    model = models.PathParameter
    extra = 1


class ParameterInline(admin.StackedInline):
    model = models.Parameter
    extra = 1


class PathSchemaInline(admin.StackedInline):
    model = models.PathSchema
    extra = 1


class SchemaInline(admin.StackedInline):
    model = models.Schema
    extra = 1


class PropertyInline(admin.StackedInline):
    model = models.Property
    extra = 1


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    inlines = [InfoInline, PathInline, SecurityInline, SchemaInline, ParameterInline]
    list_display = ["name", "swagger", "base_path"]


@admin.register(models.Path)
class PathAdmin(admin.ModelAdmin):
    inlines = [PathParameterInline, PathSchemaInline, ResponseInline, ]
    list_display = ["path", "method"]


@admin.register(models.Schema)
class SchemaAdmin(admin.ModelAdmin):
    inlines = [PropertyInline, ]
    list_display = ["name", "type"]


admin.site.register(models.Property)
admin.site.register(models.Parameter)
