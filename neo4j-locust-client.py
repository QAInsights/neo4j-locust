from locust import SequentialTaskSet, task, constant, User
import neo4j_client


class Neo4jClient(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.driver = ""

    def on_start(self):
        self.driver = neo4j_client.Neo4jLocust("localhost:7687", "naveenkumar", "neo4j")
        print(self.driver.connect())

    @task
    def send_query(self):
        cypher_query = '''
        MATCH (n:Actor) RETURN n LIMIT 25
        '''
        database = "neo4j"
        res = self.driver.send(cypher_query, database)
        print(res)

    def on_stop(self):
        self.driver.disconnect()


class Neo4jUser(User):
    tasks = [Neo4jClient]
    wait_time = constant(1)
