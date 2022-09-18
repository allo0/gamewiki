from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class GoogleEmailSignin():
    kind: str
    localId: str
    email: str
    displayName: str
    idToken: str
    registered: str
    refreshToken: str
    expiresIn: str

    def __init__(self, kind, localId, email, displayName, idToken, registered, refreshToken, expiresIn):
        self.kind = kind
        self.localId = localId
        self.displayName = displayName
        self.registered = registered
        self.refreshToken = refreshToken
        self.expiresIn = expiresIn
        self.idToken = idToken
        self.email = email


class GoogleEmailSignup(BaseModel):
    idToken: str
    email: str
    refreshToken: str
    expiresIn: str
    localId: str


class GoogleEmailRequest(BaseModel):
    email: str = "ias.topalidis@gmail.com"
    password: str = "mao2mao"
    returnSecureToken: bool = True
