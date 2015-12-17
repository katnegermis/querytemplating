import os
import json

from classes import *

def readqpfile(path):
    """ Read a qp-file.

    qp-file format:

    - Lines starting with '//' in a qp-file are comments.
    - Lines containing only a newline character are ignored.
    - Configuration for a qp-file is written in JSON and must be placed
    between lines containing '// config'.
    - Lines not matched by the above rules are considered to be part of the
    file's SQL statement.
    """
    readsql = ""
    readjson = ""
    readingconfig = False
    readconfig = False
    with open(path, 'r') as f:
        for l in f:
            if l.startswith("// config"):
                if not readingconfig:
                    readingconfig = True
                else:
                    readconfig = True
                continue
            if readingconfig and not readconfig:
                readjson += l
                continue
            if l.startswith("//") or l == "\n" or len(l) == 0:
                continue
            readsql += l
    return readsql, readjson


def interpretqueryfile(path):
    """ Takes as input a path to a query file.
    Returns a `Query` with associated `QueryConfig`.
    """
    readsql, readjson = readqpfile(path)
    try:
        queryargs = json.loads(readjson) if len(readjson) > 0 else {}
    except ValueError:
        print "Error in {p}:".format(p=path)
        raise

    setupqueries = []
    for setupqueryfiles in queryargs.get('setupqueries', []):
        cursetupqueries = []
        for setupqueryfilename in setupqueryfiles:
            setupquerypath = os.path.join(queryargs.get('configdir', os.path.dirname(path)), setupqueryfilename)
            setupquery = interpretqueryfile(setupquerypath)
            cursetupqueries.append(setupquery)
        setupqueries.append(cursetupqueries)
    name = queryargs.get('name', os.path.basename(path))
    kwargs = {k: queryargs[k] for k in queryargs if k not in ['name', 'setupqueries']}
    return QueryTemplate(sql=readsql, name=name, setupqueries=setupqueries, **kwargs)

