import sys
import os
import asyncio
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

async def run_chat_loop():
    load_dotenv()
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    server_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "server.py"))
    
    print("Booting up EnterpriseWorkflowServer")
    
    client = MultiServerMCPClient({
        "EnterpriseWorkflowServer": {
            # Use sys.executable to guarantee we use the venv Python
            "command": sys.executable,
            "args": [server_script],
            "transport": "stdio",
            "env": dict(os.environ),
        }
    })
    
    try:
        tools = await client.get_tools()
        print(f"Tools successfully loaded: {[t.name for t in tools]}")
    except Exception as e:
        print(f"\nCritical failure connecting to server: {e}")
        return

    agent = create_react_agent(llm, tools=tools)

    print("\n" + "="*50)
    print("MCP Agent Initialized. Type 'exit' or 'quit' or 'stop' to stop.")
    print("="*50)

    while True:
        try:
            user_query = input("\nYou: ")
        except EOFError:
            break

        if user_query.lower() in ['exit', 'quit', 'stop']:
            print("Shutting down agent...")
            break
            
        if not user_query.strip():
            continue

        print("\n[Agent is thinking...]")
        
        async for event in agent.astream({"messages": [("user", user_query)]}):
            for node, values in event.items():
                if node == "tools":
                    print(f"[Executing Tool]: {values['messages'][-1].name}")
                elif node == "agent":
                    message = values["messages"][-1]
                    if message.content:
                        print(f"[Agent]: {message.content}")

if __name__ == "__main__":
    asyncio.run(run_chat_loop())