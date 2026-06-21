from core import redis_client
import asyncio
import base64

def whisper_model():
    pass

async def voice_to_text():

    while True:
        try:
            messages = await redis_client.xreadgroup(
                groupname="stt_group",
                consumername="worker_1",
                streams={"audio_stream": ">"},
                count=1,
                block=5000
            )

            if not messages:
                continue

            for stream, msgs in messages:
                for msg_id, data in msgs:

                    audio = base64.b64decode(data[b"audio"])

                    # NON-BLOCKING whisper call
                    text = await asyncio.to_thread(
                        whisper_model,
                        audio
                    )

                    await redis_client.xadd(
                        "transcription_stream",
                        {
                            "session_id": data[b"session_id"],
                            "text": text
                        }
                    )

                    await redis_client.xack(
                        "audio_stream",
                        "stt_group",
                        msg_id
                    )

        except Exception as e:
            print("Worker error:", e)
            await asyncio.sleep(1)