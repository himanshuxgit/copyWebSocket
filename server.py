from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Allow all origins for WebSocket connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected WebSocket clients
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Broadcast to all clients except sender
            for client in clients:
                if client != websocket:
                    await client.send_text(json.dumps(message, ensure_ascii=False))  # Preserve special characters
    
    except Exception as e:
        print(f"Client disconnected: {e}")
    
    finally:
        clients.remove(websocket)
