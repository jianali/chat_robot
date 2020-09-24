import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


# dic = {'name': 'jack', 'create_time': datetime.datetime(2019, 3, 19, 10, 6, 6)}
#
# print(json.dumps(dic, cls=DateEncoder))