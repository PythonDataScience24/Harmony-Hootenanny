# Exception catching

## Where we use try/catches:
Basically everywhere, where we expect errors to be raised: 
for example if we query our database (either connection errors or faulty queries) 
or in our request handler, where we return error code 500 if an error is raised at a certain point.

## how we dealt with exceptions
Database exceptions are just printed with some formatting, internal server errors are parsed to the frontend where we display what went wrong.
Overall we decided to not let our progamm exit on errors because that wouldn't make sense for a server.