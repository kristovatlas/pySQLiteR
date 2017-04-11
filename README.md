#PySQLiteR

A lite-r version of Python Standard Library's `sqlite3` module.

## Project goals

 * Provide simple interface that satisfies most everyday needs for small,
   non-optimized SQLite database
 * Functionality is included in some set of source files that can be easily
   copied to other project

## Advantages

Removes some of the following annoying tasks of managing sqlite3 development:
 * Creating your own SQL statements
 * Managing where to store the db file
 * Error handling
 * Error logging
 * Managing where to store your log file
 * Argument parameterization and type-checking

## Disadvantages

 * Much less than full SQLite syntax implemented
