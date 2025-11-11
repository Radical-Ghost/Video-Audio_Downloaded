import os
import time
import shutil
import yt_dlp


def download_media(url, audio_only=False, playlist=False, file_format=None, subtitles=False, subtitle_lang='all', quality='highest'):
    # Ensure Downloads directory exists next to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(base_dir, 'Downloads')
    os.makedirs(downloads_dir, exist_ok=True)

    # Options for yt-dlp
    # Use %(ext)s to reflect the actual produced extension, and write into the Downloads folder
    ydl_opts = {
        'outtmpl': os.path.join(downloads_dir, '%(title)s.%(ext)s'),
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

    # If audio-only and a specific format was requested, add ffmpeg-based postprocessor
    # but only if ffmpeg/ffprobe are available. Otherwise skip conversion and keep
    # the downloaded audio container (e.g. .webm) and inform the user.
    if audio_only and file_format:
        ffmpeg_path = shutil.which('ffmpeg')
        ffprobe_path = shutil.which('ffprobe')
        if ffmpeg_path and ffprobe_path:
            # Extract audio then convert to requested codec
            ydl_opts.setdefault('postprocessors', [])
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': file_format,
                'preferredquality': '192',
            })
        else:
            print('\n⚠️ ffmpeg/ffprobe not found on PATH. Skipping audio conversion.')
            print('The file will be saved in its original container (for example, .webm).')
            print("To enable automatic conversion to your requested format, install ffmpeg and ensure it's on PATH, or set the 'ffmpeg_location' option.\n")

    # Download the media with error handling
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download and get info dict (for playlists this contains 'entries')
            info = ydl.extract_info(url, download=True)

            # Collect titles downloaded (single video or playlist)
            titles = []
            if playlist and info and isinstance(info, dict) and info.get('entries'):
                for entry in info.get('entries'):
                    if entry:
                        titles.append(entry.get('title'))
            else:
                if info and isinstance(info, dict):
                    titles.append(info.get('title'))

            # Helper to normalize strings for matching filenames
            def _normalize(s):
                if not s:
                    return ''
                return ''.join(ch.lower() for ch in s if ch.isalnum())

            # Verify the files exist in Downloads folder and print absolute paths
            found_any = False
            files = os.listdir(downloads_dir)
            for title in titles:
                norm = _normalize(title)
                matches = [f for f in files if norm and norm in _normalize(f)]
                if matches:
                    found_any = True
                    for m in matches:
                        print(f"✅ Successfully downloaded: '{title}'")
                        print(f"📁 File saved as: {os.path.abspath(os.path.join(downloads_dir, m))}\n")

            if not found_any:
                # Nothing matched exactly; show the newest files to help locate the download
                print("\n⚠️ Download finished but I couldn't locate the file by title in the Downloads folder.")
                print(f"Looking in: {os.path.abspath(downloads_dir)}")
                # Show newest 10 files
                files_with_mtime = []
                for f in files:
                    try:
                        full = os.path.join(downloads_dir, f)
                        mtime = os.path.getmtime(full)
                        files_with_mtime.append((mtime, f))
                    except Exception:
                        continue
                files_with_mtime.sort(reverse=True)
                to_show = files_with_mtime[:10]
                if to_show:
                    print('\nNewest files in Downloads:')
                    for mtime, fname in to_show:
                        print(f" - {fname}  (modified: {time.ctime(mtime)})")
                else:
                    print(' - (No files found in Downloads/)')

    except yt_dlp.utils.DownloadError as e:
        print(f"Error: {e}\nThe media could not be downloaded. Please check the URL and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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