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
    print(r.text);

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

params = {'author':judgeNumber, 'status':'accepted', 'refresh':'0', 'count':'100'};
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

submId = submId_re.findall(r.text);
probId = probId_re.findall(r.text);
probName = probName_re.findall(r.text);
getSubmission(submId[0], judgeId, password, s);
