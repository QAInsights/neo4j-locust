from locust import constant, SequentialTaskSet

from neo4j_client import *


class Neo4jTasks(SequentialTaskSet):

    def on_start(self):
        try:
            self.client.connect("naveenkumar", "neo4j")
        except ConnectionError as exception:
            logging.info(f"Caught {exception}")
            self.user.environment.runner.quit()

    @task
    def send_query(self):
        cypher_query = '''
        MATCH (n:Actor) RETURN n LIMIT 25
        '''
        database = "neo4j"

        res = self.client.send(cypher_query, database)
        # print(res)

    # @task
    # def write_query(self):
    #     cypher_query = '''
    #     CREATE (u:User { name: "NaveenKumar", userId: "714" })
    #     '''
    #     database = "neo4j"
    #     res = self.client.write(cypher_query, database)
    #     print(res)

    def on_stop(self):
        self.client.disconnect()


class Neo4jCustom(Neo4jUser):
    tasks = [Neo4jTasks]
    host = "localhost:7687"
    wait_time = constant(1)
