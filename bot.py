import checker
import chconfig
import telegram.ext
from telegram.ext import Updater


def aliveMessage(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=chconfig.CHANNELID, 
                             text='Hello im Alive and ready to bot !!\nI will be checking newegg every 2 minutes and updating here.')


def main():
    u = Updater(chconfig.TOKEN, use_context=True)
    j = u.job_queue
    j.run_once(aliveMessage, when=0)
    j.run_repeating(checker.check, interval=120, first=1)
    u.start_polling()
    u.idle()


if __name__ == "__main__":
    main()