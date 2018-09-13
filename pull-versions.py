#!/usr/bin/env python

import subprocess
import urllib2
import yaml
from csv import writer, QUOTE_ALL
from os import devnull
from sys import stdout


def readgittags(repo, ref):    # clone, get the tags, find the version
    # print("pulling, ", repo, ref)
    FNULL = open(devnull, 'w') # Python3 subprocess supports stdout to /dev/null, Python2.7 don't
    subprocess.call(['rm', '-rf', './vercheck'], stdout=FNULL)
    subprocess.call(['git', 'clone', repo, './vercheck'],cwd='.', stdout=FNULL, stderr=FNULL)
    verhash = subprocess.Popen(['git', 'reset', '--hard', ref],cwd='./vercheck', 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().split()[4]
    version = subprocess.Popen(['git', 'describe', '--tags', '--long'],cwd='./vercheck', 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().rstrip()
    subprocess.call(['rm', '-rf', './vercheck'], stdout=FNULL)
    if 'fatal' in version:
        version = "v1.0.0-" + verhash
    return version

def main():
    versiontable= []
    with open("go_deps.yml", 'r') as stream:
        try:
            doc = yaml.load(stream)
            for package,refs in doc['packages'].items():
                version = 0
                url = refs['src_repo']
                refhash = refs['src_ref']
                if ('github.com' in url or 'go.googlesource.com' or 'gopkg.in' in url) : 
                    version = readgittags(url, refhash)
                    package = package.split('/')[-1]
                    # print("appending: ", package, url, version)
                    versiontable.append([package, url, version])
                else:
                    print("unsupported source: ", package, "," , url, "," , refhash , "," , version)
        except yaml.YAMLError as exc:
            print(exc)
    print("\n")
    print('''PACKAGE NAME , SOURCE REPOSITORY , VERSION NUMBER''')
    versiontable.sort()
    writer(stdout, quoting=QUOTE_ALL).writerows(versiontable)

if __name__ == "__main__":
    main()