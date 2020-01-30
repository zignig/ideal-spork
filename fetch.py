# nmigen fetcher 
from git import Repo
import os

repos = {
    'nmigen' :'https://github.com/m-labs/nmigen',
    'nmigen-soc' :'https://github.com/m-labs/nmigen-soc',
    'nmigen-boards' :'https://github.com/m-labs/nmigen-boards',
}

def Fetch(item):
    try:
        r = Repo('lib'+os.sep+item[0])
    except:
        r = Repo.init('lib'+os.sep+item[0])

for  i in repos.items():
    Fetch(i)
