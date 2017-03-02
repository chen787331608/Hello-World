#!/usr/bin/env python
# encoding:utf-8
# Author: Chen De Long

from hashlib import md5
import os
import time
import re
import json


file_list = []
if os.path.exists('config'):
    source_list = json.load(open('config'))["source"]
    target_list = json.load(open('config'))["target"]
else:
    print "error : no config"
    os.exit()
for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.js') or filename.endswith('.css'):
            if filename not in source_list:
                continue
            file_path = root + '/' + filename
            file_list.append([file_path, filename])

file_count = len(file_list)
md5_list = []
num = 0
print "Start watching ..."
while True:
    for file_path in file_list:
        file_str = open(file_path[0]).read()
        if len(md5_list) < file_count:
            md5_list.append(md5(file_str).hexdigest())
        else:
            if md5(file_str).hexdigest() != md5_list[num]:
                version = time.strftime("%m.%d.%H%M", time.localtime())
                print time.strftime("%Y%m%d  %H:%M:%S", time.localtime()), file_path[0]
                filename = file_path[1]
                for target_file in target_list:
                    target = open(target_file).read()
                    sub_str = filename + r"?" + version + "\""
                    regex = re.sub(r"\.", r"\.", filename) + r"\?.+?\""
                    target = re.sub(regex, sub_str, target)
                    open(target_file, 'w').write(target)

                md5_list[num] = md5(file_str).hexdigest()
        num = num + 1
    num = 0
    time.sleep(2)
