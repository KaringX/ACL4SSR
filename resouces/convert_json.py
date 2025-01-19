# list convert to json
import sys
import os
import json
import requests
from helper.helper import debug_log as deug_log

MAP_RULES_KEY_DICT = {
    'IP-CIDR': 'ip_cidr',
    'IP-CIDR6': 'ip_cidr',
    'DOMAIN': 'domain',
    'DOMAIN-SUFFIX': 'domain_suffix',
    'DOMAIN-KEYWORD': 'domain_keyword',
    'PROCESS-NAME': 'process_name',
}

# disabled process_name
SPECIAL_TREATMENT_PN_LIST = ['Crypto.list', 'ProxyMedia.list']

# Adblock Addon
ADDON_ADBLOCK_DOMAINS = {
    'BanADCompany': 'https://github.com/d3ward/toolz/raw/master/src/data/adblock_data.json',
}


# def deug_log(msg: str):
#     print(msg)
#     pass


def main(src_path: str, out_path: str = None):
    # out_path = get_out_path(out_path)
    # src_path = os.path.abspath(src_path)
    deug_log(f"{src_path} to {out_path}")
    listdir_format(src_path, out_path=out_path)


def get_out_path(out_path: str = None):
    return (
        os.getcwd()
        if out_path is None or len(out_path) == 0
        else os.path.abspath(out_path)
    )


def listdir_format(src_path: str, out_path: str):
    for item in os.listdir(src_path):
        target_path = os.path.join(src_path, item)

        if os.path.isdir(target_path):
            out_path2 = os.path.join(out_path, item)
            if os.path.exists(out_path2) is False:
                os.mkdir(out_path2)
                deug_log(f"mkdir {out_path2}")
            listdir_format(target_path, out_path=out_path2)
        else:
            converto_json(target_path, out_path=out_path)


def read_rules_from_file(src_file: str) -> dict | None:
    splits = os.path.splitext(src_file)
    if splits[1] != ".list":
        # deug_log(f"ERR: only support '.list' {src_file}")
        return None
    if not os.path.isfile(src_file):
        deug_log(f"ERR: not file {src_file}")
        return None

    content = {"version": 1, "rules": [{}]}

    # disable process name
    is_spical_pn = False
    for sfile in SPECIAL_TREATMENT_PN_LIST:
        if src_file.endswith(sfile):
            is_spical_pn = True

    with open(src_file, "r") as f:
        line = f.readline()
        while line:
            # line.strip()
            in_key = False
            row = line.split(",")
            if len(row) >= 2:
                rule, cont = row[0].upper(), row[1].strip()
                # if cont in ['le.com', 'in.com']:
                # deug_log(f"row:{row} drop le.com/match google.com")
                # rule = 'PASS'
                if is_spical_pn is True and rule == 'PROCESS-NAME':
                    deug_log(f"row:{row} drop PROCESS-NAME")
                    rule = 'PASS'

                if rule in MAP_RULES_KEY_DICT:
                    rkey = MAP_RULES_KEY_DICT[rule]

                    if rkey in content['rules'][0]:
                        content['rules'][0][rkey].append(cont)
                    else:
                        content['rules'][0][rkey] = [cont]

                    in_key = True
                # END if

            #! DEBUG
            if in_key is False:
                if row[0] not in ["USER-AGENT", "URL-REGEX"] and line[0] not in [
                    '#',
                    '\n',
                ]:
                    deug_log(f"row:{row} first:{line[0]} UNKOWN")
            line = f.readline()
            # END while

    if len(content['rules'][0]) == 0:
        deug_log(f"empty rules: {src_file}")
        return None

    return content


def converto_json(src_file: str, out_path: str):
    splits = os.path.splitext(src_file)
    out_file = os.path.join(out_path, os.path.basename(splits[0]) + ".json")
    content = read_rules_from_file(src_file)
    if content is None:
        return False

    return writeto_rulefile(out_file, content)
    # END converto_josn


def writeto_rulefile(out_file: str, content: dict):
    json_string = json.dumps(content)
    with open(out_file, "w") as json_file:
        json_file.write(json_string)
        deug_log(f"wirte to {out_file}")
        return True
    return False


## Addon
def addon_adblock(out_path: str):
    for name, url in ADDON_ADBLOCK_DOMAINS.items():
        content = get_url_content(url)
        if isinstance(content, str) and len(content) > 100:
            json_data = json.loads(content)
            domains = extract_strings_from_dict(json_data)
            content = {"version": 1, "rules": [{'domain_suffix': domains}]}
            out_file = os.path.join(out_path, name + ".json")
            if isinstance(domains, list) and len(domains) > 0:
                writeto_rulefile(out_file=out_file, content=content)
        else:
            continue
        # END for


def get_url_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        deug_log(f"Error downloading url:{url} \tStatus code: {response.status_code}")
        return None


def extract_strings_from_dict(data_dict, my_dict=None):
    if my_dict is None:
        my_dict = []

    for key, value in data_dict.items():
        if isinstance(value, dict):
            # 递归调用处理子字典
            extract_strings_from_dict(value, my_dict)
        elif isinstance(value, str):
            my_dict.append(value)
        elif isinstance(value, list):
            # 如果值是一个列表，处理列表中的每一项
            for item in value:
                if isinstance(item, dict):
                    extract_strings_from_dict(item, my_dict)
                elif isinstance(item, str):
                    my_dict.append(item)

    return my_dict


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <first_parameter> <second_parameter>")

    elif sys.argv[1] == "--single":
        src_file = sys.argv[2]
        out_path = os.path.dirname(src_file)
        content = converto_json(src_file, out_path)
        if content is False:
            deug_log(f"src file:{src_file} empty")
            exit(-1)

    else:
        src_path = get_out_path(sys.argv[1])
        out_path = get_out_path(sys.argv[2])
        main(src_path, out_path)
        addon_adblock(out_path)
