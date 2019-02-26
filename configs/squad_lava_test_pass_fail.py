import sys
import pycurl
import json
from StringIO import StringIO
from optparse import OptionParser

FAIL_MARK = "LAVA Test Fail!"
PASS_MARK = "LAVA Test SUCCESS"


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

    print("**********************************************************")
    print("pass : %d / fail : %d / except : %d" % (pass_cnt, fail_cnt, except_cnt))
    print("**********************************************************")

    if isForcePass == "true" and pass_cnt > 0 :
        return PASS_MARK

    if fail_cnt > 0 :
        return FAIL_MARK

    return PASS_MARK


def benchmark_check(url, referenceDict, scoreORtime) :
    body = getBuffer(url)

    tmpHash = body[1:-1].split(',')
    testrunUrl = ""

    for _ in tmpHash:
        if '"testrun"' in _ :
            testrunUrl = "http" + _.split('http')[1][:-1]
            print("testruns : %s" % testrunUrl)
        else:
            pass

    body = getBuffer(testrunUrl + "metrics_file/")

    metrics_file_dict = json.loads(body)
    pass_cnt = 0
    fail_cnt = 0

    print("**********************************************************")
    for _ in list(referenceDict.keys()) :
        if _ in metrics_file_dict.keys() :
            print("metrics  %s : %s" % (_, metrics_file_dict[_]))
            print("referenceDict %s : %s" % (_, referenceDict[_]))
            if scoreORtime == "score" :
                if int(metrics_file_dict[_]) < int(referenceDict[_]) :
                    print(" **--> %s case fail" % _)
                    fail_cnt += 1
                else :
                    print(" --> %s case pass" % _)
                    pass_cnt += 1
            elif scoreORtime == "time" :
                if int(metrics_file_dict[_]) > int(referenceDict[_]) :
                    print(" **--> %s case fail" % _)
                    fail_cnt += 1
                else :
                    print(" --> %s case pass" % _)
                    pass_cnt += 1
            else :
                print("type strange, input type must be score or time")
                return FAIL_MARK

            print("\n")

    if fail_cnt == 0 and pass_cnt == 0:
        print("metrics_file some strange, may be mismatch testrunUrl with metrics_file url")
        return FAIL_MARK

    else :
        print("**********************************************************")
        print("pass : %d / fail : %d" % (pass_cnt, fail_cnt))
        print("**********************************************************")

    if fail_cnt > 0 :
        return FAIL_MARK

    return PASS_MARK


def main():
    exceptionList = []
    isForcePass = "false"
    referenceDict = {}
    caseList = []
    ret = FAIL_MARK
    scoreORtime = ""
    ret = ""

    parser = OptionParser()
    parser.add_option("-e", "--except", action="store", type="string", dest="exception", help="Pass/Fail check exception list")
    parser.add_option("-s", "--score", action="store", type="string", dest="score", help="performance or benchmark get score, args : benchmark and score")
    parser.add_option("-t", "--time", action="store", type="string", dest="time", help="performance or benchmark get time, args : benchmark and time")
    parser.add_option("-p", "--force pass", dest="forcePass", default=False, help="only 1 pass is PASS, true of false")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("incorrect number of arguments")

    if options.exception :
        exceptionList = options.exception.split(" ")
        # print("exception Case : %s" % str(exceptionList))

    if options.forcePass :
        isForcePass = options.forcePass
        # print("forcePass : %s" % isForcePass)

    if options.score :
        caseList = options.score.split(",")
        caseList = [x.strip(' ') for x in caseList]
        scoreORtime = "score"
        # print("case list : %s" % str(caseList))

    if options.time :
        caseList = options.time.split(",")
        caseList = [x.strip(' ') for x in caseList]
        scoreORtime = "time"
        # print("case list : %s" % str(caseList))

    ret = pass_fail_check(args[0], exceptionList, isForcePass)
    if ret == PASS_MARK :
        if len(caseList) > 0 :
            for _ in caseList :
                _item_ = _.split(" ")
                # dict add
                referenceDict[_item_[0]] = _item_[1]

            ret = benchmark_check(args[0], referenceDict, scoreORtime)

    print(ret)
    sys.stdout.flush()
    return ret


if __name__ == "__main__":
    ret = ""
    try:
        ret = main()
    finally:
        # one more print
        print(ret)
        sys.stdout.flush()
        pass
