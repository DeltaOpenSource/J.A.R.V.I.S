import keywords
import pygame
import threading
import webbrowser
from Levenshtein import distance
import config
import requests
import os

pygame.mixer.init()
def play_sound(file):
    def _play():
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
          
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"⚠️ Не удалось воспроизвести {file}: {e}")
    threading.Thread(target=_play, daemon=True).start()

def youtube_open_video(query: str):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 1,
        'key': config.YOUTUBE_API_KEY,
        'safeSearch': 'none',  
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    video_id = data['items'][0]['id']['videoId']
    return f"https://youtu.be/{video_id}?autoplay=1"

def find_closest_command(text: str, command_list, threshold=2):
    if not text.strip():
        return False
    words = text.strip().split()
    for word in words:
        for cmd in command_list:
            clean_cmd = cmd.strip().lower()
            if distance(word.lower(), clean_cmd) <= threshold:
                return True
    return False

def find_closest_site(text: str, site_list, threshold=2):
    if not text.strip():
        return False
    
    words = text.strip().split()

    for word in words:
        for cmd in site_list:
            if distance(word.lower(), cmd) <= threshold:
                return site_list[cmd]
    return False

def handler_commands(command: str):
    if not command:
        return
    
    cmd = command.strip().lower()

    if find_closest_command(command, keywords.GREETINGS):
        play_sound('voice/41.wav')

    if find_closest_command(command, keywords.EXIT):
        os.system('shutdown /s /t 0')

    if find_closest_command(command, keywords.OPEN_OTHER):
        video_url = youtube_open_video(command.replace("запусти", ""))
        webbrowser.open(video_url)
        play_sound('voice/41.wav')
    
    elif find_closest_command(command, keywords.OPEN):
        url = find_closest_site(cmd, keywords.SITES, threshold=2)
        try:
          webbrowser.open(url, new=2)
          play_sound('voice/41.wav')
        except TypeError:
          pass