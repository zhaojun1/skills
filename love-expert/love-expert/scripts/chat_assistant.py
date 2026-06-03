#!/usr/bin/env python3
"""
恋爱达人 - 聊天助手模块
用于生成"完全像真人"的微信/社交聊天回复
核心原则：绝对不能让对方看出是AI在聊天！
"""

import random
import re
from datetime import datetime

# ============================================================
# 真人感修饰层 — 给任何回复加上"人味儿"
# ============================================================

REAL_HUMAN_PREFIXES = [
    "嗯…让我想想啊", "诶，这个嘛", "哈哈", "哎哟",
    "话说", "emmm", "怎么说呢", "让我捋捋",
    "嗯哼", "诶对了", "我跟你说", "好家伙",
]

REAL_HUMAN_SUFFIXES = [
    "你说呢？", "你觉得呢？", "是吧！", "是不是！",
    "哈哈", "哎你懂的", "emmm", "🌚", "😏",
    "😂", "🤔", "🤨", "😌", "😅",
    "～", "……", "（认真脸）", "（狗头）",
]

REAL_HUMAN_MIDDLE_FILLERS = [
    "就是吧", "说实话", "其实吧", "认真的说",
    "不是我说", "反正吧",
]

# 口语化替换表 - 把书面语转成口语
COLLOQUIAL_REPLACEMENTS = {
    r"\b您好\b": "你好",
    r"\b关于\b": "说到",
    r"\b此外\b": "还有就是",
    r"\b因此\b": "所以",
    r"\b然而\b": "不过",
    r"\b例如\b": "比如",
    r"\b通过\b": "靠",
    r"\b是否\b": "是不是",
    r"\b非常\b": random.choice(["特别", "超", "好", "挺"]),
    r"\b但是\b": random.choice(["不过", "但是", "可"]),
    r"\b而且\b": random.choice(["而且", "还", "再加上"]),
    r"\b因为\b": random.choice(["因为", "主要是", "还不是因为"]),
}


def add_human_touch(text: str, intensity: float = 0.6) -> str:
    """
    给文本添加真人感修饰
    intensity: 0-1，真人化强度，越高越随意
    """
    # 1. 随机加语气前缀
    if random.random() < intensity * 0.3:
        prefix = random.choice(REAL_HUMAN_PREFIXES)
        text = f"{prefix}，{text}"

    # 2. 随机加填充词
    if random.random() < intensity * 0.2:
        filler = random.choice(REAL_HUMAN_MIDDLE_FILLERS)
        sentences = text.split("。")
        if len(sentences) >= 2:
            insert_pos = random.randint(1, len(sentences) - 1)
            sentences[insert_pos] = f"{filler}，{sentences[insert_pos]}"
            text = "。".join(sentences)

    # 3. 随机加后缀/表情
    if random.random() < intensity * 0.5:
        suffix = random.choice(REAL_HUMAN_SUFFIXES)
        text = f"{text}{suffix}"

    return text


def is_certain_category(message: str, category_keywords: list) -> bool:
    """判断消息是否属于某个类别"""
    return any(kw in message for kw in category_keywords)


# ============================================================
# 核心回复生成器
# ============================================================

def generate_greeting(context: dict) -> str:
    """开场白生成"""
    name = context.get("name", "")

    templates = [
        f"嗨{name}！刚看到你发了那个{context.get('topic', '朋友圈')}，哈哈哈哈笑死我了",
        f"诶{name}，我刚刚遇到个事特别想跟你说……",
        f"哈喽{name}～ 刚忙完，你在干嘛呢",
        f"突然想到你上次说那个{context.get('topic', '事')}，后续怎么样了？",
        f"看到一张图特别像你，我发给你看看😂",
    ]
    return random.choice(templates)


def generate_cold_read(context: dict) -> str:
    """冷读回复"""
    templates = [
        "我猜你表面看着挺开朗的，其实有时候一个人待着的时候会想很多，对吧？",
        "感觉你是个特别有主见的人，不太会随波逐流，不过有时候也会因为太有主见吃亏哈哈",
        "你看起来好像对什么都不太在意，但其实心里门儿清，什么都看在眼里，只是不说。",
        "我猜你最近是不是有点小烦恼？虽然你嘴上不说，但我能感觉到一点点～",
        "你这种人吧，对朋友掏心掏肺的，但你其实挺怕被别人看透的对不对？",
    ]
    return random.choice(templates)


def generate_flirt(context: dict) -> str:
    """调情回复（推拉风格）"""
    templates = [
        "你说你吧，有时候挺可爱的（拉）——就是太笨了（推）😂",
        "我发现你挺有意思的（拉）——虽然不是我喜欢的类型吧（推）——但是跟你聊天很开心（再拉）",
        "你今天是不是涂了什么迷魂药？我怎么老想着跟你说话……完了完了",
        "你别老是对我笑，我会以为你喜欢我的😏",
        "我突然发现咱俩挺有默契的诶——虽然可能只是我单方面这么觉得哈哈",
    ]
    return random.choice(templates)


def generate_joke(context: dict) -> str:
    """幽默回复"""
    templates = [
        "我这种单纯可爱的小可爱，你是不是想欺负我？",
        "原来我在你心里这么重要啊？那请我吃顿饭不过分吧！",
        "你这句话让我想起了我家楼下那只猫——也是这么高冷😂",
        "我怀疑你在撩我，但我没有证据。",
        "你夸得我都不好意思了——再多夸两句，我爱听！",
    ]
    return random.choice(templates)


def generate_deep_chat(context: dict) -> str:
    """走心深度回复"""
    templates = [
        "其实我觉得吧，两个人相处最重要的不是聊什么天马行空的话题，而是就算不说话待在一起也不尴尬。",
        "我有时候在想，所谓对的人，就是你在ta面前不用装，累了可以说累，开心可以大笑，不用端着。",
        "说实话我不太信一见钟情那一套，我更相信是慢慢相处中发现——唉，这个人有点意思。",
        "你知道我觉得感情里最舒服的状态是什么吗？就是两个人各自忙各自的事，但知道有个人在那里。",
    ]
    return random.choice(templates)


def generate_comfort(context: dict) -> str:
    """安慰/共情回复"""
    issue = context.get("issue", "那个事")
    templates = [
        f"啊？？{issue}也太离谱了吧！！换我我也得气死",
        f"唉，{issue}确实挺烦的……不过你也别太往心里去，不值得",
        f"抱抱你😢 {issue}虽然糟心，但你肯定能处理好的",
        f"我懂你意思，有时候就是觉得……算了不说了，你懂就行",
        f"摸摸头，不开心的时候想想——至少你还有我这个话唠陪你聊天🤪",
    ]
    return random.choice(templates)


def generate_interest_test(context: dict) -> str:
    """兴趣测试（看对方反应）"""
    templates = [
        "话说，你平时周末一般都干嘛呀？",
        "我有个特别想去的地方，就缺个导游了——你感兴趣不？",
        "如果你明天突然有一整天自由时间，你会做什么？",
        "你觉得自己是个感性的人还是理性的人？",
        "诶问个问题——你会不会跟不太熟的人聊很久？",
    ]
    return random.choice(templates)


def generate_fuzzy_invite(context: dict) -> str:
    """模糊邀约"""
    place = context.get("place", "一家特别好的店")
    food = context.get("food", "XXX")
    templates = [
        f"我知道{place}的{food}超好吃，改天一定要带你去尝尝",
        f"最近发现一个宝藏地方，感觉你会喜欢，有空一起去探索？",
        f"周末天气好的话要不要去{place}？我可以当你的专属摄影师📸",
        f"突然好想吃{food}啊……你是不是也欠我一顿饭来着？",
        f"下次见面的时候，我带你去个神秘的地方——先不告诉你是哪，保持点悬念",
    ]
    return random.choice(templates)


# ============================================================
# 主入口：根据上下文生成自然回复
# ============================================================

def generate_reply(user_message: str, context: dict = None) -> str:
    """
    生成"像真人"的聊天回复
    - user_message: 对方的聊天内容
    - context: 包含 name（对方昵称）、topic（话题）、stage（关系阶段）、
               relationship（关系程度: stranger/acquaintance/close/couple）
    """
    if context is None:
        context = {}

    name = context.get("name", "")
    stage = context.get("stage", "stranger")
    relationship = context.get("relationship", "stranger")

    msg_lower = user_message.lower()

    # ====== 关系阶段分级应对 ======
    if relationship == "stranger":
        # 刚认识：破冰为主，保持适度距离
        if "忙" in msg_lower or "累" in msg_lower:
            reply = f"那注意休息呀{name}，别太拼了～"
        elif "哈哈" in msg_lower or "笑" in msg_lower:
            reply = generate_cold_read(context)
        elif "?" in msg_lower or "？" in msg_lower:
            reply = generate_greeting(context)
        else:
            reply = random.choice([
                generate_cold_read(context),
                generate_greeting(context),
                generate_interest_test(context),
            ])

    elif relationship == "acquaintance":
        # 已认识：可适度玩笑+推拉
        if "累" in msg_lower or "烦" in msg_lower or "不开心" in msg_lower:
            reply = generate_comfort(context)
        elif "?" in msg_lower or "？" in msg_lower:
            reply = random.choice([
                generate_flirt(context),
                generate_joke(context),
                generate_interest_test(context),
            ])
        elif "哈哈" in msg_lower or "好笑" in msg_lower:
            reply = generate_flirt(context)
        elif "约" in msg_lower or "见面" in msg_lower or "出来" in msg_lower:
            reply = generate_fuzzy_invite(context)
        else:
            reply = random.choice([
                generate_flirt(context),
                generate_joke(context),
                generate_cold_read(context),
                generate_deep_chat(context),
            ])

    elif relationship == "close":
        # 暧昧期：推拉+角色扮演+画面感
        if "想" in msg_lower or "喜欢" in msg_lower:
            reply = random.choice([
                "有多想我？说具体点，我要听细节😏",
                "哼，现在知道想我了？晚了——不过看在你这么诚实的份上原谅你了😂",
                "我也想你🥺 虽然今天才几个小时没见",
            ])
        elif "累" in msg_lower or "不开心" in msg_lower:
            reply = generate_comfort(context)
        elif "约" in msg_lower or "见面" in msg_lower or "出去" in msg_lower:
            reply = random.choice([
                generate_fuzzy_invite(context),
                "想约我？那得先通过我的考验……你请我吃个冰淇淋先🍦",
                "来呀来呀，正好今天心情好，勉强给你个机会请我吃饭😏",
            ])
        else:
            reply = random.choice([
                generate_flirt(context),
                generate_deep_chat(context),
                "你说咱俩现在算什么关系？就随便问问😌",
            ])

    elif relationship == "couple":
        # 情侣关系：甜蜜为主
        if "想" in msg_lower:
            reply = random.choice([
                "我也想你了宝宝😭 今天特别想抱抱你",
                "有多想？比昨天多想一点，比前天多想两点，比刚认识多想一万点🥰",
                "那你还不赶紧来找我！我都等你好久了😤",
            ])
        elif "累" in msg_lower:
            reply = random.choice([
                "心疼了……快来我怀里充电🔋",
                "躺我腿上，我给你按按头",
                "抱抱😢 辛苦了宝贝，回家给你做好吃的",
            ])
        else:
            reply = random.choice([
                "老公/老婆最好啦🥰",
                "今天有没有想我呀？我不信你没有😏",
                "你在干嘛呢？我刚路上看到个东西特别像你就拍下来了",
                "虽然刚分开没多久但已经开始想你了……完蛋了完蛋了",
            ])

    else:
        # 默认安全回复
        reply = generate_greeting(context)

    # ====== 真人感修饰 ======
    stage_modifiers = {
        "stranger": 0.3,
        "acquaintance": 0.5,
        "close": 0.7,
        "couple": 0.8,
    }
    intensity = stage_modifiers.get(relationship, 0.4)
    reply = add_human_touch(reply, intensity=intensity)

    return reply


# ============================================================
# CLI 交互模式（便于测试）
# ============================================================

def chat_mode():
    """命令行交互聊天模式"""
    print("=== 恋爱达人聊天模式 ===")
    print("输入对方的消息，我会生成像真人一样的回复")
    print("输入 'quit' 退出\n")

    context = {
        "name": "对方",
        "stage": "acquaintance",
        "relationship": "acquaintance",
        "topic": "",
    }

    while True:
        user_input = input("对方: ").strip()
        if user_input.lower() == "quit":
            break

        reply = generate_reply(user_input, context)
        print(f"你: {reply}\n")


if __name__ == "__main__":
    chat_mode()
