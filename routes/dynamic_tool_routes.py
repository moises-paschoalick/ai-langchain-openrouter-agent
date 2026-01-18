from flask import Blueprint, request, jsonify
from services.dynamic_tool_service import DynamicToolService

dynamic_tool_bp = Blueprint('dynamic_tool_bp', __name__)
tool_service = DynamicToolService()

@dynamic_tool_bp.route('/tools', methods=['POST'])
def create_tool():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    parameters = data.get('parameters')
    strict = data.get('strict', False)

    if not name or not description or not parameters:
        return jsonify({"error": "name, description, and parameters are required"}), 400

    tool = tool_service.register_tool(name, description, parameters, strict)
    return jsonify(tool.to_dict()), 201

@dynamic_tool_bp.route('/tools', methods=['GET'])
def list_tools():
    tools = tool_service.get_all_tools()
    return jsonify([t.to_dict() for t in tools])
