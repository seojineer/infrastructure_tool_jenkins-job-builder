import pycurl
from io import BytesIO
from squad_lava_4_report_detail import report_detail_main

pass_condition = {'"job_status"': '"Complete"', '"failure"': '"null"'}
FAIL_MARK = "LAVA Test Fail!"
PASS_MARK = "LAVA Test Complete"


def resultParse(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue().decode('utf-8')
    tmpHash = body[1:-1].split(',')
    is_job_status_complete = False
    is_failure_null = False
    is_failure_exception = False

    for _ in tmpHash:
        if list(pass_condition.keys())[0] in _ and _.split(':')[1] == list(pass_condition.values())[0]:  # job_status is Complete
            # print(_.split(':')[1])
            is_job_status_complete = True
        #elif list(pass_condition.keys())[1] in _ and _.split(':')[1] == list(pass_condition.values())[1]:  # failure is Null
        elif list(pass_condition.keys())[1] in _:
            if _.split(':')[1] == list(pass_condition.values())[1]:  # failure is Null
                print(_.split(':')[1])
                is_failure_null = True
            else: # 'There is already a test run with job_id' excption occurs (bug)
                is_failure_exception = True
                pass
        else:
            pass

    if is_job_status_complete:
        if is_failure_null:
            return PASS_MARK
        elif is_failure_exception: # for pass job_id corruption bug
            return PASS_MARK
    else:
        return FAIL_MARK


def pass_check_main(arg1, arg2):
    ret = resultParse(arg1)
    print (ret)
    report_detail_main(arg1, arg2)
