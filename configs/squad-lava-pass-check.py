import pycurl
from StringIO import StringIO
import sys
from squad_lava_report_detail import rdmain

pass_condition = {'"job_status"': '"Complete"', '"failure"': "null"}


def resultParse(url):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    tmpHash = body[1:-1].split(',')
    is_job_status_complete = False
    is_failure_numm = False

    for _ in tmpHash:
        if pass_condition.keys()[0] in _ and \
           _.split(':')[1] == pass_condition.values()[0]:  # job_status is Complete
            # print(_.split(':')[1])
            is_job_status_complete = True
        elif pass_condition.keys()[1] in _ and \
             _.split(':')[1] == pass_condition.values()[1]:  # failure is Null
            # print(_.split(':')[1])
            is_failure_numm = True
        else:
            pass

    if is_job_status_complete and is_failure_numm :
        return "LAVA Test SUCCESS"
    else:
        return "LAVA Test Fail!"


def main(arg1):
    ret = resultParse(arg1)
    print(ret)
    if ret == "LAVA Test Fail!" :
        rdmain(arg1)
    return ret


if __name__ == "__main__":
    try:
        main(sys.argv[1])  # http://192.168.1.20:5000/api/testjobs/xx/
    finally:
        pass
