import os
import time
import tkinter
import pickle
from pytube import YouTube, Playlist
from multiprocessing import Process, cpu_count

option = None
options = ['video', 'playlist']


def download_video(video_url):
    try:
        while open('downloading.ytd', 'rb') is IOError:
                time.sleep(1)

        file = open('downloading.ytd', 'rb')
        download_file = pickle.load(file)
        downloading_videos = download_file[0]
        downloaded_videos = download_file[1]
        file.close()
    except Exception:
        downloading_videos = []
        downloaded_videos = []
    
    yt = YouTube(video_url)
    print(f"Downloading single video: {yt.title}")

    file = open('downloading.ytd', 'wb')
    downloading_videos.append(yt.title)
    download_status = [downloading_videos, downloaded_videos]
    pickle.dump(download_status, file)
    file.close()

    print(f"Download: {downloading_videos}")
    stream = yt.streams.get_by_resolution("720p")
    #print(f"Size: {stream.filesize/1048576} MB")

    time.sleep(120)
    file = open('downloading.ytd', 'wb')
    downloading_videos.remove(yt.title)
    downloaded_videos.append(yt.title)
    download_status = [downloading_videos, downloaded_videos]
    pickle.dump(download_status, file)
    file.close()


def download(url_entry):
    url = url_entry.get()
    if options[option.get()] == 'video':
        video_process = Process(target=download_video, args=(url,))
        video_process.start()
    elif options[option.get()] == 'playlist':
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            video_process = Process(target=download_video, args=(video_url,))
            video_process.start()
            time.sleep(10)


def update(window, downloading_list, complete_download_list):
    if downloading_list.cget('bg') == 'white':
        downloading_list.config(bg='black', fg='white')
    else:
        downloading_list.config(bg='white', fg='black')

    if complete_download_list.cget('bg') == 'black':
        complete_download_list.config(bg='white', fg='black')
    else:
        complete_download_list.config(bg='black', fg='white')

    try:
        while open('downloading.ytd', 'rb') is IOError:
            time.sleep(1)
            
        file = open('downloading.ytd', 'rb')
        download_file = pickle.load(file)
        downloading_videos = download_file[0]
        downloaded_videos = download_file[1]
        file.close()
    except Exception:
        downloading_videos = []
        downloaded_videos = []

    downloading_list.delete(0, tkinter.END)
    complete_download_list.delete(0, tkinter.END)

    for item in downloading_videos:
        downloading_list.insert(downloading_list.size(), item)

    for item in downloaded_videos:
        complete_download_list.insert(complete_download_list.size(), item)

    print(downloading_videos)
    print(downloaded_videos)
    window.after(5000, update, window, downloading_list, complete_download_list)


def main():
    global option

    try:
        os.remove('downloading.ytd')
    except Exception:
        pass

    window = tkinter.Tk()

    frame_1 = tkinter.Frame(master=window)
    frame_1.pack()

    url_label = tkinter.Label(
        master=frame_1,
        text='YouTube URL:'
    )
    url_label.pack(side='left')

    url_entry = tkinter.Entry(
        master=frame_1
    )
    url_entry.pack(side='right')

    frame_2 = tkinter.Frame(master=window)
    frame_2.pack()
    option = tkinter.IntVar()
    for i in range(len(options)):
        radiobutton = tkinter.Radiobutton(
            master=frame_2,
            text=options[i],
            variable=option,
            value=i,
            justify='center'
        )
        radiobutton.pack(side='left')

    frame_3 = tkinter.Frame(master=window)
    frame_3.pack()
    downloading_label = tkinter.Label(
        master=frame_3,
        text="Downloading"
    )
    downloading_label.grid(row=0, column=0)
    downloading_list = tkinter.Listbox(
        master=frame_3
    )
    downloading_list.grid(row=1, column=0)

    complete_download_label = tkinter.Label(
        master=frame_3,
        text="Downloaded"
    )
    complete_download_label.grid(row=0, column=1)
    complete_download_list = tkinter.Listbox(
        master=frame_3
    )
    complete_download_list.grid(row=1, column=1)

    download_button = tkinter.Button(
        master=window,
        text='Download',
        command=lambda: download(
            url_entry
        )
    )
    download_button.pack(padx=10, pady=10)

    update(window, downloading_list, complete_download_list)

    warning_label = tkinter.Label(
        master=window,
        text="This program was entirely built for educational purposes only. Do not use this program to download YouTube videos."
    )
    warning_label.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
