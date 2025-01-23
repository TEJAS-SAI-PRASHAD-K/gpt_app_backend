from ..config import Settings
from tavily import TavilyClient
import trafilatura

settings = Settings()
tavily_client = TavilyClient(api_key = settings.TAVILY_API_KEY)
class SearchService:
    def web_search(self,query:str):
        results = []
        response = tavily_client.search(query)
        search_results = response.get("results",[])
        
        for result in search_results:
            downloaded_content = trafilatura.fetch_url(result.get("url"))
            final_content = trafilatura.extract(downloaded_content,include_comments=False)
            results.append({
                "title": result.get("title",""),
                "url": result.get("url"),
                "content": final_content})
        
        return results