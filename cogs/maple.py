import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from src.constant import level_mapping, job_url

class Mob(discord.ui.View):
    def __init__(self, mob, index = 0) -> None:
        super().__init__()
        self.mob = mob
        self.index = index

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.index > 0:
            self.index -= 1
        await self.callback(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.index + 1 < len(self.mob):
            self.index += 1
        await self.callback(interaction)

    async def callback(self, interaction: discord.Interaction):
        id = self.mob[self.index][0]
        embed = discord.Embed(
            title=f"{self.mob[self.index][1]} {self.index+1}/{len(self.mob)}", description=f"[更多詳細資訊](https://maplestory.wiki/TWMS/256/mob/{id})", color=0xBEBEFE
        )
        embed.add_field(name="", value=formatted_mob_info(self.mob[self.index]), inline=False)
        embed.set_thumbnail(url=f"https://maplestory.io/api/TWMS/256/mob/{self.mob[self.index][0]}/icon")
        await interaction.response.edit_message(embed=embed, view=self, content=None)


def formatted_mob_info(mob):
    result = []
    result.append(f"ID: {mob[0]}")
    result.append(f"等級: {mob[3]}")
    result.append(f"Boss: {'否' if not mob[4] else '是'}")
    result.append(f"碰撞傷害: {'否' if not mob[5] else '是'}")
    result.append(f"HP: {mob[6]}")
    result.append(f"速度: {mob[7]}")
    result.append(f"物防: {mob[8]}")
    result.append(f"魔防: {mob[9]}")
    result.append(f"命中率: {mob[10]}")
    result.append(f"迴避率: {mob[11]}")
    result.append(f"經驗值: {mob[12]}")
    return "\n".join(result)

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
    
    @maple.command(name="mob", description="取得怪物資訊")
    @app_commands.describe(
        name="怪物名稱"
    )
    async def mob(self, context: Context, name: str) -> None:
        mob = await self.bot.database.select("maple_mob", "*", name = name)
        if not mob:
            embed = discord.Embed(
                title="查無搜尋結果", description="請輸入正確怪物名稱", color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            buttons = Mob(mob)
            id = mob[0][0]
            embed = discord.Embed(
                title=f"{name} 1/{len(mob)}", description=f"[更多詳細資訊](https://maplestory.wiki/TWMS/256/mob/{id})", color=0xBEBEFE
            )
            embed.add_field(name="", value=formatted_mob_info(mob[buttons.index]), inline=False)
            embed.set_thumbnail(url=f"https://maplestory.io/api/TWMS/256/mob/{id}/icon")
            await context.send(embed=embed, view=buttons)

async def setup(bot) -> None:
    await bot.add_cog(Maple(bot))
