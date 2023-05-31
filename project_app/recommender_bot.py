import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a command handler function
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('ENTER ID FROM 200 TO 168552')


def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        query.edit_message_text(text="DONE PROCESSING")
        user_id = context.user_data['user_id']
        # Send a request to your recommender system to get top-5 posts for this user id
        response = requests.get(f'http://localhost:8000/post/recommendations/?id={user_id}')
        # Parse the JSON response from your recommender system
        top_5_posts = response.json()
        # Split the message into multiple parts
        if len(top_5_posts) == 1:
            query.message.reply_text("USER NOT FOUND! ENTER ID FROM 200 TO 168552")
        else:
            query.message.reply_text(f'Here are TOP-5 posts user {user_id} might like:')
            for i, post in enumerate(top_5_posts['recommendations']):
                out_message = f'{i + 1}. {post["text"]}'
                if len(out_message) > 4096:
                    for n in range(0, len(out_message), 4096):
                        query.message.reply_text(out_message[n:n + 4096])
                else:
                    query.message.reply_text(out_message)

            keyboard = [[InlineKeyboardButton("YES", callback_data='2')],
                       [InlineKeyboardButton("NO", callback_data='3')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text('TRY ANOTHER ID?', reply_markup=reply_markup)

    if query.data == '2':
        query.message.reply_text('ENTER ID FROM 200 TO 168552')
    elif query.data == '3':
        query.message.reply_text('You can start over by pressing /start. SEE YOU!')

# Define a message handler function
def get_id(update, context):
    """Echo the user message."""
    user_id = update.message.text
    keyboard = [[InlineKeyboardButton("PRESS HERE", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('PRESS THE BUTTON TO PROCEED', reply_markup=reply_markup)
    context.user_data['user_id'] = user_id

def main():
    """Start the bot."""
    # Create an Updater object and attach it to your bot's token
    updater = Updater("6022575976:AAFb2w7UFJEc5FZWu_T2KS7oYsXwPYNn6J0", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))

    # Add message handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_id))

    dp.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()