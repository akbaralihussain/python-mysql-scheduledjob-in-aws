import sys
import logging
import pymysql
import json
import os
import requests
import random

# rds settings
user_name = os.environ['database_uid']
password = os.environ['database_pwd']
db_host = os.environ['database_host']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
try:
    conn = pymysql.connect(host=db_host, user=user_name, passwd=password, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    # Generate a random number between 1 and 200
    randTodoId = random.randint(1, 200)
    url = 'https://jsonplaceholder.typicode.com/todos/{0}'.format(randTodoId)
    data = requests.get(url, timeout=2.50)
    # data = {
    #   "userId": 1,
    #   "id": 2,
    #   "title": "quis ut nam facilis et officia qui",
    #   "completed": "false"
    # }

    ItemId = data["id"]
    UserId = data['userId']
    Title = data['title']
    IsCompleted = data['completed'] 

    item_count = 0
    sql_string = f"insert into ToDoItems (UserId, Title, Completed) values({UserId}, '{Title}', '{IsCompleted}')"

    with conn.cursor() as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS Organizer")
        cur.execute("USE Organizer")
        cur.execute("create table if not exists ToDoItems ( Id int NOT NULL AUTO_INCREMENT, UserId int NOT NULL, Title varchar(255) NOT NULL, Completed varchar(5) NULL, PRIMARY KEY (Id))")
        cur.execute(sql_string)
        conn.commit()
        cur.execute("select * from ToDoItems")
        logger.info("The following items have been added to the table:")
        for row in cur:
            item_count += 1
            logger.info(row)
    conn.commit()

    return "Added %d items to RDS for MySQL table" %(item_count)
    