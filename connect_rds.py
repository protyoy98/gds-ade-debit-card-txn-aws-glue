from multiprocessing import connection
import boto3
import boto3.session
from botocore.exceptions import ClientError
import mysql.connector
import json

# returns username and password of rds from secret manager as a tuple
def get_rds_uname_pass(secret_name, secret_region):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=secret_region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # print(get_secret_value_response)
    secret = json.loads(get_secret_value_response['SecretString'])
    username = secret['username']
    password = secret['password']
    return (username, password)


# connect to database with secrets and returns the connection
def connect_to_rds(host_name, port_no, secret_name, region_name):
    connection = None

    username, password = get_rds_uname_pass(secret_name, region_name)
    try:
        connection = mysql.connector.connect(
            host = host_name,
            port = port_no,
            username = username,
            password = password
        )
        return connection
    except Exception as e:
        raise e


# creates a connection cursor, database and tables in rds
def create_db_table_in_rds(db_name, table_name, connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    print(f"database: {db_name} created successfully")
    cursor.execute(f"USE {db_name}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}\
                   ( customer_id INT,\
                    debit_card_number BIGINT(16),\
                    bank_name VARCHAR(40),\
                    total_amount_spend DOUBLE\
                   );")
    print(f"Table {db_name}.{table_name} created successfully")
    cursor.execute(f"DESC {db_name}.{table_name};")
    

if __name__ == '__main__':
    # details for db connection
    host_name = 'gds-ade-txn-db.c3ok0s4e4v7b.us-east-1.rds.amazonaws.com'
    port_no = 3306
    secret_name = 'gds-ade-txn-db-credentials'
    region_name = 'us-east-1'

    #table details
    db_name = 'gds_ade_txn'
    table_name = 'transactions'

    #creating table in rds
    connection = connect_to_rds(host_name, port_no, secret_name, region_name)
    create_db_table_in_rds(db_name, table_name, connection)