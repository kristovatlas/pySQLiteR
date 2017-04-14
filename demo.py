"""A demo app using sqliter as a DB wrapper

Version 1 schema:
    * person
        * id (INTEGER, PRIMARY KEY AUTOINCREMENT)
        * fname (TEXT)
        * mi (TEXT)
        * lname (TEXT)

Todos:
    * make (fname, mi, lname) a UNIQUE constraint
"""

from sqliter import sqliter #sqliter.py
from sqliter.sqliter import Where, SQLRawExpression #sqliter.py

APP_NAME = 'PersonDemo'
AUTHOR = 'Atlas'
APP_VERSION = 1

TBL_PERSON = sqliter.DatabaseTable()
TBL_PERSON.name = 'person'
TBL_PERSON.set_cols((('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
                     ('fname', 'TEXT'),
                     ('mi', 'TEXT'),
                     ('lname', 'TEXT'),
                     ('time_added', 'INTEGER'))) #TODO: change to TIMESTAMP NOT NULL DEFAULT current_timestamp

def main():
    """Setup db, write two person records, and read them."""
    print "DEMO: Connecting to DB..."
    with sqliter.DatabaseConnection(
        db_tables=[TBL_PERSON], app_tuple=(APP_NAME, AUTHOR, APP_VERSION)) as db_con:

        print "DEMO: Populating records.."

        bob = {'fname': 'Bob',
               'mi': 'J',
               'lname': 'Smith',
               'time_added': sqliter.Reserved.CURRENT_TIMESTAMP}

        john_jacobs = {'fname': 'John',
                       'lname': 'Jacobs',
                       'time_added': sqliter.Reserved.CURRENT_TIMESTAMP}

        john_imposter = {'fname': 'John',
                         'lname': 'Imposter',
                         'time_added': sqliter.Reserved.CURRENT_TIMESTAMP}

        db_con.insert(TBL_PERSON, bob)
        db_con.insert(TBL_PERSON, john_jacobs)
        db_con.insert(TBL_PERSON, john_imposter)

        #1) print all rows
        print "DEMO: All people:"
        for person in db_con.select(col_names=None, db_table=TBL_PERSON):
            print "\tid={0} fname={1} mi={2} lname={3}".format(person['id'],
                                                               person['fname'],
                                                               person['mi'],
                                                               person['lname'])

        #2) All rows for Johns
        print "DEMO: All people named John:"
        where1 = Where(TBL_PERSON)
        for person in db_con.select(
                col_names=None, where=where1.eq('fname', 'John')):
            print "\tid={0} fname={1} mi={2} lname={3}".format(person['id'],
                                                               person['fname'],
                                                               person['mi'],
                                                               person['lname'])

        #3) Print records for John Jacobs
        print "DEMO: All people named John Jacobs:"
        where2 = Where(TBL_PERSON)
        for person in db_con.select(
                col_names=None,
                where=where2.and_(
                    where2.eq('fname', 'John'),
                    where2.eq('lname', 'Jacobs'))):

            print "\tid={0} fname={1} mi={2} lname={3}".format(person['id'],
                                                               person['fname'],
                                                               person['mi'],
                                                               person['lname'])

        #4) Print first id for John Jacobs records created in the past
        print "DEMO: First id for person named John Jacobs in the past:"
        where3 = Where(TBL_PERSON, limit=1)
        record1 = db_con.select(
            col_names=['id'],
            where=where3.and_(
                where3.and_(where3.eq('fname', 'John'),
                            where3.eq('lname', 'Jacobs')),
                where3.lt('time_added',
                          SQLRawExpression("DATETIME(CURRENT_TIMESTAMP,'+1 minute')"))))
        print "\t{0}".format(record1[0]['id'])

        #5) Change John Jacobs' name to John Rockwell
        where4 = Where(TBL_PERSON)
        db_con.update(
            col_val_map={'lname': 'Rockwell'},
            where=where4.and_(
                where4.eq('fname', 'John'),
                where4.eq('lname', 'Jacobs')))
        where5 = Where(TBL_PERSON)
        record2 = db_con.select(
            col_names=['id'],
            where=where5.and_(
                where5.eq('fname', 'John'),
                where5.eq('lname', 'Rockwell')))
        print "DEMO: First id for person named John Rockwell:"
        print "\t{0}".format(record2[0]['id'])

        #6) Do an UPDATE that has no effect
        where5 = Where(TBL_PERSON)
        changed = db_con.update(
            col_val_map={'lname': 'NOCHANGE'},
            where=where5.eq('lname', 'DOESNTEXIST'))
        print "DEMO: Updated any people with last name 'DOESNTEXIST' to 'NOCHANGE'?:"
        print "\t{0}".format(str(changed))


if __name__ == '__main__':
    main()
