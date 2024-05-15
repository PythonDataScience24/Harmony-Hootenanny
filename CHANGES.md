# Changes to our Project structure with abstraction and decomposition
## decomposition: `app.py` to subfiles
Our server originally ran with a single file: `app.py`.
Since this file got quite convoluted by handling the server setup, API, database connection and queries and websocket all in one, we decided to move
to a new design where we delegate each of those functions to their own respective file. `routes.py` handles our API, 
`events.py` handles the websocket events and `extensions.py` handles the websocket implementation.
The `__init__.py` file handles the initialization of our server and the `run.py` sets some parameters for 
our server before calling the initialization of our API and websocket.  Lastly db interactions are handled in the `database.py` file.

## abstraction: in the `database.py`
### Context Managers (`@contextmanager`): 
The use of context managers demonstrates abstraction. Specifically, the `get_db_connection` function is a context manager that abstracts away the details of opening and closing a database connection. By using the `@contextmanager` decorator, you encapsulate the connection setup and teardown logic, allowing the caller to focus on the high-level task (executing queries) without worrying about the low-level details.
### Function Abstractions (`init_db`, `get_user`, `set_username`): 
Each of these functions abstracts a specific database operation. For example:
`init_db`: Initializes the database by executing the schema from a local file. The caller doesn’t need to know how the schema is read or executed; they only need to call `init_db()`.
`get_user`: Retrieves user data from the database. Again, the caller doesn’t need to know the intricacies of querying the database; they simply call get_user().
`set_username`: Updates a user’s username. The implementation details (such as the SQL query and commit) are abstracted away.