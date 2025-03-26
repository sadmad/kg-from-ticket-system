import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

url = os.environ["neo4j-url"]
user = os.environ["user"]
passNeo = os.environ["pass"]

AUTH = (user, passNeo)

driver = GraphDatabase.driver(url, auth=AUTH)    
def queryGraph(cypherQuery):
    try:
        with driver.session(database='neo4j') as session:
            result = session.run(cypherQuery)
            for record in result:
                print(record["path"])
    except Exception as e:
            print(f"😈 :Error: {e}" )
    finally:
        driver.close()

einstein_query = """
MATCH path=(a:Person {name: 'Albert Einstein'})-[:STUDIED]->(s:Subject)
RETURN path
UNION
MATCH path=(a:Person {name: 'Albert Einstein'})-[:WON]->(n:NobelPrize)
RETURN path
UNION
MATCH path=(a:Person {name: 'Albert Einstein'})-[:BORN_IN]->(g:Country)
RETURN path
UNION
MATCH path=(a:Person {name: 'Albert Einstein'})-[:DIED_IN]->(u:Country)
RETURN path
"""

if __name__ == "__main__":
    queryGraph(einstein_query)
