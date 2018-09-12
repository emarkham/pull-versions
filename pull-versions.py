#!/usr/bin/env python

import yaml
import os
import subprocess
import pprint
import urllib2
from bs4 import BeautifulSoup

def scrape_github(repo):
    if 'github.com' in repo:
        if repo.endswith(".git"):
            repo = repo[:-4]
    # Alternate idea, screen scrape if I don't like readgittags()
    try:
        page = urllib2.urlopen(repo+'/tags')
    except Exception as exc:
        print(exc)
    soup = BeautifulSoup(page, 'html.parser')
    try:
        version = soup.find('h4', attrs={'commit-title'}).text
    except:
        version = "NO_VERSION_FOUND"
    return version
    # print(soup.get_text())

def readgittags(repo, ref):
    # clone, get the tags, fine dhe version
    FNULL = open(os.devnull, 'w')
    subprocess.call(['rm', '-rf', './vercheck'], stdout=FNULL)
    subprocess.call(['git', 'clone', repo, './vercheck'],cwd='.', stdout=FNULL, stderr=FNULL)
    verhash = subprocess.Popen(['git', 'reset', '--hard', ref],cwd='./vercheck', stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().split()[4]
    version = subprocess.Popen(['git', 'describe', '--tags', '--long'],cwd='./vercheck', stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().rstrip()
    subprocess.call(['rm', '-rf', './vercheck'], stdout=FNULL)
    if 'fatal' in version:
        version = "v1.0.0-" + verhash
    return version

def main():
    with open("go_deps.yml", 'r') as stream:
        try:
            doc = yaml.load(stream)
            print('"PACKAGE NAME" , SOURCE REPOSITORY , VERSION NUMBER')
            for package,refs in doc['packages'].items():
                url = refs['src_repo']
                refhash = refs['src_ref']
                if ('github.com' in url or 'go.googlesource' in url) :
                    version = readgittags(url, refhash)
                    package = package.split('/')[-1]
                print('{} , {} , {}'.format(package, url, version))
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    main()