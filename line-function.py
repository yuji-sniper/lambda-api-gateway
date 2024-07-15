import json
import os
import requests

def lambda_handler(event, context):
    channel_access_token = os.environ['CHANNEL_ACCESS_TOKEN']
    
    #=========================
    # LINEからのリクエスト解析
    #=========================
    messagetext = event['events'][0]['message']['text']
    print("messagetext: " + messagetext)
    replyToken = event['events'][0]['replyToken']
    print("replyToken: " + replyToken)

    #=========================
    # LINEへのレスポンス作成
    #=========================
    resmessage = [
        {'type':'text','text':messagetext}
    ]
    payload = {'replyToken': replyToken, 'messages': resmessage}
    # カスタムヘッダーの生成(dict形式)
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {channel_access_token}'}
    # headersにカスタムヘッダーを指定
    r = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=json.dumps(payload))
    print("LINEレスポンス:" + r.text)
    return
    
