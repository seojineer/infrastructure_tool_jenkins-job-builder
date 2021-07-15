import pycurl
from io import BytesIO 
import threading
from squad_lava_3_pass_check import pass_check_main

fetched_key = '"fetched"'
fetched_complete_val = "true"
retryPeriod = 300   # 300s, 5 min
waitMaxTime = 7200  # 7200s, 2 hours
FETCHED_FAIL_MARK = "LAVA Fetched Fail!"
FETCHED_PASS_MARK = "LAVA Fetched SUCCESS"


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

        body = buffer.getvalue().decode('utf-8')
        tmpHash = body[1:-1].split(',')

        for _ in tmpHash:
            if fetched_key in _:
                key = _.split(':')[0]
                if key == fetched_key:
                    val = _.split(':')[1]
                    # print(fetched_key + " = %s" % val)

                    if val == fetched_complete_val:
                        print(FETCHED_PASS_MARK)
                        pass_check_main(self.url, self.url2)
                        return "pass"

                    # print("Try : %d, Polling peiod %ds, spent time %dm, waiting..." % (self.polltry, retryPeriod, self.waitTime / 60))

        self.polltry += 1
        self.waitTime += retryPeriod

        if self.waitTime >= waitMaxTime :
            print(FETCHED_FAIL_MARK)
            return "fail"

        threading.Timer(retryPeriod, self.resultParse).start()


def fetched_check_main(arg1, arg2):
    periodTask = AsyncTask(arg1, arg2)
    periodTask.resultParse()
