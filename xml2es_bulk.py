#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:xml2es_bulk.py
# For ipg-xml Files   and Translate
# date 2016-12-19

import time
import re
import gc
import json
import requests
from os import walk
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from segtok import segmenter


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

es = Elasticsearch(["localhost", "192.168.1.105"])


def xmlRegex(xmlStr):
    """
        Clear the format <img> <maths>
    """
    xmlStr = re.sub(r'<br />|<br/>', '', xmlStr)
    xmlStr = re.sub(r'<img.*?/>', 'IMG', xmlStr)
#    xmlStr = re.sub(r'<.*/>', '', xmlStr)
#    xmlStr = re.sub(r'[\n\t\r]', '', xmlStr)
    xmlStr = re.sub(r'&#.{3,5};', '', xmlStr)
    xmlStr = re.sub(r'<sub>|</sub>|<sup>|</sup>|<i>|</i>',
                    ' ', xmlStr)
    xmlStr = re.sub(r'<b>|</b>', '', xmlStr)
#    xmlStr = re.sub(r'<p.{12}num=\"[0-9]{4}\">\W{22}</p>', '', xmlStr)
    return xmlStr


def transRegex(text):
    '''$srcSentence =~ s/%/%25/g;
       $srcSentence =~ s/\+/%2B/g;
       $srcSentence =~ s/ /%20/g;
       $srcSentence =~ s/\//%2F/g;
       $srcSentence =~ s/\?/%3F/g;
       $srcSentence =~ s/#/%23/g;
       $srcSentence =~ s/&/%26/g;
       $srcSentence =~ s/=/%3D/g;
                                '''
    text = re.sub(r'%', '%25', text)
    text = re.sub('\+', '%2B', text)
#   text = re.sub('\ ', '%20', text)
    text = re.sub('\/', '%2F', text)
    text = re.sub('\?', '%3F', text)
    text = re.sub(r'#', '%23', text)
    text = re.sub(r'&', '%26', text)
    text = re.sub(r'=', '%3D', text)
    text = re.sub(r',', ' ,', text)
    text = re.sub(r';', ' ;', text)
    text = re.sub(r':', ' :', text)
    return text


def translate(text):
    if text == u'' or len(text) >= 10000:
        return ''
    post = r"http://123.207.91.118:1518/MTServer" +\
           r"/translation?from=en&to=zh&src_text="
    cn_text = ""
    text = text.lower()
    sents = [sent for sent in segmenter.split_single(text)]
    for sent in sents:
        if sent == u'' or len(sent) >= 3000:
            return ''
        T_sent = transRegex(sent)
        r = requests.post(post + T_sent)
        try:
            if "tgt_text" in r.json():
                cn_text += r.json()["tgt_text"]
        except:
            return ''
    return cn_text


def xmlParse(xmlStr):
    root = ET.fromstring(xmlStr)
    json_dict = {}
    pubRef = root[0][0][0]
    country = pubRef[0].text
    pub_id = pubRef[1].text
    pub_date = pubRef[3].text
    app_type = root[0][1].attrib['appl-type']
    appRef = root[0][1][0]
    app_id = appRef[1].text
    app_date = appRef[2].text
    json_dict.update({"pub_id": pub_id})
    json_dict.update({"pub_date": pub_date})
    json_dict.update({"country": country})
    json_dict.update({"app_type": app_type})
    json_dict.update({"app_id": app_id})
    json_dict.update({"app_date": app_date})

    title_en = root[0].find("invention-title").text
    title = {"title_en": "", "title_cn": ""}
    title.update({"title_en": title_en})
    title_cn = translate(title_en)
    title.update({"title_cn": title_cn})
    json_dict.update({"title": title})
    abstract = root.find('abstract')[0].text
    abstract_en = re.sub(r'<b>|</b>|</ b>', '', abstract)
    abstract = {"abstract_en": "", "abstract_cn": ""}
    abstract.update({"abstract_en": abstract_en})
    abstract_cn = translate(abstract_en)
    abstract.update({"abstract_cn": abstract_cn})

    json_dict.update({"abstract": abstract})
    parties = root[0].find('us-parties')
    inventors = []
    for inventor in parties[1].iter('addressbook'):
        inventor_text = inventor[1].text + ' ' + inventor[0].text
        inventors.append({"inventor": inventor_text})
    json_dict.update({"inventors": inventors})

    description = root.find('description')
    descriptions = []
    for dp in description:
        description_text = ""
        description_dict = {"description_en": "", "description_cn": ""}
        for figref in dp.iter():
            if figref.text is not None:
                description_text += figref.text
            if figref.tag == 'figref' and figref.tail is not None:
                description_text += figref.tail
        description_text = re.sub(r'[\n\t\r]', '', description_text)
        description_dict.update({"description_en": description_text})
        description_text_cn = translate(description_text)
        description_dict.update({"description_cn": description_text_cn})
        descriptions.append({"description": description_dict})
    json_dict.update({"descriptions": descriptions})

    claim = root.find('claims')
    claims = []
    for dp in claim.findall('claim'):
        claim_text = ''
        claim_dict = {"claim_en": "", "claim_cn": ""}
        for claim in dp.iter():
            if claim.text is not None:
                claim_text += claim.text
            if claim.tag == 'claim-ref' and claim.tail is not None:
                claim_text += claim.tail
        claim_text = re.sub(r'[\n\t\r]', '', claim_text)
        claim_dict.update({"claim_en": claim_text})
        claim_text_cn = translate(claim_text)
        claim_dict.update({"claim_cn": claim_text_cn})
        claims.append({"claim": claim_dict})
    json_dict.update({"claims": claims})

    return json_dict

###############################################################################

if __name__ == '__main__':
    count = 0
    list_count = 0
    numx = 0
    actions = []
    start = time.time()
    suc_list = json.loads(open('suc.json').read())["success"]
    for root, dirs, files in walk('.'):
        for filename in files:
            if '.xml' in filename and filename[0] != 'i':
                file_object = open(root + '/' + filename)
                all_the_text = file_object.read()
                file_object.close()
                xml_str = xmlRegex(all_the_text)
                count += 1
                if count in suc_list:
                    continue
                print filename, count,
                try:
                    json_dict = xmlParse(xml_str)
                    json_patent = json.dumps(json_dict)
                    action = {
                                 "_index": "patent",
                                 "_type": "US_Grant",
                                 "_id": "%d" % count,
                                 "_source": json_patent
                             }
                    actions.append(action)
                    list_count += 1
                    if list_count == 10:
                        print 'add to elasticsearch ...'
                        helpers.bulk(es, actions)
                        print 'add success'
                        list_count = 0
                        del actions[:]
                        gc.collect()

                except ET.ParseError:
                    numx += 1
                    print 'Error : Parse failed !!!'
                    continue
                except KeyboardInterrupt:
                    print 'Exit'
                    exit(0)
                print 'Sucess Parse', time.time() - start
    print 'patent_doc total:', count, 'sucess :',\
                                      count - numx, 'failed :', numx
#   '''
    print 'add to elasticsearch ...'
    helpers.bulk(es, actions)
    print 'add success'
#                            '''
