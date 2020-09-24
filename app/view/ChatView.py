from sanic.response import json
from sanic import Blueprint
from sanic.views import HTTPMethodView
from app.service.DiagnosticTreeService import DiagnosticTreeService
from app.service.GuideTreeService import GuideTreeService


chat_view = Blueprint(
    'chat',
    url_prefix='/chat'
)


#根据传入的组件返回对应的运维诊断文档树
def getDiagnosticTree(component):

    # 首先根据聊天记录传过来的值找到数据库中对应的tree_id

    diagnosticTreeService = DiagnosticTreeService()
    result=diagnosticTreeService.getDiagnosticTree(component)
    return result

# chat_view.add_route()

# 这里可以根据处理逻辑，封装为一个controller文件夹
#根据传入的组件返回对应的运维诊断文档树
def getGuideTree(id):
    # 首先根据聊天记录传过来的值找到数据库中对应的tree_id
    guideTreeService = GuideTreeService()
    result=guideTreeService.getGuideTree(id)
    return result


if __name__ == '__main__':
    result=getGuideTree(0)
    # 将result从tuple转换为dict
    # b=["id","describe","component","none"]
    # t=dict({"id":id,"describe":describe,"component":component} for id,describe,component in result)
    print(result[:][1])
    # print(dict(b,result))