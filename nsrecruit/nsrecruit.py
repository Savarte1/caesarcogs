from redbot.core import commands
import sans
from sans.api import Api as nsapi
from sans.utils import pretty_string
import xmltodict
import json
import re

class NSRecruit(commands.Cog):
    """NSRecruiter"""
    
    nsapi.agent = "CAESAR, by Artevenia"

    @commands.command()
    async def recruit(self, ctx):
        """Gives a list of up to 8 nations to send recruitment telegrams"""
        def hasNumbers(inputString):
            return bool(re.search(r'\d', inputString))
            
        req = nsapi("happenings", limit="15", filter='founding')

        happenings = await req

        foundings = xmltodict.parse(pretty_string(happenings))

        nations = foundings["WORLD"]["HAPPENINGS"]["EVENT"]

        nation_string = ""

        nationnumber = 0

        for founding in nations:
            nation = founding['TEXT'].split("@@")
            if nationnumber == 8:
                break
            if not hasNumbers(nation[1]):
                nationnumber += 1
                nation_string += (nation[1] + ", ")

        
        await ctx.send(nation_string)