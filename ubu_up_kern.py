#!/usr/bin/python3
import sys
from uuk import *

answer = {'y':'yes', 'n':'no'}
target_url = 'http://kernel.ubuntu.com/~kernel-ppa/mainline/'
print("Trying to download list of available kernels.")
ln = UrlList(target_url)    # list of paths for kernels
# RC or NOT
while True:
    try:
        rc = input("Interested in 'RC' aka release candidate? yes/no:\n>>>")
        if rc in answer['y']:
            break
        elif rc in answer['n']:
            ln.drop_rc()
            break
        else:
            raise AnswerError('Answer *%s* is not included:' % rc,'answer: y/ye/yes or n/no')

    except (AnswerError, ValueError) as e:
        print(e.expression, e.message)

download_from_here = target_url+kernel_version_url(ln)
lnd = UrlList(download_from_here)
dln = UrlSortForDownload(lnd)
download(download_from_here, dln)
InstallKernel().install_kernel(dln)
