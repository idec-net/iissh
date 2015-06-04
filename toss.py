#!/usr/bin/env python2
# -*- coding: utf8 -*-

import os, sys, base64, hashlib, re
import time

tosslimit=70000
botuser="iissh"
addrprefix="lenina-ssh, "

indexdir="/srv/iissh/echo/"
msgdir="/srv/iissh/msg/"

def hsh(s):
    return base64.urlsafe_b64encode( hashlib.sha256(s).digest() ).replace('-','A').replace('_','z')[:20]

def touch(fname):
    if os.path.exists(fname):
        os.utime(fname, None)
    else:
        open(fname, 'a').close()

def savemsg(hash, echo, message):
    global indexdir, msgdir

    hashfile=os.path.join(msgdir, hash)
    echofile=os.path.join(indexdir, echo)

    touch(hashfile)
    touch(echofile)

    open(hashfile, "w").write(message)
    open(echofile, "a").write(hash+"\n")

def echo_flt(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{1,60}\.\d{1,9}$')
    if rr.match(ea): return True
    else: return False

def msgfrm(mo):
    if ("repto" in mo):
        rptline="/repto/"+mo["repto"]
    else:
        rptline=""
    
    plainmsg="\n".join( ["ii/ok"+rptline, mo["echo"], str(mo["time"]), mo["sender"], mo["addr"], mo["to"], mo["subj"], "", mo["msg"]] )
    msgid=hsh(plainmsg)
    return msgid, plainmsg

def toss(msgfrom,addr,tmsg):
    lines = tmsg.splitlines()
    mo = dict(time=int(time.time()),sender=msgfrom,addr=addr,echo=lines[0],to=lines[1],subj=lines[2],msg='\n'.join(lines[4:]))
    if mo["msg"].startswith('@repto:'):
        tmpmsg = mo["msg"].splitlines()
        mo["repto"] = tmpmsg[0][7:]
        mo["msg"] = '\n'.join(tmpmsg[1:])
    return mo

passwd=open("/etc/passwd").read().splitlines()
users={}
for line in passwd:
    line=line.split(":")
    users[line[0]]=line[4]

group=open("/etc/group").read().splitlines()
groups={}
for line in group:
    line=line.split(":")
    groups[line[0]]=line[3].split(",")

botgroups=[x for x in groups[botuser] if x!=botuser]

addrCount=1

for point in botgroups:
    tossdir="/home/"+point+"/tosses/"
    tosses=os.listdir(tossdir)
    
    for filename in tosses:
        fname=os.path.join(tossdir, filename)
        txt = open(fname).read()
        
        if len(txt)>tosslimit:
            print "msg big: "+fname
            continue
        
        mo = toss(users[point], addrprefix+str(addrCount), txt)
        if mo:
            if (mo["subj"]=="" or mo["msg"]==""):
                print "error: empty message or subj: "+fname
                continue
            if (not echo_flt(mo["echo"])):
                print "error: wrong echo "+mo["echo"]+": "+fname
                continue
            
            hash, text=msgfrm(mo)
            savemsg(hash, mo["echo"], text)
            print "msg ok: "+hash
            os.remove(fname)
    addrCount+=1
