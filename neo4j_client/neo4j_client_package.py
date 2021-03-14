from neo4j import GraphDatabase, basic_auth


class Neo4jLocust:

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
            print("Connected")

        except ConnectionError:
            print("Connection Error")

    def send(self, cypher_query, database):

        # print(cypher_query, database)
        with self.driver.session(database=database) as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data())
        return results

    def disconnect(self):
        self.driver.close()
        print("Disconnected")
