import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')  # Ensure this is set in .env
telegram_token = os.getenv('TELEGRAM_TOKEN')

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize bot and dispatcher
bot = Bot(token=telegram_token)
dp = Dispatcher(bot)

# Set up logging
logging.basicConfig(level=logging.INFO)

class Reference:
    """Stores the conversation history."""
    def __init__(self):
        self.history = []  # List to store past messages

reference = Reference()

# Function to clear past conversation history
def clear_past():
    reference.history = []

@dp.message_handler(commands=['clear'])
async def clear_past_conversation(message: types.Message):
    """Clears previous conversation history."""
    clear_past()
    await message.reply("Previous conversation history has been cleared.")

@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    """Sends a welcome/help message when /start or /help is used."""
    helper_text = """
    🤖 Hi! I am EcoBot, crafted by Thishu Kumar Maharaj. I'm here to guide you on your journey toward an eco-friendly lifestyle! 🌍♻️!
    
    **Commands:**
    🔹 /start - Start the bot
    🔹 /help - Get help
    🔹 /clear - Clear conversation history
    """
    await message.reply(helper_text)

@dp.message_handler()
async def chat_with_gemini(message: types.Message):
    """Handles user messages and responds using Gemini API."""
    print(f'>>> User: {message.text}')

    # Store user message properly
    reference.history.append({"role": "user", "parts": [{"text": message.text}]})

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(reference.history)

        # Extract AI response text
        ai_response = response.text

        # Store AI response correctly
        reference.history.append({"role": "assistant", "parts": [{"text": ai_response}]})

        print(f'>>> Gemini: {ai_response}')
        await bot.send_message(chat_id=message.chat.id, text=ai_response)

    except Exception as e:
        print(f"Error: {e}")
        await message.reply("⚠️ Sorry, an error occurred while processing your request.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
