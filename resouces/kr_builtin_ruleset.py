"""merge rule-set for karing


- outbound:
    - direct_out    [direct] 直连
    - block_out     [block] 屏蔽
    - selector_out  [currentSelected] 当前选择(default)
    - [selector] 自动选择

 - default
    - geoip/[area].srs
    - geosite/[area].srs

- cn:
    - https://github.com/ACL4SSR/ACL4SSR/tree/master/Clash/config
        - ACL4SSR_Online_Full.ini
        - ACL4SSR_Online.ini
- Adblock
    - category-ads 包含了常见的广告域名
    - category-ads-all 包含了常见的广告域名，以及广告提供商的域名

- emoji
    - 🌏 🚀 🛑
"""

import sys
import os
import json


def debug_log(msg: str):
    print(msg)
    pass


# diy change for karing
OPT_CFG_JSON_DIR = 'recommend'
OPT_OUTBOUND_CHG_MAP = {
    'direct_out': 'direct',
    'block_out': 'block',
    'selector_out': 'currentSelected',
}

# rule-set
OPT_RULESET_GROUPS = {}
OPT_RULESET_GROUPS['default'] = {
    '🛑 Adblock': {
        'default': 'off',
        'outbound': 'block_out',
        'rules': [
            # 'acl:BanAD',
            'geosite:category-ads',
        ],
    },
    '🍃 AdblockPlus': {
        'default': 'off',
        'outbound': 'block_out',
        'rules': ['acl:BanProgramAD', 'acl:BanADCompany'],
    },
    '🛑 malware': {
        'default': 'on',
        'outbound': 'block_out',
        'rules': [
            # 恶意软件
            'geosite:malware',  # 2.8K
            'geoip:malware',  # 7.3K
            # 钓鱼网站
            'geoip:phishing',  # 50
            'geosite:phishing',  # 7.2K
            # 后台挖矿
            'geosite:cryptominers',  # 3.7K
        ],
    },
    'Ⓜ️ Bing': {
        'default': 'off',
        'outbound': 'selector_out',
        'rules': ['geoip:bing', 'geosite:bing'],
    },
    'Ⓜ️ OneDrive': {
        'default': 'off',
        'outbound': 'direct_out',
        'rules': [
            'geosite:onedrive',
        ],
    },
    'Ⓜ️ Microsoft': {
        'default': 'off',
        'outbound': 'selector_out',
        'rules': [
            'geosite:microsoft',
            'geosite:microsoft-dev',
            'geosite:microsoft-pki',
        ],
    },
    '🍎 Apple': {
        'default': 'off',
        'outbound': 'direct_out',
        'rules': [
            'geosite:apple',
            'geosite:apple-ads',
            'geosite:apple-dev',
            'geosite:apple-pki',
            'geosite:apple-update',
        ],
    },
    '🌏 Google': ["geosite:google", "geoip:google"],
    '🎧 TikTok': ['geosite:tiktok'],
    '📸 Instagram': ['geosite:instagram'],
    '📹 YouTube': ['geosite:youtube'],
    '🎥 Netflix': ['geoip:netflix', 'geosite:netflix'],
    '📲 Telegram': ['geoip:telegram', 'geosite:telegram'],
    '💬 OpenAI': ['geoip:openai', 'geosite:openai'],
    '🐱 GitHub': ['geoip:github', 'geosite:github'],
    '🎮 Game': ['acl:Epic', 'acl:Origin', 'acl:Sony', 'acl:Steam', 'acl:Nintendo'],
}

## start china
OPT_RULESET_GROUPS['cn'] = {
    '🛑 广告拦截': {
        'default': 'off',
        'outbound': 'block_out',
        'rules': [
            'acl:BanAD',  # 135K = adblockclashlite
            'geosite:category-ads',  # 6.0K
        ],
    },
    '🍃 应用净化': {
        'default': 'off',
        'outbound': 'block_out',
        'rules': [
            'acl:BanProgramAD',  # 7.0K
            'acl:BanADCompany',  # 1.44 KB
        ],
    },
    'Ⓜ️ 微软Bing': {
        'default': 'off',
        'outbound': 'selector_out',
        'rules': ['geoip:bing', 'geosite:bing'],
    },
    'Ⓜ️ 微软云盘': {
        'default': 'off',
        'outbound': 'direct_out',
        'rules': [
            'geosite:onedrive',
        ],
    },
    'Ⓜ️ 微软服务': {
        'default': 'off',
        'outbound': 'selector_out',
        'rules': [
            'geosite:microsoft',
            'geosite:microsoft-dev',
            'geosite:microsoft-pki',
        ],
    },
    '🍎 苹果服务': {
        'default': 'off',
        'outbound': 'direct_out',
        'rules': [
            'geosite:apple',
            # 'geosite:apple-ads',
            'geosite:apple-dev',
            'geosite:apple-pki',
            'geosite:apple-update',
        ],
    },
    '🌏 Google': ["geosite:google", "geoip:google"],
    '📢 谷歌FCM': {
        'default': 'off',
        'outbound': 'direct_out',
        'rules': [
            'acl:GoogleFCM',
        ],
    },
    '📲 电报消息': ['geoip:telegram', 'geosite:telegram'],
    '💬 OpenAI': ['geoip:openai', 'geosite:openai'],
    '🐱 GitHub': ['geoip:github', 'geosite:github'],
    '🎮 游戏平台': [
        'acl:Epic',
        'acl:Origin',
        'acl:Sony',
        'acl:Steam',
        'acl:Nintendo',
    ],
    '🎧 TikTok': ['geosite:tiktok'],
    '📸 Instagram': ['geosite:instagram'],
    '📹 油管视频': ['geosite:youtube'],
    '🎥 奈飞视频': ['geoip:netflix', 'geosite:netflix'],
    # '📺 巴哈姆特': 'acl:Bahamut',
    '📺 哔哩哔哩': {
        'default': 'on',
        'outbound': 'direct_out',
        'rules': [
            'acl:BilibiliHMT',
            'acl:Bilibili',
        ],
    },
    '🎶 网易音乐': {
        'default': 'off',
        'outbound': 'direct_out',
        'rules': [
            'acl:NetEaseMusic',
        ],
    },
    '🎯 国内直连': {
        'default': 'on',
        'outbound': 'direct_out',
        'rules': [
            # 'acl:LocalAreaNetwork',
            # geosite:cn # 355K  geolocation-cn 和 tld-cn 的合集
            #       'geosite:geolocation-cn',  # 31K
            # 'geoip:cn' # 42K
            'acl:ChinaIp',  # 24K
            'acl:ChinaDomain',  # 3.6K
            'acl:ChinaCompanyIp',  # 1.1K
            # 'geosite:google-cn', # 1.8K
            # 'acl:GoogleCN',  # 345
            'acl:UnBan',  # 281
            'acl:SteamCN',  # 271
            'acl:Download',  # 178
            'acl:ChinaMedia',  # 414
        ],
    },
    '🌏 国外穿墙': {
        'default': 'on',
        'outbound': 'selector_out',
        'rules': [
            'geosite:geolocation-!cn',  # 170K
            'geosite:google',  # 8.7K
            'acl:ProxyGFWlist',  # 37K
            'acl:ProxyMedia',  # 2.9K
        ],
    },
}
##end china

##start ru
OPT_RULESET_GROUPS['ru'] = OPT_RULESET_GROUPS['default'].copy()
OPT_RULESET_GROUPS['ru']['🇷🇺 antizapret'] = {
    'default': 'on',
    'outbound': 'selector_out',
    'rules': [
        'geoip:blocked@ru',
        'geosite:blocked@ru',
    ],
}
##end ru

##start iran
OPT_RULESET_GROUPS['ir'] = OPT_RULESET_GROUPS['default'].copy()
OPT_RULESET_GROUPS['ir']['🛑 Adblock'] = {
    'default': 'off',
    'outbound': 'block_out',
    'rules': [
        'geosite:category-ads',
        'geosite:category-ads-ir',  # 123
    ],
}
OPT_RULESET_GROUPS['ir']['☁️ parspack'] = {
    'default': 'on',
    'outbound': 'direct_out',
    'rules': ['geoip:parspack'],
}
OPT_RULESET_GROUPS['ir']['☁️ arvancloud'] = {
    'default': 'on',
    'outbound': 'direct_out',
    'rules': ['geoip:arvancloud'],
}
##end iran


def maker_for_area(area: str, config: dict, root_path: str) -> bool:
    # config dir/file
    cfg_dir = os.path.join(root_path, OPT_CFG_JSON_DIR)
    if not os.path.exists(cfg_dir):
        os.mkdir(cfg_dir)
        debug_log(f"mkdir {cfg_dir}")

    files = {
        'rule_set': os.path.join(cfg_dir, f"{area}-set.json"),
        'rules': os.path.join(cfg_dir, f"{area}.json"),
    }

    # for each group
    route_dict = {'rules': {}, 'rule_set': {}}
    for gkey, gval in config.items():
        msg = f"area:{area} gkey:{gkey}"
        gval = maker_one_row(gval)

        for rule_set in gval['rules']:
            if not rule_file_exists(rule_set, root_path=root_path):
                debug_log(f"ERR: {msg} {rule_set} srs file not exists")
                return
            # rule set
            route_dict['rule_set'][rule_set] = maker_one_rule_set(rule_set)
            # END for rule set

        # rules
        rule = maker_one_rule(name=gkey, group=gval)
        route_dict['rules'][rule['name']] = rule

        # END for

    ret = 0
    for fk, file in files.items():
        # convert to list
        route_list = list(route_dict[fk].values())

        json_string = json.dumps({fk: route_list}, indent=4, ensure_ascii=False)
        with open(file, "w") as json_file:
            json_file.write(json_string)
            debug_log(f"wirte to {file}")
            ret += 1

    return True if ret == len(files) else False


def maker_one_rule(name: str, group: dict) -> dict:
    outbound = group['outbound']
    rule_set = group['rules']
    switch = group['default'] if group['default'] in ['on', 'off'] else 'off'
    return {
        "rule_set": rule_set,
        "outbound": outbound,
        # "name": f"{name}[karing]",
        "name": name,
        'switch': True if group['default'] == 'on' else False,
    }


def maker_one_rule_set(rule: str) -> dict:
    splits = rule.split(':')
    row = {
        "tag": "acl:BanAD",
        "type": "local",
        "format": "binary",
        "path": "acl/BanAD.srs",
    }
    row['tag'] = rule
    row['path'] = f"{splits[0]}/{splits[1]}.srs"
    return row


def maker_one_row(gval: any) -> dict:
    OPT_DEFAULT_GRULE = {'default': 'off', 'outbound': 'selector_out', 'rules': []}

    vtype = type(gval)
    if vtype is str:
        tmp_val = gval
        gval = OPT_DEFAULT_GRULE
        gval['rules'] = [tmp_val]
    elif vtype is list:
        tmp_val = gval
        gval = OPT_DEFAULT_GRULE
        gval['rules'] = tmp_val
    elif vtype is dict:
        if 'rules' not in gval:
            raise ValueError(f"ERR: rules not in gval:{gval}")

        row = OPT_DEFAULT_GRULE
        row.update(gval)
        gval = row

    else:
        raise ValueError(f"ERR: type:{vtype} gval:{gval}")

    ## chg for karing
    gval['outbound'] = OPT_OUTBOUND_CHG_MAP[gval['outbound']]

    return gval


def rule_file_exists(rule: str, root_path: str) -> bool:
    splits = rule.split(':')
    if splits[0] == 'acl':
        rule_dir = os.path.join(root_path, 'ACL4SSR')
    elif splits[0] == 'geoip':
        rule_dir = os.path.join(root_path, 'geo/geoip')
    elif splits[0] == 'geosite':
        rule_dir = os.path.join(root_path, 'geo/geosite')
    else:
        raise ValueError(f"unkown rule dir:{splits}")

    rule_file = os.path.join(rule_dir, f"{splits[1]}.srs")
    return os.path.exists(rule_file)


def main():
    if len(sys.argv) < 2:
        debug_log("Usage: python script.py <srs_file_root_path>")
        return

    root_path = sys.argv[1]
    if not os.path.isdir(root_path):
        deug_log(f"path:{root_path} not dir")
        return

    root_path = os.path.abspath(root_path)
    for area, config in OPT_RULESET_GROUPS.items():
        maker_for_area(area, config, root_path)


if __name__ == '__main__':
    main()
