import os


def load_env_file():
	env_file = os.path.join(os.path.dirname(__file__), ".env")
	if not os.path.exists(env_file):
		return

	with open(env_file, encoding="utf-8") as file:
		for line in file:
			line = line.strip()
			if not line or line.startswith("#") or "=" not in line:
				continue
			key, value = line.split("=", 1)
			key = key.strip()
			value = value.strip().strip('"').strip("'")
			if key:
				os.environ.setdefault(key, value)


load_env_file()


# GitHub Personal Access Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_xxx")

# Organization Name
ORG_NAME = "mstr-kiai"

# 保存路径
SNAPSHOT_DIR = "snapshots"
LOG_DIR = "logs"
