# Module Imports
import mariadb
import sys

class DBHelper:


    __instance   = None
    __host       = None
    __user       = None
    __password   = None
    __database   = None

    __connection = None
    __cursor     = None

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__database = database
    ## End def __init__

    # Connect to MariaDB Platform
    def __open(self):
        try:

            self.__connection = mariadb.connect(
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=3306)

            # Instantiate Cursor
            self.__cursor = self.__connection.cursor()

            q = "INSERT INTO `q_domains_monitoring_domains_filtered` (`filtered_id`, `filtered_domain_value`) VALUES (NULL, 'xx')"
            self.__cursor.execute(q)


            print(f"Connected to MariaDB")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
    ## End def __open

    def __close(self):
        self.__connection.close()
        self.__cursor.close()
    ## End def __close

    def query(self, query):
        self.__open()
        self.__cursor.execute(query);
        self.__close()
        return 1
    ## End def insert
