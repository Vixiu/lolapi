from lcu_driver import Connector
connector = Connector()

async def get_summoner_data(connection):
  summoner = await connection.request('GET', '/lol-summoner/v1/current-summoner')
  data = await summoner.json()
  print(f"summonerName:    {data['displayName']}")
  print(f"summonerLevel:   {data['summonerLevel']}")
  print(f"profileIconId:   {data['profileIconId']}")
  print(f"summonerId:      {data['summonerId']}")
  print(f"puuid:           {data['puuid']}")
  print(f"---")

@connector.ready
async def connect(connection):
    await get_summoner_data(connection)

connector.start()