import ckanapi
from util import synthesize_query, get_wprdc_data

from pprint import pprint

HARD_LIMIT = 500001 # A limit set by the CKAN instance.
    
#query = 'SELECT * FROM "{}" WHERE "MUNICODE" = \'828\' LIMIT 3'.format(resource_id)

#get_wprdc_data(dataset_id='22c13021f-74a9-4289-a1e5-fe0472c89881', select_fields=['*'], where_fields=['MUNICPALITY = PITTSBURGH'])

#get_wprdc_data(dataset_id='123abc', select_fields=['foo', 'bar'], where_fields=['COLOR = RED', 'COUNT > 1', 'NAME LIKE "%james%"'], order_by='COUNT DESC')

if __name__ == '__main__':
    print("Running tests to demonstrate querying functionality.")
    kwargs = {'resource_id': 'f8ab32f7-44c7-43ca-98bf-c1b444724598',
            'select_fields': ['*'],
            #'where_clauses': ['"DogName" = \'BATMAN\'']
            'where_clauses': ['"DogName" LIKE \'DOGZ%\'']
            }
    query = synthesize_query(**kwargs)
    print("The query parameters sent to the get_wprdc_data function look like this: ")
    pprint(kwargs)
    print("\nThe resulting query is:")
    print(query)
    print("\nThe field names should usually be surrounded by double quotes (unless they are snake case field names), and string values need to be surrounded by single quotes.")
    records = get_wprdc_data(**kwargs)
    print(f"Executing the query fetches {len(records)} record{'s' if len(records) != 1 else ''}.")
    if len(records) > 0:
        print(f"The first record looks like this:")
        pprint(records[0])


    print("\nHere's another query, just getting dog names that contain 'CAT':")
    query = synthesize_query(resource_id='f8ab32f7-44c7-43ca-98bf-c1b444724598', select_fields=['"DogName" AS name'], where_clauses=['"DogName" LIKE \'%CAT%\''])
    print(query)
    records = get_wprdc_data(resource_id='f8ab32f7-44c7-43ca-98bf-c1b444724598', select_fields=['"DogName" AS name'], where_clauses=['"DogName" LIKE \'%CAT%\''])
    if len(records) > 0:
        print(f"The returned list of records looks like this:")
        pprint(records)

    # More sample queries:
    # SELECT COUNT(*) FROM "f8ab32f7-44c7-43ca-98bf-c1b444724598" WHERE "Breed" = 'POODLE STANDARD'
    print("\nFinally, let's use some other functionality to test some other query elements. Here's the query:")
    kwargs = {'resource_id': 'f8ab32f7-44c7-43ca-98bf-c1b444724598',
            'select_fields': ['COUNT("DogName") AS amount', '"DogName"'],
            #'select_fields': ['DISTINCT ON("DogName")', 'COUNT("_id") AS amount'],
            #'select_fields': ['DISTINCT ON("DogName")', '"DogName"', 'COUNT("DogName") AS amount'],
            #'select_fields': ['COUNT("DogName") AS amount'],
            'where_clauses': ['"Breed" = \'POODLE STANDARD\''],
            #'where_clauses': ['"Breed" LIKE \'POODLE T%\''],
            'group_by': '"DogName"',
            'order_by': 'amount DESC',
            }
    query = synthesize_query(**kwargs)
    print(query)
    records = get_wprdc_data(**kwargs)
    print("Here are the results:")
    print(records)

