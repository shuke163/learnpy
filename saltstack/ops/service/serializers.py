from service.models import *
from assets.serializers import *


class JinjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jinja
        fields = ('id', 'name', 'path', 'content')


class StateSerializer(serializers.ModelSerializer):
    jinjas = JinjaSerializer(many=True)

    class Meta:
        model = State
        fields = ('id', 'name', 'remark', 'fun', 'path', 'content', 'jinjas', 'successStatus', 'failureStatus')


class ServiceTypeSerializer(serializers.ModelSerializer):
    states = serializers.PrimaryKeyRelatedField(many=True, queryset=State.objects.all())

    class Meta:
        model = ServiceType
        fields = ('id', 'name', 'remark', 'states')


class ServiceGroupSerializer(serializers.ModelSerializer):
    serviceTypes = serializers.PrimaryKeyRelatedField(many=True, queryset=ServiceType.objects.all())

    class Meta:
        model = ServiceGroup
        fields = ('id', 'name', 'remark', 'serviceTypes', 'pillars', 'hasNewPillars')


class ServiceSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(many=False, queryset=Host.objects.all())
    group = serializers.PrimaryKeyRelatedField(many=False, queryset=ServiceGroup.objects.all())
    type = serializers.PrimaryKeyRelatedField(many=False, queryset=ServiceType.objects.all())

    class Meta:
        model = Service
        fields = ('id', 'name', 'remark', 'host', 'group', 'type', 'status', 'currentJobId', 'currentJobDesc')


class ServiceJobSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=False)
    state = StateSerializer(many=False)

    class Meta:
        model = ServiceJob
        fields = ('id', 'jid', 'service', 'state', 'result', 'createTime')
