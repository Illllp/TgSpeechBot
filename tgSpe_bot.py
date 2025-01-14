import logging
import os
import tempfile
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from pydub import AudioSegment
from speech_recognition import Recognizer, AudioFile
from moviepy.editor import VideoFileClip
import speech_recognition as sr

# Replace with your bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MAX_DURATION = 60*5  # Maximum duration in seconds

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message to the user."""
    await update.message.reply_text('Hello! Send me a voice message or a video note.')

async def recognize_speech_from_audio(audio_file_path: str) -> str:
    """Asynchronously recognizes speech from an audio file."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = await asyncio.to_thread(recognizer.recognize_google, audio_data, language="ru-RU")
        return text
    except Exception as e:
        logging.error(f"Speech recognition error: {e}")
        return f"Speech recognition error: {e}"

async def handle_voice_or_video_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles voice messages and video notes, transcribing the audio."""
    temp_files = []
    try:
        if update.message.voice:
            file_extension = "ogg"
            file_info = update.message.voice
            duration = file_info.duration
        elif update.message.video_note:
            file_extension = "mp4"
            file_info = update.message.video_note
            duration = file_info.duration
        else:
            await update.message.reply_text("Please send a voice message or a video note.")
            return

        if duration > MAX_DURATION:
            await update.message.reply_text(f"The message is too long. Maximum duration is {MAX_DURATION} seconds.")
            return

        with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False) as temp_original_file:
            file_path = temp_original_file.name
            temp_files.append(file_path)
            file = await context.bot.get_file(file_info.file_id)
            await file.download_to_drive(file_path)

        audio_file_path = file_path
        if file_extension == "mp4":
            # Extract audio from video
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
                extracted_audio_path = temp_audio_file.name
                temp_files.append(extracted_audio_path)
                try:
                    video = VideoFileClip(file_path)
                    audio = video.audio
                    audio.write_audiofile(extracted_audio_path)
                    video.close()
                except Exception as e:
                    logging.error(f"Error extracting audio from video: {e}")
                    await update.message.reply_text("Error processing the video file.")
                    return
                audio_file_path = extracted_audio_path

        # Convert to WAV if necessary
        if not audio_file_path.lower().endswith(".wav"):
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
                wav_file_path = temp_wav_file.name
                temp_files.append(wav_file_path)
                try:
                    sound = AudioSegment.from_file(audio_file_path)
                    sound.export(wav_file_path, format="wav")
                except Exception as e:
                    logging.error(f"Error converting audio to WAV: {e}")
                    await update.message.reply_text("Error converting the audio file.")
                    return
                audio_file_path = wav_file_path

        # Recognize speech asynchronously
        text = await recognize_speech_from_audio(audio_file_path)
        await update.message.reply_text(f"{text}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await update.message.reply_text(f"An error occurred: {e}")
    finally:
        # Ensure temporary files are deleted
        for file_path_to_remove in temp_files:
            try:
                os.remove(file_path_to_remove)
            except FileNotFoundError:
                logging.warning(f"Temporary file not found: {file_path_to_remove}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handle the /start command
    application.add_handler(CommandHandler('start', start_command))

    # Handle voice messages and video notes
    application.add_handler(MessageHandler(filters.VOICE | filters.VIDEO_NOTE, handle_voice_or_video_note))

    # Start the bot
    application.run_polling()
