from rest_framework import serializers
from assets.models import *


class HostGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostGroup
        fields = ('id', 'name', 'createTime',)


class HostSerializer(serializers.ModelSerializer):
    hostGroup = serializers.PrimaryKeyRelatedField(many=False, queryset=HostGroup.objects.all())

    class Meta:
        model = Host
        fields = (
            'id', 'hostGroup', 'serialNumber', 'ip', 'ipEth1', 'kernel', 'os', 'osArch', 'osRelease', 'saltId',
            'saltStatus', 'createTime', 'updateTime')
