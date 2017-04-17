# coding:utf-8

class JsonException(Exception):
    def __init__(self, err="this string is not a json string!"):
        Exception.__init__(self, err)


