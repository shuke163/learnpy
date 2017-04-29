from sm import settings
from service.models import *
import re
import json


class Tools:
    @staticmethod
    def stateCheck(data):
        if data.get('id') == "":
            name = data.get('name')
            if name == "":
                raise Exception("名称不能为空")
            elif len(State.objects.filter(name=name)) > 0:
                raise Exception("名称已经存在")
            for item in data.get("jinjas"):
                name = item.get('name')
                if name == "":
                    raise Exception("模板的名称不能为空")
                elif len(Jinja.objects.filter(name=name)) > 0:
                    raise Exception("模板的名称已经存在")
        else:
            state = State.objects.get(id=data.get('id'))
            name = data.get('name')
            if name == "":
                raise Exception("名称不能为空")
            elif name != state.name and len(State.objects.filter(name=name)) > 0:
                raise Exception("名称已经存在")
            for item in data.get("jinjas"):
                name = item.get('name')
                if name == "":
                    raise Exception("模板的名称不能为空")
                if item.get('id') == "":
                    if len(Jinja.objects.filter(name=name)) > 0:
                        raise Exception("模板的名称已经存在")
                else:
                    jinja = Jinja.objects.get(id=item.get('id'))
                    if name != jinja.name and len(Jinja.objects.filter(name=name)) > 0:
                        raise Exception("模板的名称已经存在")

    @staticmethod
    def getPillars(state):
        pillars = {}
        groups = re.findall("\{\{\s*(\w+)\s*\}\}", state.content)
        for group in groups:
            pillars[group] = ""
        for jinja in state.jinjas.all():
            groups = re.findall("\{\{\s*config\.(\w+)\s*\}\}", jinja.content)
            for group in groups:
                pillars[group] = ""
        return pillars

    @staticmethod
    def isPillarsAdd(oldPillars, newPillars):
        for key in newPillars:
            if key not in oldPillars:
                return True
        return False

    @staticmethod
    def serviceTypeCheck(data):
        if data.get('id') == "":
            name = data.get('name')
            if name == "":
                raise Exception("名称不能为空")
            elif len(ServiceType.objects.filter(name=name)) > 0:
                raise Exception("名称已经存在")
        else:
            serviceType = ServiceType.objects.get(id=data.get('id'))
            name = data.get('name')
            if name == "":
                raise Exception("名称不能为空")
            elif name != serviceType.name and len(ServiceType.objects.filter(name=name)) > 0:
                raise Exception("名称已经存在")

    @staticmethod
    def serviceGroupCheck(data):
        if data.get('id') == "":
            name = data.get('name')
            if name == "":
                raise Exception("名称不能为空")
            elif len(ServiceGroup.objects.filter(name=name)) > 0:
                raise Exception("名称已经存在")
        else:
            serviceGroup = ServiceGroup.objects.get(id=data.get('id'))
            name = data.get('name')
            if name == "":
                raise Exception("名称不能为空")
            elif name != serviceGroup.name and len(ServiceGroup.objects.filter(name=name)) > 0:
                raise Exception("名称已经存在")

    @staticmethod
    def generatePillarContent(serviceGroup):
        content = ""
        content += serviceGroup.name + ":\n"
        pillars = json.loads(serviceGroup.pillars)
        for serviceTypeName, items in pillars.items():
            content += "  " + serviceTypeName + ":\n"
            for key, value in items.items():
                content += "    " + key + ": " + value + "\n"
        return content

    @staticmethod
    def addPillarsPathConfig(saltAPI, path):
        initPath = settings.PROJECT_ROOT + "init.sls"
        content = saltAPI.readPillar(initPath)
        if content == "":
            content = "include:\n"
        target = path
        target = target.replace("/", ".")
        target = target.replace(".sls", "")
        target = "  - " + target
        for line in content.split("\n"):
            if line == target:
                # 已存在
                return
        content += target + "\n"
        saltAPI.writePillar(initPath, content)

    @staticmethod
    def delPillarsPathConfig(saltAPI, path):
        initPath = settings.PROJECT_ROOT + "init.sls"
        content = saltAPI.readPillar(initPath)
        target = path
        target = target.replace("/", ".")
        target = target.replace(".sls", "")
        target = "  - " + target + "\n"
        if target in content:
            content = content.replace(target, "")
            saltAPI.writePillar(initPath, content)
