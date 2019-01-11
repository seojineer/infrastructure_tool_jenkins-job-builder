import pycurl
from StringIO import StringIO
import threading
import sys

submitted_key = '"submitted"'
submitted_complete_val = "true"


class AsyncTask:
    def __init__(self, url):
        self.url = url
        self.polltry = 0
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
                        return "LAVA submitted SUCCESS"

        self.polltry += 1

        if self.polltry >= 5 :
            return "LAVA submitted Fail!"

        threading.Timer(30, self.resultParse).start()

        return "LAVA submitted Fail!"


def main(arg1):
    periodTask = AsyncTask(arg1)
    ret = periodTask.resultParse()
    print(ret)
    return ret


if __name__ == "__main__":
    try:
        main(sys.argv[1])  # http://192.168.1.20:5000/api/testjobs/xx/
    finally:
        pass
