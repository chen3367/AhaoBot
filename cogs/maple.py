import discord
import typing
import aiohttp, aiofiles
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
        description="楓之谷相關指令",
        hidden=True
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

    @maple.command(name="character_register", description="登錄角色(每個DC帳號最多登錄3隻)")
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
                myCharactor = Charactor()
                class_info = myCharactor.getClassInfo(class_name)
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

    @maple.command(name="character_update", description="更新能力值")
    @app_commands.describe(
        ign="遊戲ID",
        level="等級",
        attack="基礎攻擊",
        attack_p="攻擊力%",
        dmg_p="傷害%",
        boss_p="BOSS傷害%",
        strike_p="爆擊傷害%",
        ignore_p="無視防禦%",
        finaldmg_p="最終傷害%",
        str_clear="吃%STR",
        str_p="STR%",
        str_unique="不吃%STR",
        dex_clear="吃%DEX",
        dex_p="DEX%",
        dex_unique="不吃%DEX",
        int_clear="吃%INT",
        int_p="INT%",
        int_unique="不吃%INT",
        luk_clear="吃%LUK",
        luk_p="LUK%",
        luk_unique="不吃%LUK",
    )
    async def character_update(self, context: Context, ign: str, level: int, attack: int, attack_p: int, dmg_p: int, boss_p: int, strike_p: float,
                               ignore_p: float, finaldmg_p: int, str_clear: int, str_p: int, str_unique: int, dex_clear: int, dex_p: int, 
                               dex_unique: int, int_clear: int, int_p: int, int_unique: int, luk_clear: int, luk_p: int, luk_unique: int) -> None:
        try:
            args = {k:v for k, v in locals().items() if k not in ("self", "context", "ign")}
            search_result = await self.bot.database.select_one("discord_name", "maple_character", ign=ign)
            if not search_result:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 尚未登錄", color=0xE02B2B
                )
            elif search_result[0] != context.message.author.name and context.message.author.id != self.bot.owner_id:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 僅能由登錄者{search_result[0]}修改", color=0xE02B2B
                )
            elif any(arg < 0 for arg in args.values()):
                embed = discord.Embed(
                    title="錯誤", description="請輸入大於零的數字", color=0xE02B2B
                )
            else:
                set_statement = ",".join(f"{k}={v}" for k, v in args.items())
                await self.bot.database.update("maple_character", set_statement, ign=ign)
                embed = discord.Embed(
                    title="更新成功", description=f"遊戲ID:{ign}", color=0xBEBEFE
                )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(embed=embed, ephemeral=True)

    @maple.command(name="character_update_one", description="更新單項能力值")
    @app_commands.describe(
        ign="遊戲ID",
        item="更新項目",
        value="更新數值"
    )
    @app_commands.autocomplete(item=autocompletion_dict({k:v for k, v in var.DATA_MAPPING.items() if v != "ALL_P"}))
    async def character_update_one(self, context: Context, ign: str, item: str, value: float) -> None:
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
                await self.bot.database.update("maple_character", f"{item}={value}", ign=ign)
                if item not in ("STRIKE_P", "IGNORE_P"):
                    value = int(value)
                REVERSED_DATA_MAPPING = {val:key for key, val in var.DATA_MAPPING.items()}
                embed = discord.Embed(
                    title="更新成功", description=f"遊戲ID: {ign}\n更新項目: {REVERSED_DATA_MAPPING[item]}\n更新值: {value}", color=0xBEBEFE
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
                CLASS_NAME = var.CLASS_LIST[search_result[2]]
                embed = discord.Embed(title=f"{search_result[1]} ({CLASS_NAME})", description="", color=0xBEBEFE)
                embed.add_field(name="登錄者", value=search_result[0])
                embed.add_field(name="等級", value=search_result[3])
                embed.add_field(name="基礎攻擊", value=search_result[4])
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
                image = discord.File("image/thumbnail.png", filename="thumbnail.png")
                embed.set_thumbnail(url="attachment://thumbnail.png")
            await context.send(file=image, embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
            await context.send(embed=embed)

    @maple.command(name="calculate_ignore", description="計算無視")
    @app_commands.describe(
        ignore_original="原始無視%",
        ignore_extra="額外無視%",
    )
    async def calculate_ignore(self, context: Context, ignore_original: float, ignore_extra: float) -> None:
        try:
            if not (0 <= ignore_original <= 100 and 0 <= ignore_extra <= 100):
                embed = discord.Embed(
                    title="錯誤", description=f"輸入資料有誤", color=0xE02B2B
                )
            else:
                ignore_result = 1 - (1 - 0.01 * ignore_original) * (1 - 0.01 * ignore_extra)
                embed = discord.Embed(title="無視防禦", description=f"{ignore_original}% + {ignore_extra}% = {round(ignore_result*100, 2)}%", color=0xBEBEFE)
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(embed=embed, ephemeral=True)

    @maple.command(name="calculate_equivalent", description="計算等效數值")
    @app_commands.describe(
        ign="遊戲ID",
        item="計算項目",
        value="增加值",
        defense_p="怪物防禦%"
    )
    @app_commands.autocomplete(item=autocompletion_dict({k:v for k, v in var.DATA_MAPPING.items() if v != "LEVEL"}))
    async def calculate_equivalent(self, context: Context, ign: str, item: str, value: int, defense_p: int = 300) -> None:
        try:
            search_result = await self.bot.database.select_one("*", "maple_character", ign=ign)
            if not search_result:
                embed = discord.Embed(
                    title="錯誤", description=f"遊戲ID:'{ign}' 尚未登錄", color=0xE02B2B
                )
            else:
                myCharactor = Charactor()

                # 更新職業相關參數
                CLASS_NAME = var.CLASS_LIST[search_result[2]]
                myCharactor.updateAbilityByData(myCharactor.getClassInfo(CLASS_NAME))

                # 讀取DB資料，更新至myCharactor
                data = {
                    'LEVEL': search_result[3],
                    'ATTACK': search_result[4],
                    'ATTACK_P': search_result[5],
                    'DMG_P': search_result[6],
                    'BOSS_P': search_result[7],
                    'STRIKE_P': search_result[8],
                    'IGNORE_P': search_result[9],
                    'FINALDMG_P': search_result[10],
                    'DEFENSE_P': defense_p,
                    'STR_CLEAR': search_result[11],
                    'STR_P': search_result[12],
                    'STR_UNIQUE': search_result[13],
                    'DEX_CLEAR': search_result[14],
                    'DEX_P': search_result[15],
                    'DEX_UNIQUE': search_result[16],
                    'INT_CLEAR': search_result[17],
                    'INT_P': search_result[18],
                    'INT_UNIQUE': search_result[19],
                    'LUK_CLEAR': search_result[20],
                    'LUK_P': search_result[21],
                    'LUK_UNIQUE': search_result[22]
                }
                myCharactor.updateAbilityByData(data)

                # 計算等效數值
                new_data = {item:value*[1, 0.01][item.endswith("_P")]}
                result = {k:round(v*[1, 100][k.endswith("_P")], 3) for k, v in myCharactor.cal_Equivalent(new_data).items()}


                REVERSED_DATA_MAPPING = {val:key for key, val in var.DATA_MAPPING.items()}
                embed = discord.Embed(title=f"{search_result[1]} ({CLASS_NAME})", description=f"{value}{REVERSED_DATA_MAPPING[item]}=", color=0xBEBEFE)
                embed.add_field(name="基礎攻擊", value=result['ATTACK'])
                embed.add_field(name="攻擊力%", value=result['ATTACK_P'])
                embed.add_field(name="傷害%", value=result['DMG_P'])
                embed.add_field(name="BOSS傷%", value=result['BOSS_P'])
                embed.add_field(name="爆擊傷害%", value=result['STRIKE_P'])
                embed.add_field(name="無視防禦%", value=result['IGNORE_P'])
                # embed.add_field(name="最終傷害%", value=result['FINALDMG_P'])
                embed.add_field(name="STR", value=result['STR_CLEAR'])
                embed.add_field(name="STR%", value=result['STR_P'])
                embed.add_field(name="不吃%STR", value=result['STR_UNIQUE'])
                embed.add_field(name="DEX", value=result['DEX_CLEAR'])
                embed.add_field(name="DEX%", value=result['DEX_P'])
                embed.add_field(name="不吃%DEX", value=result['DEX_UNIQUE'])
                embed.add_field(name="INT", value=result['INT_CLEAR'])
                embed.add_field(name="INT%", value=result['INT_P'])
                embed.add_field(name="不吃%INT", value=result['INT_UNIQUE'])
                embed.add_field(name="LUK", value=result['LUK_CLEAR'])
                embed.add_field(name="LUK%", value=result['LUK_P'])
                embed.add_field(name="不吃%LUK", value=result['LUK_UNIQUE'])
                embed.add_field(name="全屬性%", value=result['ALL_P'])
                image = discord.File("image/thumbnail.png", filename="thumbnail.png")
                embed.set_thumbnail(url="attachment://thumbnail.png")
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )
        await context.send(file=image, embed=embed)

    @maple.command(name="change_thumbnail_by_attachment", hidden=True)
    @commands.is_owner()
    async def change_thumbnail_by_attachment(self, context: Context, image: discord.Attachment) -> None:
        try:
            await image.save("image/thumbnail.png")
            embed = discord.Embed(
                title="成功", description="", color=0xBEBEFE
            )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )            
        await context.send(embed=embed, ephemeral=True)

    @maple.command(name="change_thumbnail_by_url", hidden=True)
    @commands.is_owner()
    async def change_thumbnail_by_url(self, context: Context, url: str) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    async with aiofiles.open("image/thumbnail.png", 'wb') as f:
                        await f.write(await resp.read())
            embed = discord.Embed(
                title="成功", description="", color=0xBEBEFE
            )
        except Exception as e:
            embed = discord.Embed(
                title="錯誤", description=e, color=0xE02B2B
            )            
        await context.send(embed=embed, ephemeral=True)

async def setup(bot) -> None:
    await bot.add_cog(Maple(bot))