import re
import time
import random
import requests
import chconfig
import telegram.ext
from telegram.ext import Updater

statusDict = {}
inStockList = []

def sendRequestToNewEgg(url):
    userAgent = random.choice(chconfig.userAgentList)
    headers = {'User-Agent':userAgent}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            if chconfig.newEggBadResponse in res.text:
                statusDict[url] = False
            else:
                statusDict[url] = True
        elif res.status_code != 200:
            print('Status code error on:', url, 'CODE:', str(res.status_code))
    except Exception:
        print("Something wrong while trying to get", url)


def checkNewEggStock():
    for url in chconfig.newEggProdList3080:
        sendRequestToNewEgg(url)



def check(context: telegram.ext.CallbackContext):
    print('Running check....')
    checkNewEggStock()

    for key in statusDict:
        if key in inStockList:
            if (statusDict[key] is False):
                context.bot.send_message(chat_id=chconfig.CHANNELID, 
                            text=key + ' <-- No Longer in stock !!')
                inStockList.remove(key)
        elif (statusDict[key] is True):
            context.bot.send_message(chat_id=chconfig.CHANNELID, 
                            text=key + ' <-- IN STOCK !! HURRY UP !!')
            inStockList.append(key)
    print('instock status:', inStockList)