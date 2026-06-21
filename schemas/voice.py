from pydantic import BaseModel


class VoiceMeta(BaseModel):

    user_id : int
    desciption : str

