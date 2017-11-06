from django.shortcuts import HttpResponse, render
from host.models import Idc, User
from host.views.views import auth
from host.utils import log
import json


@auth
def idcmanage(request):
    """
    创建dic功能函数
    :param request:
    :return:
    """
    ret = {"status": False, "error": None, "data": None}
    if request.method == "POST":
        idc = request.POST.get("idc")
        regionId = request.POST.get("regionId")
        area = request.POST.get("area")
        owner_id = request.POST.get("owner_id")
        print("*" * 50)
        print("提交的IDC数据为：", idc, regionId, area, owner_id)
        try:
            # 写入数据
            insert_data = {"idc": idc, "regionId": regionId, "area": area, "owner_id": owner_id}
            Idc.objects.create(**insert_data)
            ret["status"] = True
            ret["data"] = "success"
            # 记录log
            log.logger.info("New idc info".center(50, "*"))
            log.logger.info(
                "username:{},idc:{},regionId:{},area:{},owner_id:{}".format(request.session.get("user"), idc, regionId,
                                                                            area, owner_id))
        except Exception as e:
            print("Error: ", e)
            ret["data"] = "failed"
            ret["error"] = "Create idc faild"
        return HttpResponse(json.dumps(ret))
    # 获取数据
    user = request.session.get("user")
    idc_obj = Idc.objects.all()
    owner_obj = User.objects.all().values("id", "username")
    return render(request, 'host/cloud_idc.html', locals())
