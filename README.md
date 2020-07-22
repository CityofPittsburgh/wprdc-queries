# wprdc-queries
Python code for SQL-querying of datastores on the WPRDC data portal

Functions in `util.py` allow the creation and execution of SQL queries for getting data from the CKAN-based data portal at https://data.wprdc.org.

Run `demo.py` (`> python demo.py`) for a demonstration of how the queries can be assembled and run. (Inspect the code also for further clarification of how to format queries.)

CKAN stores its data tables in "resources" which are below the package level, a package being a folder-like collection of resources. The package is what is often referred to as the dataset.

To query a data table you need to know its resource ID.

This URL

https://data.wprdc.org/dataset/allegheny-county-dog-licenses/resource/f8ab32f7-44c7-43ca-98bf-c1b444724598

is the table of lifetime dog licenses for Allegheny County. You can navigate to it by clicking on the "Lifetime Dog Licenses" resource link on the landing page for the dataset:

https://data.wprdc.org/dataset/allegheny-county-dog-licenses

The resource ID is that long alphanumeric string with all the dashes in the URL ("f8ab32f7-44c7-43ca-98bf-c1b444724598").

Field names to use in constructing the query can be seen in the data table view on a page like
https://data.wprdc.org/dataset/allegheny-county-dog-licenses/resource/f8ab32f7-44c7-43ca-98bf-c1b444724598
Field names can also be obtained from the data dictionary which is shown below the data table.
