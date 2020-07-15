# -*- coding: utf-8 -*-
#Created on Wed Jul  1 01:06:14 2020, @author: dj

#___IMPORTS___
import requests
from bs4 import BeautifulSoup as BF
import time
import discord
from discord import utils
from discord.ext import commands
from xml.etree import ElementTree as ET
from classes import newsContent
import datetime
#___END IMPORTS___

HEADERS = {'_user': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

configRoot = ET.parse('config.xml').getroot()       # getting the root of the configuration file
_CONSOLE_OUTPUT =  True if int(configRoot.find('consoleout').text) != 0 else False
token = str(configRoot.find('token').text)          # getting bot token
channelID = int(configRoot.find('channelID').text)  # getting channel ID for bot messages
checkPeriod = int(configRoot.find('period').text)   # getting check period
newsCount = int(configRoot.find('newscount').text)  # getting the number of news items to check

targets = ET.parse('targets.xml').getroot()         # getting the root of the target file
currentTarget = targets[0].find('pathURL').text     # getting the first target
mainPath = str(targets[0].find('mainPath').text)    # getting the site address. the site uses relative links

hd = newsContent(targets[0].find('mainPath').text)

#___BOT INICIALIZATION___
bot = commands.Bot(command_prefix='!')

def getDataFromSite():
    response = requests.get(currentTarget, headers = HEADERS)
    return BF(response.content, 'html.parser')
    
#___PARSE FUNCTION___
def parse():
    soup = getDataFromSite()

    foundTags = soup.findAll('div', class_ = 'teaser-item')
    newsBlocks = []

    for item in range(0, newsCount):
        newsBlocks.append({
            'header': foundTags[item].find('h2', class_ = 'pos-title').find('a').text,
            'href': mainPath + foundTags[item].find('h2', class_ = 'pos-title').find('a').get('href'),
            'description': foundTags[item].find('li', class_ = 'element element-textarea element-textareapro first last').text,
            'image': foundTags[item].find('img').get('data-src')
        })
    
    hd.setContent(newsBlocks)   
#___END PARSE FUNCTION___


#___BOT FUNCTIONS___
@bot.event
async def on_ready():
    if _CONSOLE_OUTPUT:
        print('Bot started...')
    channel = bot.get_channel(channelID)
    if _CONSOLE_OUTPUT:
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),' Check news...')
    parse()
    while(True):
        newListLinks = []
        oldLinks = hd.getAllLinksFromFile()
        for link in hd.content:
            newListLinks.append(link['href'])
            if link['href'] not in oldLinks:
                
                # if len(oldLinks) > newsCount:
                    # oldLinks.pop()
                # else:
                    # oldLinks.append(link['href'])

                emb = discord.Embed(title = 'Новости игровых распродаж и халявы.', colour = discord.Color.green())
                emb.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
                emb.add_field(name = link['header']+'\n', value = link['description'])
                emb.set_image(url = link['image'])

                await channel.send(embed = emb)
                # for ol in oldLinks:
                    # print(ol)

        hd.writeThisLinksToFile(newListLinks)
        time.sleep(checkPeriod)
        if _CONSOLE_OUTPUT:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),' Check news...')
        parse()

#___END BOT FUNCTIONS___


#___MAIN START___
print("start")
if (getDataFromSite()):
    if _CONSOLE_OUTPUT:
        print('Connection with site - OK.')
    bot.run(token)
else:
    if _CONSOLE_OUTPUT:
        print('Connection FAILED.')






