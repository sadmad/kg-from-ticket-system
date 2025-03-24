import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

url = os.environ["neo4j-url"]
user = os.environ["user"]
passNeo = os.environ["pass"]

AUTH = (user, passNeo)
def connectToDatabae ():
    try:
        with GraphDatabase.driver(url, auth=AUTH) as driver:
            driver.verify_connectivity()
            print("Connection established.")
    except Exception as e:
        print(f":space_invader:Error: {e}") 

    finally:
        driver.close()

def create_entities(tx):
    tx.run( "merge (a:Person {name: 'Albert Einstein'})")
    tx.run( "merge (n:NobelPrize {name: 'Nobel Prize in Physics'})")
    tx.run( "merge (p:Subject {name: 'Physics'})")
    tx.run( "merge (g:Country {name: 'Germany'})")
    tx.run( "merge (u:Country Person {name: 'USA'})")

def create_relationships():
    tx.run(
        """
        MATCH (a:Person {name: 'Albert Einstein'}), (p:Subjetct {name: Physics})
        MERGE (a)-[:STUDIED]->(p)    """
    )