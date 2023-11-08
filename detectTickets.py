# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:48:11 2023

@author: Léo
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
from datetime import date

from string import Template
from email.message import EmailMessage
import ssl
import smtplib
import pymysql

import psycopg2

urljuv = "https://singletickets.acmilan.com/en/milan-juventus/serie-a-23-24/"

mail_success = f"Y'a des places dispos pour le match MILAN JUV sur : "+urljuv+"\n\nJ'espère que vous arriverez à choper une place\n\n\n"
mail_issue = f"Problème lors de la récupération des données du site. \n\nEssayez de regarder le site :"+urljuv+" c'est peut-être parce qu'il y a des nouvelles places"


def isavailable(urljuv):
    try:
        ticket_found = False
        while ticket_found == False:
            time.sleep(60)
            response = requests.get(urljuv)
            if response.ok:
                soup = BeautifulSoup(response.text, 'lxml')
                target_div = soup.find("div", class_="btn disabled seoLinkDisabled uppercase")
                # Vérifiez si la balise a été trouvée
                if target_div:
                    # Obtenez le contenu de la balise
                    div_content = target_div.text.strip()
                    
                    # Affichez ou enregistrez le contenu comme vous le souhaitez
                    if div_content != "COMING SOON":
                        print("Nouvelle place dispo")
                        sendmail(["email@gmail.com", "email@gmail.com", "email@gmail.com"], mail_success)
                        ticket_found = True
                else:
                    print("La balise div spécifiée n'a pas été trouvée sur la page.")
                    #ici envoyer mail pour dire changement
                    sendmail(["email@gmail.com", "email@gmail.com", "email@gmail.com"], mail_success)
                    ticket_found = True
            else: 
                print(response)
                sendmail(["email@gmail.com", "email@gmail.com"], mail_issue)
                ticket_found = True
            
    except ValueError:
            print(ValueError)
            
def sendmail(emails, text):
    try:
        print("je suis sendmail")
        #envoi mail
        email_sender = 'email@gmail.com'
        email_password = 'password'
        email_receiver = emails
        
        subject = "TICKET DISPO MILAN JUV !"
        body = text
    
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    except ValueError:
        print(ValueError)
    
        
if __name__ == "__main__":
    isavailable(urljuv)
    
