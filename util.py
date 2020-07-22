import ckanapi

from pprint import pprint

HARD_LIMIT = 500001 # A limit set by the CKAN instance.

def query_resource(site, query):
    """Use the datastore_search_sql API endpoint to query a public CKAN resource."""
    ckan = ckanapi.RemoteCKAN(site)
    response = ckan.action.datastore_search_sql(sql=query)
    # A typical response is a dictionary like this
    #{u'fields': [{u'id': u'_id', u'type': u'int4'},
    #             {u'id': u'_full_text', u'type': u'tsvector'},
    #             {u'id': u'pin', u'type': u'text'},
    #             {u'id': u'number', u'type': u'int4'},
    #             {u'id': u'total_amount', u'type': u'float8'}],
    # u'records': [{u'_full_text': u"'0001b00010000000':1 '11':2 '13585.47':3",
    #               u'_id': 1,
    #               u'number': 11,
    #               u'pin': u'0001B00010000000',
    #               u'total_amount': 13585.47},
    #              {u'_full_text': u"'0001c00058000000':3 '2':2 '7827.64':1",
    #               u'_id': 2,
    #               u'number': 2,
    #               u'pin': u'0001C00058000000',
    #               u'total_amount': 7827.64},
    #              {u'_full_text': u"'0001c01661006700':3 '1':1 '3233.59':2",
    #               u'_id': 3,
    #               u'number': 1,
    #               u'pin': u'0001C01661006700',
    #               u'total_amount': 3233.59}]
    # u'sql': u'SELECT * FROM "d1e80180-5b2e-4dab-8ec3-be621628649e" LIMIT 3'}
    data = response['records']

    # Note that if a CKAN table field name is a Postgres reserved word (like 
    # ALL or CAST or NEW), you get a not-very-useful error
    #      (e.g., 'query': ['(ProgrammingError) syntax error at or near
    #     "on"\nLINE 1: SELECT * FROM (SELECT load, on FROM)
    # and you need to escape the reserved field name with double quotes.
    # It's actually best to escape all field names with double quotes,
    # but if it's all lowercase letters and underscores in the CKAN table, 
    # you can get away with not escaping it in yourquery.

    return data

def query_any_resource(resource_id, query):
    site = "https://data.wprdc.org"
    ckan = ckanapi.RemoteCKAN(site)
    # From resource ID, determine package ID.
    package_id = ckan.action.resource_show(id=resource_id)['package_id']
    # From package ID, determine if the package is private.
    private = ckan.action.package_show(id=package_id)['private']
    if private:
        print("As of February 2018, CKAN still doesn't allow you to run a datastore_search_sql query on a private dataset. Sorry. See this GitHub issue if you want to know a little more: https://github.com/ckan/ckan/issues/1954")
        raise ValueError("CKAN can't query private resources (like {}) yet.".format(resource_id))
    else:
        return query_resource(site, query)

def intersection(list1, list2):
    return list(set(list1) & set(list2))

def validate_where_clause(where_clause):
    operators = ['=', '>', '<', '>=', '<=', '<>', '!=', 'BETWEEN', 'LIKE', 'IN']
    parts = where_clause.split(' ')
    if intersection(operators, parts) == []:
        raise ValueError(f"No operator found in the WHERE clause {where_clause}.")

def remove_fields(records, fields_to_remove):
    """This function removes selected fields from the CKAN records. The intent is
    to remove the '_full_text' field, which is row-level metadata to facilitate
    searches of the records, but this function could be used to purge other 
    fields, like '_geom' and '_the_geom_webmercator', which may not be of 
    interest in some situations."""
    for r in records:
        _ = [r.pop(key, None) for key in fields_to_remove]
    return records

def synthesize_query(resource_id, select_fields=['*'], where_clauses=None, group_by=None, order_by=None):
    query = f'SELECT {", ".join(select_fields)} FROM "{resource_id}"'
    if where_clauses is not None:
        for clause in list(where_clauses):
            validate_where_clause(clause)
        query += f" WHERE {', '.join(where_clauses)}"

    if group_by is not None:
        query += f" GROUP BY {group_by}"
    if order_by is not None:
        query += f" ORDER BY {order_by}"
    return query

def get_wprdc_data(resource_id, select_fields=['*'], where_clauses=None, group_by=None, order_by=None):
    query = synthesize_query(resource_id, select_fields, where_clauses, group_by, order_by)
    print(f"order_by = {order_by}")
    print(f"group_by = {group_by}")

    records = query_any_resource(resource_id, query)

    if len(records) == HARD_LIMIT:
        print(f"Note that there may be more results than you have obtained since the WPRDC CKAN instance only returns {HARD_LIMIT} records at a time.")
        # If you send a bogus SQL query through to the CKAN API, the resulting error message will include the full query used by CKAN,
        # which wraps the query you send something like this: "SELECT * FROM (<your query>) LIMIT 500001", so you can determine the actual
        # hard limit that way.

    # Clean out fields that no one needs.
    records = remove_fields(records, ['_full_text']) 
    return records
