from django.core.mail import send_mail
import random
from django.conf import settings
from .models import voter
'''
def send_otp(email):
    subject = f'OTP verification'
    otp = random.randint(1000,9999)
    otp = str(otp)
    msg = f'Your OTP is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject,msg,email_from,[email])
    vtr = voter.objects.get(email=email)
    vtr.otp = otp
    vtr.save()
    '''

import smtplib
subject = f'OTP verification'
otp = random.randint(1000,9999)
otp = str(otp)
msg = f'Your OTP is {otp}'
def send_otp(mal,msg,rcv):  
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("tempomail736@gmail.com",'c')
    server.sendmail('tempomail736@gmail.com',msg,rcv)
    
    print("succesful")
