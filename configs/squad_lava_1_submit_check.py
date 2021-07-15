import pycurl
from io import BytesIO
import threading
from squad_lava_2_fetched_parser import fetched_check_main

submitted_key = '"submitted"'
submitted_complete_val = "true"
retryPeriod = 60   # 60s, 1 min
waitMaxTime = 1800  # 1800s, 30 minutes
SUBMIT_FAIL_MARK = "LAVA Submitted Fail!"
SUBMIT_PASS_MARK = "LAVA Submitted SUCCESS"


class AsyncTask:
    def __init__(self, url, url2):
        self.url = url
        self.url2 = url2
        self.waitTime = 0
        self.polltry = 1
        pass

    def resultParse(self):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue().decode('UTF-8')
        tmpHash = body[1:-1].split(',')

        for _ in tmpHash:
            if submitted_key in _:
                key = _.split(':')[0]
                if key == submitted_key:
                    val = _.split(':')[1]
                    # print(submitted_key + " = %s" % val)

                    if val == submitted_complete_val:
                        print(SUBMIT_PASS_MARK)
                        fetched_check_main(self.url, self.url2)
                        return "pass"

                    # print("Try : %d, Polling peiod %ds, spent time %dm, waiting..." % (self.polltry, retryPeriod, self.waitTime / 60))

        self.polltry += 1
        self.waitTime += retryPeriod

        if self.waitTime >= waitMaxTime :
            print(SUBMIT_FAIL_MARK)
            return "fail"

        threading.Timer(retryPeriod, self.resultParse).start()


def submit_check_main(arg1, arg2):
    periodTask = AsyncTask(arg1, arg2)
    periodTask.resultParse()
