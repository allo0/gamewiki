from typing import List, Optional

import httpx
from fastapi import APIRouter, Query, Path
from igdb.wrapper import IGDBWrapper

from config.appConf import Settings
from source.models.igdb.igdb_model import GenreType, GameDetails, ListGameDetails

wrapper = IGDBWrapper(Settings.TWITCH_CLIENT_ID, Settings.TWITCH_CLIENT_SECRET)

igdbRouter = APIRouter(
    tags=["IGDB APIs functionality"
          ])


async def get_token():
    client = httpx.Client()
    reqUrl = "https://id.twitch.tv/oauth2/token?client_id=" + Settings.TWITCH_CLIENT_ID + "&client_secret=" + Settings.TWITCH_CLIENT_SECRET + "&grant_type=client_credentials"
    headersList = {
        "Accept": "*/*",
    }

    payload = ""

    data = client.post(reqUrl, headers=headersList)

    return data.json()["access_token"]


@igdbRouter.get("/genres")
async def get_genres():
    access_token = await get_token()

    client = httpx.Client()
    reqUrl = "https://api.igdb.com/v4/genres"

    headersList = {
        "Accept": "*/*",
        "Authorization": "Bearer " + access_token,
        "Client-ID": Settings.TWITCH_CLIENT_ID,
        "Content-Type": "text/plain"
    }

    payload = "fields name,slug,url;limit 100;sort id asc;"

    data = client.post(reqUrl, data=payload, headers=headersList)

    return data.json()


@igdbRouter.post("/suggestions")
async def get_suggestions(limit: int = Query(title="The ID of the item to get", le=500), genres: List[GenreType] = Query(...)):
    access_token = await get_token()
    genres = [genre.value for genre in genres]

    client = httpx.Client()
    reqUrl = "https://api.igdb.com/v4/games"

    headersList = {
        "Accept": "*/*",
        "Authorization": "Bearer " + access_token,
        "Client-ID": Settings.TWITCH_CLIENT_ID,
        "Content-Type": "text/plain"
    }

    payload = "fields cover,genres,name,platforms,similar_games,summary,total_rating,url;where genres=" + str(
        genres) + ";limit " + str(limit) + ";"

    data = client.post(reqUrl, data=payload, headers=headersList)

    game_details_list = ListGameDetails()
    games = data.json()
    for game in games:
        try:
            game_details = GameDetails()

            game_details.id = game['id']
            game_details.name = game['name']
            game_details.summary = game['summary']
            # game_details.total_rating = game['total_rating']
            # game_details.genres = game['genres']
            game_details.url = game['url']

            # Get Image URL (cover)
            reqUrl = "https://api.igdb.com/v4/covers"
            payload = "fields alpha_channel,animated,checksum,game,height,image_id,url,width;where game=" + str(
                game['id']) + ";limit " + str(limit) + ";"

            data = client.post(reqUrl, data=payload, headers=headersList)
            data = data.json()
            for dt in data:
                game_details.cover = dt['url']

            # Get Image URL (screenshots)
            reqUrl = "https://api.igdb.com/v4/screenshots"
            payload = "fields alpha_channel,animated,checksum,game,height,image_id,url,width;where game=" + str(
                game['id']) + ";limit " + str(limit) + ";"

            data = client.post(reqUrl, data=payload, headers=headersList)
            data = data.json()

            for image in data:
                game_details.screenshots.append(image['url'])

            game_details_list.list_of_games.append(game_details)
        except KeyError:
            pass

    return game_details_list
