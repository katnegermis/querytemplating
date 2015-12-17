import itertools
import sys

log = sys.stdout.write
flush = sys.stdout.flush


class QueryTemplate(object):
    """ A template for generating SQL statements.
    """
    def __init__(self, sql, name, **kwargs):
        self.sql = sql
        self.name = name
        self.variables = kwargs.get('variables', {})
        self._setupquerytuples = kwargs.get('setupqueries', [])
        self._repeats = kwargs.get('repeats', 3)
        self._arraysize = kwargs.get('arraysize', 100)
        self.passthrough = kwargs

    def makequeries(self):
        for varcombination in self._variablecombinations():
            params = {k: v for (k, v) in varcombination}
            _sql = self.sql.format(**params)
            query = Query(sql=_sql, params=params, name=self.name, setupqueries=[])
            for setupquerytemplates in self._setupquerytuples:
                for setupcombinations in itertools.product(*(list(q.makequeries()) for q in setupquerytemplates)):
                    query.setupqueries = setupcombinations
                    yield query
            else:
                yield query

    def _variablecombinations(self):
        """ Produce all combinations of keys and values from a dictionary.
        """
        kvpairs = ([(k, v) for v in self.variables[k]] for k in self.variables)
        return itertools.product(*kvpairs)

    def __str__(self):
        return ("QueryTemplate(name={name}, variables={variables}, setupqueries={setup})"
                "".format(name=self.name, variables=self.variables, setup=self._setupquerytuples))


class Query(object):
    def __init__(self, sql, params, name, **kwargs):
        self.sql = sql
        self.params = params
        self.name = name
        self.setupqueries = kwargs.get('setupqueries', [])

    def __str__(self):
        return ("Query(name={name}, params={params}, setupqueries={setup})"
                "".format(name=self.name, params=self.params, setup=self.setupqueries))
