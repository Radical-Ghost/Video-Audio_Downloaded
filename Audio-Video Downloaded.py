import yt_dlp

def download_media(url, audio_only=False, playlist=False, file_format=None, subtitles=False, subtitle_lang='all', quality='highest'):
    # Options for yt-dlp
    ydl_opts = {
        'outtmpl': f'%(title)s.{file_format}',  # Use the chosen file format
        'quiet': False,  # Show progress and info
        'no_warnings': False,  # Show warnings if any
        'extract_flat': False,  # Disable flat extraction for playlists
    }

    # Set format based on quality
    if audio_only:
        if quality == 'highest':
            ydl_opts['format'] = 'bestaudio/best'
        elif quality == 'medium':
            ydl_opts['format'] = 'm4a/best'
        elif quality == 'low':
            ydl_opts['format'] = 'mp3/best'
    else:
        if quality == 'highest':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == 'medium':
            ydl_opts['format'] = 'mp4[height<=720]/best'
        elif quality == 'low':
            ydl_opts['format'] = 'mp4[height<=480]/best'

    # If downloading a playlist, add playlist options
    if playlist:
        ydl_opts['yes_playlist'] = True  # Download the entire playlist
    else:
        ydl_opts['noplaylist'] = True  # Download only the single video

    # Add subtitles if requested
    if not audio_only and subtitles:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitleslangs'] = [subtitle_lang]  # Use the chosen subtitle language

    # Download the media
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    print("Welcome to the Video/Audio Downloader!")
    url = input("Enter the URL of the video/playlist: ")

    # Ask if the user wants to download audio or video
    choice = input("Do you want to download audio only? (y/n): ").lower()
    audio_only = choice == 'y'

    # Ask if the user wants to download a playlist
    playlist_choice = input("Is this a playlist? (y/n): ").lower()
    playlist = playlist_choice == 'y'

    # Choose file format
    if audio_only:
        file_format = input("Choose audio format (mp3, m4a, opus, wav, etc.): ").lower()
    else:
        file_format = input("Choose video format (mp4, mkv, webm, etc.): ").lower()

    # Ask for subtitles if video is selected
    subtitles = False
    subtitle_lang = 'all'  # Default to all languages
    if not audio_only:
        subtitles_choice = input("Do you want to download subtitles? (y/n): ").lower()
        subtitles = subtitles_choice == 'y'
        if subtitles:
            subtitle_lang = input("Enter the subtitle language code (e.g., 'en' for English, 'all' for all languages): ").strip().lower()

    # Ask for quality preference
    quality = input("Choose quality: (1) Highest, (2) Medium, (3) Low: ").strip()
    if quality == '1':
        quality = 'highest'
    elif quality == '2':
        quality = 'medium'
    elif quality == '3':
        quality = 'low'
    else:
        print("Invalid choice. Defaulting to highest quality.")
        quality = 'highest'

    # Download the media
    download_media(url, audio_only, playlist, file_format, subtitles, subtitle_lang, quality)

if __name__ == "__main__":
    main()