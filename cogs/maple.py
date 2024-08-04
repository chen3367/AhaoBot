import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from constant import level_mapping, job_url

def find_closest_greater_or_equal(nums, x):
    left, right = 0, len(nums) - 1
    result = None

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < x:
            left = mid + 1
        else:
            result = nums[mid]
            right = mid - 1

    return result

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
                title="Error",
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
        await context.send(job_url[job])

    @maple.command(name="leveling", description="練功地圖推薦")
    @app_commands.describe(
        level="角色等級"
    )
    async def leveling(self, context: Context, level: int) -> None:
        if level <= 0 or level > 300:
            embed = discord.Embed(
                title="Error",
                description="請輸入角色等級",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            levels = list(level_mapping.keys())
            closest_level = find_closest_greater_or_equal(levels, level)
            embed = discord.Embed(
                title="練功地圖推薦", description="參考: https://forum.gamer.com.tw/C.php?bsn=7650&snA=935239", color=0xBEBEFE
            )
            i = levels.index(closest_level)
            embed.add_field(name=f"{levels[i-1]+1}-{closest_level}等", value=level_mapping[closest_level], inline=False)
            image = discord.File(f"image/leveling/{closest_level}.png", filename=f"{closest_level}.png")
            embed.set_image(url=f"attachment://{closest_level}.png")
            await context.send(file=image, embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Maple(bot))
