import base64
import re
import urllib.request


def get_negative_paper_ids(datatype, user, password,
                           host="http://tazendra.textpressolab.com/~postgres/cgi-bin/curation_status.cgi"):
    if datatype == "humdis":
        datatype = "humandisease"
    request = urllib.request.Request(host + "?action=listCurationStatisticsPapersPage&select_datatypesource=caltech&"
                                            "select_curator=two1823&listDatatype=" + datatype + "&method=allval%20neg&"
                                            "checkbox_cfp=on&checkbox_afp=on&checkbox_str=on&checkbox_nnc=on&"
                                            "checkbox_svm=on" + datatype)
    base64string = base64.b64encode(bytes('%s:%s' % (user, password), 'ascii'))
    request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
    with urllib.request.urlopen(request) as response:
        res = response.read().decode("utf8")
        m = re.match('.*<textarea rows="4" cols="80" name="specific_papers">(.*)</textarea>.*',
                     res.replace('\n', ''))
        if m:
            curated_papers = set(m.group(1).split())
    return list(curated_papers)
