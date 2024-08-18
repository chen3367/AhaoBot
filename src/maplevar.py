import sqlite3

def getMobList():
    conn = sqlite3.connect("database/database.db")
    result = conn.execute("SELECT DISTINCT(name) FROM maple_mob ORDER BY id")
    mob_list = {mob[0]:mob[0] for mob in result.fetchall()}
    conn.close()
    return mob_list

mob_list = getMobList()

tips = {
    "【攻略】製作書掉落資訊": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1013981",
    "【攻略】個人(打王)增益效果統整": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1024032",
    "【攻略】伊甸的糧食倉庫 經驗表": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1027857",
    "【攻略】裝備效益計算機": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1029318",
    "【工具】BOSS篩選器": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1025763"
}

jobtips = {
    "英雄": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1029191",
    "聖騎士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=928713",
    "黑騎士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=999902",
    "主教": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1021664",
    "冰雷大魔導士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=946674",
    "火毒大魔導士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1021709",
    "箭神": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1002462",
    "神射手": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1014283",
    "開拓者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1001808",
    "夜使者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1023760",
    "暗影神偷": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1028659",
    "影武者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=999580",
    "槍神": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1022424",
    "拳霸": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1019146",
    "重砲指揮官": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1029227",
    "聖魂劍士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1023953",
    "烈焰巫師": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=960392",
    "破風使者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1016324",
    "暗夜行者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=974208",
    "閃雷悍將": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1020164",
    "米哈逸": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1010720",
    "狂狼勇士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1027906",
    "龍魔導士": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=941768",
    "夜光": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1026291",
    "精靈遊俠": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=919629",
    "幻影俠盜": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=891539",
    "隱月": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1020845",
    "爆拳槍神": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=974038",
    "煉獄巫師": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1021000",
    "狂豹獵人": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=894749",
    "機甲戰神": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=976654",
    "惡魔殺手": "https://forum.gamer.com.tw/Co.php?bsn=7650&sn=6152106",
    "惡魔復仇者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1015079",
    "傑諾": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=959673",
    "凱撒": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1015441",
    "凱殷": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1024022",
    "卡蒂娜": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1011427",
    "天使破壞者": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1002369",
    "阿戴爾": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1016892",
    "伊利恩": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1027011",
    "卡莉": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1025791",
    "亞克": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=992523",
    "菈菈": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1019349",
    "虎影": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1020893",
    "凱內西斯": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1006030",
    "神之子": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1014516",
    "劍豪": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1015610",
    "陰陽師": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=895604",
    "琳恩": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1028484",
    "墨玄": "https://forum.gamer.com.tw/C.php?bsn=7650&snA=1012847"
}

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