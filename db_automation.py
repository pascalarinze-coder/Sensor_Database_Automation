#Python script to automate the creation of 5-table sensor database schema
import mysql.connector
from mysql.connector import errorcode

config={
    'host':'localhost',
    'user': 'root',
    'password': ''
}

def create_database(db_name):

    db_connect=None
    cursor=None

    try:
        db_connect = mysql.connector.connect(**config)
        cursor = db_connect.cursor()
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8')
        print(f'{db_name} was created successfully')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f'{db_name} already exists ')
        else:
            print(f'Error: {err.msg}')
    finally:
        if cursor:
            cursor.close()
        if db_connect and db_connect.is_connected():
            db_connect.close()

def create_table(table_name, column_definition):
    try:
        db_connect = mysql.connector.connect(**config)
        cursor = db_connect.cursor()
        cursor.execute(f'USE sensors')
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} {column_definition}')
        print(f"Table '{table_name}': checked/created successfully.")
    except mysql.connector.Error as err:
        print(f'Error creating {table_name}: {err.msg}')
    
    finally:
        if cursor:
            cursor.close()
        if db_connect and db_connect.is_connected():
            db_connect.close()

table_name_list = {
            'Location': ("(idLocation INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
            "name VARCHAR (45) NOT NULL UNIQUE, "
            "description VARCHAR(45) NOT NULL) "
            "ENGINE = InnoDB" ), 
            
            
            'Unit': ("(unit VARCHAR(45) NOT NULL PRIMARY KEY,"
            "description VARCHAR(45) NOT NULL) "
            "ENGINE = InnoDB" ),

            'Sensor': (
            "(idSensor INT UNSIGNED NOT NULL AUTO_INCREMENT, "
            "idLocation INT UNSIGNED NOT NULL, "
            "name VARCHAR(45) NOT NULL, "
            "unit VARCHAR(45) NOT NULL, "
            "PRIMARY KEY (idSensor), "
            "INDEX fk_Sensor_Location_idx (idLocation ASC), "
            "INDEX fk_Sensor_Units1_idx (unit ASC), "
            "UNIQUE INDEX uniq_loc_vs_sensor (idLocation ASC, name ASC), "
            "CONSTRAINT fk_Sensor_Location FOREIGN KEY (idLocation) "
            "REFERENCES Location (idLocation) ON DELETE CASCADE ON UPDATE CASCADE, "
            "CONSTRAINT fk_Sensor_Units1 FOREIGN KEY (unit) "
            "REFERENCES Unit (unit) ON DELETE CASCADE ON UPDATE CASCADE) " 
            "ENGINE = InnoDB" ),


            'Reading': (
            "(idReading INT UNSIGNED NOT NULL AUTO_INCREMENT, "
            "idSensor INT UNSIGNED NOT NULL, "
            "timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "value FLOAT NOT NULL, "
            "PRIMARY KEY (idReading), "
            "INDEX fk_Reading_Sensor1_idx (idSensor ASC),"
            "CONSTRAINT fk_Reading_Sensor1 FOREIGN KEY (idSensor) "
            "REFERENCES Sensor (idSensor) ON DELETE CASCADE ON UPDATE CASCADE) "
            "ENGINE = InnoDB" ),
    

            'Alert': (
            "(idAlert INT UNSIGNED NOT NULL AUTO_INCREMENT, "
            "idSensor INT UNSIGNED NOT NULL, "
            "timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "description VARCHAR(45) NOT NULL, "
            "cleared BIT NULL, "
            "PRIMARY KEY (idAlert), "
            "INDEX fk_Alert_Sensor1_idx (idSensor ASC), "
            "CONSTRAINT fk_Alert_Sensor1 FOREIGN KEY (idSensor) "
            "REFERENCES Sensor (idSensor) ON DELETE CASCADE ON UPDATE CASCADE) "
            "ENGINE = InnoDB"),       
        }
        
def drop_database(db_name):    
    try:
        db_connect = mysql.connector.connect(**config)
        cursor = db_connect.cursor()
        cursor.execute(f'DROP DATABASE {db_name}')
        print(f'{db_name} was dropped')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_DROP_EXISTS:
            print(f'{db_name} does not exists')
        else:
            print(f'Error: {err.msg}')
    finally:
        if cursor:
            cursor.close()
        if db_connect and db_connect.is_connected():
            db_connect.close()
            
if __name__ =="__main__":
#    drop_database('sensors')
    #setup database
    create_database('sensors')
    print(f"select another task")
    #setup table
    for name, columns in table_name_list.items():
        create_table(name, columns)
    print("Database and Tables successfully initialized")

