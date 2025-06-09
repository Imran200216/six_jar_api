from pydantic import BaseModel

class SignInModel(BaseModel):
    identityToken: str