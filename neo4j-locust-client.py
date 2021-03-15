from locust import SequentialTaskSet, task, constant, User

from neo4j_client import Neo4jClient


class Neo4jTest(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.driver = ""

    def on_start(self):
        self.driver = Neo4jClient("localhost:7687", "naveenkumar", "neo4j")
        self.driver.connect()

    @task
    def send_query(self):
        cypher_query = '''
        MATCH (n:Actor) RETURN n LIMIT 25
        '''
        database = "neo4j"
        res = self.driver.send(cypher_query, database)
        print(res)

    @task
    def write_query(self):
        cypher_query = '''
        CREATE (u:User { name: "NaveenKumar", userId: "702" })
        '''
        database = "neo4j"
        res = self.driver.write(cypher_query, database)
        print(res)

    def on_stop(self):
        self.driver.disconnect()


class Neo4jUser(User):
    tasks = [Neo4jTest]
    wait_time = constant(1)
