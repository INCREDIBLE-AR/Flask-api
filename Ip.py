import telebot
import requests

API_TOKEN = "7561859306:AAGPGfbgGYvqF3y1ExYJAVxwOMgFQkYJdQ4"  # bot token
bot = telebot.TeleBot(API_TOKEN)

# Group/Chat ID where commands will work
ALLOWED_GROUP_ID = -1001929127676 # group ID
LOG_CHAT_ID = 1996509071  # Group/Chat ID for logging positive responses

# Admin IDs for restricted commands
ADMINS = [1841192361, 1996509071]  # admin IDs

# User database
user_database = []

# Add user to the database
def add_user_to_database(user_id, username):
    if user_id not in [user['id'] for user in user_database]:
        user_database.append({'id': user_id, 'username': username})

# Remove user from the database
def remove_user_from_database(user_id):
    global user_database
    user_database = [user for user in user_database if user['id'] != user_id]

# Get all users from the database
def get_all_users_from_database():
    return user_database

# Check if user has started the bot
def user_has_started(message):
    return message.from_user.id in [user['id'] for user in user_database]

# /start command to mark user as started
@bot.message_handler(commands=['start'])
def start_bot(message):
    add_user_to_database(message.from_user.id, message.from_user.username)
    bot.reply_to(message, "Welcome to the bot! You can now use the /brilliant command.")

# /brilliant command (only in allowed group)
@bot.message_handler(commands=['brilliant'])
def get_brilliant_info(message):
    if not user_has_started(message):
        bot.reply_to(message, "Please start the bot first by sending /start.")
        return
    
    if message.chat.id != ALLOWED_GROUP_ID:
        bot.reply_to(message, "❌ This command can only be used in the designated group.")
        return

    try:
        # Extract phone number from user message
        command = message.text.split(" ")
        if len(command) != 2:
            bot.reply_to(message, "Please use the correct format: /brilliant <phone_number>")
            return
        
        phone_number = command[1]
        api_url = f"https://peach-dahlia-18.tiiny.io/?phone={phone_number}"
        
        # Fetch data from API
        response = requests.get(api_url)
        data = response.json()
        
        # Check if API returned error
        if "error" in data:
            bot.reply_to(message, "𝐁𝐫𝐢𝐥𝐥𝐢𝐚𝐧𝐭 𝐍𝐮𝐦𝐛𝐞𝐫: Not found")
        else:
            # Extract necessary data
            original_number = data.get("registered_sim", "Unknown")
            brilliant_number = data.get("brilliant_number", "Unknown")
            developer = "t.me/STLP_Team"

            # Format the message for the user
            reply_message = (
                "𝗕𝗿𝗶𝗹𝗹𝗶𝗮𝗻𝘁 𝗡𝘂𝗺𝗯𝗲𝗿 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻\n"
                f"𝐎𝐫𝐠𝐢𝐧𝐚𝐥 𝐍𝐮𝐦𝐛𝐞𝐫: {original_number}\n"
                f"𝐁𝐫𝐢𝐥𝐥𝐢𝐚𝐧𝐭 𝐍𝐮𝐦𝐛𝐞𝐫: {brilliant_number}\n"
                f"✨ 𝓓𝓮𝓿𝓮𝓵𝓸𝓹𝓮𝓻 : {developer}"
            )
            bot.reply_to(message, reply_message)

            # Log positive responses
            username = message.from_user.username or "Unknown"
            log_message = (
                "🔒 **Positive Response Logged**\n\n"
                f"📱 **Original Number:** {original_number}\n"
                f"🌟 **Brilliant Number:** {brilliant_number}\n"
                f"👤 **Requested By:** @{username} (User ID: {message.from_user.id})\n"
            )
            bot.send_message(LOG_CHAT_ID, log_message, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# /users command (Admins only, hidden)
@bot.message_handler(commands=['users'])
def show_users(message):
    if message.from_user.id in ADMINS:
        users = get_all_users_from_database()
        user_count = len(users)
        response = f"📊 Total Users: {user_count}"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "❌ You are not authorized to use this command.")

# /broadcast command (Admins only, hidden)
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id in ADMINS:
        if message.reply_to_message:
            if message.reply_to_message.photo:
                file_id = message.reply_to_message.photo[-1].file_id
                caption = message.text.replace('/broadcast ', '').strip() or "Broadcast message"
                users = get_all_users_from_database()
                for user in users:
                    try:
                        bot.send_photo(user['id'], file_id, caption=caption)
                    except Exception as e:
                        print(f"Failed to send message to {user['id']}: {e}")
                        remove_user_from_database(user['id'])
                bot.send_message(message.chat.id, "✅ Broadcast sent!")
            else:
                bot.send_message(message.chat.id, "❌ Please reply to a photo message to broadcast with an image.")
        else:
            bot.send_message(message.chat.id, "❌ Reply to a message to broadcast.")
    else:
        bot.send_message(message.chat.id, "❌ You are not authorized to use this command.")

# Restrict bot usage outside the group
@bot.message_handler(func=lambda message: True)
def restrict_usage(message):
    if message.chat.id != ALLOWED_GROUP_ID:
        bot.reply_to(message, "Join this group to use the bot: @STLP_Community")

print("Bot is running...")
bot.polling()
