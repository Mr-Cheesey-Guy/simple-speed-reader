#SPEED READER
from tkinter import *
import time
root=Tk()
current_word_index=0
prevtime=0
fullscreen=False

displaying_words=False

def toggle_fullscreen(*args):
    global fullscreen
    if not fullscreen:
        root.attributes("-fullscreen", True)
        fullscreen=True
    else:
        root.attributes("-fullscreen", False)
        fullscreen=False

def stop(a):
    global displaying_words
    displaying_words=False

def start():
    global displaying_words
    displaying_words=True

paused=False

def pause(a):
    global paused
    if not paused:
        paused=True
    else:
        paused=False

def forward(a):
    global current_word_index, extraword, i, text
    i=0
    current_word_index+=10
    if current_word_index>=len(text):
        current_word_index=len(text)-1

def back(a):
    global current_word_index, extraword, i
    i=0
    current_word_index-=10
    if current_word_index<0:
        current_word_index=0

def plusforward(a):
    global current_word_index, extraword, i, text
    i=0
    current_word_index+=50
    if current_word_index>=len(text):
        current_word_index=len(text)-1

def plusback(a):
    global current_word_index, extraword, i
    i=0
    current_word_index-=50
    if current_word_index<0:
        current_word_index=0

def updatetext():
    global current_word_index, text, extraword, pausetime
    extraword=text[current_word_index].split("\n")
    worddisplay.config(text=extraword[i])
    wordcount.config(text=str(round((current_word_index/len(text))*100, 2))+"%, about "+str(round((pausetime*len(text))*1.2)-round(pausetime*current_word_index*1.2))+" seconds remaining")

    cover.config(bg="#101010")
    worddisplay.config(bg="#101010")
    wordcount.config(bg="#101010")

def pauseupdate():
    cover.config(bg="black")
    worddisplay.config(bg="black")
    wordcount.config(bg="black")
    root.update()

helvetbig=("Helvetica", 50, "bold")
helvetreg=["Helvetica", 10]
helvetother=("Helvetica", 20)
root.config(bg="#202020")
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", stop)
root.bind("<space>", pause)
root.bind("<Right>", forward)
root.bind("<Left>", back)
root.bind("<l>", plusforward)
root.bind("<j>", plusback)
root.geometry("1000x500")
root.title("Speed reader")
root.minsize(900, 450)

title=Label(root, text="Read text quickly", bg="#505050", fg="white", font=helvetbig)
title.place(relx=0.2, rely=0, anchor="n")

texttoreadback=Label(root, bg="#353535")
texttoreadback.place(relx=0.5, rely=0.5, anchor="c")

instruction=Label(root, text="Type or paste text to be read here", bg="#353535", fg="#dddddd")
instruction.place(relx=0.15, y=100, anchor="c")

text_to_read_input=Text(root, bg="#101010", fg="white", font=helvetreg)
text_to_read_input.place(relx=0.5, rely=0.5, anchor="c")

texttoreadsize=Scale(root, from_=9, to=30, orient=VERTICAL, bg="#202020", fg="white", borderwidth=0, length=250, width=20, font="none, 10")
texttoreadsize.set(9)
texttoreadsize.place(relx=0.95, rely=0.5, anchor="e")

startbutton=Button(text="Start", font=helvetother, width=10, borderwidth=0, bg="black", fg="white", command=lambda: start())
startbutton.place(relx=0.6, rely=0.91, anchor="c")

tspeed=Text(root, bg="#101010", fg="white", font=helvetother, width=10, height=1)
tspeed.place(relx=0.4, rely=0.91, anchor="c")

tspeed_label=Label(root, bg="#202020", fg="white", font=helvetreg, width=14, height=1, text="WPM (speed)")
tspeed_label.place(relx=0.4, rely=0.97, anchor="c")

prevwidth=root.winfo_width()
prevheight=root.winfo_height()
createdcover=False
savedtext=""
while True:
    if displaying_words:
        #wpm: words per minute
        wpm=tspeed.get(0.0, END)
        try:
            pausetime=60/int(wpm)
            if not createdcover:
                text_to_read_input.config(state=DISABLED)
                tspeed.config(state=DISABLED)
                paused=False
                cover=Label(bg="#101010", width=500, height=200)
                cover.place(relx=0.5, rely=0.5, anchor="c")
                savedtext=text_to_read_input.get(0.0, END)
                text=text_to_read_input.get(0.0, END).split(" ")
                text_to_read_input.destroy()
                worddisplay=Label(font=helvetbig, bg="#101010", fg="white")
                worddisplay.place(relx=0.5, rely=0.5, anchor="c")
                wordcount=Label(font=helvetother, bg="#101010", fg="#888888")
                wordcount.place(relx=0.5, rely=0.7, anchor="c")
                createdcover=True
            current_word_index=0
            while current_word_index<len(text):
                extraword=text[current_word_index].split("\n")
                i=0
                while i<len(extraword):
                    prevtime=time.perf_counter()
                    worddisplay.config(text=extraword[i])
                    wordcount.config(text=str(round((current_word_index/len(text))*100, 2))+"%, about "+str(round((pausetime*len(text))*1.2)-round(pausetime*current_word_index*1.2))+" seconds remaining")
                    root.update()
                    if i==0 and len(extraword)!=1:
                        while time.perf_counter()-prevtime<=pausetime*10:
                            #time.sleep(pausetime*10)
                            updatetext()
                            root.update()
                            while paused:
                                pauseupdate()
                                if not displaying_words: break
                            if not displaying_words: break
                    else:
                        while time.perf_counter()-prevtime<=pausetime:
                            #time.sleep(pausetime)
                            updatetext()
                            root.update()
                            while paused:
                                pauseupdate()
                                if not displaying_words:
                                    break
                            if not displaying_words:
                                break
                    while paused:
                        pauseupdate()
                        if not displaying_words: break
                    cover.config(bg="#101010")
                    worddisplay.config(bg="#101010")
                    wordcount.config(bg="#101010")
                    i+=1
                if not displaying_words: break
                current_word_index+=1
            displaying_words=False
            root.update()
        except:
            tspeed.config(state=NORMAL)
            tspeed.delete(0.0, END)
            tspeed.insert(END, "?")
            displaying_words=False
        
    else:
        if createdcover:
            text_to_read_input=Text(root, bg="#101010", fg="white", font=helvetreg)
            text_to_read_input.place(relx=0.5, rely=0.5, anchor="c")
            cover.destroy()
            worddisplay.destroy()
            wordcount.destroy()
            text_to_read_input.config(state=NORMAL)
            tspeed.config(state=NORMAL)
            text_to_read_input.insert(END, savedtext)
        createdcover=False
        titlerelx=(title.winfo_x()+round(title.winfo_width()/2))/root.winfo_width()
        title.place(relx=titlerelx+((0.5-titlerelx+((root.winfo_pointerx()-root.winfo_rootx()-(root.winfo_width()/2))/30000))/10))
        helvetreg[1]=texttoreadsize.get()
        text_to_read_input.config(font=helvetreg)
        
        text_to_read_input.config(width=round((root.winfo_width())/(helvetreg[1])), height=round((root.winfo_height()/3)/(helvetreg[1])))
        if root.winfo_width()!=prevwidth or root.winfo_height()!=prevheight:
            texttoreadback.config(width=round(root.winfo_width()/6), height=round(root.winfo_height()/24))
            title.config(width=round(root.winfo_width()/20))
        instruction.place(y=texttoreadback.winfo_y()+40)
        prevwidth=root.winfo_width()
        prevheight=root.winfo_height()
        time.sleep(0.01)
    root.update()
    
