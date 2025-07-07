# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo", version="1.0")

@mcp.tool
def echo(text: str) -> str:
    return text

@mcp.tool
def add(a: float, b: float) -> float:
    return a + b

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", "5000")), path="/mcp")
