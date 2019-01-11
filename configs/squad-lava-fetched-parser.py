import pycurl
from StringIO import StringIO
import threading
import sys

fetched_key = '"fetched"'
fetched_complete_val = "true"
retryPeriod = 300   # 300s, 5 min
waitMaxTime = 7200  # 7200s, 2 hours


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
            if fetched_key in _:
                key = _.split(':')[0]
                if key == fetched_key:
                    val = _.split(':')[1]
                    print(fetched_key + " = %s" % val)

                    if val == fetched_complete_val:
                        return "Fetched from LAVA SUCCESS"

                    print("Try : %d, Polling peiod %ds, spent time %dm, waiting..." % (self.polltry, retryPeriod, self.waitTime / 60))

        self.polltry += 1
        self.waitTime += retryPeriod

        if self.waitTime >= waitMaxTime :
            return "Fetched from LAVA Fail!"

        threading.Timer(retryPeriod, self.resultParse).start()


def main(arg1):
    periodTask = AsyncTask(arg1)
    ret = periodTask.resultParse()
    return ret


if __name__ == "__main__":
    try:
        main(sys.argv[1])  # http://192.168.1.20:5000/api/testjobs/xx/
    finally:
        pass
