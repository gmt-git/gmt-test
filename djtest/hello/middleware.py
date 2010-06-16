from datetime import datetime
from djtest.hello.models import HttpReqs

class HttpReqsSave():

    def process_request(self, request):
        req = HttpReqs(path = request.path)
        req.date = datetime.now()
        req.method = request.method
        req.save()
