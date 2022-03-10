import base64
import re
import urllib.request


def get_papers_from_cs_form(datatype, user, password, method,
                            host="http://tazendra.textpressolab.com/~postgres/cgi-bin/curation_status.cgi"):
    if datatype == "humdis":
        datatype = "humandisease"
    request = urllib.request.Request(host + "?action=listCurationStatisticsPapersPage&select_datatypesource=caltech&"
                                            "select_curator=two1823&listDatatype=" + datatype + "&method=" + method +
                                     "&checkbox_nnc=on")
    base64string = base64.b64encode(bytes('%s:%s' % (user, password), 'ascii'))
    request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
    with urllib.request.urlopen(request) as response:
        res = response.read().decode("utf8")
        m = re.match('.*<textarea rows="4" cols="80" name="specific_papers">(.*)</textarea>.*',
                     res.replace('\n', ''))
        if m:
            curated_papers = set(m.group(1).split())
    return list(curated_papers)
