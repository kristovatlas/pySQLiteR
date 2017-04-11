"""A script that deletes the demo database file, useful for debugging only."""
#Standard Python Library 2.7
import os

import demo
from sqliter import sqliter

with sqliter.DatabaseConnection(
    db_tables=[demo.TBL_PERSON],
    app_tuple=(demo.APP_NAME, demo.AUTHOR, demo.APP_VERSION)) as DB_CON:

    db_filepath = DB_CON.db_filepath

    try:
        os.remove(db_filepath)
    except OSError:
        pass
