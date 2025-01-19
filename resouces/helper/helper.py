import os, sys
import requests
import re


def debug_log(msg: str):
    if msg.startswith('ERR'):
        msg = msg.replace('ERR', '\x1b[31mERR\x1b[0m')
    print(msg)
    # pass


def get_out_path(out_path: str = None):
    return (
        os.getcwd()
        if out_path is None or len(out_path) == 0
        else os.path.abspath(out_path)
    )


def writeto_rulefile(out_file: str, content: dict | str):
    file_string = json.dumps(content) if isinstance(content, dict) else content

    with open(out_file, "w") as json_file:
        json_file.write(file_string)
        debug_log(f"wirte to {out_file}")


def get_url_content(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        return response.text if response.status_code == 200 else None

    except requests.exceptions.HTTPError as http_err:
        debug_log(f"HTTP error occurred: {http_err} \tURL: {url}")
    except requests.exceptions.ConnectionError as conn_err:
        debug_log(f"Connection error occurred: {conn_err} \tURL: {url}")
    except requests.exceptions.Timeout as timeout_err:
        debug_log(f"Timeout error occurred: {timeout_err} \tURL: {url}")
    except requests.exceptions.RequestException as req_err:
        debug_log(f"An error occurred: {req_err} \tURL: {url}")
    return None


def correct_name(text: str) -> str:
    # Define the replacements as a dictionary
    replacements = {
        " ": "-",
        "–": "-",
        ",": "-",
        "/": "_",
        ":": "",
        "'": "",
        "(": "_",
        ")": "",
    }

    # Apply the replacements
    replaced_text = ''.join(replacements.get(c, c) for c in text)

    # Collapse consecutive "-" or "_" into a single "_"
    collapsed_text = re.sub(r'-+', '-', replaced_text)
    collapsed_text = re.sub(r'_+', '_', collapsed_text)

    # Remove trailing "-" or "_"
    final_text = re.sub(r'[-_]+$', '', collapsed_text)

    # Replace "-_" and "_-" with "_"
    final_text = re.sub(r'-_|_-', '_', final_text)

    return final_text


def remove_ansi_escape_codes(text: str) -> str:
    # Regular expression pattern for ANSI escape codes
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)


def is_url(string):
    pattern = re.compile(
        r'^(https?://)?'  # http:// 或 https://（可选）
        r'([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,6}'  # 域名部分
        r'(:[0-9]{1,5})?'  # 端口号（可选）
        r'(/.*)?$'  # 路径部分（可选）
    )
    return bool(pattern.match(string))


if __name__ == '__main__':
    # text = "example  string//with spaces---and////slashes"
    text = 'uBlock-filters-–-Resource-abuse-'
    text = 'Dandelion-Sprouts-Anti-Malware-List-_for-AdGuard-Home-and-for-AdGuard-for-Android_Windows-DNS-filtering'
    print(correct_name(text))

    # text = '\x1b[36mINFO\x1b[0m[0000] parsed rules: 778/1450'
    # print(remove_ansi_escape_codes(text).startswith('INFO'))
