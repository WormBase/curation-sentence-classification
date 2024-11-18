import base64
import re
import urllib.request


def get_papers_from_cs_form(datatype, user, password, method,
                            host="https://caltech-curation.textpressolab.com/priv/cgi-bin/curation_status.cgi"):
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


import requests


def get_pmid_from_wbpaperid(wbpaperid):
    # Ensure the ID has 8 digits by padding with zeros if necessary
    wbpaperid = wbpaperid.zfill(8)

    # Ensure the ID is in the format 'WB:WBPaper' if not already present
    if not wbpaperid.startswith('WB:WBPaper'):
        wbpaperid = f'WB:WBPaper{wbpaperid}'

    # URL for the API request
    url = f'https://stage-literature-rest.alliancegenome.org/reference/by_cross_reference/{wbpaperid}'

    # Headers for the API request
    headers = {
        'accept': 'application/json'
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        # Extract the PMID from the crossReferences list
        for cross_reference in data.get('cross_references', []):
            if cross_reference.get('curie_prefix') == 'PMID':
                return cross_reference.get('curie')
    return None
