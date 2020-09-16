from sanic.response import json
from sanic import Blueprint
from sanic.views import HTTPMethodView
from app.service.DiagnosticTreeService import DiagnosticTreeService

chat_view = Blueprint(
    'chat',
    url_prefix='/chat'
)


#根据传入的组件返回对应的运维诊断文档树
def getDiagnosticTree(component):

    # 首先根据聊天记录传过来的值找到数据库中对应的tree_id

    diagnosticTreeService = DiagnosticTreeService()
    diagnosticTreeService.getDiagnosticTree("123")
    return "运维诊断树"

# chat_view.add_route()


if __name__ == '__main__':
    getDiagnosticTree("123")