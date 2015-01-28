#!/usr/bin/python
import os;
import sys;
import getpass;
import requests;
import re;


baseURL = 'http://acm.timus.ru/';


def getSubmission(submIdURL, username, password, session):
    u = baseURL+submIdURL;
    print(u);
    payload = {'Action':'getsubmit', 'JudgeID':username, 'Password':password};
    r = session.post(u,payload);
    l = "";
    for c in r.text:
        if(c=='\r'):
            continue;
        l=l+c;    
    return l;

def buildURL(page, params):
    s = baseURL+page+".aspx?";
    for param in params:
        s = s + param +"="+params[param]+"&";
    return (s[:-1]);

#Get JudgeID and Password
print("Enter JudgeID: ",end="", flush=True);
judgeId = sys.stdin.readline().rstrip();
password = getpass.getpass();
judgeNumber = re.match(r'([0-9]*)', judgeId).group(1);

params = {'author':judgeNumber, 'status':'accepted', 'refresh':'0', 'count':'1000'};
buildURL('status', params);

u = buildURL('status',params);
s = requests.session();

r = s.get(u);
#TODO: what happens if judgeID is invalid ?


submId_pattern = r'"(getsubmit\.aspx/[0-9]*\.[a-z]*)"';
probId_pattern = r'"problem\.aspx\?space=1&amp;num=([0-9]*)"';
probName_pattern = r'<SPAN CLASS="problemname">\. ([^<]*)</SPAN>';

submId_re = re.compile(submId_pattern);
probId_re = re.compile(probId_pattern);
probName_re = re.compile(probName_pattern);

submIds = submId_re.findall(r.text);
probIds= probId_re.findall(r.text);
probNames = probName_re.findall(r.text);

os.makedirs('TIMUS',exist_ok=True);
i = 0;
submIds.reverse();
probIds.reverse();
probNames.reverse();

log = open('./TIMUS/log','w');

for (submId,probId,probName) in zip(submIds, probIds, probNames):
    ext = re.search(r'[0-9]+\.(.*)',submId ).group(1);
    f = open('./TIMUS/'+probIds[i]+'.'+ext,'w');
    f.write('//'+probName+'\n');
    log.write('Downloading '+submId+'\n');
    f.write(getSubmission(submId, judgeId, password, s));
    log.write('Finished '+submId+'to '+probIds[i]+'.'+ext+'\n');
    i=i+1;
