# nmigen fetcher 
from git import Repo
import os

repos = {
    'nmigen' :'https://github.com/m-labs/nmigen',
    'nmigen-soc' :'https://github.com/m-labs/nmigen-soc',
    'nmigen-boards' :'https://github.com/m-labs/nmigen-boards',
}

def Fetch(item):
    name = item[0]
    url = item[1]
    path = 'lib'+os.sep+name
    print(name,url,path)
    try:
        r = Repo(path)
    except:
        print(name + " does not exist , creating")
        r = Repo.init(path)
        r.create_remote('origin',url)
        r.remotes.origin.pull('master')

    return r

local_repos = []
for  i in repos.items():
    local_repos.append(Fetch(i))
