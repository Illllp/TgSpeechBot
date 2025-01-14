# Telegram Voice and Video Note to Text Bot

This is a simple Telegram bot that transcribes voice messages and video notes into text using Google's speech recognition.

## Features

- Handles voice messages and video notes sent to the bot.
- Extracts audio from video notes.
- Converts audio to WAV format for better compatibility.
- Uses Google's speech recognition to transcribe audio to text.
- Supports Russian language for transcription.

## Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (You can create a new bot and get a token from [BotFather](https://t.me/BotFather))
- FFmpeg (required for extracting audio from video files, you may need to install it on your system)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Illllp/TgSpeechBot
   cd TgSpeechBot
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate  # On Windows
   ```

3. **Install the necessary libraries:**
   You will need the following Python libraries. You can install them using pip:
   ```bash
   pip install python-telegram-bot pydub SpeechRecognition moviepy
   ```

## Setting up the bot

1. **Replace the placeholder token:**
   Open the `bot.py` file and replace `"YOUR_TELEGRAM_BOT_TOKEN"` with your actual Telegram bot token.
   ```python
   BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

## Running the bot

1. **Start the bot:**
   ```bash
   python tgSpe_bot.py
   ```

2. **Interact with the bot:**
   Open Telegram and search for your bot by its username. Send the bot a voice message or a video note.

## Usage

1. Start a chat with your bot on Telegram.
2. Send the bot a voice message or a video note (up to 300 seconds by default).
3. The bot will process the audio and reply with the transcribed text.

## Configuration

- `MAX_DURATION`:  You can change the maximum allowed duration for voice and video messages in the `bot.py` file. The default value is 300 seconds.

## Contributing

Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License

[LICENSE](LICENSE)
