import argparse
import csv
import os
import shutil
from datetime import datetime
from typing import Dict, List

import requests

from config import (
    GITHUB_TOKEN,
    ORG_NAME,
    SNAPSHOT_DIR,
    LOG_DIR,
)


GRAPHQL_URL = "https://api.github.com/graphql"


HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}


GRAPHQL_QUERY = """
query($org: String!, $cursor: String) {
  organization(login: $org) {
    membersWithRole(first: 100, after: $cursor) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        login
        name
        url
      }
    }
  }
}
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitHub organization member tracker"
    )

    parser.add_argument(
        "--compare",
        help=(
            "Compare with historical snapshot date "
            "format: YYYYMMDD"
        ),
    )

    return parser.parse_args()



def github_graphql(
    variables: dict,
) -> dict:

    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={
            "query": GRAPHQL_QUERY,
            "variables": variables,
        },
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if "errors" in result:
        raise RuntimeError(
            result["errors"]
        )

    return result["data"]



def get_members() -> List[Dict]:

    members = []

    cursor = None


    while True:

        print(
            "Fetching members page..."
        )


        data = github_graphql(
            {
                "org": ORG_NAME,
                "cursor": cursor,
            }
        )


        connection = (
            data["organization"]
            ["membersWithRole"]
        )


        for user in connection["nodes"]:

            members.append(
                {
                    "login": user["login"],
                    "name": (
                        user["name"]
                        or user["login"]
                    ),
                    "url": user["url"],
                }
            )


        page_info = connection["pageInfo"]


        if not page_info["hasNextPage"]:
            break


        cursor = page_info["endCursor"]


    return sorted(
        members,
        key=lambda x: x["login"].lower(),
    )



def save_snapshot(
    members: List[Dict],
    filename: str,
):

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "login",
                "name",
                "url",
            ],
        )

        writer.writeheader()

        writer.writerows(
            members
        )



def load_snapshot(
    filename: str,
) -> Dict[str, Dict]:

    if not os.path.exists(filename):
        return {}


    with open(
        filename,
        encoding="utf-8",
    ) as f:

        reader = csv.DictReader(f)

        return {
            row["login"]: row
            for row in reader
        }



def compare_members(
    old_file: str,
    new_file: str,
):

    old_members = load_snapshot(
        old_file
    )

    new_members = load_snapshot(
        new_file
    )


    old_users = set(
        old_members.keys()
    )

    new_users = set(
        new_members.keys()
    )


    added = [
        new_members[user]
        for user in sorted(
            new_users - old_users
        )
    ]


    removed = [
        old_members[user]
        for user in sorted(
            old_users - new_users
        )
    ]


    return added, removed



def append_change_log(
    added,
    removed,
):

    os.makedirs(
        LOG_DIR,
        exist_ok=True,
    )


    logfile = os.path.join(
        LOG_DIR,
        "changes.csv",
    )


    exists = os.path.exists(
        logfile
    )


    with open(
        logfile,
        "a",
        newline="",
        encoding="utf-8",
    ) as f:


        writer = csv.writer(f)


        if not exists:

            writer.writerow(
                [
                    "time",
                    "action",
                    "login",
                    "name",
                ]
            )


        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        for user in added:

            writer.writerow(
                [
                    now,
                    "Added",
                    user["login"],
                    user["name"],
                ]
            )


        for user in removed:

            writer.writerow(
                [
                    now,
                    "Removed",
                    user["login"],
                    user["name"],
                ]
            )



def print_changes(
    added,
    removed,
):

    print()

    print("=" * 60)
    print("Added Members")
    print("=" * 60)


    if added:

        for user in added:

            print(
                f"+ {user['name']} "
                f"({user['login']})"
            )

    else:

        print("None")


    print()

    print("=" * 60)
    print("Removed Members")
    print("=" * 60)


    if removed:

        for user in removed:

            print(
                f"- {user['name']} "
                f"({user['login']})"
            )

    else:

        print("None")



def main():

    args = parse_args()


    os.makedirs(
        SNAPSHOT_DIR,
        exist_ok=True,
    )


    today = datetime.now().strftime(
        "%Y%m%d"
    )


    today_snapshot = os.path.join(
        SNAPSHOT_DIR,
        f"members_{today}.csv",
    )


    latest_snapshot = os.path.join(
        SNAPSHOT_DIR,
        "members_latest.csv",
    )


    print(
        "Fetching organization members..."
    )


    members = get_members()


    print(
        f"Found {len(members)} members."
    )


    save_snapshot(
        members,
        today_snapshot,
    )


    #
    # Decide comparison target
    #

    if args.compare:

        compare_snapshot = os.path.join(
            SNAPSHOT_DIR,
            f"members_{args.compare}.csv",
        )

        print(
            f"Compare with: {compare_snapshot}"
        )

    else:

        compare_snapshot = latest_snapshot



    if os.path.exists(
        compare_snapshot
    ):

        added, removed = compare_members(
            compare_snapshot,
            today_snapshot,
        )


        print_changes(
            added,
            removed,
        )


        append_change_log(
            added,
            removed,
        )


    else:

        print(
            "No previous snapshot found."
        )


    #
    # Update latest snapshot
    #

    shutil.copy(
        today_snapshot,
        latest_snapshot,
    )


    print()

    print(
        "Done."
    )



if __name__ == "__main__":
    main()