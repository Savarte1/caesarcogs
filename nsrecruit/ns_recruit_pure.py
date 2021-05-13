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

    h = await nsapi("happenings", limit=str(15+len(done)*15), filter='founding')
    events = x2d.parse(pretty_string(h))["WORLD"]["HAPPENINGS"]["EVENT"]

    nations, e_iter = list(), events.__iter__()
    new = lambda: e_iter.__next__()['TEXT'].split("@@")[1]
    nation = new()
    for n in range(8):
        try:
            while nope(nation): nation = new()
        except (StopIteration, RuntimeError): break
        (done.append(nation), nations.append(nation))
    assert nations
    return await channel.send(', '.join(nations))

@client.event
async def on_ready():print('running.')
async def review(channel, e):
    e.title, d_iter = "Run out of noobs.", done.__iter__()
    for i in range(len(done)//8+1):
      try:
        e.add_field(name=str(i+1), value=', '.join([d_iter.__next__()for _ in range(8)]), inline=False)
      except StopIteration:
        e.add_field(name=str(len(done)//8+1), value=', '.join(done[-(len(done)%8):]), inline=False)
    await channel.send(embed=e)

@client.event
async def on_message(message):
  if message.content.startswith('!'):
    if message.content[1:].startswith("recruit"):
      try: await recruit(message.channel)
      except:
          await review(message.channel, __import__('discord').Embed(color=0xff6600))
    else: print(message.content[1:], 'is not a command')
