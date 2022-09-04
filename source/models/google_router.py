import json
import logging
import random

import aiohttp

import backoff
from circuitbreaker import circuit
from fastapi import APIRouter
from fastapi import HTTPException

from config.backoffConf import backoff_cnf
from config.circuitConf import circuit_conf
from source.models.auth.auth_controller import logger

from source.models.user.user_model import GoogleEmailRequest, GoogleEmailSignin
from utils.handlers import backoff_handlers, circuit_handlers

googleRouter = APIRouter(
    tags=["firebase signup/login functionality"],
    responses={200: {"description": "Response Successfull"},
               422: {"description": "Validation Error"}
               },
)


@googleRouter.post("/login")
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def login(info: GoogleEmailRequest):
    reqUrl = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyA9k-AJIRwa5IiB5o_aHecyCpM4hJxe9A0"

    headersList = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "email": info.email,
        "password": info.password,
        "returnSecureToken": info.returnSecureToken
    })

    async with aiohttp.ClientSession() as session:
        async with session.post(reqUrl, data=payload, headers=headersList) as resp:
            try:
                obj = await resp.json()
                logger.debug(obj)

                return GoogleEmailSignin(kind=obj["kind"], localId=obj["localId"],
                                         displayName=obj["displayName"], registered=obj["registered"],
                                         refreshToken=obj["refreshToken"], expiresIn=obj["expiresIn"],
                                         idToken=obj["idToken"], email=obj["email"])

            except Exception as e:
                return await resp.json()
