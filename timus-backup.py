#!/usr/bin/python
import os;
import sys;
import getpass;
import requests;
import re;


baseURL = 'http://acm.timus.ru/';


def getSubmission(submURLURL, username, password, session):
    u = baseURL+submURLURL;
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


#Get JudgeID and Password from user
print("Enter JudgeID: ",end="", flush=True);
judgeId = sys.stdin.readline().rstrip();
password = getpass.getpass();
judgeNumber = re.match(r'([0-9]*)', judgeId).group(1);
s = requests.session();

#TODO: what happens if judgeID is invalid ?
'''If judgeId is invalid, then page has text Author Not Found.
   Search for that text and then report error. 
'''

submURL_pattern = r'"(getsubmit\.aspx/[0-9]*\.[a-z]*)"';
probId_pattern = r'"problem\.aspx\?space=1&amp;num=([0-9]*)"';
probName_pattern = r'<SPAN CLASS="problemname">\. ([^<]*)</SPAN>';

submURL_re = re.compile(submURL_pattern);
probId_re = re.compile(probId_pattern);
probName_re = re.compile(probName_pattern);

os.makedirs('TIMUS',exist_ok=True);
log = open('./TIMUS/log','w');

payload = {'author':judgeNumber, 'status':'accepted', 'refresh':'0', 'count':'100'};

while True:
    r = s.get(baseURL+'status.aspx', params=payload);
    submURLs = submURL_re.findall(r.text);
    probIds= probId_re.findall(r.text);
    probNames = probName_re.findall(r.text);

    
    i = 0;
    submURLs.reverse();
    probIds.reverse();
    probNames.reverse();

    #No More Submissions
    if(len(submURLs) == 0):
        break;

    for (submURL,probId,probName) in zip(submURLs, probIds, probNames):
        (submId,ext) = re.search(r'([0-9]+)\.(.*)',submURL ).groups();
        f = open('./TIMUS/'+probIds[i]+'.'+ext,'w');
        log.write('Downloading '+submURL+'\n');
        f.write(getSubmission(submURL, judgeId, password, s));
        log.write('Finished '+submURL+'to '+probIds[i]+'.'+ext+'\n');
        if(i==0):
            x = int(submId);
            x = x-1;
            payload['from'] = str(x);
            print(x);
        i=i+1;
