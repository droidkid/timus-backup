#!/usr/bin/python
import os;
import sys;
import getpass;
import requests;
import re;

def regexString(problemClass):
    s = r'<TD CLASS="'+problemClass+r'"><A HREF="status\.aspx\?space=1&amp;num=([0-9]*)&amp;author=[0-9]*" TITLE="(.*)" REL="nofollow">\1</A></TD>'
    return s;

#Get JudgeID and Password
print("Enter JudgeID: ",end="", flush=True);
judgeId = sys.stdin.readline().rstrip();
password = getpass.getpass();
judgeNumber = judgeId[:-2];

s = requests.session();
r = s.get('http://acm.timus.ru/author.aspx?id='+judgeNumber);
print("Receieved Problem List");
#TODO: Check what happens if judgeID is invalid


accepted = regexString("accepted"); 
tried = regexString("tried");
empty = regexString("empty");

pattern = re.compile(accepted);
print("List of Solved Questions: ");
solved = 0;
for (probId, probName) in pattern.findall(r.text):
    print(probId+" "+probName);
    solved=solved+1;
print("Solved: "+str(solved));
