import pycurl
from StringIO import StringIO

reportList = ['"failure"', '"external_url"']


def resultParse(url):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    tmpHash = body[1:-1].split(',')

    for _ in tmpHash:
        if reportList[0] in _ :
            print(_.split(':')[2])
        elif reportList[1] in _ :
            print("http" + _.split('http')[1][:-1])
        else:
            pass


def report_detail_main(arg1):
    ret = resultParse(arg1)
    print(ret)
