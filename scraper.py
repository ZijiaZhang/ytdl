"""
This file is inspired by the work of HermanFassett,  https://github.com/HermanFassett/youtube-scrape/blob/master/scraper.js
"""

import json
import re

import requests


def parseChannelRenderer(channelRenderer):
    return {
        "id": channelRenderer["channelId"],
        "title": channelRenderer["title"]["simpleText"],
        "url": f"https://www.youtube.com{channelRenderer['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
        "thumbnail_src": channelRenderer["thumbnail"]["thumbnails"][-1]["url"]
    }


def parseVideoRenderer(videoRenderer):
    video = {
        "id": videoRenderer["videoId"],
        "title": ''.join(map(lambda x: ''.join(x.values()), videoRenderer['title']['runs'])),
        "url": f"https://www.youtube.com{videoRenderer['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
        "duration": videoRenderer['lengthText']['simpleText'] if videoRenderer.get('lengthText', None) else "Live",
        "upload_date": videoRenderer['publishedTimeText']['simpleText'] if videoRenderer.get('publishedTimeText') else "Live",
        "thumbnail_src": videoRenderer['thumbnail']['thumbnails'][-1]['url'],
        "views": videoRenderer['viewCountText']['simpleText'] if 'simpleText' in videoRenderer['viewCountText'] else ''.join(map(lambda x: ''.join(x.values()), videoRenderer['viewCountText']['runs'])) if videoRenderer.get('viewCountText', None) else "0"
    }

    uploader  = {
        "username": videoRenderer['ownerText']['runs'][0]['text'],
        "url": f"https://www.youtube.com{videoRenderer['ownerText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}"
    }

    return { "video": video, "uploader": uploader }


def parseRadioRenderer(radioRenderer):
    raise Exception('Not Implement')


def parsePlaylistRenderer(playlistRenderer):
    video = {
        "id": playlistRenderer["playlistId"],
        "title": playlistRenderer['title']['simpleText'],
        "url": f"https://www.youtube.com{playlistRenderer['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}",
        "thumbnail_src": playlistRenderer["thumbnailRenderer"]["playlistVideoThumbnailRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
    }

    uploader = {
        "username": playlistRenderer["shortBylineText"]["runs"][0]["text"],
        "url": f"https://www.youtube.com{playlistRenderer['shortBylineText']['runs'][0]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']}"
    }

    return {"video": video, "uploader" :uploader}


def parseJsonFormat(contents, json_data):
    for sectionList in contents:
        try:
            if "itemSectionRenderer" in sectionList:
                for content in sectionList.get("itemSectionRenderer",{}).get("contents", {}):
                    try:
                        if "channelRenderer" in content:
                            json_data["results"].append(parseChannelRenderer(content["channelRenderer"]))
                        if "videoRenderer" in content:
                            json_data["results"].append(parseVideoRenderer(content["videoRenderer"]))

                        # if "radioRenderer" in content:
                        #     json_data["results"].append(parseRadioRenderer(content["radioRenderer"]))

                        if "playlistRenderer" in content:
                            json_data["results"].append(parsePlaylistRenderer(content["playlistRenderer"]))

                    except Exception as ex:
                        print("Failed to parse renderer:", ex)

            elif "continuationItemRenderer" in sectionList:
                json_data["nextPageToken"] = sectionList["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]

        except Exception as ex:
            print("Failed to read contents for section list:", ex)


if __name__ == '__main__':
    json_data = { "results": []}
    query = 'music 2020'
    url = f'https://www.youtube.com/results?q={query}'
    request = requests.get(url)
    if (request.status_code == 200):
        text = request.text
        # json = request.json()
        json_data["parser"] = "json_format"
        json_data["key"] = re.search(r"\"innertubeApiKey\":\"([^\"]*)\"", text)[1]
        data = []
        sectionLists = []
        try:
            match = re.search(r"ytInitialData[^{]*(.*\"adSafetyReason\":[^;]*});", text)
            if match and match.lastindex >= 1:
                json_data["parser"] += ".object_var"
            else:
                json_data["parser"] += ".original"
                match = re.search(r'ytInitialData"[^{]*(.*);\s*window\["ytInitialPlayerResponse"\]', text)

            data = json.loads(match[1])
            json_data["estimatedResults"] = data.get("estimatedResults", 0)
            sectionLists = data.get(
                "contents", {}) .get(
                "twoColumnSearchResultsRenderer",{}).get(
                "primaryContents", {}).get(
                "sectionListRenderer", {}).get(
                "contents", {})
        except Exception as e:
            print(e)

        parseJsonFormat(sectionLists, json_data)

    print(json_data)

def search(query):
    json_data = { "results": []}
    url = f'https://www.youtube.com/results?q={query}'
    request = requests.get(url)
    if (request.status_code == 200):
        text = request.text
        # json = request.json()
        json_data["parser"] = "json_format"
        json_data["key"] = re.search(r"\"innertubeApiKey\":\"([^\"]*)\"", text)[1]
        data = []
        sectionLists = []
        try:
            match = re.search(r"ytInitialData[^{]*(.*\"adSafetyReason\":[^;]*});", text)
            if match and match.lastindex >= 1:
                json_data["parser"] += ".object_var"
            else:
                json_data["parser"] += ".original"
                match = re.search(r'ytInitialData"[^{]*(.*);\s*window\["ytInitialPlayerResponse"\]', text)

            data = json.loads(match[1])
            json_data["estimatedResults"] = data.get("estimatedResults", 0)
            sectionLists = data.get(
                "contents", {}) .get(
                "twoColumnSearchResultsRenderer",{}).get(
                "primaryContents", {}).get(
                "sectionListRenderer", {}).get(
                "contents", {})
        except Exception as e:
            print(e)

        parseJsonFormat(sectionLists, json_data)

    return json_data