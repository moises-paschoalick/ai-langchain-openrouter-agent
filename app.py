from flask import Flask
from flask_cors import CORS
from routes.chat_routes import chat_bp
from routes.thread_routes import thread_bp
from routes.tool_routes import tool_bp
from routes.dynamic_tool_routes import dynamic_tool_bp

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
app.register_blueprint(chat_bp)
app.register_blueprint(thread_bp)
app.register_blueprint(tool_bp)
app.register_blueprint(dynamic_tool_bp)

if __name__ == "__main__":
    app.run(debug=True)
