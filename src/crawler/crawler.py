import os, sys
from datetime import datetime

PGA_PATH = os.path.join('..', '..', 'bin', 'pga')
SIVA_PATH = os.path.join('..', '..', 'bin', 'siva')
CRAWLED_URLS_PATH = os.path.join('..', '..', 'data', 'crawled_urls')


def sample(n):
    os.system(PGA_PATH + " list -f json | jq -r '.url' | shuf -n " + str(n) + ' > ' + os.path.join(CRAWLED_URLS_PATH, str(n) + '-urls-' + str(datetime.now()).replace(' ', '-')[:19] +'.txt'))


def main():
    sample(10)


# Alternative version downloading directly from the dataset instead of Github
'''
def main():
    os.system('mkdir ' + CRAWLED_URLS_PATH)
    os.chdir(CRAWLED_URLS_PATH)
    os.system(PGA_PATH + " list -f json | jq -r '.sivaFilenames[]' | shuf -n 10 | " + PGA_PATH + " get -i")
    os.chdir('siva/latest')
    ds = os.listdir('.')
    urls = []
    print('ds', ds)
    print(os.getcwd())
    exit()
    for d in ds:
        os.chdir(d)
        print(os.listdir('.'))
        siva = os.path.join('..', '..', '..', SIVA_PATH)
        os.system(siva + ' unpack *')
        config = open('config', 'r').readlines()
        for l in config:
            if l.split()[0] == 'url':
                url = l.split()[2]
                urls.append(url)
                break
        os.chdir(os.path.join('..', '..', '..'))
    os.chdir(CRAWLED_URLS_PATH)
    with open('urls.txt', 'w') as f:
        f.writelines(urls)
'''

if __name__ == '__main__':
    main()
