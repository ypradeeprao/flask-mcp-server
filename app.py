from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/mcp/initialize", methods=["POST"])
def mcp_initialize():
    data = request.json
    return jsonify({
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {
            "capabilities": {
                "name": "MCP Demo Tool",
                "version": "1.0",
                "methods": {
                    "echo": {
                        "description": "Echo back the input text",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"}
                            },
                            "required": ["text"]
                        }
                    },
                    "add": {
                        "description": "Add two numbers",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "number"},
                                "b": {"type": "number"}
                            },
                            "required": ["a", "b"]
                        }
                    }
                }
            }
        }
    })

@app.route("/mcp/execute", methods=["POST"])
def mcp_execute():
    data = request.json
    method = data.get("params", {}).get("method")
    args = data.get("params", {}).get("args", {})
    request_id = data.get("id")

    if method == "echo":
        return jsonify({"jsonrpc": "2.0", "id": request_id, "result": {"echo": args.get("text", "")}})
    elif method == "add":
        try:
            a = float(args.get("a"))
            b = float(args.get("b"))
            return jsonify({"jsonrpc": "2.0", "id": request_id, "result": {"sum": a + b}})
        except Exception as e:
            return jsonify({"jsonrpc": "2.0", "id": request_id, "error": str(e)})
    else:
        return jsonify({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}})

if __name__ == "__main__":
    import sys
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 5000))
    app.run(host="0.0.0.0", port=port)
