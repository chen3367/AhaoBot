import discord
import typing
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from src.maple import var
from src.maple.character import Charactor

class Mob(discord.ui.View):
    def __init__(self, mob, bot, index = 0) -> None:
        super().__init__()
        self.mob = mob
        self.bot = bot
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
        mob_id = self.mob[self.index][0]
        maps = await self.bot.database.select("b.*", "maple_mob_map a inner join maple_map b on a.map_id = b.id", mob_id = mob_id)
        embed = discord.Embed(
            title=f"{self.mob[self.index][1]} {self.index+1}/{len(self.mob)}", description=f"[更多詳細資訊](https://maplestory.wiki/TWMS/256/mob/{mob_id})", color=0xBEBEFE
        )
        embed.add_field(name="", value=formatted_mob_info(self.mob[self.index], maps), inline=False)
        embed.set_thumbnail(url=f"https://maplestory.io/api/TWMS/256/mob/{mob_id}/icon")
        await interaction.response.edit_message(embed=embed, view=self, content=None)

def autocompletion_dict(items: dict):
    async def getChoice(
            interaction: discord.Interaction,
            current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for name, value in items.items():
            if current in name:
                data.append(app_commands.Choice(name=name, value=value))
            if len(data) >= 25:
                break
        return data
    return getChoice

def autocompletion_list(items: list[str]):
    async def getChoice(
            interaction: discord.Interaction,
            current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for item in items:
            if current in item:
                data.append(app_commands.Choice(name=item, value=item))
            if len(data) >= 25:
                break
        return data
    return getChoice

def formatted_mob_info(mob, maps):
    result = []
    formatted_maps = "\n".join(f"[{_map[2]}: {_map[1]}](https://maplestory.wiki/TWMS/256/map/{_map[0]})" for _map in maps)
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
    result.append(f"出現地圖:\n{formatted_maps}")
    if len("\n".join(result)) <= 1024:
        return "\n".join(result)
    else:
        while len("\n".join(result)) > 1024 - 51 - len(str(mob[0])):
            last_occurence = result[-1].rindex("\n")
            result[-1] = result[-1][:last_occurence]
        result.append(f"...[更多地圖](https://maplestory.wiki/TWMS/256/mob/{mob[0]})")
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

    @maple.command(name="tips", description="實用攻略")
    async def tips(self, context: Context) -> None:
        embed = discord.Embed(
            title="實用攻略", description="來源: [巴哈姆特](https://forum.gamer.com.tw/B.php?bsn=7650)", color=0xBEBEFE
        )
        for title, url in var.TIPS.items():
            embed.add_field(name=title, value=url, inline=False)
        await context.send(embed=embed)
        
    @maple.command(name="jobtips", description="職業攻略")
    @app_commands.describe(
        job="職業名稱"
    )
    @app_commands.autocomplete(job=autocompletion_dict(var.JOB_TIPS))
    async def jobtips(self, context: Context, job: str) -> None:
        await context.send(job)

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
            levels = list(var.LEVEL_MAPPING.keys())
            closest_level = find_closest_greater_or_equal(levels, level)
            embed = discord.Embed(
                title="練功地圖推薦", description="參考: https://forum.gamer.com.tw/C.php?bsn=7650&snA=935239", color=0xBEBEFE
            )
            i = levels.index(closest_level)
            embed.add_field(name=f"{levels[i-1]+1}-{closest_level}等", value=var.LEVEL_MAPPING[closest_level], inline=False)
            image = discord.File(f"image/leveling/{closest_level}.png", filename=f"{closest_level}.png")
            embed.set_image(url=f"attachment://{closest_level}.png")
            await context.send(file=image, embed=embed)
    
    @maple.command(name="mob", description="取得怪物資訊")
    @app_commands.autocomplete(name=autocompletion_list(var.MOB_LIST))
    @app_commands.describe(
        name="怪物名稱"
    )
    async def mob(self, context: Context, name: str) -> None:
        mob = await self.bot.database.select("*", "maple_mob", name = name)
        if not mob:
            embed = discord.Embed(
                title="查無搜尋結果", description="請輸入正確怪物名稱", color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            buttons = Mob(mob, self.bot)
            mob_id = mob[0][0]
            maps = await self.bot.database.select("b.*", "maple_mob_map a inner join maple_map b on a.map_id = b.id", mob_id = mob_id)
            embed = discord.Embed(
                title=f"{name} 1/{len(mob)}", description=f"[更多詳細資訊](https://maplestory.wiki/TWMS/256/mob/{mob_id})", color=0xBEBEFE
            )
            embed.add_field(name="", value=formatted_mob_info(mob[buttons.index], maps), inline=False)
            embed.set_thumbnail(url=f"https://maplestory.io/api/TWMS/256/mob/{mob_id}/icon")
            await context.send(embed=embed, view=buttons)

    @maple.command(name="character_register", description="登錄角色")
    @app_commands.describe(
        ign="遊戲ID",
        class_name="職業名稱"
    )
    @app_commands.autocomplete(class_name=autocompletion_list(var.CLASS_LIST))
    async def character_register(self, context: Context, ign: str, class_name: str) -> None:
        try:
            search_result = await self.bot.database.select_one("discord_name", "maple_character", ign=ign)
            registered_count = await self.bot.database.select_one("COUNT(*)", "maple_character", discord_name=context.message.author.name)
            if search_result:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 已由{search_result[0]}登錄", color=0xE02B2B
                )
            elif registered_count[0] >= 3 and context.message.author.id != self.bot.owner_id:
                embed = discord.Embed(
                    title="錯誤", description="最多登錄3筆\n查詢已登錄角色: `/maple character_list`\n刪除已登錄角色: `/maple character_delete`", color=0xE02B2B
                )
            else:
                c = Charactor()
                class_info = c.getClassInfo(class_name)
                await self.bot.database.insert("maple_character",
                    discord_name=context.message.author.name,
                    ign=ign,
                    class_idx=class_info['CLASS_IDX'],
                )
                embed = discord.Embed(
                    title="登錄成功", description=f"遊戲ID: {ign}\n職業名稱: {class_name}", color=0xBEBEFE
                )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(embed=embed, ephemeral=True)

    @maple.command(name="character_update", description="更新角色資訊")
    @app_commands.describe(
        ign="遊戲ID",
        data="更新項目",
        value="更新數值"
    )
    @app_commands.autocomplete(data=autocompletion_dict(var.DATA_MAPPING))
    async def character_update(self, context: Context, ign: str, data: str, value: float) -> None:
        try:
            search_result = await self.bot.database.select_one("discord_name", "maple_character", ign=ign)
            if not search_result:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 尚未登錄", color=0xE02B2B
                )
            elif search_result[0] != context.message.author.name and context.message.author.id != self.bot.owner_id:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 僅能由登錄者{search_result[0]}修改", color=0xE02B2B
                )
            elif value < 0:
                embed = discord.Embed(
                    title="錯誤", description="請輸入大於零的數字", color=0xE02B2B
                )
            else:
                await self.bot.database.update("maple_character", f"{data}={value}", ign=ign)
                if data not in ("strike_p", "ignore_p"):
                    value = int(value)
                reversed_data_mapping = {val:key for key, val in var.DATA_MAPPING.items()}
                embed = discord.Embed(
                    title="更新成功", description=f"遊戲ID: {ign}\n更新項目: {reversed_data_mapping[data]}\n更新值: {value}", color=0xBEBEFE
                )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(embed=embed, ephemeral=True)

    @maple.command(name="character_delete", description="刪除角色")
    @app_commands.describe(
        ign="遊戲ID",
    )
    async def character_delete(self, context: Context, ign: str) -> None:
        try:
            search_result = await self.bot.database.select_one("discord_name", "maple_character", ign=ign)
            if not search_result:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 尚未登錄", color=0xE02B2B
                )
            elif search_result[0] != context.message.author.name and context.message.author.id != self.bot.owner_id:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 僅能由登錄者{search_result[0]}刪除", color=0xE02B2B
                )
            else:
                await self.bot.database.delete("maple_character", ign=ign)
                embed = discord.Embed(
                    title="刪除成功", description=f"遊戲ID:'{ign}' 已從清單上移除", color=0xBEBEFE
                )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(embed=embed, ephemeral=True)

    @maple.command(name="character_list", description="查詢已登錄角色")
    async def character_list(self, context: Context) -> None:
        try:
            registered_list = await self.bot.database.select("ign", "maple_character", discord_name=context.message.author.name)
            if not registered_list:
                embed = discord.Embed(
                    title="尚未登錄任何角色", description="登錄角色: `/maple character_register`", color=0xBEBEFE
                )
            else:
                igns = "\n".join(ign[0] for ign in registered_list)
                embed = discord.Embed(
                    title=f"{context.message.author.name}已登錄角色", description=igns, color=0xBEBEFE
                )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(embed=embed, ephemeral=True)
    
    @maple.command(name="character_info", description="角色詳細資訊")
    @app_commands.describe(
        ign="遊戲ID",
    )
    async def character_info(self, context: Context, ign: str) -> None:
        try:
            search_result = await self.bot.database.select_one("*", "maple_character", ign=ign)
            if not search_result:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 尚未登錄", color=0xE02B2B
                )
            else:
                c = Charactor()
                class_name = c.getClasslist()[search_result[2]]
                embed = discord.Embed(title=f"{search_result[1]} ({class_name})", description="", color=0xBEBEFE)
                embed.add_field(name="登錄者", value=search_result[0], inline=True)
                embed.add_field(name="等級", value=search_result[3])
                embed.add_field(name="基礎攻擊", value=search_result[4], inline=True)
                embed.add_field(name="攻擊力%", value=search_result[5])
                embed.add_field(name="傷害%", value=search_result[6])
                embed.add_field(name="BOSS傷害%", value=search_result[7])
                embed.add_field(name="爆擊傷害%", value=search_result[8])
                embed.add_field(name="無視防禦%", value=search_result[9])
                embed.add_field(name="最終傷害%", value=search_result[10])
                embed.add_field(name="吃%STR", value=search_result[11])
                embed.add_field(name="STR%", value=search_result[12])
                embed.add_field(name="不吃%STR", value=search_result[13])
                embed.add_field(name="吃%DEX", value=search_result[14])
                embed.add_field(name="DEX%", value=search_result[15])
                embed.add_field(name="不吃DEX", value=search_result[16])
                embed.add_field(name="吃%INT", value=search_result[17])
                embed.add_field(name="INT%", value=search_result[18])
                embed.add_field(name="不吃INT", value=search_result[19])
                embed.add_field(name="吃%LUK", value=search_result[20])
                embed.add_field(name="LUK%", value=search_result[21])
                embed.add_field(name="不吃LUK", value=search_result[22])
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
            await context.send(embed=embed, ephemeral=True)

async def setup(bot) -> None:
    await bot.add_cog(Maple(bot))