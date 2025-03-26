from flask import Flask, request
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher

import os

TOKEN = os.environ.get("BOT_TOKEN")  # Render에 환경변수로 저장할 예정
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # 예: https://yourapp.onrender.com

app = Flask(__name__)

updater = Updater(token=TOKEN, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

# 자동 인사 핸들러
def welcome(update: Update, context: CallbackContext):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            name = member.full_name
            welcome_message = f"""{name}님 반갑습니다 :))  
유튜브 “코인알려주는라디오” 찐 개미들의  
소통 커뮤니티에 오신 걸 환영합니다🙌🙌

저희는 매매권유❌ 금전적요구❌  
[코알라TV] 사칭을 주의하시길 바랍니다."""
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=welcome_message,
                parse_mode=ParseMode.HTML
            )

# 키워드 응답 핸들러
def keyword_response(update: Update, context: CallbackContext):
    if update.message and update.message.text:
        if update.message.text.strip() == "@1":
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="📌 안내: 이 그룹의 규칙은 다음과 같습니다...\n1. 예의 지키기\n2. 광고 금지\n3. 질문 환영!"
            )

dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, keyword_response))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

if __name__ == "__main__":
    updater.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
