# Submission library based on the codespeed example:

from datetime import datetime
import socket
import urllib
import urllib2

CODESPEED_URL = 'http://speed.pyston.org/'

def _formdata(commitid, benchmark, executable, value):
    hostname = socket.gethostname()

    if "cpython" in executable.lower():
        project = "CPython"
    elif "pypy" in executable.lower():
        project = "PyPy"
    else:
        project = "Pyston"

    # Mandatory fields
    data = {
        'commitid': commitid,
        'branch': 'default',  # Always use default for trunk/master/tip
        'project': project,
        'executable': executable,
        'benchmark': benchmark,
        'environment': hostname,
        'result_value': value,
    }

    """
    # Optional fields
    current_date = datetime.today()
    data.update({
        'revision_date': current_date,  # Optional. Default is taken either
                                        # from VCS integration or from current date
        'result_date': current_date,  # Optional, default is current date
    })
    """

    return data

def submit(commitid, benchmark, executable, value):
    data = _formdata(commitid, benchmark, executable, value)

    params = urllib.urlencode(data)
    response = "None"
    print "Saving result for executable %s, revision %s, benchmark %s" % (
        data['executable'], data['commitid'], data['benchmark'])

    retries = 1
    while True:
        try:
            f = urllib2.urlopen(CODESPEED_URL + 'result/add/', params)
            break
        except urllib2.HTTPError as e:
            print str(e)

            if retries > 0 and e.code in (500,):
                print "Retrying..."
                continue

            print e.read()
            raise
    response = f.read()
    f.close()
    print "Server (%s) response: %s\n" % (CODESPEED_URL, response)
