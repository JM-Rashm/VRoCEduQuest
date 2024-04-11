
from src import create_app
from flask_cors import CORS

appInstance = create_app()
app = appInstance['app']
config = appInstance['config']

CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug= config.DEBUG)

