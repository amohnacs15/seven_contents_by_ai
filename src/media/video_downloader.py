import youtube_dl
from storage.firebase_storage import firebase_storage_instance, PostingPlatform

"""Save a YouTube video URL to mp3.

    Args:
       # url (str): A YouTube video URL.

    Returns:
        #str: The filename of the mp3 file.
"""        
def save_to_mp3(url):

    options = {
        'outtmpl': 'src/output_downloads/%(title)s-%(id)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'nocheckcertificate': True
     }

    with youtube_dl.YoutubeDL(options) as downloader:
        print('Preparing download...')
        downloader.download(["" + url + ""])
        return downloader.prepare_filename(downloader.extract_info(url, download=False)).replace(".m4a", ".mp3").replace(".webm", ".mp3")

def download_video( url ):
    options = options = {
        'outtmpl': 'src/output_downloads/%(title)s-%(id)s.%(ext)s',
        'format': 'bestvideo/best',
        'nocheckcertificate': True
     }
    with youtube_dl.YoutubeDL(options) as downloader:
        downloader.download(["" + url + ""]) 
        file_path = downloader.prepare_filename(downloader.extract_info(url, download=False)) 
        return file_path
    
def get_downloaded_video_local_path( remote_video_url ):
    try:
        upload_file_path = download_video(remote_video_url)
        firebase_storage_instance.upload_file_to_storage(
            "ai_content_video/" + upload_file_path,
            upload_file_path
        )
        return upload_file_path
    except Exception as e:
        print(f'Error downloading video: {e}')
        return    