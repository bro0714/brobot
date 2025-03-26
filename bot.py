from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

TOKEN = '7679797075:AAFHXBzrS-2Xce09xEJ6eMDc6RaTp9kQtLU'

# 새 유저 입장 시 자동 인사
def welcome(update, context):
    for member in update.message.new_chat_members:
        name = member.full_name
        welcome_message = f"👋 환영합니다, {name}님!\n이 그룹에 오신 것을 진심으로 환영해요!"
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=welcome_message,
            parse_mode=ParseMode.HTML
        )

# @1 입력 시 안내 멘트
def keyword_response(update, context):
    message_text = update.message.text.strip()
    if message_text == "@1":
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="📌 안내: 이 그룹의 규칙은 다음과 같습니다...\n1. 예의 지키기\n2. 광고 금지\n3. 질문 환영!"
        )

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), keyword_response))

    updater.start_polling()
    print("🤖 봇이 실행 중입니다...")
    updater.idle()

if __name__ == '__main__':
    main()