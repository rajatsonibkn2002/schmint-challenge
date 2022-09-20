import discord, json, requests


serverID = 1021365176387260416
roles = {
            1: 1021417414757462069,  #Schmint
            2: 1021417513587838986,  #OG
            3: 1021417474958303374   #Simplr
        }

from discord.ext import tasks

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        self.myLoop.start()

    @tasks.loop(seconds = 10) # repeat after every 10 seconds
    async def myLoop(self):
        print("Started")
        server = client.get_guild(serverID)

        url = "http://127.0.0.1:8000/api/roles"
        response = json.loads(requests.get(url).text)
        for r in response:
            if not r['assigned']:                
                for member in server.members:
                    if(f'{member.name}#{str(member.discriminator)}' == r['discord']):
                        role = server.get_role(roles[r['tokenId']])
                        try:
                            await member.add_roles(role)
                        except Exception as e:
                            print(e)

                        patchjson = {'assigned': True}
                        response = requests.patch(f"{url}/{r['id']}", data=patchjson)
                        print(f"Role {role} assigned to {member}")



intents = discord.Intents.all()
intents.members = True
client = MyClient(intents=intents)
client.run('MTAyMTM2NjAxNTA4MDI2Nzg2Ng.GbAqpX.80FICkIJkt_dobaemp-tUeA8zMqgZmEXgO3mMo')