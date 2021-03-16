# # pip3 install neo4j-driver
# # python3 example.py
#
# from neo4j import GraphDatabase, basic_auth
#
# driver = GraphDatabase.driver(
#     "bolt://localhost:7687",
#     auth=basic_auth("naveenkumar", "neo4j"))
#
# cypher_query = '''
# MATCH (m:Movie {title:$movie})<-[:RATED]-(u:User)-[:RATED]->(rec:Movie)
# RETURN distinct rec.title AS recommendation LIMIT 20
# '''
#
# with driver.session(database="neo4j") as session:
#     results = session.read_transaction(
#         lambda tx: tx.run(cypher_query,
#                           movie="Crimson Tide").data())
#     for record in results:
#         print(record['recommendation'])
#
# driver.close()

class MyClass:

    def m(self):
        print("method")

    @classmethod
    def cm(cls):
        print("Class method")

    @staticmethod
    def sm(a, b):
        print("Static methods")
        print(a+b)
        return a + b


a = MyClass()
a.m()
a.cm()
a.sm(1, 1)

