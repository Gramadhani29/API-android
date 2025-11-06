from flask import Flask
from flask_cors import CORS
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from schema import schema

app = Flask(__name__)
CORS(app)

# GraphiQL Explorer Interface
explorer_html = ExplorerGraphiQL().html(None)

@app.route('/graphql', methods=['GET'])
def graphql_playground():
    return explorer_html, 200

@app.route('/graphql', methods=['POST'])
def graphql_server():
    from flask import request, jsonify
    
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route('/')
def index():
    return '''
    <h1>API GraphQL Manajemen Pinjam Buku</h1>
    <p>Akses GraphiQL interface di: <a href="/graphql">/graphql</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
