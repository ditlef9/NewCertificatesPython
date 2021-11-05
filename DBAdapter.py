import mysql.connector
from mysql.connector import errorcode


class DBAdapter:
    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None

    __cnx = None  # Connection
    __cursor = None  # Cursor

    # New MySQL class ----------------------------------------------------------------------
    def __new__(cls, host='localhost', user='root', password='', database='', *args, **kwargs):
        print("Creating Instance")
        instance = super(DBAdapter, cls).__new__(cls, *args, **kwargs)
        return instance

    # Initialize MySQL class ----------------------------------------------------------------
    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    # Open MySQL connection ----------------------------------------------------------------
    def open(self):
        try:
            self.__cnx = mysql.connector.connect(user=self.__user, password=self.__password,
                                                 host=self.__host,
                                                 database=self.__database)
            self.__cursor = self.__cnx.cursor()
            print("Connected to MySQL")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    # Close MySQL connection ----------------------------------------------------------------
    def close(self):
        self.__cnx.close()
        self.__cursor.close()

    # Last row id --------------------------------------------------------------------------
    def lastRowId(self, table):
        last_row_id = self.__cursor.lastrowid
        return last_row_id

    # Insert data ---------------------------------------------------------------------------
    # add = ("INSERT INTO employees "
    #                "(first_name, last_name, hire_date, gender, birth_date) "
    #                "VALUES (%s, %s, %s, %s, %s)")
    # data = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
    def insert(self, add, data):
        print("Insert into MySQL")
        self.__cursor.execute(add, data)
        last_row_id = self.__cursor.lastrowid
        self.__cnx.commit()

        return last_row_id

    # Create table ---------------------------------------------------------------------------
    # table = (
    #     "CREATE TABLE `employees` ("
    #     "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    #     "  `birth_date` date NOT NULL,"
    #     "  PRIMARY KEY (`emp_no`)"
    #     ") ENGINE=InnoDB")
    def createTable(self, table_description):
        try:
            print("Creating table", end='')
            self.__cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
