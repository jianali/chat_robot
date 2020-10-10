# orm框架工具，将数据库中返回的tuple数组转换为orm对应的map对象

class OrmUtil:


# 调用demo示例，OrmUtil.toMap(guideResult,["id","describe","component","none"])
    @staticmethod
    def toMap(arrdata,model):
        result=[]
        if len(arrdata)==0 or len(model)==0:
            return "数据为空，检查传入参数"
        else:
            for x in arrdata:
                result.append(dict(zip(model,list(x))))
        return result

    @staticmethod
    def toObject(arrdata,model):
        result = []
        if len(arrdata) == 0 or len(model) == 0:
            return "数据为空，检查传入参数"
        else:
            for x in arrdata:
                result.append()
        return result