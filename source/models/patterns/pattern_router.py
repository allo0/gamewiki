import logging
import random
from logging.config import dictConfig

import backoff
from circuitbreaker import circuit
from fastapi import APIRouter
from fastapi import HTTPException

from config.backoffConf import backoff_cnf
from config.circuitConf import circuit_conf
from config.loggingConf import LogConfig
from utils.handlers import backoff_handlers, circuit_handlers

dictConfig(LogConfig().dict())
logger = logging.getLogger("gamewiki")
logging.basicConfig(filename='test.log', filemode='w',
                    encoding='utf-8', format=LogConfig().LOG_FORMAT,
                    )

patternRouter = APIRouter(
    tags=["Test patterns"],
    responses={400: {"description": "Circuit/Retry worked"},
               200: {"description": "Request OK"},
               503: {"description": "Circuit is Open or max tries for retry"}},
)


@patternRouter.get("/circuit")
@circuit(failure_threshold=circuit_conf.FAILURE_THRESHOLD,
         recovery_timeout=circuit_conf.RECOVERY_TIMEOUT,
         expected_exception=circuit_handlers.exception_condition,
         fallback_function=circuit_handlers.fallback_response
         )
def circuit_breaker():
    number = random.randint(0, 10)
    logger.debug(circuit_handlers.circuit_hdlr())

    if number % 2 == 0:
        raise HTTPException(status_code=400, detail="Item not found")
    else:
        return {"detail": "Item found"}


@patternRouter.get("/retry")
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def retry_pattern():
    number = random.randint(0, 10)
    if number % 2 == 0:
        raise HTTPException(status_code=400, detail="Item not found")
    else:
        return {"detail": "Item found"}


@patternRouter.get("/help")
async def help():
    return {"detail": "Send help"}

