import requests
from datetime import datetime, timedelta, timezone

HANDLE = "yeomoon"
STATS_URL = f"https://solved.ac/api/v3/user/problem_stats?handle={HANDLE}"
TOP100_URL = f"https://solved.ac/api/v3/user/top_100?handle={HANDLE}"

RANK_NAMES = {
    0: "Unrated",
    1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
    6: "Silver V", 7: "Silver IV", 8: "Silver III", 9: "Silver II", 10: "Silver I",
    11: "Gold V", 12: "Gold IV", 13: "Gold III", 14: "Gold II", 15: "Gold I",
    16: "Platinum V", 17: "Platinum IV", 18: "Platinum III", 19: "Platinum II", 20: "Platinum I",
    21: "Diamond V", 22: "Diamond IV", 23: "Diamond III", 24: "Diamond II", 25: "Diamond I",
    26: "Ruby V", 27: "Ruby IV", 28: "Ruby III", 29: "Ruby II", 30: "Ruby I"
}

RANK_EMOJIS = {
    0: "❔", # Unrated
    1: "🥉", 2: "🥉", 3: "🥉", 4: "🥉", 5: "🥉", # Bronze
    6: "🥈", 7: "🥈", 8: "🥈", 9: "🥈", 10: "🥈", # Silver
    11: "🥇", 12: "🥇", 13: "🥇", 14: "🥇", 15: "🥇", # Gold
    16: "☘️", 17: "☘️", 18: "☘️", 19: "☘️", 20: "☘️", # Plantinum
    21: "💎", 22: "💎", 23: "💎", 24: "💎", 25: "💎", # Diamond
    26: "❤️", 27: "❤️", 28: "❤️", 29: "❤️", 30: "❤️" # Ruby
}

def fetch_stats(): return requests.get(STATS_URL).json()
def fetch_top100(): return requests.get(TOP100_URL).json()["items"]

def calc_main_info(stats):
    total_solved = sum(item["solved"] for item in stats)
    most = max(stats, key=lambda x: (x["solved"], x["level"]))
    rank_level, rank_count = most["level"], most["solved"]

    rank_name = RANK_NAMES.get(rank_level, f"Lv{rank_level}")
    rank_ratio = round(rank_count / total_solved * 100, 1) if total_solved > 0 else 0
    rank_emoji = RANK_EMOJIS.get(rank_level, "❔")
    return total_solved, rank_name, rank_ratio, rank_emoji

def calc_hardest(top100):
    hardest = max(top100, key=lambda x: (x["level"], x["averageTries"]))
    emoji = RANK_EMOJIS.get(hardest["level"], "❔")
    title = hardest.get("titleKo") or hardest["titles"][0]["title"]
    pid = hardest["problemId"]
    return title, pid, emoji

def update_readme(total, rank_name, rank_ratio, rank_emoji, hardest_title, hardest_id, hardest_emoji):
    path = "README.md"
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)
    updated_time = now_kst.strftime("%y/%m/%d %H:%M")
    hardest_url = f"https://www.acmicpc.net/problem/{hardest_id}"

    template = f"""# 📖 Baekjoon
### 제가 푼 백준 문제의 답을 적어두었어요!
- 💻 현재까지 총 {total}개의 문제를 풀었어요
- {rank_emoji} 그 중 {rank_ratio}%는 {rank_name} 문제에요
- {hardest_emoji} 제가 풀었던 가장 어려운 문제는 [{hardest_title}]({hardest_url}) 이었어요

## 🍙 안내 사항
- 제 풀이가 가장 좋은 방식이 아닐 수도 있으니 참고해주세요
- 문제 랭크 분류는 [solved.ac](https://solved.ac/)를 따릅니다
> 마지막 업데이트 : {updated_time} (KST)
"""
    with open(path, "w", encoding="utf-8") as f: f.write(template)

if __name__ == "__main__":
    stats = fetch_stats()
    top100 = fetch_top100()
    total, rank_name, rank_ratio, rank_emoji = calc_main_info(stats)
    hardest_title, hardest_id, hardest_emoji = calc_hardest(top100)
    update_readme(total, rank_name, rank_ratio, rank_emoji, hardest_title, hardest_id, hardest_emoji)