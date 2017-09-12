#!/usr/bin/python3
import urllib.request, re
from collections import Sequence
from bs4 import BeautifulSoup
from subprocess import call, check_output # for 'wget', 'uname -m'

class UrlList(Sequence):
    ''' Creates list of all urls from "url" '''
    def __init__(self, url):
        self.links = []
        self.index = -1
        opened_for_soup = urllib.request.urlopen(url)
        print('Checking:==>', url)
        soup = BeautifulSoup(opened_for_soup, 'lxml')
        for link in soup.find_all('a'):
            self.links.append(link.get('href'))

    def latest(self):
        ''' print latest 5 results from "links" '''
        print('Latest 5 kernels are:')
        for link in self.links[-5:]:
            print(link.strip('v/'))

    def drop_rc(self):
        clean = []
        for link in self.links:
            if not re.search("rc\d", link):
                clean.append(link)
        self.links = clean[:]

    def last(self):
        return self.links[-1]

    def link_list(self):
        return self.links

    def __len__(self):
        return len(self.links)

    def __getitem__(self, sliced):
        return self.links[sliced]

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == (len(self.links) - 1):
            self.index = -1
            raise StopIteration
        self.index += 1
        return self.links[self.index]

class AnswerError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class UrlSortForDownload:
    def __init__(self, urls):
        self.links = []
        self.index = -1
        self.arch = Machine().arch()
        self.choice = choose()
        for link in urls:
            if link not in self.links:
                if link.endswith('all.deb'):
                    self.links.append(link)
                if link.endswith(self.arch + '.deb'):
                    if self.choice in link:
                        self.links.append(link)

    def link_list(self):
        return self.links

    def __len__(self):
        return len(self.links)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == (len(self.links) - 1):
            self.index = -1
            raise StopIteration
        self.index += 1
        return self.links[self.index]

class Machine:
    ''' machine specifics - call to unix command('uname -m') '''
    def __init__(self):
        self.architecture = self.arch()

    def arch(self):
        if (check_output(['uname', '-m']).decode().strip()) == 'x86_64' or 'amd64':
            return 'amd64'
        else:
            return 'unknown'

def choose():
    ''' Choices: 1 == generic, 2 == lowlatency '''
    while True:
        try:
            choice = int(input('Choose:\n1) generic\n2) low latency\n>>> '))
            if choice == 1:
                return str('generic')
            elif choice == 2:
                return str('lowlatency')
        except ValueError:
            print('Choose coorrectly int(1) or int(2) - ')

def kernel_version_url(urls):
    chosenOne = [0,1,2,3,4]
    while True:
        links = {}    
        for index, link in enumerate((urls[:-6:-1])):
            links[index] =  link
            print(index, '==>', link)
        try:
            ch = int(input("Choose kernel to download:\n>>>"))
            if ch in chosenOne:
                return links[ch]
            else:
                raise AnswerError('Answer * %s * - eat more SPAM.' % ch, 'use numbers 0-4:')
        except AnswerError as e:
            print(e.expression, e.message)
        except ValueError:
            print('Eat more SPAM! Enter number (0-4)')

def download(path, links):
    for name in links:
        print('downloading:', name)
        call(['wget', '-c', path + name])

class InstallKernel:
    def install_kernel(self, instalable):
        while True:
            try:
                if (str(input('Install it now? (y/n)')) == 'y'):
                    for filename in instalable:
                        print('instaling:', filename)
                        call(['sudo', 'dpkg', '-i', filename])
                    break
                else:
                    print('SeeYaa!')
                    break
            except (TypeError):
                print('Enter "y" or "n".')
