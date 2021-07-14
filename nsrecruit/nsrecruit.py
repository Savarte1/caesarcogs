from redbot.core import commands
from sans.api import Api as nsapi
from sans.utils import pretty_string
import xmltodict as x2d
#import json, sans

class NSRecruit(commands.Cog):
    """NSRecruiter"""
    nsapi.agent = "CAESAR, by Artevenia"

    done=[]
    def complete(self, other):
        self.done.append(other)
        return 1

    def nope(self, nation):
        if any([t.isdigit()for t in nation]) or nation in self.done:
            return 1

    @commands.command()
    async def recruit(self, ctx):
        """Gives a list of up to 8 nations to send recruitment telegrams"""

        h = await nsapi("happenings", limit="100", filter='founding')
        events = x2d.parse(pretty_string(h))["WORLD"]["HAPPENINGS"]["EVENT"]

        nations, e_iter = list(), events.__iter__()
        nation = e_iter.__next__()

        for n in range(8):
            while self.nope(nation):
              nation = e_iter.__next__()['TEXT'].split("@@")[1]
            self.complete(nation) and nations.append(nation)

        await ctx.send(', '.join(nations))
