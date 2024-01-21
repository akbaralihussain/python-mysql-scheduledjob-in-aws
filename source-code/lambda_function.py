#######################################################
# Python + MySQL code sample customized by TechieInYou 
# The original code is taken from https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-lambda-tutorial.html#vpc-rds-create-deployment-package
#
# pymysql & requests library will be importing from Lambda layer
# all other libraries are available by default in Python runtime provided by Lambda
#######################################################
import sys
import logging
import pymysql
import json
import os
import requests
import random

# rds settings reading from environment variables
user_name = os.environ['database_uid']
password = os.environ['database_pwd']
db_host = os.environ['database_host']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=db_host, user=user_name, passwd=password, connect_timeout=5)
    logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    # Generate a random number between 1 and 200
    randTodoId = random.randint(1, 200)

    # fetch todo item from {JSON} Placeholder
    url = 'https://jsonplaceholder.typicode.com/todos/{0}'.format(randTodoId)
    res = requests.get(url, timeout=4.50)
    
    data = json.loads(res.content)
    UserId = data['userId']
    Title = data['title']
    IsCompleted = data['completed'] 
    sql_string = f"insert into ToDoItems (UserId, Title, Completed) values({UserId}, '{Title}', '{IsCompleted}')"

    result = None
    with conn.cursor() as cur:
        # creating database in the first run
        cur.execute("CREATE DATABASE IF NOT EXISTS Organizer")
        cur.execute("USE Organizer")
        # creating table in the first run
        cur.execute("create table if not exists ToDoItems ( Id int NOT NULL AUTO_INCREMENT, UserId int NOT NULL, Title varchar(255) NOT NULL, Completed varchar(5) NULL, PRIMARY KEY (Id))")
        # insert new row with the ToDo item
        cur.execute(sql_string)
        conn.commit()
        # checking the latest row count
        cur.execute("select * from ToDoItems")
        cur.fetchall()
        result = "MySQL Table Organizer.ToDoItems has %d ToDo items" %(cur.rowcount)    
    conn.commit()

    logger.info(result)
    return result
    