import tkinter as tk
from tkinter import messagebox

import find_image

import requests
from PIL import Image, ImageTk
from io import BytesIO
from bs4 import BeautifulSoup
import webbrowser
#bs4
def download_src_list(keyword):
    if(search_textbox.get() == ""):
        messagebox.showerror("Empty search","Lütfen aradığınız png için bir anahtar kelime giriniz.")
        return
    global last
    global download_url_list
    global images_to_show
    last = 4
    download_url_list.clear()
    images_to_show.clear()
    url = f"https://www.freeiconspng.com/search.html?q={keyword}&tip=png"

    response = requests.get(url)

    #eğer status code 200 ise diye bir if bloğu ekle

    html_content = response.text

    soup = BeautifulSoup(html_content,'html.parser')

    image_divs = soup.find_all(class_="logo-img")

    for image_div in image_divs:
        image_a = image_div.find('a')
        if(image_a and 'href' in image_a.attrs):
            href = image_a['href']
            img_number = href.split('/')[-1]
            download_url_list.append("https://www.freeiconspng.com/download/"+img_number)

    fetch_images_from_download_url()
            

    


#functions
def on_image_click(event):
    print(event.widget.cget("text"))
    webbrowser.open_new(event.widget.cget("text"))

def fetch_images_from_download_url():
    global download_url_list
    global images_to_show
    global last
    for img_url in download_url_list[last-4:last]:
        response = requests.get(img_url)
        # eğer status code 200 ise
        img_data = response.content

        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200))

        img_tk = ImageTk.PhotoImage(img)
        images_to_show.append(img_tk)

    show_images()
    
def show_images():
    global last
    try:
        img_label1.config(image=images_to_show[last-1],text=download_url_list[last-1])
        img_label2.config(image=images_to_show[last-2],text=download_url_list[last-2])
        img_label3.config(image=images_to_show[last-3],text=download_url_list[last-3])
        img_label4.config(image=images_to_show[last-4],text=download_url_list[last-4])
        print(last)
        last = last + 4

    except:
        messagebox.showerror("Result Error","Sonuç bulunamadı.")


#variables
download_url_list = []
images_to_show = []
last=4


root = tk.Tk()

#tk root

root.title("PNG-ICO Downloader")
root.geometry("1000x400")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_columnconfigure(0, weight=1)

#tk frames
top_frame = tk.Frame(root,bg="grey",height=100, width=1000)
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame = tk.Frame(root,bg="grey",height=300, width=1000)
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

#tk objects

img_label1 = tk.Label(middle_frame,image=None)
img_label1.pack(side=tk.LEFT,padx=5)
img_label1.bind("<Button-1>",on_image_click)
img_label2 = tk.Label(middle_frame,image=None)
img_label2.pack(side=tk.LEFT,padx=5)
img_label2.bind("<Button-1>",on_image_click)
img_label3 = tk.Label(middle_frame,image=None)
img_label3.pack(side=tk.LEFT,padx=5)
img_label3.bind("<Button-1>",on_image_click)
img_label4 = tk.Label(middle_frame,image=None)
img_label4.pack(side=tk.LEFT,padx=5)
img_label4.bind("<Button-1>",on_image_click)


search_label = tk.Label(top_frame,bg="white",fg="black",text="Search : ")
search_label.pack(side=tk.LEFT,padx=20)

search_textbox = tk.Entry(top_frame,bg="white",fg="black",width=70)
search_textbox.pack(side=tk.LEFT,padx=1)

first_page_button = tk.Button(top_frame,text="Search",bg="aqua",command=lambda:download_src_list(search_textbox.get()),width=10)
first_page_button.pack(side=tk.LEFT,padx=20)

next_page_button = tk.Button(top_frame,text="next",bg="aqua",command=fetch_images_from_download_url,width=10)
next_page_button.pack(side=tk.LEFT,padx=20)


def main():
    root.mainloop()
if __name__ == "__main__":
    main()