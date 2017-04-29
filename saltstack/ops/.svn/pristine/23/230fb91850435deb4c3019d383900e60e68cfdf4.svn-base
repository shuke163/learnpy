from rest_framework import serializers
from job.models import *


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'type', 'name',)


class CommandSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(many=False, queryset=Module.objects.all())

    class Meta:
        model = Command
        fields = ('id', 'module', 'fun', 'doc')


class CommandRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandRecord
        fields = ('id', 'cmd', 'jid', 'result', 'createTime')
