from sans.api import Api as nsapi
from sans.utils import pretty_string
import xmltodict as x2d
client=__import__('discord').Client()
nsapi.agent = "CAESAR, by Artevenia"

done = []
def nope(nation):
    if any([t.isdigit()for t in nation]) or nation in done:
          return 1
    if not nation or nation.__class__.__name__ == 'OrderedDict':
          return 2
    else: return 0

async def recruit(channel):
    """Gives a list of up to 8 nations to send recruitment telegrams"""

    h = await nsapi("happenings", limit=str(), filter='founding')
    events = x2d.parse(pretty_string(h))["WORLD"]["HAPPENINGS"]["EVENT"]

    nations, e_iter = list(), events.__iter__()
    new = lambda: e_iter.__next__()['TEXT'].split("@@")[1]
    nation = new()
    for n in range(8):
        while nope(nation): nation = new()
        (done.append(nation), nations.append(nation))
    print(nations)
    return await channel.send(', '.join(nations))

@client.event
async def on_ready():print('running.')

@client.event
async def on_message(message):
  if message.content.startswith('!'):
    if message.content[1:].startswith("recruit"):
      await recruit(message.channel)
    else: print(message.content[1:], 'is not a command')
