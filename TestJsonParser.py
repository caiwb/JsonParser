# coding:utf-8

import JsonParser, string

a1 = JsonParser.JsonParser()
a2 = JsonParser.JsonParser()
a3 = JsonParser.JsonParser()

json_test = [
    '{}',
    '{"":""}',
    '{"a":123}',
    '{"a":-123}',
    '{"a":1.23}',
    '{"a":1e1}',
    '{"a":true,"b":false}',
    '{"a":null}',
    '{"a":[]}',
    '{"a":{}}',
    ' {"a:": 123}',
    '{ "a  " : 123}',
    '{ "a" : 123    	}',
    '{"true": "null"}',
    '{"":"\\t\\n"}',
    '{"\\"":"\\""}',
    # '{"a":' + '1' * 310 + '.0' + '}'
    '{"a":"abcde,:-+{}[]"}',
    '{"a": [1,2,"abc"]}',
    '{"d{": "}dd", "a":123}',
    '{"a": {"a": {"a": 123}}}',
    '{"a": {"a": {"a": [1,2,[3]]}}}',
    '{"a": "\\u7f51\\u6613CC\\"\'"}',
    '{"a":1e-1, "cc": -123.4}',
    '{ "{ab" : "}123", "\\\\a[": "]\\\\"}'

    # '{"a":[}',
    # '{"a":"}'
    # '{"a":True}'
    # '{"a":Null}'
    # '{"a":foobar}'
    # "{'a':1}"
    # '{1:1}'
    # '{true:1}'
    # '{"a":{}'
    # '{"a":-}'
    # '{"a":[,]}'
    # '{"a":.1}'
    # '{"a":+123}'
    # '{"a":"""}'
    # '{"a":"\\"}'
]

# test_json_str3 = '{"a":1e-1}'
# test_dict = {'login': 'facebook',
#              'arr': [{'a': {'abc': 'abc', '你好啊': '你好啊'}}, {"123": None}],
#              'id': 69631}

file_path = 'E:/jsonStringFile.txt'


for test_json_str in json_test:
    a1.load(test_json_str)
    print a1.data
    d1 = a1.dumpDict()
    print d1
# a2.loadDict(d1)
# a2.dumpJson(file_path)
#
# a3.loadJson(file_path)
# d3 = a3.dumpDict()
#
# print d3
