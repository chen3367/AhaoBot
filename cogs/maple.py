import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Maple(commands.Cog, name="maple"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="maple",
        description="Maplestory functions.",
    )
    async def maple(self, context: Context) -> None:
        """
        Maplestory functions.

        :param context: The hybrid command context.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

    @maple.command(name="jobtips", description="職業攻略")
    @app_commands.describe(
        job="職業名稱"
    )
    @app_commands.choices(job=[
         app_commands.Choice(name="夜使者", value="NightLord"),
         app_commands.Choice(name="暗影神偷", value="Shadower"),
         app_commands.Choice(name="影武者", value="DualBlade")
    ])
    async def jobtips(self, context: Context, job: str) -> None:
            url_dict = {
                 "NightLord": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1023760",
                 "Shadower": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1028659",
                 "DualBlade": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=999580"
            }
            await context.send(url_dict[job])

async def setup(bot) -> None:
    await bot.add_cog(Maple(bot))
