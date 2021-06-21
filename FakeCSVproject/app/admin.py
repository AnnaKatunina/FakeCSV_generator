from django.contrib import admin

from FakeCSVproject.app.models import Schema, Column, Dataset

admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(Dataset)
