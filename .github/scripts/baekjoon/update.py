# IMPORT
import requests, os, subprocess
from bs4 import BeautifulSoup

# LOAD
os.makedirs('.github/scripts/baekjoon', exist_ok=True)
with open('.github/scripts/baekjoon/update.txt', 'r', encoding='utf-8') as f: updated = f.read()

# SETUP
RANK_NAMES = {
    0: ("Unrated", "Unrated"),
    1: ("Bronze", "Bronze V"), 2: ("Bronze", "Bronze IV"), 3: ("Bronze", "Bronze III"), 4: ("Bronze", "Bronze II"), 5: ("Bronze", "Bronze I"),
    6: ("Silver", "Silver V"), 7: ("Silver", "Silver IV"), 8: ("Silver", "Silver III"), 9: ("Silver", "Silver II"), 10: ("Silver", "Silver I"),
    11: ("Gold", "Gold V"), 12: ("Gold", "Gold IV"), 13: ("Gold", "Gold III"), 14: ("Gold", "Gold II"), 15: ("Gold", "Gold I"),
    16: ("Platinum", "Platinum V"), 17: ("Platinum", "Platinum IV"), 18: ("Platinum", "Platinum III"), 19: ("Platinum", "Platinum II"), 20: ("Platinum", "Platinum I"),
    21: ("Diamond", "Diamond V"), 22: ("Diamond", "Diamond IV"), 23: ("Diamond", "Diamond III"), 24: ("Diamond", "Diamond II"), 25: ("Diamond", "Diamond I"),
    26: ("Ruby", "Ruby V"), 27: ("Ruby", "Ruby IV"), 28: ("Ruby", "Ruby III"), 29: ("Ruby", "Ruby II"), 30: ("Ruby", "Ruby I")
}
cookie_baekjoon = os.getenv("COOKIE")
HEADERS_BAEKJOON = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": cookie_baekjoon,
    "Referer": "https://www.acmicpc.net/"
}
URL = "https://www.acmicpc.net/status?user_id=yeomoon"
CODE_MAP = {
    "Python 3": "py"
}

# FUNCTION
def prlevel(id: int):
    _data = requests.get("https://solved.ac/api/v3/problem/show?problemId=" + str(id)).json()
    return RANK_NAMES[_data["level"]]
def solve(id: str): return requests.get(f"https://www.acmicpc.net/source/download/{id}", headers=HEADERS_BAEKJOON).text

# PROFILE
soup = BeautifulSoup(requests.get(URL, headers=HEADERS_BAEKJOON).text, "html.parser")
result = {}
for tr in soup.select("#status-table > tbody > tr"):
    sid = tr["id"].replace("solution-", "")
    if sid == updated: print("b"); break
    tds = tr.find_all("td")
    result[sid] = {
        "problem_id": int(tds[2].find("a")["href"].split("/")[-1]),
        "problem_title": tds[2].find("a")["title"],
        "result": tds[3].get_text(strip=True),
        "memory": int(tds[4].get_text(strip=True)) if tds[4].get_text(strip=True).isdigit() else None,
        "time": int(tds[5].get_text(strip=True)) if tds[5].get_text(strip=True).isdigit() else None,
        "language": tds[6].find("a").get_text(strip=True)
    }
print(result)
result = dict(reversed(result.items()))
print(result)

# WORK
for id, data in result.items():
    if data["result"] in ["맞았습니다!!", "100점"]: subprocess.run(["python", ".github/scripts/readme/update.py"], check=True)
    drn = "./" + prlevel(data["problem_id"])[0] + "/" + prlevel(data["problem_id"])[1]
    os.makedirs(drn, exist_ok=True)
    fln = drn + "/" + str(data["problem_id"]) + " - " + data["problem_title"].replace("/", "-") + "." + CODE_MAP.get(data["language"], "code")
    with open(fln, 'w', encoding='utf-8') as f: f.write(solve(id))
    with open('.github/scripts/baekjoon/update.txt', 'w', encoding='utf-8') as f: f.write(id); f.close()

    cm = str(data["problem_id"]) + " - " + data["result"]
    pat = os.environ["PAT_TOKEN"]
    commands = [
        ["git", "config", "--global", "user.name", "youmoon"],
        ["git", "config", "--global", "user.email", "kimyeomoon@gmail.com"],
        ["git", "add", "."],
        ["git", "commit", "-m", cm, "-m", "Memory: " + str(data['memory']) + "kb, Time: " + str(data['time']) + "ms"],
        ["git", "push", f"https://youmoon:{pat}@github.com/youmoon/Baekjoon.git", "main"]
    ]
    for cmd in commands: subprocess.run(cmd, check=True)