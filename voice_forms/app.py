# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:15:59 2020

@author: sangamesh kulkarni(TechGhost)
"""


# Importing essential libraries
from flask import Flask, render_template, request
from textblob import TextBlob
import re
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

import smtplib 
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import socket
import dns.resolver


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    text= request.form['message']
    phone=request.form['phone']
    email=request.form['emailadd']
    
    blob=TextBlob(text)
    res=blob.sentiment.polarity
    
    phone_re = re.compile('^[0-9]{10}$')
    email_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    
    text_corrected=tool.correct(text)
    print(text_corrected)
    
    
    addressToVerify =email
    records = dns.resolver.query('scottbrady91.com', 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    host = socket.gethostname()
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    server.connect(mxRecord)
    server.helo(host)
    server.mail('me@domain.com')
    code, message = server.rcpt(str(addressToVerify))
    server.quit()
    
    if re.search(email_re,email) and phone_re.search(phone) and code==250:
        
        fromaddr = "hypertext18assassins@gmail.com"
        toaddr = email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Message from hyper-text assasins"
        if(res>0):
            body = "Thank you !!!   We are glad to hear this from you...."
        if(res<0):
            body = "Thank you !!!  We are very sorry to hear this from you....u can raise complaint at hypertex18assassins@gmail.com"
        if(res==0):
            body = "Thank you !!!"
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login(fromaddr, "sangamesh")   
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text) 
        s.quit()
        
        
        
        
        if(res>0):
            return render_template('index.html', ans='Thank you !!!  We are glad to hear this from you😊')
        if(res<0):
            return render_template('index.html', ans='Thank you !!!  We are very sorry to hear this from you😢....u can raise complaint at hypertex18assassins@gmail.com')
        if(res==0):
            return render_template('index.html', ans='Thank you😊 !!!') 
    else:
        return render_template('index.html',ans="Form not submitted....... Invalid email or/and  phone number")
    
 

          

if __name__ == '__main__':
	app.run(debug=True)
