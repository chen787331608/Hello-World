#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from app import app

reload(sys)
sys.setdefaultencoding('utf8')

app.run(debug=True, port=8888)
