import pycurl
from StringIO import StringIO
import threading
from squad_lava_2_fetched_parser import fetched_check_main

submitted_key = '"submitted"'
submitted_complete_val = "true"
retryPeriod = 60   # 60s, 1 min
waitMaxTime = 1800  # 1800s, 30 minutes


class AsyncTask:
    def __init__(self, url):
        self.url = url
        self.waitTime = 0
        self.polltry = 1
        pass

    def resultParse(self):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue()
        tmpHash = body[1:-1].split(',')

        for _ in tmpHash:
            if submitted_key in _:
                key = _.split(':')[0]
                if key == submitted_key:
                    val = _.split(':')[1]
                    print(submitted_key + " = %s" % val)

                    if val == submitted_complete_val:
                        print ("LAVA submitted SUCCESS")
                        fetched_check_main(self.url)
                        return "pass"

                    print("Try : %d, Polling peiod %ds, spent time %dm, waiting..." % (self.polltry, retryPeriod, self.waitTime / 60))

        self.polltry += 1
        self.waitTime += retryPeriod

        if self.waitTime >= waitMaxTime :
            print("LAVA Submitted Fail!")
            return "fail"

        threading.Timer(retryPeriod, self.resultParse).start()


def submit_check_main(arg1):
    periodTask = AsyncTask(arg1)
    periodTask.resultParse()
