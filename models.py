from werkzeug import generate_password_hash,check_password_hash
import sqlite3 as sql

class DatabaseHandler:
    ''''
    This class have methods to interact with sqlite3 database
    '''


    def __init__(self, dbfilename):
        self._dbfilename = dbfilename

    def reset_schema(self, schemasql):
        ''''
        To be used if database schema needs to be reset. schemasql is a sql file that defines the tables to be created
        '''
        conn = sql.connect(self._dbfilename)
        cur = conn.cursor()
        queries = self._get_schema_queries(schemasql)
        for query in queries:
            cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()

    def _get_schema_queries(self, schema):
        ''''
        Returns all queries to be executed to create schema of database
        '''
        query = open(schema, 'r').read()
        queries = query.split(';')
        return queries

    def insert_user(self,firstname, lastname, email, password):
        'Inserts a new user into database'

        query = 'INSERT INTO users (firstname, lastname, email, password) values (?, ?, ?, ?)'
        pwdhash = self.set_password(password)
        conn = sql.connect(self._dbfilename)
        cur = conn.cursor()
        cur.execute(query, (firstname, lastname, email, pwdhash))
        conn.commit()
        cur.close()
        conn.close()

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password, pwdhash):
        return check_password_hash(pwdhash, password)

    def get_user(self, email):
        'Returns the details of existing user with email'
        conn = sql.connect(self._dbfilename)
        cur = conn.cursor()
        cur.execute("select firstname, lastname, password from users where email = ?" , (email,))
        user = cur.fetchall()
        cur.close()
        conn.close()
        return user

