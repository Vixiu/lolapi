import asyncio
import willump

async def get_summoner_data():
    summoner = await (await wllp.request("GET", "/lol-summoner/v1/current-summoner")).json()
    print(f"summonerName:    {summoner['displayName']}")
    print(f"summonerLevel:   {summoner['summonerLevel']}")
    print(f"profileIconId:   {summoner['profileIconId']}")
    print(f"summonerId:      {summoner['summonerId']}")
    print(f"puuid:           {summoner['puuid']}")
    print(f"---")


async def main():
    global wllp
    wllp = await willump.start()
    await get_summoner_data()
    await wllp.close()

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()