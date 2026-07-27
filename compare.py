import argparse
import csv
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare two GitHub member CSV snapshots"
    )

    parser.add_argument(
        "old",
        help="Old CSV snapshot file"
    )

    parser.add_argument(
        "new",
        help="New CSV snapshot file"
    )

    return parser.parse_args()



def load_members(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    members = {}

    with open(
        filename,
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:
            members[row["login"]] = row

    return members



def compare_members(old_file, new_file):

    old_members = load_members(old_file)
    new_members = load_members(new_file)

    old_logins = set(old_members.keys())
    new_logins = set(new_members.keys())

    added = [
        new_members[login]
        for login in sorted(new_logins - old_logins)
    ]

    removed = [
        old_members[login]
        for login in sorted(old_logins - new_logins)
    ]

    return added, removed



def print_members(title, members, prefix):

    print()
    print("=" * 60)
    print(f"{title} ({len(members)})")
    print("=" * 60)

    if not members:
        print("None")
        return

    for user in members:
        print(
            f"{prefix} {user['name']} "
            f"({user['login']})"
        )



def save_result(added, removed):

    with open(
        "compare_result.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "action",
                "login",
                "name",
                "url",
            ],
        )

        writer.writeheader()

        for user in added:
            writer.writerow(
                {
                    "action": "Added",
                    "login": user["login"],
                    "name": user["name"],
                    "url": user["url"],
                }
            )

        for user in removed:
            writer.writerow(
                {
                    "action": "Removed",
                    "login": user["login"],
                    "name": user["name"],
                    "url": user["url"],
                }
            )



def main():

    args = parse_args()

    added, removed = compare_members(
        args.old,
        args.new,
    )

    print(
        f"\nCompare:"
    )

    print(
        f"OLD: {args.old}"
    )

    print(
        f"NEW: {args.new}"
    )


    print_members(
        "Added Members",
        added,
        "+"
    )

    print_members(
        "Removed Members",
        removed,
        "-"
    )


    save_result(
        added,
        removed,
    )


    print(
        "\nSaved: compare_result.csv"
    )



if __name__ == "__main__":
    main()