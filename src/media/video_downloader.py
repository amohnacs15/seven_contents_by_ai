import youtube_dl

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