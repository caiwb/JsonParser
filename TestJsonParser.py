# coding:utf-8

import JsonParser

a1 = JsonParser.JsonParser()
a2 = JsonParser.JsonParser()
a3 = JsonParser.JsonParser()

# test_json_str = '{ "programmers": [{ "firstName": "Brett", "lastName":"McLaughlin", "email": "aaaa" },{ "firstName": "Jason", "lastName":"Hunter", "email": "bbbb" },{ "firstName": "Elliotte", "lastName":"Harold", "email": "cccc" }],"authors": [{ "firstName": "Isaac", "lastName": "Asimov", "genre": "science fiction" },{ "firstName": "Tad", "lastName": "Williams", "genre": "fantasy" },{ "firstName": "Frank", "lastName": "Peretti", "genre": "christian fiction" }]}'
test_json_str =  '{"login": "facebook","arr":[{"a":{"abc":"abc", "你好啊":"你好啊"}},{"123":null}] ,"id": 69631}'
test_dict = {'login': 'facebook','arr':[{'a':{'abc':'abc', '你好啊':'你好啊'}},{"123":None}] ,'id': 69631}

# test_json_str = '{"你":"好"}'
# test_dict = {'你':'好'}

file_path = 'E:/jsonStringFile.txt'

a1.load(test_json_str)
print a1.data

d1 = a1.dumpDict()
print d1

a2.loadDict(d1)
a2.dumpJson(file_path)

a3.loadJson(file_path)
d3 = a3.dumpDict()

print d3
