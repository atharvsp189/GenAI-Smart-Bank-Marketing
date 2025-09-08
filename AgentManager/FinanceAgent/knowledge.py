from ..Knowledge import indexer
from AgentManager.log import logger

class get_knowledge():
    def __init__(self):
        pass
    
    def search_past_resolutions(self, query: str):
        try:
            logger.info("Knowledge agent has been called")
            results = indexer.retriever.invoke(query)
            logger.info(f"Searching past resolutions for Query: {query}")
        
            # for i, doc in enumerate(results, 1):
            #     print(f"\n🔹 Result {i}: ")
            #     print(doc)   # show first 500 chars
            #     print("Metadata:", doc.metadata)
            return {
                "content": results[0].page_content,
                "source": results[0].metadata['source'],
                "title": results[0].metadata['title']
            }
        except Exception as e:
            return f"An error occurred during retrieval: {str(e)}"


if __name__ == "__main__":
    query = "persnonal loan from state bank of india"
    k = get_knowledge()
    print(k.search_past_resolutions(query))
