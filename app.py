from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
CORS(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # GraphiQL interface untuk testing
    )
)

@app.route('/')
def index():
    return '''
    <h1>API GraphQL Manajemen Pinjam Buku</h1>
    <p>Akses GraphiQL interface di: <a href="/graphql">/graphql</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
