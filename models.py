from werkzeug import generate_password_hash,check_password_hash
import sqlite3 as sql

class DatabaseHandler:
    ''''
    This class have methods to interact with sqlite3 database
    '''
    def __init__(self):
        self._DBFILENAME = './/static//Data//Database.db'


    def execute_dml(self, query, params):
        conn = sql.connect(self._DBFILENAME)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()

    def execute_select_query(self, query, params):
        conn = sql.connect(self._DBFILENAME)
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    # def reset_schema(self, schemasql):
    #     ''''
    #     To be used if database schema needs to be reset. schemasql is a sql file that defines the tables to be created
    #     '''
    #     conn = sql.connect(self._DBFILENAME)
    #     cur = conn.cursor()
    #     queries = self._get_schema_queries(schemasql)
    #     for query in queries:
    #         cur.execute(query)
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #
    # def _get_schema_queries(self, schema):
    #     ''''
    #     Returns all queries to be executed to create schema of database
    #     '''
    #     query = open(schema, 'r').read()
    #     queries = query.split(';')
    #     return queries
    #

class UserHandler:

    def __init__(self):
        self._dbObj = DatabaseHandler()

    def insert_user(self, firstname, lastname, email, password):
        'Inserts a new user into database'
        query = 'INSERT INTO users (firstname, lastname, email, password) values (?, ?, ?, ?)'
        pwdhash = self.set_password(password)
        self._dbObj.execute_dml(query, (firstname, lastname, email, pwdhash))

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password, pwdhash):
        return check_password_hash(pwdhash, password)

    def get_user(self, email):
        'Returns the details of existing user with email'
        query = "select firstname, lastname, password from users where email = ? "
        data = self._dbObj.execute_select_query(query, (email,))
        if len(data) > 0:
            return data[0]
        else:
            return None

class UserTiffin:

    def __init__(self, userEmail):
        self.userEmail = userEmail
        self.dbObj = DatabaseHandler()

    def add_new_tiffin(self, timing, type, size, addressName):
        insertTiffinQuery = "INSERT INTO user_tiffin (email, timing, type, size, address, status) VALUES (?, ?, ?, ?, ?, ?) "
        params = (self.userEmail, timing, type, size, addressName, 'ACTIVE')
        self.dbObj.execute_dml(insertTiffinQuery, params)

    def check_active_tiffin(self, timing):
        checkQuery = "SELECT * FROM user_tiffin WHERE email = ? AND timing = ?"
        params = (self.userEmail, timing)
        rows = self.dbObj.execute_select_query(checkQuery, params)
        if len(rows) > 0:
            return True
        else:
            return False

    def get_active_tiffins(self):
        checkQuery = "SELECT timing, type, size, address, status FROM user_tiffin WHERE email = ? "
        params = (self.userEmail,)
        rows = self.dbObj.execute_select_query(checkQuery, params)
        return rows

    def update_tiffin(self,timing):
        pass

    def cancel_tiffin(self, timing):
        pass


class UserAddress:

    def __init__(self, userEmail):
        self.userEmail = userEmail
        self._dbObj = DatabaseHandler()


    def add_new_delivery_address(self, addressName, addressLine1, addressLine2, city, pincode):
        insertAddressQuery = "INSERT INTO user_address (email, address_name, address_line1, address_line2, city, pin_code) VALUES (?, ?, ?, ?, ?, ?)"
        params = (self.userEmail, addressName, addressLine1, addressLine2, city, pincode)
        self._dbObj.execute_dml(insertAddressQuery, params)

    def get_existing_addresses_for_user(self):
        getAddressQuery = "SELECT address_line1 || ' ' || address_line2 || ' ' ||  city || ' ' || pin_code, address_name FROM user_address WHERE email = ?"
        addresses = self._dbObj.execute_select_query(getAddressQuery, (self.userEmail, ))
        if len(addresses) < 1:
            addresses.append(('None', 'None'))
        return addresses

    def update_delivery_address(self, addressName):
        pass




# conn = sql.connect('.//static//Data//Database.db')
# query = """
# CREATE TABLE user_address (
# email text ,
# address_name text ,
# address_line1 text,
# address_line2 text,
# city text,
# pin_code integer ,
# PRIMARY KEY (email, address_name),
# CONSTRAINT fk_email FOREIGN KEY (email) REFERENCES users(email)
#
# )
#  """

# query1 = "select name from sqlite_master where type = 'table'"
# query2 = "DELETE  from user_tiffin WHERE email = 'prem.lata@gmail.com' "
# query3 = "SELECT *  from user_tiffin WHERE email = 'prem.lata@gmail.com' and timing = 'Lunch' "
# cur = conn.cursor()
# cur.execute(query2)
# data = cur.fetchall()
# print( data)
# print(data == None, len(data))
# conn.commit()
# cur.close()
# conn.close()