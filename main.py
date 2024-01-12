from pytube import YouTube
import tkinter as tk
from tkinter import ttk
import threading
from queue import Queue
from PIL import Image
import requests as r
import os
import sys
from pathlib import Path
import tkinter.filedialog as fd


def default_directory() -> str:
    OPERATING_SYSTEM: str = sys.platform
    path = None
    match OPERATING_SYSTEM:
        case "linux":
            path = os.path.join(str(Path.home()),"Downloads")
        case "windows":
            path = os.path.join(str(Path.home()),"Downloads")
    return path

# Function to parse urls and add them to the download_queue if they are valid
def link_parser(link:str,download_queue:Queue):
    try:
        request = r.get(url=f"{link}")
        if len(link) > 0:
            if link in download_queue.queue:
                print("Video already in queue.")
            elif ("youtube" in link) and request.status_code in range(200,300) and YouTube(link).check_availability:
                download_queue.put(link)
                print(download_queue.queue)
            else:
                print("Error:404")
        else:
            print("You haven't entered a link.")
    except r.exceptions.MissingSchema:
        print('The provided url is not valid.')
    except r.exceptions.InvalidSchema:
        print("The provided url does not exist.")
    except r.exceptions.ConnectionError:
        print("Failed to connect to the provided url.")


def select_file(bottom_window):
    root = bottom_window
    try:
        x = fd.askopenfile(parent=root,mode="r")
        print(" ".join(x.readlines()))
    except AttributeError:
        print("No file selected.")


def stream_filter(video):
    audio_streams = video.streams.filter(type="audio")
    print(audio_streams)

def downloader(download_queue):
    queue = download_queue.queue
    for i in queue:
        video = YouTube(i)
        stream_filter(video=video)

def download_pop_up():
    thread_lock.acquire()
    directory = default_directory()
    root = tk.Tk()
    root.title("New Download")
    root.resizable(width=False,height=False)
    root.geometry("500x300")

    bottom_frame = tk.Frame(root,width=500,height=300,bg="#353535")
    bottom_frame.pack()
    bottom_frame.propagate(False)

    # Address
    url_frame = tk.Frame(bottom_frame,width=400,height=50,bg="#353535")
    url_frame.place(x=50,y=30)
    url_frame.propagate(False)
    url_label = tk.Label(url_frame,text="URL: ",font="raleway 16",width=5,bg="#353535",fg="white")
    url_label.pack(side="left")
    url_entry = tk.Entry(url_frame,width=40,font="raleway 20",background="#303030",border=1,borderwidth=1,fg="white")
    url_entry.pack(side="left")

    # File Name
    file_name_frame = tk.Frame(bottom_frame,width=400,height=50,bg="#353535")
    file_name_frame.place(x=50,y=80)
    file_name_frame.propagate(False)
    file_name_frame_label = tk.Label(file_name_frame,text="File: ",font="raleway 16",width=5,bg="#353535",fg="white")
    file_name_frame_label.pack(side="left")
    file_name_entry = tk.Entry(file_name_frame,width=40,font="raleway 20",background="#303030",border=1,borderwidth=1,fg="white")
    file_name_entry.pack(side="left")

    # Save Location
    destination_frame = tk.Frame(bottom_frame,width=400,height=50,bg="#353535")
    destination_frame.place(x=50,y=135)
    destination_frame.propagate(False)
    destination_label = tk.Label(destination_frame,text="Dir: ",font="raleway 16",width=5,bg="#353535",fg="white")
    destination_label.pack(side="left")
    destination_entry = tk.Entry(destination_frame,width=40,font="raleway 20",background="#303030",border=1,borderwidth=1,fg="white",textvariable="")
    destination_entry.insert(0, directory)
    destination_entry.pack(side="left")

    # Buttons
    button_frame = tk.Frame(bottom_frame,width=400,height=50,bd=2,bg="#353535",highlightbackground="black",highlightthickness=2)
    button_frame.place(x=50,y=240)
    button_frame.propagate(False)
    download_button = tk.Button(button_frame,text="Download",border=1,bg="#353535",fg="white",width=10,height=2,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white")
    download_button.pack(side="right")
    add_to_queue = tk.Button(button_frame,text="Add to Queue",border=1,bg="#353535",fg="white",width=10,height=2,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white")
    add_to_queue.pack(side="right")
    select_text_file = tk.Button(button_frame,text="Select Text File",border=1,bg="#353535",fg="white",width=10,height=2,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white",command=lambda:select_file(root))
    select_text_file.pack(side="left")
    thread_lock.release()

def main():
    download_queue = Queue()
    download_queue.put("https://www.youtube.com/watch?v=cTCZfjrXyq0")
    download_queue.put("https://www.youtube.com/watch?v=00D_hw9w9Ms")
    completed_downloads = {}
    # add_button_img = Image.open("")
    # Root Window
    root = tk.Tk()
    root.geometry("800x500")
    root.resizable(width=False,height=False)
    root.title("YoutubeDownloader")

    # Frames
    main_frame = tk.Frame(root,width=800,height=500,bg="#353535")
    main_frame.pack()
    left_frame = tk.Frame(main_frame,bg="#303030",width=200,height=490,highlightbackground="black",highlightthickness=1)
    left_frame.place(x=5,y=5)
    queue_frame = tk.Frame(main_frame,bg="#303030",width=585,height=445,highlightbackground="black",highlightthickness=1)
    queue_frame.place(x=210,y=50)
    top_right_frame = tk.Frame(main_frame,bg="#303030",width=585,height=40,highlightbackground="black",highlightthickness=1,padx=3,pady=3)
    top_right_frame.place(x=210,y=5)
    top_right_frame.propagate(False)

    # Buttons
    new_link_button = tk.Button(top_right_frame,text="New",border=0,bg="#353535",fg="white",width=10,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white",command=download_pop_up)
    new_link_button.pack(side="left")
    delete_button = tk.Button(top_right_frame,text="Delete",border=0,bg="#353535",fg="white",width=10,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white")
    delete_button.pack(side="left")
    resume_button = tk.Button(top_right_frame,text="Resume",border=0,bg="#353535",fg="white",width=10,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white")
    resume_button.pack(side="left")
    pause_button = tk.Button(top_right_frame,text="Pause",border=0,bg="#353535",fg="white",width=10,image="",highlightbackground="#353535",font="raleway",activebackground="#6b2f6b",activeforeground="white")
    pause_button.pack(side="left")
    root.mainloop()

thread_lock = threading.Lock()
ui_thread = threading.Thread(target=main,daemon=False)
download_pop_up_thread = threading.Thread(target=download_pop_up,daemon=True)

if __name__ == "__main__":
    print("Launching App...")
    ui_thread.start()
    download_pop_up_thread.start()