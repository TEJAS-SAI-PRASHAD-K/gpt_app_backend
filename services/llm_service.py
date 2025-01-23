import google.generativeai as genai
from ..config import Settings

class LLM_Service:
    def __init__(self):
        settings = Settings()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    def generate_response(self, query: str, search_results: list[dict]):
        # Create context text from search results
        context_text = "\n\n".join([
            f"Source {i+1} {result['url']}:\n {result['content']}"
            for i, result in enumerate(search_results)
        ])
        
        # Create the prompt using f-string for proper variable interpolation
        prompt = f"""
Given the following context from web search results:
{context_text}

Query: {query}

Please provide a comprehensive response that:
1. Directly addresses the query using primarily information from the provided context
2. Analyzes the information step-by-step, showing your reasoning
3. Cites specific parts of the context to support key points (use [Source X] format)
4. Notes any important gaps or uncertainties in the context
5. Only draws from general knowledge when the context is insufficient, explicitly noting when doing so
6. Synthesizes the information into clear, logically organized sections
7. Provides a clear summary of key findings at the end

Remember to use inline citations [Source X] when referencing specific information from the context.
"""
        
        try:
            response = self.model.generate_content(prompt, stream = True)
            for pieces in response:
                yield pieces.text
        except Exception as e:
            return f"Error generating response: {str(e)}"