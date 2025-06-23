from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from connection_manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"📩 {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("🚫 Пользователь отключился")
