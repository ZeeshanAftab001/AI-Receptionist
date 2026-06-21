from fastapi import APIRouter,Response,status



agent_router=APIRouter(prefix="/agent",tags=["agent"])

@agent_router.post("/process/voice")
async def process_voice():
    return Response("voice processed successfully!",status_code=status.HTTP_200_OK)