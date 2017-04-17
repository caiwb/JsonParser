# coding:utf-8

import string, copy


class Stack:
    def __init__(self):
        self.items = []

    def top(self):
        if self.size() > 0:
            return self.items[self.size() - 1]

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def showItems(self):
        return self.items


class JsonParser:
    def __init__(self):
        self.data = {}

    def load(self, s):
        if not isinstance(s, str) or len(s) < 2:
            raise TypeError("this string is not a json string")

        stack = Stack()

        # string
        wordStr = ""
        strStart = -1
        strEnd = -1

        # number
        number = 0
        numberStart = -1
        numberEnd = -1
        isFloat = False
        floatPointIndex = -1

        #const
        colonChar = ':'
        blankChar = ' '
        minusChar = '-'
        pointChar = '.'
        commaChar = ','
        leftBraceChar = '{'
        rightBraceChar = '}'
        leftBracketChar = '['
        rightBracketChar = ']'
        doubleQuotationChar = '"'
        doubleLineChar = '\\'
        zeroChar = '0'
        nineChar = '9'
        eChar = 'e'
        trueStr = 'true'
        falseStr = 'false'
        nullStr = 'null'

        #other
        isTranfering = False
        inDoubleQuotation = False
        legalChars = [colonChar, blankChar, '\n', '\t', '\r', '\0']
        loopCount = 0
        inLeftBracketChar = False

        for c in s:
            list = stack.items
            o = ord(c)

            if (c == minusChar or c == pointChar or (zeroChar <= c <= nineChar)
                or (c == eChar and numberStart != -1)) \
                    and strStart == -1:
                # 处理数字
                if numberStart == -1:
                    numberStart = loopCount
                if c == pointChar or c == eChar:  # 小数
                    isFloat = True
                    floatPointIndex = loopCount if c == pointChar else -1
            else:
                if numberStart != -1 and numberEnd == -1:
                    numberEnd = loopCount
                    try:
                        if isFloat:
                            if floatPointIndex != -1 and \
                                    (s[floatPointIndex - 1] <= zeroChar
                                     or s[floatPointIndex - 1] >= nineChar
                                     or s[floatPointIndex + 1] <= zeroChar
                                     or s[floatPointIndex + 1] >= nineChar):
                                raise TypeError("the float is not a standard "
                                                "format for json")
                            number = string.atof(s[numberStart: numberEnd])
                        else:

                            number = string.atoi(s[numberStart: numberEnd])
                    except Exception:
                            raise Exception("the number is not a standard "
                                            "format")
                    stack.push(number)
                    number = 0
                    numberStart = -1
                    numberEnd = -1
                    isFloat = False

                if (c == leftBraceChar or c == commaChar) \
                        and strStart == -1 and not isTranfering:
                    # 处理{and,
                    stack.push(c)

                elif c == leftBracketChar \
                        and strStart == -1 and not isTranfering:
                    # 处理[
                    inLeftBracketChar = True
                    stack.push(c)

                elif c == doubleQuotationChar and not isTranfering:
                    # 处理"
                    inDoubleQuotation = True if not inDoubleQuotation else False
                    if strStart == -1:
                        strStart = loopCount + 1
                    else:
                        strEnd = loopCount
                        wordStr = s[strStart: strEnd]
                        stack.push(wordStr)
                        wordStr = ""
                        strStart = -1
                        strEnd = -1

                elif nullStr.find(c) != -1 and strStart == -1:  # 处理null
                    if s[loopCount: loopCount + 4] == nullStr:
                        stack.push(None)

                elif trueStr.find(c) != -1 and strStart == -1:  # 处理true
                    if s[loopCount: loopCount + 4] == trueStr:
                        stack.push(True)

                elif falseStr.find(c) != -1 and strStart == -1:  # 处理false
                    if s[loopCount: loopCount + 5] == falseStr:
                        stack.push(False)

                elif c == rightBraceChar and strStart == -1 \
                        and not isTranfering: # 处理}
                    result = {}
                    while stack.top() != leftBraceChar and stack.size() > 2:
                        value = stack.pop()
                        key = stack.pop()
                        if not isinstance(key, str):
                            raise TypeError("the key must be a instance of "
                                            "string")
                        result.update({key: value})
                        if stack.top() == commaChar:
                            stack.pop()
                            continue
                    if stack.top() == leftBraceChar:
                        stack.pop()
                    stack.push(result)

                elif c == rightBracketChar and strStart == -1 \
                        and not isTranfering: # 处理]
                    inLeftBracketChar = False
                    result = []
                    while stack.top() != leftBracketChar and stack.size() > 0:
                        if stack.top() != commaChar:
                            result.insert(0, stack.pop())
                        else:
                            raise TypeError("this string is not a json string")
                        if stack.top() == commaChar:
                            stack.pop()
                            continue
                    if stack.top() == leftBracketChar:
                        stack.pop()
                    stack.push(result)

                elif c == doubleLineChar or isTranfering: # 处理转义符
                    isTranfering = True if not isTranfering else False

                elif not inDoubleQuotation and c not in legalChars:
                    raise TypeError("this string is not a json string")

            loopCount += 1

        if inLeftBracketChar:
            raise TypeError("this string is not a json string")

        if stack.size() == 1:
            self.data = stack.pop()
        else:
            raise TypeError("this string is not a json string")

    def dump(self):
        jsonStr = self.__convertDataToJson(self.data)

        return jsonStr.encode("utf-8")

    def __convertDataToJson(self, obj):
        if isinstance(obj, str) or isinstance(obj, unicode):
            return '"%s"' % obj
        elif isinstance(obj, int):
            return '%d' % obj
        elif isinstance(obj, float):
            return '%f' % obj
        elif not obj:
            return 'null'
        elif isinstance(obj, dict):
            s = '{'
            loopCount = 0
            for key in obj.keys():
                if isinstance(key, str) or isinstance(key, unicode):
                    s += '"%s":' % key
                elif isinstance(key, int):
                    s += '%d' % key
                elif isinstance(key, float):
                    s += '%f' % key
                s += self.__convertDataToJson(obj[key])
                if loopCount < len(obj.keys()) - 1:
                    s += ','
                else:
                    s += '}'
                loopCount += 1
            return s
        elif isinstance(obj, list):
            s = '['
            loopCount = 0
            for item in obj:
                s += self.__convertDataToJson(item)
                if loopCount < len(obj) - 1:
                    s += ','
                else:
                    s += ']'
                loopCount += 1
            return s

    def dumpJson(self, f):
        jsonStr = self.dump()
        try:
            with open(f, 'w') as fp:
                fp.write(jsonStr)
        except Exception as e:
            raise ValueError(e)
        finally:
            file.close()

    def loadJson(self, f):
        try:
            with open(f, 'w') as fp:
                jsonStr = fp.read()
        except Exception as e:
            raise IOError(e)
        finally:
            self.load(jsonStr)
            file.close()

    def loadDict(self, d):
        if not isinstance(d, dict):
            raise TypeError("param is not a dict!")
        self.data.update(d)

    def dumpDict(self):
        dictUnicode = self.data
        self.__convertStringToUnicode(None, None, dictUnicode)
        return dictUnicode

    def __convertUnicodeToString(self, obj, key, value):
        if isinstance(value, dict):
            for k in value.keys():
                if isinstance(k, unicode):
                    v = value[k]
                    value.pop(k)
                    k = k.encode("utf-8")
                    value[k] = v
                    self.__convertUnicodeToString(value, k, v)

        elif isinstance(value, unicode):
            obj[key] = value.encode("utf-8")

        elif isinstance(value, list):
            for item in value:
                self.__convertUnicodeToString(obj, key, item)

    def __convertStringToUnicode(self, obj, key, value):
        if isinstance(value, dict):
            for k in value.keys():
                if isinstance(k, str):
                    v = value[k]
                    value.pop(k)
                    k = k.decode("utf-8")
                    value[k] = v
                    self.__convertStringToUnicode(value, k, v)

        elif isinstance(value, str):
            obj[key] = value.decode("utf-8")

        elif isinstance(value, list):
            for item in value:
                self.__convertStringToUnicode(obj, key, item)

    def update(self, d):
        if not isinstance(d, dict):
            raise TypeError("param is not a dict!")
        self.data.update(d)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            return
        self.data.update({key: value})
