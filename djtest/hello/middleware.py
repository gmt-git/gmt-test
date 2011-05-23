#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from djtest.hello.models import HttpReqs


class HttpReqsSave():

    def process_request(self, request):
        req = HttpReqs(full_path=request.get_full_path())
        req.date = datetime.now()
        req.method = request.method
        req.meta = "\n".join(["%s=%s" % (k, v) for k, v in request.META.items()])
        req.cookies = "\n".join(["%s=%s" % (k, v) for k, v in request.COOKIES.items()])
        req.save()
