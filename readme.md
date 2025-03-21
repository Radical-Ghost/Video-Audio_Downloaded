# YouTube Video/Audio Downloader

A Python script to download videos, audio, and playlists from YouTube using the `yt-dlp` library. It supports multiple formats, quality settings, and subtitle downloads.

## Features

-   Download video or audio from YouTube.
-   Supports downloading playlists.
-   Customizable file formats (e.g., mp4, mkv, mp3, m4a, etc.).
-   Select video/audio quality (highest, medium, low).
-   Option to download subtitles in multiple languages.

## Prerequisites

-   Python 3.x installed on your system.
-   [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) package installed. If not, you can install it using:

```bash
pip install yt-dlp
```

## Usage

1. Clone or download this repository.
2. Ensure [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) is installed.

### Running the Script

Run the script using Python:

```bash
python your_script_name.py
```

Follow the prompts to download videos, audio, or playlists.

## Options

1. **URL Input**: Enter the YouTube video/playlist URL.
2. **Audio or Video**: Choose whether to download audio only or full video.
3. **Playlist**: Indicate whether the URL is a playlist.
4. **File Format**: Select the desired output format:
    - Audio: mp3, m4a, opus, wav, etc.
    - Video: mp4, mkv, webm, etc.
5. **Subtitles (Optional)**: Download subtitles if available. You can specify a language code (e.g., `en` for English, `all` for all available languages).
6. **Quality**: Choose from the following options:
    - Highest
    - Medium
    - Low

## Example

Downloading a YouTube video in MP4 format with English subtitles:

```bash
python Audio-Video Downloaded.py
```

Input:

```
Enter the URL of the video/playlist: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Do you want to download audio only? (y/n): n
Is this a playlist? (y/n): n
Choose video format (mp4, mkv, webm, etc.): mp4
Do you want to download subtitles? (y/n): y
Enter the subtitle language code (e.g., 'en' for English, 'all' for all languages): en
Choose quality: (1) Highest, (2) Medium, (3) Low: 1
```

## Dependencies

-   Python 3.x
-   yt-dlp

Install dependencies with:

```bash
pip install yt-dlp
```

## Notes

-   Ensure you have the necessary permissions to download and store YouTube content.
-   Use the correct file extension for the chosen format to avoid errors.

## License

This script is for educational purposes. Ensure compliance with YouTube's terms of service when downloading content.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.
