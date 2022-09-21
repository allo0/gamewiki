import aiohttp
import backoff
from fastapi import APIRouter, Depends, Response
from fastapi import HTTPException
from starlette.requests import Request

from config.appConf import Settings
from config.backoffConf import backoff_cnf
from source.models.auth.auth_controller import logger
from source.models.auth.steamsignin import SteamSignIn
from source.models.steam.steam_model import Welcome10
from utils.handlers import backoff_handlers

steamRouter = APIRouter(
    tags=["Steam APIs functionality"
          ])


@steamRouter.get("/steam_login")
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def steam_login(steam_signin: SteamSignIn = Depends(SteamSignIn)):
    url = steam_signin.ConstructURL(Settings.API_URL + '/v1/processlogin')
    logger.debug(url)
    return steam_signin.RedirectUser(url)


@steamRouter.get('/processlogin')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def steam_id(request: Request, steam_signin: SteamSignIn = Depends(SteamSignIn)):
    try:
        steam_id = steam_signin.ValidateResults(request.query_params)
        logger.debug("SteamID: {}\n".format(steam_id))
        if steam_id is False:
            raise HTTPException(status_code=417, detail="Expectation Failed")
        return {"steamId": steam_id}

    except Exception:
        raise HTTPException(status_code=418, detail="I am a Teapot")


@steamRouter.get('/user')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def get_player_summaries(steam_id: str):
    req_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + Settings.STEAM_API_KEY + "&steamids=" + steam_id

    async with aiohttp.ClientSession() as session:
        async with session.get(req_url) as resp:
            print(resp.json)
            try:

                obj = await resp.json()

                logger.debug(obj)
                if len(obj) == 0:
                    return HTTPException(status_code=400, detail="Empty object")
                return await obj

            except Exception as e:
                return await resp.json(content_type=None)


@steamRouter.get('/user_friendlist')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def get_friend_list(steam_id: str, relationship: str):
    req_url = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=" + Settings.STEAM_API_KEY + "&steamid=" + steam_id + "&relationship=" + relationship

    async with aiohttp.ClientSession() as session:
        async with session.get(req_url) as resp:
            try:
                obj = await resp.json()

                if len(obj) == 0:
                    return HTTPException(status_code=400, detail="Empty object")

                # friend_list = GetFriendList()
                friend_list = obj
                logger.debug(friend_list)
                return friend_list

            except Exception as e:
                return await resp.json()


@steamRouter.get('/user_achievements')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def get_player_achievements(steam_id: str, app_id: str = '440'):
    req_url = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid=" + app_id \
              + "&key=" + Settings.STEAM_API_KEY + "&steamid=" + steam_id

    async with aiohttp.ClientSession() as session:
        async with session.get(req_url) as resp:
            try:
                obj = await resp.json()
                if len(obj) == 0:
                    return HTTPException(status_code=400, detail="Empty object")
                # achievs = GetPlayerAchievements()
                achievs = obj
                logger.debug(achievs)
                return achievs

            except Exception as e:
                return await resp.json()


@steamRouter.get('/user_stats_for_game')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def get_user_stats_for_game(steam_id: str, app_id: str = '440'):
    req_url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=" + app_id \
              + "&key=" + Settings.STEAM_API_KEY + "&steamid=" + steam_id

    async with aiohttp.ClientSession() as session:
        async with session.get(req_url) as resp:
            try:
                obj = await resp.json()
                if len(obj) == 0:
                    return HTTPException(status_code=400, detail="Empty object")
                stats = obj
                logger.debug(stats)
                return stats

            except Exception as e:
                return await resp.json()


@steamRouter.get('/user_owned_games')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def get_owned_games(steam_id: str):
    req_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?&key=" + Settings.STEAM_API_KEY + "&steamid=" + steam_id + "&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(req_url) as resp:
            try:
                obj = await resp.json()
                if len(obj) == 0:
                    return HTTPException(status_code=400, detail="Empty object")
                games = obj
                logger.debug(games)
                return games

            except Exception as e:
                return await resp.json()


@steamRouter.get('/game_achievements')
@backoff.on_exception(backoff.expo,
                      HTTPException,
                      max_tries=backoff_cnf.MAX_RETRIES,
                      on_backoff=backoff_handlers.backoff_hdlr,
                      logger=logger
                      )
async def get_game_achievements(steam_id: str, app_id: str = '440'):
    req_url = "https://steamcommunity.com/profiles/" + steam_id + "/stats/" + app_id + "/achievements/?xml=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(req_url) as resp:
            try:

                logger.debug(resp)
                body = await resp.text()

                return Response(content=body, media_type="application/xml")

            except Exception as e:
                return e
