import csv
import os
import re
from datetime import datetime


INPUT_FILE = "snapshots/members_latest.csv"

OUTPUT_FILE = "logs/fired.csv"


def is_fired_login(login: str) -> bool:
    """
    判断是否是离职账号

    example:
    faca48ee387e7cbaa8b68faed6d5f2_mstr

    """

    pattern = r"^[a-f0-9]{32}_mstr$"

    return re.match(pattern, login) is not None


def load_members():
    members = []

    with open(INPUT_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            members.append(row)

    return members


def save_fired(users):
    os.makedirs("logs", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "login",
                "name",
                "url",
                "detect_time",
            ],
        )

        writer.writeheader()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for user in users:
            writer.writerow(
                {
                    "login": user["login"],
                    "name": user["name"],
                    "url": user["url"],
                    "detect_time": now,
                }
            )


def main():
    members = load_members()

    fired = [user for user in members if is_fired_login(user["login"])]

    print(f"Total members: {len(members)}")

    print(f"Fired members: {len(fired)}")

    print()

    print("=" * 60)

    print("Fired Members")

    print("=" * 60)

    for user in fired:
        print(f"- {user['name']}")

        print(f"  login: {user['login']}")

    save_fired(fired)


if __name__ == "__main__":
    main()
