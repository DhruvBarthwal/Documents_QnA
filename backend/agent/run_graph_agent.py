from agent.graph import build_graph
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    graph = build_graph()

    while True:
        query = input("\nAsk a question (or 'exit'): ")
        if query.lower() == "exit":
            break

        result = graph.invoke({
            "query": query,
            "contexts": [],
            "answer": ""
        })

        print("\nAnswer:\n", result["answer"])