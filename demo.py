import subprocess
import json
from dotenv import load_dotenv
from github import Github, Auth
import os
import requests_cache

requests_cache.install_cache()

load_dotenv()  # take environment variables
GH_TOKEN = os.getenv("GH_TOKEN", default=None)


def repo_list():
    auth = Auth.Token(GH_TOKEN)
    g = Github(auth=auth)
    return list(g.get_user("dxw").get_repos())


def main():
    for i, repo in enumerate(repo_list()):
        do_zizmor(repo.full_name)


def do_zizmor(repo):
    process = subprocess.run(["zizmor", repo, "--format", "json"], capture_output=True)
    # Some errors are acceptable
    stdout = process.stdout.decode("utf-8")
    stderr = process.stderr.decode("utf-8")
    if "no inputs collected" in stderr:
        # print("  No inputs collected -- repo contains no actions?")
        return

    if process.returncode > 0:
        zizmor_json = json.loads(stdout)
        problems = set()

        for item in zizmor_json:
            problems.add(
                f"{item['determinations']['severity']} severity on {repo}: {item['ident']}: {item['desc']}"
            )
        for problem in problems:
            print(problem)


if __name__ == "__main__":
    main()
