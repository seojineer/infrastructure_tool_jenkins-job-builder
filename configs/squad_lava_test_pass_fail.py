import sys
import pycurl
import json
from StringIO import StringIO
from optparse import OptionParser


def getBuffer(url) :
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return body


def pass_fail_check(url, exceptionList, isForcePass) :
    body = getBuffer(url)

    tmpHash = body[1:-1].split(',')
    testrunUrl = ""

    for _ in tmpHash:
        if '"testrun"' in _ :
            testrunUrl = "http" + _.split('http')[1][:-1]
            print("testruns : %s" % testrunUrl)
        else:
            pass

    body = getBuffer(testrunUrl + "tests_file/")

    tests_file_dict = json.loads(body)
    pass_cnt = 0
    fail_cnt = 0
    except_cnt = 0

    print("**********************************************************")
    for _ in list(tests_file_dict.keys()) :
        # exception List include keys then bypass (check pass)
        if _ in exceptionList :
            print("test %s : %s" % (_, "except"))
            except_cnt += 1
        else :
            print("test %s : %s" % (_, tests_file_dict[_]))
            if tests_file_dict[_] == 'fail' :
                fail_cnt += 1
            elif tests_file_dict[_] == 'pass' :
                pass_cnt += 1
            else :
                pass

    print("pass : %d / fail : %d / except : %d" % (pass_cnt, fail_cnt, except_cnt))

    if isForcePass == "true" and pass_cnt > 0 :
        return "LAVA Test SUCCESS"

    if fail_cnt > 0 :
        return "LAVA Test Fail!"

    return "LAVA Test SUCCESS"


def main():
    exceptionList = []
    isForcePass = "false"

    parser = OptionParser()
    parser.add_option("-e", "--except", action="store", type="string", dest="exception", help="Pass/Fail check exception list")
    parser.add_option("-p", "--force pass", dest="forcePass", default=False, help="only 1 pass is PASS, true of false")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("incorrect number of arguments")

    if options.exception :
        exceptionList = options.exception.split(" ")

    if options.forcePass :
        isForcePass = options.forcePass

    print(exceptionList)
    print(isForcePass)

    ret = pass_fail_check(args[0], exceptionList, isForcePass)
    print (ret)


if __name__ == "__main__":
    try:
        main()
    finally:
        pass
