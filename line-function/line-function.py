import json
import os
import requests

def lambda_handler(event, context):
    channel_access_token = os.environ['CHANNEL_ACCESS_TOKEN']
    reply_api_endpoint = "https://api.line.me/v2/bot/message/reply"
    res_message = "なんもできんかっただ.."
    modes = [
        {
            "name": "リマインド",
            "function": remind
        },
    ]
    
    #=========================
    # LINEからのリクエスト解析
    #=========================
    message = event['events'][0]['message']['text']
    print("messagetext: " + message)
    replyToken = event['events'][0]['replyToken']
    print("replyToken: " + replyToken)
    
    # メッセージの1行目を取得
    mode = message.split("\n")[0]
    
    # モードに応じた処理を実行
    for m in modes:
        if m["name"] == mode:
            res_message = m["function"](message)

    #=========================
    # LINEへのレスポンス作成
    #=========================
    resmessage = [
        {'type':'text','text':res_message}
    ]
    payload = {'replyToken': replyToken, 'messages': resmessage}
    # カスタムヘッダーの生成(dict形式)
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {channel_access_token}'}
    # headersにカスタムヘッダーを指定
    r = requests.post(reply_api_endpoint, headers=headers, data=json.dumps(payload))
    print("LINEレスポンス:" + r.text)
    return


# リマインド機能
def remind(message):
    res_message = ""
    
    parts = message.split("\n")
        
    if len(parts) < 3:
        res_message = "なんか間違っとるだ!"
    
    task = parts[1]
    datetime = parts[2]
    
    # datetimeが8桁の数字かどうかチェック
    if (not datetime.isdigit()) or (len(datetime) != 8):
        res_message = "日付は8桁の数字で入力するだ!"
    
    # taskが空文字かどうかチェック
    if task == "":
        res_message = "タスク名を入力するだ!"
    
    # リマインド登録
    res_message = f"「{task}」を\n{datetime}に\nリマインドするだ!"
    
    return res_message
