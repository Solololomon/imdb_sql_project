# imdb_sql_project
This script takes user-inputted data to generate information for up to 40 films
based on their release year and rating according to IMDb. The results are sorted
by popularity, as determined by IMDb's algorithms.

The script amends IMDb's search URL to input custom values for the range of years and
ratings searched, and then scrapes data from the generated page. This data includes 
each film's title, year, genre, rating, runtime, and age certificate. If no suitable
matches are found, 'No result found' is printed.

A film_id is uniquely attached to each film, and the results are presented in the form of
a printed pandas DataFrame (with index removed, as we have already specified a film_id).

Finally, a 'films.db' database is created using sqlite3.

A 'manipulations.py' file is included for performing SQL queries and amendments
to the films.db schema. This file should be run on its own after running main.py
otherwise the user will have to input new parameters each time.

Note, the films.db schema will be overwritten each time you run main.py and enter new
input parameters.
