#!/usr/bin/env python

import yaml
import os
import subprocess
import pprint
import urllib2
from bs4 import BeautifulSoup

def scrape_github(repo):
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
    # 
    FNULL = open(os.devnull, 'w')
    subprocess.call(['rm', '-rf', './vercheck'], stdout=FNULL)
    subprocess.call(['git', 'clone', repo, './vercheck'],cwd='.', stdout=FNULL, stderr=FNULL)
    subprocess.call(['git', 'reset', '--hard', ref],cwd='./vercheck', stdout=FNULL, stderr=FNULL)
    tags = subprocess.Popen(['git', 'describe', '--tags', '--long'],cwd='./vercheck', stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
    subprocess.call(['rm', '-rf', './vercheck'], stdout=FNULL)
    return tags

def main():
    with open("t.yml", 'r') as stream:
        try:
            doc = yaml.load(stream)
            print("PACKAGE NAME" , "SOURCE REPOSITORY", "SOURCE REFERENCE", "VERSION NUMBER")
            for package,refs in doc['packages'].items():
                print package
                print("      src_repo   {}").format(refs['src_repo'])
                print("      src_ref    {}").format(refs['src_ref'])
                # now we git gud
                url = refs['src_repo']
                if 'github.com' in url:
                    if url.endswith(".git"):
                        url = url[:-4]
                    print(readgittags(url, refs['src_ref']))
                    # print(scrape_github(url))
                # scrape_googlesource()
                # if 'go.googlesource' in url:

                print("=================================")
                print("")
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    main()