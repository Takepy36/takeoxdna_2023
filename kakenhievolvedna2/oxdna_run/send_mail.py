#!/usr/bin/env python
# coding: utf-8

# In[392]:


import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText


# In[5]:


def program_complete_mail(login_address = "superyoshibros.2@gmail.com",
                          login_password = "fmhskhrkyiwljoye",
                          mail_title = "🎉🎉🎉PYTHON PROGRAM COMPLETED！🎉🎉🎉",
                          mailtext = "program completed"):
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    
    server.login(login_address, login_password)
    
    message = MIMEMultipart()
    message["Subject"] = mail_title
    message["From"] = login_address
    message["To"] = login_address
    text = MIMEText(mailtext)
    #例:"🎉🎉🎉Python program 【{}】 completed!🎉🎉🎉".format(program_name)
    message.attach(text)
    
    server.send_message(message)
    server.quit()


# In[2]:


def main():
    program_complete_mail()


# In[3]:


if __name__ == "__main__":
    main()


# 参考：<br>
# https://gakushikiweblog.com/python-email <br>
# https://support.google.com/accounts/answer/185833?hl=ja

# In[ ]:




