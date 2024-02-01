import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException
from flask_cors import CORS
from webargs import fields, validate
from webargs.flaskparser import FlaskParser
from neo4j import GraphDatabase
from dotenv import load_dotenv
from neo4j.exceptions import ClientError

load_dotenv()

app = Flask(__name__)
CORS(app)

class CustomFlaskParser(FlaskParser):
    def handle_error(self, error, req, schema, *, error_status_code, error_headers):
        message = error.messages
        status_code = error_status_code or 400
        response = jsonify({"error": message})
        response.status_code = status_code
        raise WerkzeugHTTPException(response=response)

parser = CustomFlaskParser()

node_args = {
    "document": fields.Str(required=True),
    "keywords": fields.List(fields.Str(), required=True),
    "source": fields.Str(allow_none=True),
    "trustworthiness": fields.Float(validate=validate.Range(min=0, max=1), required=True)
}

relationship_args = {
    "target_id": fields.Int(required=True),
    "weight": fields.Float(validate=validate.Range(min=0, max=1), required=True)
}

search_args = {
    "query": fields.Str(load_default=None),
    "keywords": fields.Str(load_default=None),
    "min_trustworthiness": fields.Float(validate=validate.Range(min=0, max=1), load_default=None),
    "regex": fields.Str(load_default=None)
}

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

@app.route('/nodes', methods=['POST'])
@parser.use_args(node_args, location="json")
def create_node(args):
    with driver.session() as session:
        params = ', '.join(f"{key}: ${key}" for key in args)
        query = f"CREATE (n:Node {{{params}}}) RETURN id(n)"
        node_id = session.run(query, args).single().value()
    return jsonify({"id": node_id}), 201

@app.route('/nodes/<id>', methods=['GET'])
def get_node(id):
    with driver.session() as session:
        result = session.run("MATCH (n:Node) WHERE id(n) = $id RETURN n", {"id": int(id)}).single()
        if result is None:
            return jsonify({'error': 'Node not found'}), 404
        node = result.value()
        node_properties = dict(node)
    return jsonify(node_properties)

@app.route('/nodes/<id>', methods=['PUT'])
@parser.use_args(node_args, location="json")
def update_node(args, id):
    with driver.session() as session:
        params = ', '.join(f"{key}: ${key}" for key in args)
        query = f"MATCH (n:Node) WHERE id(n) = $id SET n += {{{params}}} RETURN n"
        node = session.run(query, {"id": int(id), **args}).single().value()
        node_properties = dict(node)
    return jsonify(node_properties)

@app.route('/nodes/<id>', methods=['DELETE'])
def delete_node(id):
    with driver.session() as session:
        session.run("MATCH (n:Node) WHERE id(n) = $id DELETE n", {"id": int(id)})
    return '', 204

def build_search_where_clause(args):
    input_query = args.get('query')
    keywords = args.get('keywords')
    min_trustworthiness = args.get('min_trustworthiness')
    regex = args.get('regex')

    where_caluses = []
    params = {}
    if input_query:
        where_caluses.append("(n.document CONTAINS $query)")
        params["query"] = input_query
    if keywords:
        where_caluses.append(f"any(keyword IN n.keywords WHERE keyword IN $keywords)")
        params["keywords"] = keywords.split(",")
    if min_trustworthiness is not None:
        where_caluses.append(f"n.trustworthiness >= $min_trustworthiness")
        params["min_trustworthiness"] = min_trustworthiness
    if regex:
        where_caluses.append(f"(n.document =~ $regex)")
        params["regex"] = regex

    if not where_caluses:
        return jsonify({"error": "At least one of the following arguments must be provided 'query', 'keywords', 'regex', or 'min_trustworthiness'"}), 400

    return where_caluses, params

@app.route('/search', methods=['GET'])
@parser.use_args(search_args, location="query")
def search(args):
    where_caluses, params = build_search_where_clause(args)

    try:
        with driver.session() as session:
            query = f"""
                MATCH (n:Node)
                WHERE {" AND ".join(where_caluses)}
                RETURN id(n) as node_id, n as node
                ORDER BY n.trustworthiness DESC
            """
            print(query)
            print(params)
            nodes = session.run(query, params)
            nodes_properties = [{"node_id": record["node_id"], **record["node"]} for record in nodes]
    except ClientError as e:
        return jsonify({"error": e.message}), 400

    return jsonify(nodes_properties)

@app.route('/nodes/<id>/relationships', methods=['POST'])
@parser.use_args(relationship_args, location="json")
def create_relationship(args, id):
    with driver.session() as session:
        query = """
            MATCH (a:Node), (b:Node)
            WHERE id(a) = $id AND id(b) = $target_id
            MERGE (a)-[r:RELATED_TO]->(b)
            SET r.weight = $weight
            RETURN id(r) as relationship_id
        """
        relationship_id = session.run(query, {"id": int(id), **args}).single().value()
    return jsonify({"relationship_id": relationship_id}), 201

@app.route('/nodes/<id>/relationships', methods=['GET'])
def get_relationships(id):
    with driver.session() as session:
        query = """
            MATCH (n:Node)-[r]->(m)
            WHERE id(n) = $id
            RETURN id(r) as relationship_id, id(m) as node_id, r.weight as weight
        """
        relationships = session.run(query, {"id": int(id)})
        relationships_properties = [{"relationship_id": record["relationship_id"], "node_id": record["node_id"], "weight": record["weight"]} for record in relationships]
    return jsonify(relationships_properties)

@app.route('/relationships/<id>', methods=['DELETE'])
def delete_relationship(id):
    with driver.session() as session:
        query = """
            MATCH ()-[r]->()
            WHERE id(r) = $id
            DELETE r
            RETURN count(r) as deleted_count
        """
        deleted_count = session.run(query, {"id": int(id)}).single()["deleted_count"]
        if deleted_count == 0:
            return jsonify({"error": "Relationship not found"}), 404
    return jsonify({"message": "Relationship deleted successfully"}), 200

@app.route('/documentation', methods=['GET'])
def get_documentation():
    description = os.getenv("DESCRIPTION")
    name = os.getenv("NAME")
    return jsonify({"name": name, "description": description})

@app.route('/delete_all', methods=['DELETE'])
def delete_all():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    return jsonify({"message": "All nodes and relationships deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
