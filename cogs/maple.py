import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

def find_closest_greater_or_equal(nums, x):
    left, right = 0, len(nums) - 1
    result = None
    index = -1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] < x:
            left = mid + 1
        else:
            result = nums[mid]
            index = mid
            right = mid - 1

    return (result, index)

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
        url_dict = {
                "NightLord": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1023760",
                "Shadower": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1028659",
                "DualBlade": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=999580"
        }
        await context.send(url_dict[job])

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
            level_mapping = {
                0: None, 
                10: "[新手任務]",
                20: "[北部森林]綠樹的樹藤 風獨眼獸",
                46: "[沼地]危險的黑鱷魚 黑鱷魚",
                70: "[奇幻村]寧靜的沼澤 土龍",
                90: "[納西沙漠]沉睡沙漠 紅砂矮人  沙漠地鼠",
                102: "[神木村]天空之巢II [★]血腥哈維",
                121: "[玩具城]扭曲的迴廊 [★]通道守門人",
                141: "[冰原雪域]試煉的洞穴3 [★]煉獄獵犬",
                160: "[星光之塔]5樓化妝品店<4> [★]暴躁的化妝台",
                180: "[地球防衛本部]走廊 H01 [★]新葛雷白",
                190: "[黃昏的勇士之村] 被遺棄的挖掘地區2 變形石面怪人",
                200: "[左邊燈泡任務] 來自新村莊的信件",
                210: "[安息的洞穴]洞穴下側 安息的艾爾達斯",
                220: "[啾啾村]揪樂森林深處 生氣的普利溫 成熟的烏普洛",
                225: "[拉契爾恩市中心]顯露本色之處3 狂放的舞會居民 生氣的舞會居民",
                240: "[阿爾卡娜]洞穴的下路 混沌精靈",
                250: "[艾斯佩拉] 鏡光大海1~3 黑蜘蛛/蜘蛛女",
                255: "[泰涅布利斯] 苦痛迷宮內部5 暗黑的失敗之作 暗黑的被造物 巨大的泥人",
                260: "[泰涅布利斯]世界終結之處1-4 奧賽西翁",
                265: "[賽爾尼溫]王立圖書館第四區域 充滿好奇心的幽靈學者/AUT50",
                270: "[燃燒的賽爾尼溫]燃燒的王立圖書館第一區域 黑色太陽炸彈兵/AUT100",
                275: "[飯店阿爾克斯]沒有目的地的橫貫列車1 嚴格的站務員 石奇異/AUT200",
                280: "[奧迪溫]被佔領的巷道2 安格洛機器人 B型/AUT260",
                300: "[奧迪溫]大門深鎖的實驗室 3 失敗的實驗體/AUT300"
            }
            levels = list(level_mapping.keys())
            closest_level, i = find_closest_greater_or_equal(levels, level)
            embed = discord.Embed(
                title="練功地圖推薦", description="參考: https://forum.gamer.com.tw/C.php?bsn=7650&snA=935239", color=0xBEBEFE
            )
            embed.add_field(name=f"{levels[i-1]+1}-{closest_level}等", value=level_mapping[closest_level], inline=False)
            image_id = str(i).zfill(3)
            image = discord.File(f"image/leveling/{image_id}.png", filename=f"{image_id}.png")
            embed.set_image(url=f"attachment://{image_id}.png")
            await context.send(file=image, embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Maple(bot))
