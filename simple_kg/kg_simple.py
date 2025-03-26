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

def createEntities(tx):
    tx.run( "merge (a:Person {name: 'Albert Einstein'})")
    tx.run( "merge (n:NobelPrize {name: 'Nobel Prize in Physics'})")
    tx.run( "merge (p:Subject {name: 'Physics'})")
    tx.run( "merge (g:Country {name: 'Germany'})")
    tx.run( "merge (u:Country {name: 'USA'})")

def createRelationships(tx):
    tx.run(
        """
        MATCH (a:Person {name: 'Albert Einstein'}), (p:Subject {name: 'Physics'})
        MERGE (a)-[:STUDIED]->(p)
        """
    )
    tx.run("""
           MATCH (a:Person {name: 'Albert Einstein'}), (n:NobelPrize {name: 'Nobel Prize in Physics'})
           MERGE (a)-[:WON]-(n)
           
          """)
    
    tx.run("""
           MATCH (a:Person {name: 'Albert Einstein'}), (n:Country {name: 'Germany'})
           MERGE (a)-[:BORN_IN]-(n)
           
          """) 
    tx.run("""
           MATCH (a:Person {name: 'Albert Einstein'}), (n:Country {name: 'USA'})
           MERGE (a)-[:DEID_IN]-(n)
           
          """)
driver = GraphDatabase.driver(url, auth=AUTH)    
def queryGraphSimple(cypherQuery):
    try:
        with driver.session(database='neo4j') as session:
            result = session.run(cypherQuery)
            for record in result:
                print(record["Name"])
    except Exception as e:
            print(f"Error: {e}" )
    finally:
        driver.close()

def queryGraph(cypherQuery):
    try:
        with driver.session(database='neo4j') as session:
            result = session.run(cypherQuery)
            for record in result:
                print(record["path"])
    except Exception as e:
            print(f":space_invader:Error: {e}" )
    finally:
        driver.close()



def buildKnowledgeGraph():  
    try:
        with driver.session(database="neo4j") as session:
            session.execute_write(createEntities)
            session.execute_write(createRelationships)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()


returnAllTheNodes = "MATCH (n) RETURN n.name AS Name"

if __name__ == "__main__":
    #buildKnowledgeGraph()
    queryGraphSimple(returnAllTheNodes)
