import asyncio
from fastapi import FastAPI, WebSocket

from .services.llm_service import LLM_Service

from .pydantic_models.chat_body import chatBody
from .services.sort_source_service import SortSourceService
from .services.search_service import SearchService

app = FastAPI()
search_service = SearchService()
sort_source_service = SortSourceService()
llmservice = LLM_Service()

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        await asyncio.sleep(0.1)
        data = await websocket.receive_json()
        query = data.get("query")

        search_results = search_service.web_search(query)
        sorted_results = sort_source_service.sort_sources(query,search_results)
        await asyncio.sleep(0.1)
        await websocket.send_json({
            "type" : "search_results",
            "data" : sorted_results
        })
        for pieces in llmservice.generate_response(query,sorted_results):
            await asyncio.sleep(0.1)
            await websocket.send_json({
            "type" : "content",
            "data" : pieces
        })
    
    except:
        print ("Unexpected error occurred")
    finally:
        await websocket.close()

@app.post("/chat")
async def chat_endpoint(body: chatBody):
    search_results = search_service.web_search(body.query)
    sorted_results = sort_source_service.sort_sources(body.query,search_results)

    for pieces in llmservice.generate_response(body.query,sorted_results):
        await asyncio.sleep(0.1)
        await WebSocket.send_json({
            'type' : "content",
            'data' : pieces
        })