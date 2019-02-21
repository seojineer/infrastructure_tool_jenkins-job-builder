import pycurl
from StringIO import StringIO

reportList = ['"failure"', '"external_url"']


def resultParse(url, url2):
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
            print(_.split(':')[-1])
        elif reportList[1] in _ :
            print("**********************************************************")
            print("SQUAD URL : ")
            print("    %s" % url2)
            print("LAVA URL : ")
            print("    http%s" % _.split('http')[1][:-1])
            print("**********************************************************")
        else:
            pass


def report_detail_main(arg1, arg2):
    resultParse(arg1, arg2)
