import ckanapi
from util import synthesize_query, get_wprdc_data

from pprint import pprint

HARD_LIMIT = 500001 # A limit set by the CKAN instance.
    
if __name__ == '__main__':
    print("Running tests to demonstrate querying functionality.")
    kwargs = {'resource_id': 'f8ab32f7-44c7-43ca-98bf-c1b444724598',
            'select_fields': ['*'],
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

    print("\nFinally, let's test some other query elements. Here's the query:")
    kwargs = {'resource_id': 'f8ab32f7-44c7-43ca-98bf-c1b444724598',
            'select_fields': ['COUNT("DogName") AS amount', '"DogName"'],
            'where_clauses': ['"Breed" = \'POODLE STANDARD\''],
            'group_by': '"DogName"',
            'order_by': 'amount DESC',
            'limit': 5,
            }
    query = synthesize_query(**kwargs)
    print(query)
    records = get_wprdc_data(**kwargs)
    print("Here are the resulting top five names for the POODLE STANDARD breed, sorted by decreasing frequency:")
    pprint(records)
