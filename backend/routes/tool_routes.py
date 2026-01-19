from flask import Blueprint, request, jsonify
from services.tool_result_service import ToolResultService

tool_bp = Blueprint("tools", __name__)
tool_result_service = ToolResultService()

@tool_bp.route("/tools/result", methods=["POST"])
def submit_tool_result():
    data = request.json
    conversation_id = data.get("conversation_id")
    tool_name = data.get("tool_name")
    tool_output = data.get("tool_output")
    tool_call_id = data.get("tool_call_id")

    if not conversation_id or not tool_name or not tool_output:
        return jsonify({"error": "conversation_id, tool_name, and tool_output are required"}), 400

    message = tool_result_service.process_tool_result(conversation_id, tool_name, tool_output, tool_call_id)
    if not message:
        return jsonify({"error": "Conversation not found"}), 404
        
    return jsonify(message.to_dict())
