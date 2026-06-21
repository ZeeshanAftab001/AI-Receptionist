from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core import redis_client
import base64
import asyncio
import uuid

agent_router = APIRouter(prefix="/agent", tags=["agent"])


# -------------------------
# SEND AI RESPONSE TO USER
# -------------------------
async def sender(websocket, session_id):

    last_id = "0"

    while True:
        messages = await redis_client.xread(
            {"tts_stream": last_id},
            block=5000
        )

        if not messages:
            continue

        for stream, msgs in messages:
            for msg_id, data in msgs:

                last_id = msg_id

                audio = base64.b64decode(data[b"audio"])

                await websocket.send_bytes(audio)


# -------------------------
# RECEIVE USER AUDIO
# -------------------------
async def receiver(websocket, session_id):

    while True:
        audio_chunk = await websocket.receive_bytes()

        await redis_client.xadd(
            "audio_stream",
            {
                "session_id": session_id,
                "audio": base64.b64encode(audio_chunk)
            }
        )


# -------------------------
# MAIN WEBSOCKET ROUTE
# -------------------------
@agent_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    session_id = str(uuid.uuid4())
    try:
        sender_task = asyncio.create_task(sender(websocket, session_id))
        receiver_task = asyncio.create_task(receiver(websocket, session_id))

        await asyncio.gather(sender_task, receiver_task)

    except WebSocketDisconnect:
        print("Client disconnected")