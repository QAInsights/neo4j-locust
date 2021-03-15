from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import *
from neo4j._exceptions import *
from locust import events

import logging
import inspect
import time


def stopwatch(func):
    def wrapper(*args, **kwargs):
        # get task's function name
        previous_frame = inspect.currentframe().f_back
        _, _, task_name, _, _ = inspect.getframeinfo(previous_frame)

        start = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        exception=e)
        else:
            total = int((time.time() - start) * 1000)
            events.request_success.fire(request_type="TYPE",
                                        name=task_name,
                                        response_time=total,
                                        response_length=0)
        return result
    return wrapper


class Neo4jClient:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.driver = None

    def connect(self):
        bolt_url = "bolt://" + self.host
        try:
            self.driver = GraphDatabase.driver(
                bolt_url,
                auth=basic_auth(self.username, self.password))
            print("Connected to the database successfully")

        except ConnectionError as exception:
            logging.error(f"Caught {exception}")
        except BoltHandshakeError as exception:
            logging.error(f"Caught {exception}")
        except BaseException as exception:
            logging.error(f"Caught {exception}")

    @stopwatch
    def send(self, cypher_query, database):

        # print(cypher_query, database)
        with self.driver.session(database=database) as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data())
        return results

    @stopwatch
    def write(self, cypher_query, database, **kwargs):
        try:
            with self.driver.session(database=database) as session:
                results = session.write_transaction(
                    lambda tx: tx.run(cypher_query).data())
            return results
        except ServiceUnavailable as exception:
            logging.error(f"{cypher_query} raised an error with {exception}")
        except CypherSyntaxError as exception:
            logging.error(f"{cypher_query} raised an error with {exception}")
        except DatabaseError as exception:
            logging.error(f"{cypher_query} raised an error with {exception}")
        except BaseException as exception:
            logging.error(f"{cypher_query} raised an error with {exception}")

    def disconnect(self):
        self.driver.close()
