import json
import os
import sys
from github import Github
from github.GithubException import UnknownObjectException as GithubUnknownObjectException

g = Github(os.environ['GITHUB_TOKEN'], per_page=100)

class Repo:
  def __init__(self, repo):
    self.repo = repo

    content = repo.get_contents(".travis.yml")
    
    if "strb92da74ddf4b05b698e2d12ebd56e965d6749397" in content:
      self.normal_checks = '1.10.1'
    elif "2b23ee3dbb274409ae51a620ae9d6fef6516781a" in content:
      self.normal_checks = '1.10.0'
    elif "649a7e0907c0ab4b342688e7d068b574a0945b3e" in content:
      self.normal_checks = '1.9'
    elif "4256f55ef631900df06ca5c6167e21e6ed4cf55b" in content:
      self.normal_checks = '1.7'
    elif "d5f1a5d9e3fbac391b905f2bdfcdcdbfe465eabf" in content:
      self.normal_checks = '1.4'
    else:
      self.normal_checks = false

org = g.get_organization('eustasy')

repos = []
for repo in org.get_repos():
  # Skip archived repositories
  if repo.archived is False:
    print ('Processing {}...'.format(repo.name))
    repos.append(Repo(repo))

repos = sorted(repos, key=lambda repo: repo.name, reverse=False)

json_out = []
for repo in repos:
  json_out.append ({
    "name": repo.repo.name,
    "normal_checks": normal_checks
  })
  
with open('_data/normal_checks.json', 'w') as outfile:
    json.dump(json_out, outfile, indent=2)
