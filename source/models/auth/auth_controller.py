import os
from config.circuitConf import circuit_conf
from config.loggingConf import LogConfig
import logging
from logging.config import dictConfig

import firebase_admin
from fastapi import Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials

cred = credentials.Certificate("account_key.json")
firebase_admin.initialize_app(cred)

dictConfig(LogConfig().dict())
logger = logging.getLogger("gamewiki")
logging.basicConfig(filename='test.log', filemode='w',
                    encoding='utf-8', format=LogConfig().LOG_FORMAT,
                    )

def get_user(res: Response, cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token