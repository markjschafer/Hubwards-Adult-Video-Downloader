#! /usr/bin/env python3
'''
MIT License

Copyright (c) 2021 Mark Schafer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from __future__ import unicode_literals
from tkinter import SUNKEN, LEFT, RIGHT, WORD, TOP, BOTTOM, END, YES, BOTH, Y, SOLID, W
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES, ThemedStyle
from tkinter import messagebox as mbox
from tkinter.font import nametofont
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from HubwardsData import Yvideos, YTdl, HaveGot, Thumb, NoWord, PornStar
import HubwardsConst as AppC
from HubwardsCsv import insert_values_to_table
from HubwardsDialog import MySimpleDialog
from threading import Thread
import youtube_dl
import requests
import re
import datetime
import time
from time import sleep
from urllib.parse import urlparse
from pathlib import Path
import os
import sys
import subprocess
import csv
import pandas as pd
import urllib3
import gender
from easysettings import EasySettings

settings = EasySettings("PornConfigFile.conf")

###############################  CLASSES ###################################################

class BrowseVideos(object):
    def __init__(self, master, VidFolder):
       # Add Some Style
        self.VidFolder = VidFolder
        style = ThemedStyle(master)
        style.theme_use(AppC.styleTheme)
        style.configure("Treeview",rowheight=AppC.TvLineHt,font=(AppC.TvFont))
        style.configure("Treeview.Heading", font=(AppC.TvFont)) # Modify the font of the headings
        style.map('Treeview', background=[('selected', "#347083")])


        self.lbl_filler0 = tk.Label(TAB4_TOP,  text='', width=10)
        self.lbl_filler0.pack(side=tk.LEFT)
        self.btn_Reset = tk.Button(TAB4_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 15, text = "Reset", bg = "red",
                            command = self.dispTree4)
        self.btn_Reset.pack(side=tk.LEFT)
        self.lbl_filler1 = tk.Label(TAB4_TOP,  text='', width=10)
        self.lbl_filler1.pack(side=tk.LEFT)
        self.btn_view = tk.Button(TAB4_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 15, text = "View", bg = "blue",
                            command = self.ViewVideo)
        self.btn_view.pack(side=tk.LEFT)
        self.lbl_filler2 = tk.Label(TAB4_TOP,  text='', width=10)
        self.lbl_filler2.pack(side=tk.LEFT)
        self.btn_help = tk.Button(TAB4_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 15, text = "Player Help", bg = "gold",
                            command = self.TAB4help)
        self.btn_help.pack(side=tk.LEFT)


        self.Tree4_scroll = tk.Scrollbar(TAB4_BOT)
        self.Tree4_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.Tree4=ttk.Treeview(TAB4_BOT, style="Treeview", show='tree', yscrollcommand=self.Tree4_scroll.set)
        self.Tree4.pack(side=tk.RIGHT, fill="both", expand=True)
        self.Tree4_scroll.config(command=self.Tree4.yview)
        self.Tree4.heading('#0', text='Folder：'+VidFolder, anchor='w')
        self.Tree4.column('#0', anchor=tk.W, width=200)
        self.Tree4.bind('<Button-3>', self.item_return)
        self.abspath=os.path.abspath(self.VidFolder)
        self.node=self.Tree4.insert('','end',values=self.abspath, text=VidFolder,open=True)
        self.traverse_dir(self.node,self.abspath)

    def dispTree4(self):
        x = self.Tree4.get_children()
        for item in x:
            self.Tree4.delete(item)
        self.abspath=os.path.abspath(self.VidFolder)
        self.node=self.Tree4.insert('','end',values=self.abspath, text=self.VidFolder,open=True)
        self.traverse_dir(self.node,self.abspath)



    def traverse_dir(self, parent, path):
        for d in os.listdir(path):
            master = parent
            full_path=os.path.join(path, d)
            isdir = os.path.isdir(full_path)
            if isdir:
                id = self.Tree4.insert(parent,'end',values=path, text=d,open=False)
                self.traverse_dir(id, full_path)
            else:
                basename, ext = os.path.splitext(full_path)
                known = ['.mp4', '.m4v', '.avi', '.wmv', '.flv', '.mpg', '.mpeg', '.mov', '.ogv']
                if ext.lower() in known:
                    id = self.Tree4.insert(parent,'end',values=path, text=d,open=False)

    def TAB4help(self):

        d = MySimpleDialog(master,
                     text="Highlight a folder and select play, plays all files in folder "
                        "Enter key skips to next video in que "
                        "Spacebar pauses / restarts video "
                        "(.) forward single frame, (,) rewind single frame "
                        "m = Mute on/off, l = loop video, j = subtitles on/off, f = full screen on/off "
                        "s = screenshot, i = video information, [ = reduce speed, ] = increase speed "
                        "F8 displays the playlist on screen "
                        "Q quits play immediately ",
                     fsize=16,
                     buttons=["OKAY"],
                     default=0,
                     cancel=1,
                     title="Information about Video Player")
        ans = d.go()



    def item_return(self, event):
        self.ViewVideo()

    def SearchVideo():

        pass

    def ViewVideo(self):
        item = self.Tree4.selection()
        cntr = 0
        plist = open("pllist.txt", "w")
        for i in item:
            cntr += 1
            icount = len(i)
            fpath = self.Tree4.item(i, "values")[0]
            fname = self.Tree4.item(i, "text")
            fullfile = os.path.join(fpath, fname)
            plist.write(fullfile+"\n")
        plist.close()
        p1 = subprocess.Popen(['mpv', AppC.mpvConfig,'--fs', '--volume=25', '--osd-bold=yes', '--osd-duration=6000', '--osd-level=2', '--resume-playback=no','--screenshot-directory='+AppC.screenshotPath ,'--playlist=pllist.txt',],)
        p1.wait()

    def item_Delete(self):
        item = self.Tree4.selection()
        cntr = 0
        for i in item:
            cntr += 1
            icount = len(i)
            fpath = self.Tree4.item(i, "values")[0]
            fname = self.Tree4.item(i, "text")
            fullfile = os.path.join(fpath, fname)
            os.remove(fullfile)
            self.Tree4.delete(item)

    def __del__(self):
        pass

class NoWordsTable(object):
    def __init__(self, master):
        style = ThemedStyle(master)
        style.theme_use(AppC.styleTheme)
        style.configure("TButton",rowheight=AppC.BtnLineHt,font=((AppC.BtnFont)))
        self.button_add_noword = tk.Button(TAB1_LHS_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 10, text = "Add No-word", bg = "green",
                            command = self.addNoWord)
        self.button_add_noword.pack(side=tk.LEFT)
        self.button_edit_noword = tk.Button(TAB1_LHS_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 10, text = "Edit No-word", bg = "blue",
                            command =self.editNoWord)
        self.button_edit_noword.pack(side=tk.LEFT)
        self.button_del_noword = tk.Button(TAB1_LHS_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 10, text = "Delete No-Word", bg = "red",
                            command = self.del_noword)
        self.button_del_noword.pack(side=tk.LEFT)
        self.button_reload_noword = tk.Button(TAB1_LHS_TOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 10, text = "Reset", bg = "gold",
                            command = self.dispTree5)
        self.button_reload_noword.pack(side=tk.LEFT)

        style = ThemedStyle(master)
        style.theme_use(AppC.styleTheme)
        style.configure("Treeview",rowheight=AppC.TvLineHt,font=(AppC.TvFont))
        style.configure("Treeview.Heading", font=(AppC.TvFont)) # Modify the font of the headings
        style.map('Treeview', background=[('selected', "#347083")])

        # Create a Treeview Scrollbar
        self.tree5_scroll = tk.Scrollbar(TAB1_LHS_BOT)
        self.tree5_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree5 = ttk.Treeview(TAB1_LHS_BOT, style="Treeview", show='headings', yscrollcommand=self.tree5_scroll.set)
        self.tree5.pack(side=tk.RIGHT, fill="both", expand=True)
        self.tree5_scroll.config(command=self.tree5.yview)
        self.tree5['columns'] = ("id", "noword")
        for col in self.tree5['columns']:
            self.tree5.heading(col, text=col, command=lambda _col=col: treeview_sort_column(self.tree5, _col, False))
        self.tree5.column('id', width=0, stretch=tk.NO)
        self.tree5.column('noword', anchor=tk.W, width=100)

        self.dispTree5()

    def dispTree5(self):
        x = self.tree5.get_children()
        for item in x:
            self.tree5.delete(item)
        iidcntr = 0
        for row in noword.view():
            self.tree5.insert('', 'end', iid=iidcntr, values=(row))
            iidcntr = iidcntr + 1

    def del_noword(self):
        item = self.Tree5.selection()
        for i in item:
            id = self.Tree5.item(i, "values")[0]
            noword.delete(id)
        self.dispTree5()

    def editNoWord(self):
        self.GetNoWord(False)

    def addNoWord(self):
        self.GetNoWord(True)

    def GetNoWord(self, isNew):
        def top_update():
            NoWord = VNoWord.get()
            if isNew:
                noword.insert("", NoWord)
            else:
                noword.update(id, NoWord)
            self.dispTree5()
            top.destroy()

        top = tk.Toplevel(master, bg = 'blue' )
        top.title("Edit No Words Table")
        top.attributes('-topmost',True)

        if isNew == False:
            item = self.tree5.selection()
            for i in item:
                self.tree5.item(i, "values")[1]
                id = self.tree5.item(i, "values")[0]
                NoWord = self.tree5.item(i, "values")[1]
        else:
            NoWord = ""

        LNoWord = tk.Label(top, text = "Please enter a No Word")
        LNoWord.place(x = 10,y = 10)
        VNoWord = tk.StringVar(top)
        VNoWord.set(NoWord)
        ENoWord = tk.Entry(top, textvariable=NoWord, width=5, bd = 5)
        ENoWord.place(x = 310,y = 10)

        BtnUpdate = tk.Button(top, text = "Update Data", command=top_update)
        BtnUpdate.place(x = 300, y = 240)

        window_height = 400
        window_width = 900

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

###############################
class VideoDownload(object):
    def __init__(self, url, download_opts, path):
        self.url = url
        self.download_opts = download_opts
        self.path = path
        self.status = {"status": "getting mdl_etadata..."}
        self.info = None
        self.tree_id = None

    def to_columns(self):
        if self.info is None:
            return self.url, self.status["status"], "", "", ""

        percent = "unknown"

        if self.status.get("downloaded_bytes", None) and self.status.get("total_bytes", None):
            percent = "%.2f%%" % (float(self.status['downloaded_bytes'])/float(self.status['total_bytes']) * 100.0)
        if self.status["status"] == "finished":
            percent = "100%"

        # todo format speed
        speed = ""
        if self.status.get("speed"):
            speed = "%.1f kB/s" % (self.status["speed"] / 1000.0)

        eta = ""
        if self.status.get("eta"):
            seconds = self.status["eta"]

            if seconds > 3600:
                eta = ">1 hour"
            elif seconds > 60:
                eta = "%d:%2d" % (seconds / 60, seconds % 60)
            else:
                eta = "%2d" % seconds

        return self.info.get("title", self.url), self.status["status"], percent, speed, eta, self.status.get("error", "")

    def __str__(self):
        if self.info:
            return "%s | %s" % (self.info.get("title", self.url), self.status["status"])
        else:
            return "%s | %s" % (self.url, self.status["status"])


class DownloaderUI(object):
    class StdoutRedirector(object):
        def __init__(self, widget):
            self.widget = widget

        def write(self,string):
            sys.__stdout__.write(string)
            if '\n' not in string:
                string = string + '\n'
            self.widget.insert('end',string)
            self.widget.see('end')

        def writelines(self, lines):
            sys.__stdout__.writelines(lines)
            for line in lines:
                self.text.write(line)

        def flush(self):
            sys.__stdout__.flush()

    def __init__(self, parent):
        self.downloading = 0
        self.downDone = False
        style = ThemedStyle(master)
        self.Console_Display1 = tk.Text(TAB3_P_RBOT,background="lightblue", foreground="black", font=(AppC.ConsFont), height=15)
        self.Console_Display1.pack(side=tk.BOTTOM)

        self.button_add_video = tk.Button(TAB3_P_LTOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 15, text = "Add", bg = "green",
                            command = self.new_single_video_callback)
        self.button_add_video.pack(side=tk.LEFT, ipadx = 30, ipady = 10)
        self.button_remove_download_from_list = tk.Button(TAB3_P_LTOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 15, text = "Remove", bg = "blue",
                            command = self.on_remove)
        self.button_remove_download_from_list.pack(side=tk.LEFT, ipadx = 30, ipady = 10)
        self.button_clear_video = tk.Button(TAB3_P_LTOP, padx = 16, pady = 8, bd = 16,
                            fg = "black", font = ('arial', 16, 'bold'),
                            width = 15, text = "Clear Videos", bg = "gold",
                            command = self.clear_vodeos)
        self.button_clear_video.pack(side=tk.RIGHT, ipadx = 30, ipady = 10)

        style = ThemedStyle(master)
        style.theme_use(AppC.styleTheme)
        style.configure("Treeview",rowheight=AppC.TvLineHt,font=(AppC.TvFont))
        style.configure("Treeview.Heading", font=(AppC.TvFont))
        style.map('Treeview', background=[('selected', "#347083")])
        self.videos_treeview = ttk.Treeview(TAB3_P_LBOT, style="Treeview", selectmode=tk.EXTENDED, columns=('Name', 'Status', 'dl_perc', 'dl_speed', 'Remaining', 'Error'))
        [self.videos_treeview.heading(x, text=x) for x in self.videos_treeview['columns']]
        self.videos_treeview.column("#0", width=10)
        self.videos_treeview.pack(fill=tk.BOTH, expand=1)
        self.videos_not_displayed = []
        self.videos_displayed = {}
        self.update_video_ui_repeating(TAB3_P_LBOT)

    def on_remove(self):
        indices = self.videos_treeview.selection()
        for index in indices:
            title = self.videos_treeview.item(index, "values")[0]
            VideoUrl = ytdl.deletetitle(title)
            if VideoUrl:
                uPath = urlparse(VideoUrl).path
                st = find_nth(uPath, '/', 2)
                VideoID = uPath[st+1:]
                if VideoID:
                    yvideos.deleteVideoID(VideoID)

            dispTree2()
            self.videos_displayed.pop(index, None)
            self.videos_treeview.delete(index)


    def update_video_ui_repeating(self, widget):
        # check stderr
        children = self.videos_treeview.get_children()
        for child in children:
            self.videos_treeview.item(child, text="", values=self.videos_displayed[child].to_columns())
            Action = self.videos_treeview.item(child, "values")[1]
            if "been recorded in archive" in Action or "finished" in Action:
                title = self.videos_treeview.item(child, "values")[0]
                VideoUrl = ytdl.deletetitle(title)
                if VideoUrl:
                    uPath = urlparse(VideoUrl).path
                    st = find_nth(uPath, '/', 2)
                    VideoID = uPath[st+1:]
                    if VideoID:
                        yvideos.deleteVideoID(VideoID)
                        self.downDone = True

                dispTree2()
                self.videos_displayed.pop(child, None)
                self.videos_treeview.delete(child)
        for vid in self.videos_not_displayed:
            key = self.videos_treeview.insert("", "end", text="", values=vid.to_columns())
            lastKey = key
            self.videos_displayed[key] = vid
        self.videos_not_displayed.clear()

        widget.after(100, lambda: self.update_video_ui_repeating(widget))

    @staticmethod
    def download_progress_hook(video_download, status):
        video_download.status = status

    @staticmethod
    def start_download(video_download):
        with youtube_dl.YoutubeDL({}) as ydl:
            info_dict = ydl.extract_info(video_download.url, download=False)
            video_download.info = info_dict
        ydl_opts = {
            'format': AppC.YDL_format,
            'download_archive': AppC.YDL_Archive,
            'no_warnings': AppC.YDL_no_warnings,
            'quiet': AppC.YDL_quiet,
            'noplaylist' : AppC.YDL_noplaylist,
            'ignoreerrors': AppC.YDL_ignoreerrors,
            "progress_hooks": [lambda x: DownloaderUI.download_progress_hook(video_download, x)],
            **video_download.download_opts
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_download.url])

    def create_video_download(self, url, download_opts, path):
        video_download = VideoDownload(url, download_opts, path)
        self.videos_not_displayed.append(video_download)
        try:
            thread = Thread(target=self.start_download, args=(video_download,))
            thread.start()
        except:
            self.on_remove()


    def submit_new_video_for_download(self, url, destination):
        error = None
        opts = {'outtmpl': os.path.join(destination, AppC.YDL_OutStru)}
        self.create_video_download(url, opts, destination)

    def clear_vodeos(self):
        d = MySimpleDialog(master,
                     text='Are you sure you want to delete everything?',
                     fsize=16,
                     buttons=["Yes", "No"],
                     default=0,
                     cancel=1,
                     title="Clear Download Queue")
        ans = d.go()
        if ans == 0:
            ytdl.deleteall()
            dispTree2()


    def new_single_video_callback(self):
        row = ytdl.viewOne()
        if row:
            Vid = row[0]
            durl = row[2]
            url = durl
            started = 1
            ytdl.updateOne(started, Vid)
            destination = AppC.YDL_exportPath
            sys.stdout = self.StdoutRedirector(self.Console_Display1)
            self.submit_new_video_for_download(url, destination)

    def download_src(self, url, chunk_size=1024):
        self.DispStatus(" Downloading Src")
        req = urllib3.PoolManager().request('GET', url, preload_content=False)
        src = req.data.decode('utf-8')
        req.release_conn()
        return src

    def DispStatus(self, toshow):
        print(toshow)

    def download_vid(self,filename, url):
        outname = AppC.exportPath+filename
        self.DispStatus("Downloading "+filename)
        with open(outname, 'wb') as fout:
            response = requests.get(url, stream=True)
            status = response.raise_for_status()
            if status:
                self.DispStatus(status)
            for block in response.iter_content(8192):
                fout.write(block)


    def processUrl(self, url):
        self.DispStatus("Download source")
        src = self.download_src(url)

        self.DispStatus("Parse details")

        title_regex = r'setVideoTitle\(\'(.*)\'\);'
        vid_highq_regex = r'setVideoUrlHigh\(\'(.*)\'\);'

        title = re.search(title_regex, src).group(1)
        highq_url = re.search(vid_highq_regex, src).group(1)

        self.download_vid(parse_filename(title) + ".mp4", highq_url)


    def parse_filename(self, name):
        keepcharacters = (' ', '.', '_')
        return ''.join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()




#mjs############################## END OF  CLASSES #############################################





def DispCount():
    os.system("clear")
    print("\n\n\n\n\n\r"+" Raw CSV extraction -- Total Count "+str(totalcount)+" Total Saved "+str(totalokcount)+"  ", end="")

def doQuit():
        d = MySimpleDialog(master,
                     text='Are you sure you want to Quit?',
                     fsize=16,
                     buttons=["Yes", "No"],
                     default=0,
                     cancel=1,
                     title="Exit the system")
        ans = d.go()
        if ans == 0:
            master.destroy()

def Linect(fname):
    lc = sum(1 for l in open(fname))
    return lc

def csvlist():
    CsvInPath = os.path.join(AppC.csvpath,"./IN/")
    CsvList = []
    for dirpath, dirs, files in os.walk(CsvInPath):
        for filename in files:
            if filename.endswith('.csv'):
                CsvList.append(filename)
    return CsvList

def remouldCsv():
    CsvList = csvlist()
    CsvInPath = os.path.join(AppC.csvpath,"./IN/")
    CsvOutPath = os.path.join(AppC.csvpath,"./OUT/")

    VideoIDlist = []
    if CsvList:
        for csvfile in CsvList:
            Category = csvfile[:-4]

            ImportFile = os.path.join(CsvInPath, csvfile)
            ExportFile = os.path.join(CsvOutPath, csvfile)
            allcntr = 0
            savcntr = 0
            lncnt = Linect(ImportFile)

            with open(ImportFile,'r')as source:
                reader = csv.reader(source, delimiter=';')
                with open(ExportFile, "w") as result:
                    writer = csv.writer(result, delimiter=';')
                    for line in reader:
                        embed = line[0]
                        pic1 = line[1]
                        title = line[3]
                        if title.isascii() == False:
                            continue
                        tags = line[5]
                        cats = " "
                        if line[6]:
                            cats = line[6]
                        try:
                            secs = int(line[7])
                        except:
                            continue
                        if secs < AppC.minsecs:
                            continue
                        ctime = datetime.timedelta(seconds=secs)
                        Duration = str(ctime)
                        st = find_nth(embed, '/', 4)
                        en = find_nth(embed, '"', 2)
                        VideoID = embed[st+1:en]
                        VideoUrl = "https://www.pornhub.com/view_video.php?viewkey="+VideoID
                        upath = urlparse(pic1).path
                        st = find_nth(upath, '/', 2)
                        en = find_nth(upath, '/', 3)
                        ud_pt1 = upath[st+1:en]
                        st = find_nth(upath, '/', 3)
                        en = find_nth(upath, '/', 4)
                        ud_pt2 = upath[st+1:en]
                        UploadDate = str(ud_pt1) + str(ud_pt2)
                        if "Gay" not in tags:
                            continue

                        writer.writerow(("",VideoID, title, UploadDate, Duration, tags, cats, VideoUrl))


def CsvImport():
    style = ThemedStyle(master)
    style.theme_use(AppC.styleTheme)
    style.configure("TLabel",rowheight=AppC.TkrLineHt, font=AppC.TkrFont)
    action1_label['text'] = "This is a long process. You will be told when it finishes "
    master.update()

    remouldCsv()

    yvideos.deleteall()

    Rsrce = os.path.join(AppC.csvpath,"./OUT")
    '''
    ImportRaw-Pt3.sh
    csvout="${1}"/"*.csv"
    cat $csvout > allcsv.in
    sort -t ";" -k2,2 -u -o allcsv1.csv allcsv.in
    cat allcsv1.csv | tr -d "'"  > allcsv.csv
    '''
    sp = subprocess.call("./ImportRaw-Pt3.sh '%s'" % Rsrce, shell=True)

    insert_values_to_table('yvideos', './allcsv.csv')

    deletefor()

    action1_label['text'] = "CSV process is now complete. "
    master.update()
    time.sleep(5)
    action1_label['text'] = ""
    master.update()

def deletefor():
    action1_label['text'] = "Deleting records from NoList"
    master.update()

    totaldeleted = 0
    rows = noword.view()
    sechword = ""
    sqltitsrch = "SELECT * FROM yvideos WHERE VideoTitle LIKE "
    sqltitdel = "DELETE FROM yvideos WHERE VideoTitle LIKE "
    sqlcatsrch = "SELECT * FROM yvideos WHERE VideoCats LIKE "
    sqlcatdel = "DELETE FROM yvideos WHERE VideoCats LIKE "
    sqltagsrch = "SELECT * FROM yvideos WHERE lower(VideoTags) LIKE "
    sqltagdel = "DELETE FROM yvideos WHERE lower(VideoTags) LIKE "
    for row in rows:
        srchword = row[1]
        sqlnoword = "'%"+srchword+"%'"
        srows = yvideos.generic(sqltitsrch+sqlnoword)
        if len(srows) > 0:
            totaldeleted = totaldeleted + len(srows)
            yvideos.genericupd(sqltitdel+sqlnoword)
            action1_label['text'] = "Records Deleted : "+str(len(srows))+" For "+srchword+" Total Deleted "+str(totaldeleted)
            master.update()
        crows = yvideos.generic(sqlcatsrch+sqlnoword)
        if len(crows) > 0:
            totaldeleted = totaldeleted + len(crows)
            yvideos.genericupd(sqlcatdel+sqlnoword)
            action1_label['text'] = "Records Deleted : "+str(len(crows))+" For "+srchword+" Total Deleted "+str(totaldeleted)
            master.update()
        trows = yvideos.generic(sqltagsrch+sqlnoword)
        if len(trows) > 0:
            totaldeleted = totaldeleted + len(trows)
            yvideos.genericupd(sqltagdel+sqlnoword)
            action1_label['text'] = "Records Deleted : "+str(len(trows))+" For "+srchword+" Total Deleted "+str(totaldeleted)
            master.update()


    pstarsql = "WHERE Gender = 'F'"
    rows = pornstar.viewfor(pstarsql)
    sechword = ""
    sqltitsrch = "SELECT * FROM yvideos WHERE VideoTitle LIKE "
    sqltitdel = "DELETE FROM yvideos WHERE VideoTitle LIKE "
    sqlcatsrch = "SELECT * FROM yvideos WHERE VideoCats LIKE "
    sqlcatdel = "DELETE FROM yvideos WHERE VideoCats LIKE "
    for row in rows:
        srchword = row[1]
        sqlnoword = "'%"+srchword+"%'"
        srows = yvideos.generic(sqltitsrch+sqlnoword)
        if len(srows) > 0:
            totaldeleted = totaldeleted + len(srows)
            yvideos.genericupd(sqltitdel+sqlnoword)
            action1_label['text'] = "Records Deleted : "+str(len(srows))+" For "+srchword+" Total Deleted "+str(totaldeleted)
            master.update()
        crows = yvideos.generic(sqlcatsrch+sqlnoword)
        if len(crows) > 0:
            totaldeleted = totaldeleted + len(crows)
            yvideos.genericupd(sqlcatdel+sqlnoword)
            action1_label['text'] = "Records Deleted : "+str(len(crows))+" For "+srchword+" Total Deleted "+str(totaldeleted)
            master.update()

############################### TAB2 FUNCTIONS  #######################################
def videoTags_changed(event):
    x = tree1.get_children()
    for item in x:
        tree1.delete(item)
    iidcntr = 0
    videoCats_cb.set("")
    selected = videoTags_cb.get()
    selected = '"%'+selected+'%"'

    sqlexpr = "WHERE VideoTags LIKE "+selected+" ORDER BY DateUploaded DESC;"
    for row in yvideos.viewfor(sqlexpr):
        tree1.insert('', 'end', iid=iidcntr, values=(row))
        iidcntr = iidcntr + 1
    RecordCount(iidcntr)

def videoCats_changed(event):
    x = tree1.get_children()
    for item in x:
        tree1.delete(item)
    iidcntr = 0
    videoTags_cb.set("")
    selected = videoCats_cb.get()
    selected = '"%'+selected+'%"'
    sqlexpr = "WHERE VideoCats LIKE "+selected+" ORDER BY DateUploaded DESC;"
    for row in yvideos.viewfor(sqlexpr):
        tree1.insert('', 'end', iid=iidcntr, values=(row))
        iidcntr = iidcntr + 1
    RecordCount(iidcntr)


def do_copy():
    fout = open("urls.txt", "w")
    item = tree1.selection()
    for i in item:
        VideoID = tree1.item(i, "values")[1]
        cTitle = tree1.item(i, "values")[2]
        cUrl = tree1.item(i, "values")[7]
        ytdl.insert(cTitle, cUrl, 0)
        print(cUrl, file=fout)
    notebk.select(TAB3)
    dispTree2()

# LOAD / RELOAD TREE1 STRUCTURE
def dispTree1():
    action1_label['text'] = "Loading Data"
    master.update()

    x = tree1.get_children()
    for item in x:
        tree1.delete(item)
    iidcntr = 0
    videoTags_cb.set("")
    videoCats_cb.set("")
    search_entry.delete(0, tk.END)
    for row in yvideos.view():
        tree1.insert('', 'end', iid=iidcntr, values=(row))
        iidcntr = iidcntr + 1
    RecordCount(iidcntr)
    action1_label['text'] = ""
    master.update()


def RecordCount(counter):
    info1_label['text'] = " Records %d" % counter+"  "
    master.update()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    if len(l) > AppC.MaxDispSort:
        d = MySimpleDialog(master,
                     text="Too many records to sort this way, "
                          "refine your filter or change AppC.MaxDispSort setting. "
                          "  ",
                     fsize=16,
                     buttons=["OKAY"],
                     default=0,
                     cancel=1,
                     title="Warning")
        ans = d.go()
        return
    else:
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, text=col, command=lambda _col=col: \
                     treeview_sort_column(tv, _col, not reverse))

# PERFORM A TEXT SEARCH OF TREE1
def Search(Return):
    if search_entry.get() != "":
        x = tree1.get_children()
        for item in x:
            tree1.delete(item)
        iidcntr = 0
        searchtext = search_entry.get()
        rows = yvideos.search(searchtext)
        for row in rows:
            tree1.insert('', 'end', iid=iidcntr, values=(row))
            iidcntr = iidcntr + 1
    RecordCount(iidcntr)

############################### TAB3 FUNCTIONS  #######################################
def dispTree2():
    x = tree2.get_children()        #
    for item in x:                  # clear tree if exists
        tree2.delete(item)          #
    iidcntr = 0
    for row in ytdl.view():     # build new tree with new data
        vid = row[0]
        title=row[1]
        tree2.insert('', 'end', iid=iidcntr, values=(row))
        iidcntr = iidcntr + 1

def chngDFlag(event):
    item = tree2.selection()
    for i in item:
        Vid = tree2.item(i, "values")[0]
        started = 0
        ytdl.updateOne(started, Vid)

############################### GENERAL FUNCTIONS  #######################################
def get_proxies():
    res = requests.get("https://free-proxy-list.net/")
    name = "Proxylist"
    proxies = pd.read_html(res.text)
    proxies = proxies[0][:-1]
    Proxie = []
    for index,row in proxies.iterrows():
        Proxie.append("%s:%s\n"%(row["IP Address"],int(row["Port"])))
    return Proxie


def staticCount():
    staticCount.counter += 1
    os.system("clear")
    print("\n\n\n\n\n\r"+"                  Records Procrssed %d" % staticCount.counter, end="")

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

###################### TEST NEW DOWNLOADER ######################################################
def loadhavegot():
    if AppC.HaveGotOn == True:
        style = ThemedStyle(master)
        style.theme_use(AppC.styleTheme)
        style.configure("TLabel",rowheight=AppC.TkrLineHt, font=AppC.TkrFont)
        action1_label['text'] = "Adding downloaded videos to seen table "
        master.update()

        with open (AppC.YDL_Archive, "r") as lines:
            for line in lines:
                line = line.rstrip()
                line = line.split(" ")
                if len(line) > 1:
                    Vid = line[1]
                    site = line[0]
                    if site == "pornhub":
                        if havegot.isthere(Vid) == False:
                            havegot.insert(Vid, site)
        os.remove(AppC.YDL_Archive)
        action1_label['text'] = "Completed Adding downloaded videos to seen table "
        master.update()
        time.sleep(2)
        action1_label['text'] = ""
        master.update()

def prochavegot():
    if AppC.HaveGotOn == True:
        style = ThemedStyle(master)
        style.theme_use(AppC.styleTheme)
        style.configure("TLabel",rowheight=AppC.TkrLineHt, font=AppC.TkrFont)
        action1_label['text'] = "Removing downloaded videos from database "
        master.update()

        sqline = " WHERE lower(FromSite) = 'pornhub'"
        rows = havegot.viewfor(sqline)
        for row in rows:
            Vid = row[1]
            if yvideos.isthere(Vid):
                yvideos.deleteVideoID(Vid)
        action1_label['text'] = "Completed Removing downloaded videos from database "
        master.update()
        time.sleep(2)
        action1_label['text'] = ""
        master.update()


########################### NOTEBOOK FUNCTIONS ###########################################

def on_change_tab(NotebookTabChanged):
    cur_tab_index = notebk.index('current')
    if cur_tab_index == 0:
        pass
        #Front Screen
    if cur_tab_index == 1:
        pass
#        dispTree1()
    if cur_tab_index == 2:
        dispTree2()
        Downloader
    if cur_tab_index == 3:
        pass
    if cur_tab_index == 4:
        pass
    if cur_tab_index == 5:
        pass

def on_reset_tab(event):
    cur_tab_index = notebk.index('current')
    if cur_tab_index == 3:
        Tab4app.dispTree4()

def on_quit_tab(event):
    cur_tab_index = notebk.index('current')
    if cur_tab_index == 6:
        pass

def get_Archive_Source():
    pass

def get_csvpath():
    csvpath = str(filedialog.askdirectory())
    E_csvpath.delete(0, END)
    E_csvpath.insert(0, csvpath+"/")
    S_csvpath.set(csvpath+"/")

def get_imagePath():
    imagePath = str(filedialog.askdirectory())
    E_imagePath.delete(0, END)
    E_imagePath.insert(0, imagePath+"/")
    S_imagePath.set(imagePath+"/")

def get_screenshotPath():
    screenshotPath = str(filedialog.askdirectory())
    E_screenshotPath.delete(0, END)
    E_screenshotPath.insert(0, screenshotPath+"/")
    S_screenshotPath.set(screenshotPath+"/")

def get_YDL_Archive():
    YDL_ArchivePath = os.path.split(YDL_Archive)[0]
    YDL_Archive = str(filedialog.askopenfile(initialdir=YDL_ArchivePath ,mode='r', filetypes=[('Text Files', '*.txt')]))
    E_YDL_Archive.delete(0, END)
    E_YDL_Archive.insert(0, YDL_Archive+"/")
    S_YDL_Archive.set(YDL_Archive+"/")

def get_YDL_exportPath():
    YDL_exportPath = str(filedialog.askdirectory())
    E_YDL_exportPath.delete(0, END)
    E_YDL_exportPath.insert(0, YDL_exportPath+"/")
    S_YDL_exportPath.set(YDL_exportPath+"/")

def setsave():
    settings.set("FontFamily", S_FontFamily.get())
    settings.set("FontSize", S_FontSize.get())
    settings.set("ProxyOn", True if S_ProxyOn.get()==1 else False)
    settings.set("HaveGotOn", True if S_HaveGotOn.get()==1 else False)
    settings.set("allowImport", True if S_allowImport.get()==1 else False)
    settings.set("exportTags", True if S_exportTags.get()==1 else False)
    settings.set("exportCats", True if S_exportCats.get()==1 else False)
    settings.set("orientation", S_orientation.get())
    settings.set("minsecs", S_minsecs.get())
    settings.set("VideoTagsDisp", S_VideoTagsDisp.get())
    settings.set("VideoCatsDisp", S_VideoCatsDisp.get())
    settings.set("MaxDispSort", S_MaxDispSort.get())
    settings.set("Archive_Source", S_Archive_Source.get())
    settings.set("csvpath", S_csvpath.get())
    settings.set("imagePath", S_imagePath.get())
    settings.set("mpvConfig", S_mpvConfig.get())
    settings.set("screenshotPath", S_screenshotPath.get())
    settings.set("YDL_Archive", S_YDL_Archive.get())
    settings.set("YDL_exportPath", S_YDL_exportPath.get())
    settings.set("YDL_Flags", S_YDL_Flags.get())
    settings.set("YDL_format", S_YDL_format.get())
    settings.set("YDL_ignoreerrors", True if S_YDL_ignoreerrors.get()==1 else False)
    settings.set("YDL_no_warnings", True if S_YDL_no_warnings.get()==1 else False)
    settings.set("YDL_noplaylist", True if S_YDL_noplaylist.get()==1 else False)
    settings.set("YDL_quiet", True if S_YDL_quiet.get()==1 else False)
    settings.set("YDL_UseNetrc", True if S_YDL_UseNetrc.get()==1 else False)
    settings.set("YDL_Options", S_YDL_Options.get())
    settings.set("YDL_OutStru", S_YDL_OutStru.get())
    settings.set("TvFont", S_TvFont.get())
    settings.set("TvLineHt", S_TvLineHt.get())
    settings.set("TvDlFont", S_TvDlFont.get())
    settings.set("TvDlLineHt", S_TvDlLineHt.get())
    settings.set("ConsFont", S_ConsFont.get())
    settings.set("ConsLineHt", S_ConsLineHt.get())
    settings.set("CbFont", S_CbFont.get())
    settings.set("LblFont", S_LblFont.get())
    settings.set("LblLineHt", S_LblLineHt.get())
    settings.set("ProgFont", S_ProgFont.get())
    settings.set("ProgLineHt", S_ProgLineHt.get())
    settings.set("BtnFont", S_BtnFont.get())
    settings.set("BtnLineHt", S_BtnLineHt.get())
    settings.set("EntFont", S_EntFont.get())
    settings.set("EntLineHt", S_EntLineHt.get())
    settings.set("MboxFont", S_MboxFont.get())
    settings.set("TkrFont", S_TkrFont.get())
    settings.set("TkrLineHt", S_TkrLineHt.get())
    settings.set("styleTheme", variable.get())
    settings.save()

def makeBrowseVideos():
    global Tab4app

    VidPath=AppC.YDL_exportPath

    Tab4app = BrowseVideos(master, VidPath)


########################### TKINTER LAYOUT ###########################################
master = ThemedTk(theme=AppC.styleTheme)
style = ThemedStyle(master)
style.set_theme(AppC.styleTheme)
style.theme_use(AppC.styleTheme)
defaultFont = nametofont("TkDefaultFont")
defaultFont.configure(family=AppC.FontFamily, size=AppC.FontSize, weight=font.BOLD)

style = ttk.Style(master)
current_theme =style.theme_use()
style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"padding": [20, 5]}}})
style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"font" : ('URW Gothic L', '18', 'bold')}}})
notebk = ttk.Notebook(master)
notebk.pack(pady=5, expand=True)
TAB1 = ttk.Labelframe(notebk, width = 1920, height = 1050, relief = tk.RAISED, text="")
TAB2 = ttk.Labelframe(notebk, width = 1920, height = 1050, relief = tk.RAISED, text="")
TAB3 = ttk.Labelframe(notebk, width = 1920, height = 1050, relief = tk.RAISED, text="")
TAB4 = ttk.Labelframe(notebk, width = 1920, height = 1050, relief = tk.RAISED, text="")
TAB5 = ttk.Labelframe(notebk, width = 1920, height = 1050, relief = tk.RAISED, text="")
notebk.add(TAB1, text = 'Utilities')
notebk.add(TAB2, text = 'Filter Videos')
notebk.add(TAB3, text = 'Download Videos')
notebk.add(TAB4, text = 'View Videos')
notebk.add(TAB5, text = 'Settings')
notebk.enable_traversal()
notebk.bind('<<NotebookTabChanged>>', on_change_tab)
notebk.bind('<Double-Button>', on_reset_tab)
notebk.bind('<Control-q>', on_quit_tab)

####################### SET UP TAB1 PANES ###########################################
TAB1_PANEV = ttk.PanedWindow(TAB1, orient=tk.VERTICAL, width=1900, height=300)
TAB1_PANEV.pack(fill='both', expand=True)
TAB1_TOP = ttk.Label(TAB1_PANEV)
TAB1_PANEV.add(TAB1_TOP, weight=1)
TAB1_BOT = ttk.Label(TAB1_PANEV)
TAB1_PANEV.add(TAB1_BOT, weight=3)

if AppC.allowImport:
    TAB1_PANEH = ttk.PanedWindow(TAB1_BOT, orient=tk.HORIZONTAL, width=1900, height=300)
    TAB1_PANEH.pack(fill='both', expand=True)
    TAB1_LHS = ttk.Label(TAB1_PANEH)
    TAB1_RHS = ttk.Label(TAB1_PANEH)
    TAB1_PANEH.add(TAB1_LHS, weight=1)
    TAB1_PANEH.add(TAB1_RHS, weight=4)

    TAB1_V_PANE_L = ttk.PanedWindow(TAB1_LHS, orient=tk.VERTICAL, width=800, height=600)
    TAB1_V_PANE_L.pack(fill='both', expand=True)
    TAB1_LHS_TOP = ttk.Label(TAB1_V_PANE_L)
    TAB1_LHS_BOT = ttk.Label(TAB1_V_PANE_L)
    TAB1_V_PANE_L.add(TAB1_LHS_TOP, weight=1)
    TAB1_V_PANE_L.add(TAB1_LHS_BOT, weight=4)

    TAB1_V_PANE_R = ttk.PanedWindow(TAB1_RHS, orient=tk.VERTICAL, width=800, height=200)
    TAB1_V_PANE_R.pack(fill='both', expand=True)
    TAB1_RHS_TOP = ttk.Label(TAB1_V_PANE_R)
    TAB1_RHS_BOT = ttk.Label(TAB1_V_PANE_R)
    TAB1_V_PANE_R.add(TAB1_RHS_TOP, weight=1)
    TAB1_V_PANE_R.add(TAB1_RHS_BOT, weight=4)

####################### SET UP TAB1_TOP buttons ###########################################
if AppC.allowImport:

    btn_fullupdate = tk.Button(TAB1_TOP, padx = 16, pady = 8, bd = 16,
                    fg = "black", font = ('arial', 16, 'bold'),
                        width = 40, text = "Update from CSV import file ", bg = "blue",
                    command=CsvImport)
    btn_fullupdate.pack(side=tk.TOP, ipadx = 30, ipady = 10)
    btn_deletefor = tk.Button(TAB1_TOP, padx = 16, pady = 8, bd = 16,
                    fg = "black", font = ('arial', 16, 'bold'),
                        width = 40, text = "Remove Unwanted Records", bg = "green",
                    command=deletefor)
    btn_deletefor.pack(side=tk.TOP, ipadx = 30, ipady = 10)

btn_Quit = tk.Button(TAB1_TOP, padx = 16, pady = 8, bd = 16,
                fg = "black", font = ('arial', 16, 'bold'),
                    width = 40, text = "Quit System", bg = "red",
                command = doQuit)
btn_Quit.pack(side=tk.TOP, ipadx = 30, ipady = 10)


style = ThemedStyle(master)
style.theme_use(AppC.styleTheme)
style.configure("TLabel",rowheight=AppC.TkrLineHt ,font=AppC.TkrFont)

action1_label = ttk.Label(TAB1_TOP, style="TLabel", text = f"Action: ")
action1_label.pack()
action1_label['text'] = ""
master.update()

action2_label = ttk.Label(TAB1_TOP, style="TLabel", text = f"Action: ")
action2_label.pack()
action2_label['text'] = ""
master.update()

####################### SET UP TAB2 PANES ###########################################
TAB2_PANEV = ttk.PanedWindow(TAB2, orient=tk.VERTICAL, width=1880, height=1000)
TAB2_PANEV.pack(fill='both', expand=True)
TAB2_TOP = ttk.Label(TAB2_PANEV,  text='')
TAB2_BOT = ttk.Label(TAB2_PANEV, text='')
TAB2_PANEV.add(TAB2_TOP, weight=1)
TAB2_PANEV.add(TAB2_BOT, weight=10)

#################### GET CATEGORY CB TITLES ##################################
yvideos = Yvideos("Pornhub.db")
if AppC.exportCats:
    expt = open("VCats.txt", "w")
sqlstring = "SELECT VideoCats FROM yvideos"
rows = yvideos.generic(sqlstring)
d = dict()
for row in rows:
    rline = row[0]
    if not rline=="":
        words = rline.split(",")
        for word in words:
            if word in d:
                d[word] = d[word] + 1
            else:
                d[word] = 1

catdata = []
CatsDisp = AppC.VideoCatsDisp
for k in sorted(d, key=d.get, reverse=True)[:CatsDisp]:
    if AppC.exportTags:
        print(k, file=expt)
    catdata.append(k)

videoCats = (catdata)

#################### GET tAGS CB TITLES #######################

yvideos = Yvideos("Pornhub.db")
if AppC.exportTags:
    expt = open("VTags.txt", "w")
sqlstring = "SELECT VideoTags FROM yvideos"
rows = yvideos.generic(sqlstring)
d = dict()
for row in rows:
    rline = row[0]
    if not rline=="":
        words = rline.split(",")
        for word in words:
            if word in d:
                d[word] = d[word] + 1
            else:
                d[word] = 1

tagdata = []
TagsDisp = AppC.VideoTagsDisp
for k in sorted(d, key=d.get, reverse=True)[:TagsDisp]:
    if AppC.exportTags:
        print(k, file=expt)
    if k.isalpha():
        tagdata.append(k)

videoTags = sorted(tagdata)

###############################################

info1_label = ttk.Label(TAB2_TOP, style="TLabel", width = 15)
info1_label.pack(side=tk.RIGHT)

btn_reset = tk.Button(TAB2_TOP, padx = 16, pady = 8, bd = 16,
                fg = "black", font = ('arial', 16, 'bold'),
                    width = 10, text = "Reset", bg = "red",
                command=dispTree1)
btn_reset.pack(side=tk.RIGHT, ipadx = 30, ipady = 10)
btn_copy = tk.Button(TAB2_TOP, padx = 16, pady = 8, bd = 16,
                fg = "black", font = ('arial', 16, 'bold'),
                    width = 10, text = "Copy selected", bg = "green",
                command=do_copy)
btn_copy.pack(side=tk.RIGHT, ipadx = 30, ipady = 10)


### INCREASE CB DROPDOWN FONT SIZE #####
style = ThemedStyle(master)
selected_category = tk.StringVar()
videoCats_cb = ttk.Combobox(TAB2_TOP,style='TCombobox', textvariable=selected_category, font=AppC.CbFont, width=20)
master.option_add('*TCombobox*Listbox.font', AppC.CbFont)
videoCats_cb['values'] = videoCats
videoCats_cb['state'] = 'readonly'  # normal
videoCats_cb.pack(side=tk.RIGHT) #, anchor=tk.N)   #, padx=20, pady=15)
videoCats_cb.bind('<<ComboboxSelected>>', videoCats_changed)

### INCREASE CB DROPDOWN FONT SIZE #####
style = ThemedStyle(master)
selected_category = tk.StringVar()
selected_videoTags = tk.StringVar()
videoTags_cb = ttk.Combobox(TAB2_TOP, textvariable=selected_videoTags, font=AppC.CbFont, width=20)
master.option_add('*TCombobox*Listbox.font', AppC.CbFont)
videoTags_cb['values'] = videoTags
videoTags_cb['state'] = 'readonly'  # normal
videoTags_cb.pack(side=tk.RIGHT)
videoTags_cb.bind('<<ComboboxSelected>>', videoTags_changed)


search_entry = tk.Entry(TAB2_TOP, font = ('arial', 16, 'bold'), bd = 10, width = 60,
                fg = "black", bg = "powder blue", justify = tk.LEFT)
search_entry.pack(side=tk.RIGHT)
search_entry.bind('<Return>', Search)



####################### SET UP TAB2_BOT INIT ###########################################

# Add Some Style
style = ThemedStyle(master)
style.theme_use(AppC.styleTheme)
style.configure("Treeview",rowheight=AppC.TvLineHt,font=(AppC.TvFont))
style.configure("Treeview.Heading", font=(AppC.TvFont)) # Modify the font of the headings
style.map('Treeview', background=[('selected', "#347083")])

# Create a Treeview Scrollbar
tree1_scroll = tk.Scrollbar(TAB2_BOT)
tree1_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree1 = ttk.Treeview(TAB2_BOT, style="Treeview", show='headings', yscrollcommand=tree1_scroll.set)
tree1.pack(side=tk.RIGHT, fill="both", expand=True)
tree1_scroll.config(command=tree1.yview)
tree1['columns'] = ("video_id", "VideoID", "VideoTitle", "DateUploaded", "Duration", "VideoTags", "VideoCats", "VideoURL")

for col in tree1['columns']:
    tree1.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree1, _col, False))
tree1.column('video_id', width=0, stretch=tk.NO)
tree1.column('VideoID', width=0, stretch=tk.NO)
tree1.column('VideoTitle', anchor=tk.W, width=700)
tree1.column('DateUploaded', anchor=tk.W, width=75)
tree1.column('Duration', anchor=tk.W, width=80)
tree1.column('VideoTags', anchor=tk.W, width=250)
tree1.column('VideoCats', width=0, stretch=tk.NO)
tree1.column('VideoURL', width=0, stretch=tk.NO)
tree1.tag_configure('oddrow', background="white")
tree1.tag_configure('evenrow', background="lightblue")
####################### END OF TAB2_TOP INIT ###########################################


####################### SET UP TAB2 PANES ###########################################
TAB3_PANEH = ttk.PanedWindow(TAB3, orient=tk.HORIZONTAL, width=1880, height=1000)
TAB3_PANEH.pack(fill='both', expand=True)
TAB3_P_LHS = ttk.PanedWindow(TAB3_PANEH, orient=tk.VERTICAL, width=1050, height=500)
TAB3_PANEH.add(TAB3_P_LHS)
#build the LHS P_LTOP and P_LBOT panes
TAB3_P_LTOP = ttk.Label(TAB3_P_LHS, text="Downloading")
TAB3_P_LBOT = ttk.Label(TAB3_P_LHS, text="Autodownloading")
TAB3_P_LHS.add(TAB3_P_LTOP, weight=1)
TAB3_P_LHS.add(TAB3_P_LBOT, weight=8)

TAB3_P_RHS = ttk.PanedWindow(TAB3, orient=tk.VERTICAL, width=650, height=500)
TAB3_PANEH.add(TAB3_P_RHS)
#build the RHS P_RTOP and P_RBOT panes
TAB3_P_RTOP = ttk.Label(TAB3_P_RHS, text="YTDL database Heading")
TAB3_P_RBOT = ttk.Label(TAB3_P_RHS, text="YTDL Treeview")
TAB3_P_RHS.add(TAB3_P_RTOP, weight=16)
TAB3_P_RHS.add(TAB3_P_RBOT, weight=1)

####################### SET UP TAB3_RHS_TOP INIT ###########################################
# Add Some Style
style = ThemedStyle(master)
style.theme_use(AppC.styleTheme)
style.configure("Treeview",rowheight=AppC.ConsLineHt,font=(AppC.ConsFont))
style.configure("Treeview.Heading", font=(AppC.ConsFont)) # Modify the font of the headings
style.map('Treeview', background=[('selected', "#347083")])
tree2_scroll = tk.Scrollbar(TAB3_P_RTOP)
tree2_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree2 = ttk.Treeview(TAB3_P_RTOP, style="Treeview", show='headings', yscrollcommand=tree2_scroll.set)
tree2.pack(side=tk.RIGHT, fill="both", expand=True)
tree2_scroll.config(command=tree2.yview)
tree2['columns'] = ("id", "VideoTitle", "VideoUrl")

for col in tree2['columns']:
    tree2.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree2, _col, False))

tree2.column('id', width=0, stretch=tk.NO)
tree2.column('VideoTitle', anchor=tk.W, width=300)
tree2.column('VideoUrl', width=0, stretch=tk.NO)
tree2.bind("<Double-Button>", chngDFlag)


####################### SET UP TAB4 ###########################################
TAB4_PANEV = ttk.PanedWindow(TAB4, orient=tk.VERTICAL, width=1920, height=1050)
TAB4_PANEV.pack(fill='both', expand=True)
TAB4_TOP = ttk.Label(TAB4_PANEV)
TAB4_PANEV.add(TAB4_TOP, weight=1)
TAB4_BOT = ttk.Label(TAB4_PANEV)
TAB4_PANEV.add(TAB4_BOT, weight=15)

####################### SET UP TAB5 ###########################################

TAB5_PANEV = ttk.PanedWindow(TAB5, orient=tk.VERTICAL, width=1900, height=300)
TAB5_PANEV.pack(fill='both', expand=True)
TAB5_TOP = ttk.Label(TAB5_PANEV)
TAB5_PANEV.add(TAB5_TOP, weight=1)

f = ('Times', 14)
Themes = ['adapta', 'aquativo', 'arc', 'black', 'blue', 'breeze', 'clearlooks', 'elegance', 'equilux', \
'itft1', 'keramik', 'kroc', 'plastik', 'radiance', 'scidblue', 'scidgreen', 'scidgrey', 'scidmint', \
'scidpink', 'scidpurple', 'scidsand', 'smog', 'ubuntu', 'winxpblue', 'yaru']
variable = tk.StringVar()
variable.set(Themes[24])

FontFamily = AppC.FontFamily
FontSize = AppC.FontSize
ProxyOn = 1 if AppC.ProxyOn == True else 0
HaveGotOn = 1 if AppC.HaveGotOn == True else 0
allowImport = 1 if AppC.allowImport == True else 0
exportTags = 1 if AppC.exportTags == True else 0
exportCats = 1 if AppC.exportCats == True else 0
orientation = AppC.orientation
minsecs = AppC.minsecs
VideoTagsDisp = AppC.VideoTagsDisp
VideoCatsDisp = AppC.VideoCatsDisp
MaxDispSort = AppC.MaxDispSort
Archive_Source = AppC.Archive_Source
csvpath = AppC.csvpath
imagePath = AppC.imagePath
mpvConfig = AppC.mpvConfig
screenshotPath = AppC.screenshotPath
YDL_Archive = AppC.YDL_Archive
YDL_exportPath = AppC.YDL_exportPath
YDL_Flags = AppC.YDL_Flags
YDL_format = AppC.YDL_format
YDL_ignoreerrors = 1 if AppC.YDL_ignoreerrors == True else 0
YDL_no_warnings = 1 if AppC.YDL_no_warnings == True else 0
YDL_noplaylist = 1 if AppC.YDL_noplaylist == True else 0
YDL_quiet = 1 if AppC.YDL_quiet == True else 0
YDL_UseNetrc = 1 if AppC.YDL_UseNetrc == True else 0
YDL_Options = AppC.YDL_Options
YDL_OutStru = AppC.YDL_OutStru
TvFont = AppC.TvFontSz
TvLineHt = AppC.TvLineHt
TvDlFont = AppC.TvDlFontSz
TvDlLineHt = AppC.TvDlLineHt
ConsFont = AppC.ConsFontSz
ConsLineHt = AppC.ConsLineHt
CbFont = AppC.CbFontSz
LblFont = AppC.LblFontSz
LblLineHt = AppC.LblLineHt
ProgFont = AppC.ProgFontSz
ProgLineHt = AppC.ProgLineHt
BtnFont = AppC.BtnFontSz
BtnLineHt = AppC.BtnLineHt
EntFont = AppC.EntFontSz
EntLineHt = AppC.EntLineHt
MboxFont = AppC.MboxFontSz
TkrFont = AppC.TkrFontSz
TkrLineHt = AppC.TkrLineHt
styleTheme = AppC.styleTheme

S_FontFamily = tk.StringVar()
S_FontFamily.set(FontFamily)
S_FontSize = tk.IntVar()
S_FontSize.set(FontSize)
S_ProxyOn = tk.IntVar()
S_ProxyOn.set(ProxyOn)
S_HaveGotOn = tk.IntVar()
S_HaveGotOn.set(HaveGotOn)
S_allowImport = tk.IntVar()
S_allowImport.set(allowImport)
S_exportTags = tk.IntVar()
S_exportTags.set(exportTags)
S_exportCats = tk.IntVar()
S_exportCats.set(exportCats)
S_orientation = tk.StringVar()
S_orientation.set(orientation)
S_minsecs = tk.IntVar()
S_minsecs.set(minsecs)
S_VideoTagsDisp = tk.IntVar()
S_VideoTagsDisp.set(VideoTagsDisp)
S_VideoCatsDisp = tk.IntVar()
S_VideoCatsDisp.set(VideoCatsDisp)
S_MaxDispSort = tk.IntVar()
S_MaxDispSort.set(MaxDispSort)
S_Archive_Source = tk.StringVar()
S_Archive_Source.set(Archive_Source)
S_csvpath = tk.StringVar()
S_csvpath.set(csvpath)
S_imagePath = tk.StringVar()
S_imagePath.set(imagePath)
S_mpvConfig = tk.StringVar()
S_mpvConfig.set(mpvConfig)
S_screenshotPath = tk.StringVar()
S_screenshotPath.set(screenshotPath)
S_YDL_Archive = tk.StringVar()
S_YDL_Archive.set(YDL_Archive)
S_YDL_exportPath = tk.StringVar()
S_YDL_exportPath.set(YDL_exportPath)
S_YDL_Flags = tk.StringVar()
S_YDL_Flags.set(YDL_Flags)
S_YDL_format = tk.StringVar()
S_YDL_format.set(YDL_format)
S_YDL_ignoreerrors = tk.IntVar()
S_YDL_ignoreerrors.set(YDL_ignoreerrors)
S_YDL_no_warnings = tk.IntVar()
S_YDL_no_warnings.set(YDL_no_warnings)
S_YDL_noplaylist = tk.IntVar()
S_YDL_noplaylist.set(YDL_noplaylist)
S_YDL_quiet = tk.IntVar()
S_YDL_quiet.set(YDL_quiet)
S_YDL_UseNetrc = tk.IntVar()
S_YDL_UseNetrc.set(YDL_UseNetrc)
S_YDL_Options = tk.StringVar()
S_YDL_Options.set(YDL_Options)
S_YDL_OutStru = tk.StringVar()
S_YDL_OutStru.set(YDL_OutStru)
S_styleTheme = tk.StringVar()
S_styleTheme.set(styleTheme)
S_TvFont = tk.IntVar()
S_TvFont.set(TvFont)
S_TvLineHt = tk.IntVar()
S_TvLineHt.set(TvLineHt)
S_TvDlFont = tk.IntVar()
S_TvDlFont.set(TvDlFont)
S_TvDlLineHt = tk.IntVar()
S_TvDlLineHt.set(TvDlLineHt)
S_ConsFont = tk.IntVar()
S_ConsFont.set(ConsFont)
S_ConsLineHt = tk.IntVar()
S_ConsLineHt.set(ConsLineHt)
S_CbFont = tk.IntVar()
S_CbFont.set(CbFont)
S_LblFont = tk.IntVar()
S_LblFont.set(LblFont)
S_LblLineHt = tk.IntVar()
S_LblLineHt.set(LblLineHt)
S_ProgFont = tk.IntVar()
S_ProgFont.set(ProgFont)
S_ProgLineHt = tk.IntVar()
S_ProgLineHt.set(ProgLineHt)
S_BtnFont = tk.IntVar()
S_BtnFont.set(BtnFont)
S_BtnLineHt = tk.IntVar()
S_BtnLineHt.set(BtnLineHt)
S_EntFont = tk.IntVar()
S_EntFont.set(EntFont)
S_EntLineHt = tk.IntVar()
S_EntLineHt.set(EntLineHt)
S_MboxFont = tk.IntVar()
S_MboxFont.set(MboxFont)
S_TkrFont = tk.IntVar()
S_TkrFont.set(TkrFont)
S_TkrLineHt = tk.IntVar()
S_TkrLineHt.set(TkrLineHt)


left_frame = tk.Frame(TAB5_TOP, bd=2, bg='#CCCCCC', relief=SOLID, padx=10, pady=10)
tk.Label(left_frame, text="FontFamily", bg='#CCCCCC', font=f ).grid(row=0, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="FontSize", bg='#CCCCCC', font=f ).grid(row=1, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="ProxyOn", bg='#CCCCCC', font=f ).grid(row=2, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="HaveGotOn", bg='#CCCCCC', font=f ).grid(row=3, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="allowImport", bg='#CCCCCC', font=f ).grid(row=4, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="exportTags", bg='#CCCCCC', font=f ).grid(row=5, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="exportCats", bg='#CCCCCC', font=f ).grid(row=6, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="orientation", bg='#CCCCCC', font=f ).grid(row=7, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="minsecs", bg='#CCCCCC', font=f ).grid(row=8, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="VideoTagsDisp", bg='#CCCCCC', font=f ).grid(row=9, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="VideoCatsDisp", bg='#CCCCCC', font=f ).grid(row=10, column=0, sticky=W, pady=10)
tk.Label(left_frame, text="MaxDispSort", bg='#CCCCCC', font=f ).grid(row=11, column=0, sticky=W, pady=10)
tk.Button(left_frame, text="Archive_Source", bg='#CCCCCC', font=f ).grid(row=12, column=0, columnspan=30, sticky=W, pady=10)
tk.Button(left_frame, text="csvpath", bg='#CCCCCC', font=f, command=get_csvpath).grid(row=13, column=0, sticky=W, pady=10)
tk.Button(left_frame, text="imagePath", bg='#CCCCCC', font=f, command=get_imagePath ).grid(row=14, column=0, columnspan=30, sticky=W, pady=10)
tk.Button(left_frame, text="mpvConfig", bg='#CCCCCC', font=f).grid(row=15, column=0, columnspan=30, sticky=W, pady=10)
tk.Button(left_frame, text="screenshotPath", bg='#CCCCCC', font=f, command=get_screenshotPath ).grid(row=16, column=0, columnspan=30, sticky=W, pady=10)

middle_frame = tk.Frame(TAB5_TOP, bd=2, bg='#CCCCCC', relief=SOLID, padx=10, pady=10)
tk.Button(middle_frame, text="YDL_Archive", bg='#CCCCCC', font=f, command=get_YDL_Archive ).grid(row=0, column=0, columnspan=30, sticky=W, pady=10)
tk.Button(middle_frame, text="YDL_exportPath", bg='#CCCCCC', font=f, command=get_YDL_exportPath ).grid(row=1, column=0, columnspan=30, sticky=W, pady=10)
tk.Button(middle_frame, text="YDL_Flags", bg='#CCCCCC', font=f ).grid(row=2, column=0, sticky=W, pady=10)
tk.Button(middle_frame, text="YDL_format", bg='#CCCCCC', font=f ).grid(row=3, column=0, columnspan=30, sticky=W, pady=10)
tk.Label(middle_frame, text="YDL_ignoreerrors", bg='#CCCCCC', font=f ).grid(row=4, column=0, sticky=W, pady=10)
tk.Label(middle_frame, text="YDL_no_warnings", bg='#CCCCCC', font=f ).grid(row=5, column=0, sticky=W, pady=10)
tk.Label(middle_frame, text="YDL_noplaylist", bg='#CCCCCC', font=f ).grid(row=6, column=0, sticky=W, pady=10)
tk.Label(middle_frame, text="YDL_quiet", bg='#CCCCCC', font=f ).grid(row=7, column=0, sticky=W, pady=10)
tk.Label(middle_frame, text="YDL_UseNetrc", bg='#CCCCCC', font=f ).grid(row=8, column=0, sticky=W, pady=10)
tk.Button(middle_frame, text="YDL_Options", bg='#CCCCCC', font=f ).grid(row=9, column=0, sticky=W, pady=10)
tk.Button(middle_frame, text="YDL_OutStru", bg='#CCCCCC', font=f ).grid(row=10, column=0, columnspan=30, sticky=W, pady=10)
tk.Label(middle_frame, text="styleTheme", bg='#CCCCCC', font=f ).grid(row=11, column=0, sticky=W, pady=10)

right_frame = tk.Frame(TAB5_TOP, bd=2, bg='#CCCCCC', relief=SOLID, padx=10, pady=10)
tk.Label(right_frame, text="TvFont", bg='#CCCCCC', font=f ).grid(row=0, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="TvLineHt", bg='#CCCCCC', font=f ).grid(row=1, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="TvDlFont", bg='#CCCCCC', font=f ).grid(row=2, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="TvDlLineHt", bg='#CCCCCC', font=f ).grid(row=3, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="ConsFont", bg='#CCCCCC', font=f ).grid(row=4, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="ConsLineHt", bg='#CCCCCC', font=f ).grid(row=5, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="CbFont", bg='#CCCCCC', font=f ).grid(row=6, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="LblFont", bg='#CCCCCC', font=f ).grid(row=7, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="LblLineHt", bg='#CCCCCC', font=f ).grid(row=8, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="ProgFont", bg='#CCCCCC', font=f ).grid(row=9, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="ProgLineHt", bg='#CCCCCC', font=f ).grid(row=10, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="BtnFont", bg='#CCCCCC', font=f ).grid(row=11, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="BtnLineHt", bg='#CCCCCC', font=f ).grid(row=12, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="EntFont", bg='#CCCCCC', font=f ).grid(row=13, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="EntLineHt", bg='#CCCCCC', font=f ).grid(row=14, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="MboxFont", bg='#CCCCCC', font=f ).grid(row=15, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="TkrFont", bg='#CCCCCC', font=f ).grid(row=16, column=0, sticky=W, pady=10)
tk.Label(right_frame, text="TkrLineHt", bg='#CCCCCC', font=f ).grid(row=17, column=0, sticky=W, pady=10)


save_frame = tk.Frame(TAB5_TOP, bd=2, bg='#CCCCCC', relief=SOLID, padx=10, pady=10)
save_btn = tk.Button(save_frame, width=15,text='Save Data',font=f,relief=SOLID,command=setsave)

E_FontFamily = tk.Entry(left_frame, textvariable=S_FontFamily,font=f)
E_FontSize = tk.Entry(left_frame, textvariable=S_FontSize,font=f)
C_ProxyOn = tk.Checkbutton(left_frame, variable=S_ProxyOn, onvalue=1, offvalue=0,font=f)
C_HaveGotOn = tk.Checkbutton(left_frame, variable=S_HaveGotOn, onvalue=1, offvalue=0,font=f)
C_allowImport = tk.Checkbutton(left_frame, variable=S_allowImport, onvalue=1, offvalue=0,font=f)
C_exportTags = tk.Checkbutton(left_frame, variable=S_exportTags, onvalue=1, offvalue=0,font=f)
C_exportCats = tk.Checkbutton(left_frame, variable=S_exportCats, onvalue=1, offvalue=0,font=f)
E_orientation = tk.Entry(left_frame, textvariable=S_orientation,font=f)
E_minsecs = tk.Entry(left_frame, textvariable=S_minsecs,font=f)
E_VideoTagsDisp = tk.Entry(left_frame, textvariable=S_VideoTagsDisp,font=f)
E_VideoCatsDisp = tk.Entry(left_frame, textvariable=S_VideoCatsDisp,font=f)
E_MaxDispSort = tk.Entry(left_frame, textvariable=S_MaxDispSort,font=f)
E_Archive_Source = tk.Entry(left_frame, textvariable=S_Archive_Source,width=50, font=f)
E_csvpath = tk.Entry(left_frame, textvariable=S_csvpath,width=50,font=f)
E_imagePath = tk.Entry(left_frame, textvariable=S_imagePath,width=50,font=f)
E_mpvConfig = tk.Entry(left_frame, textvariable=S_mpvConfig,width=50,font=f)
E_screenshotPath = tk.Entry(left_frame, textvariable=S_screenshotPath,width=50,font=f)

E_YDL_Archive = tk.Entry(middle_frame, textvariable=S_YDL_Archive,width=50,font=f)
E_YDL_exportPath = tk.Entry(middle_frame, textvariable=S_YDL_exportPath,width=50,font=f)
E_YDL_Flags = tk.Entry(middle_frame, textvariable=S_YDL_Flags,width=50,font=f)
E_YDL_format = tk.Entry(middle_frame, textvariable=S_YDL_format,width=50,font=f)
C_YDL_ignoreerrors = tk.Checkbutton(middle_frame, variable=S_YDL_ignoreerrors, onvalue=1, offvalue=0,font=f)
C_YDL_no_warnings = tk.Checkbutton(middle_frame, variable=S_YDL_no_warnings, onvalue=1, offvalue=0,font=f)
C_YDL_noplaylist = tk.Checkbutton(middle_frame, variable=S_YDL_noplaylist, onvalue=1, offvalue=0,font=f)
C_YDL_quiet = tk.Checkbutton(middle_frame, variable=S_YDL_quiet, onvalue=1, offvalue=0,font=f)
C_YDL_UseNetrc = tk.Checkbutton(middle_frame, variable=S_YDL_UseNetrc, onvalue=1, offvalue=0,font=f)
E_YDL_Options = tk.Entry(middle_frame, textvariable=S_YDL_Options,width=50,font=f)
E_YDL_OutStru = tk.Entry(middle_frame, textvariable=S_YDL_OutStru,width=50,font=f)
O_styleTheme = tk.OptionMenu(middle_frame,variable,*Themes)
O_styleTheme.config(width=15,font=('Times', 14))

E_TvFont = tk.Entry(right_frame, textvariable=S_TvFont,font=f)
E_TvLineHt = tk.Entry(right_frame, textvariable=S_TvLineHt,font=f)
E_TvDlFont = tk.Entry(right_frame, textvariable=S_TvDlFont,font=f)
E_TvDlLineHt = tk.Entry(right_frame, textvariable=S_TvDlLineHt,font=f)
E_ConsFont = tk.Entry(right_frame, textvariable=S_ConsFont,font=f)
E_ConsLineHt = tk.Entry(right_frame, textvariable=S_ConsLineHt,font=f)
E_CbFont = tk.Entry(right_frame, textvariable=S_CbFont,font=f)
E_LblFont = tk.Entry(right_frame, textvariable=S_LblFont,font=f)
E_LblLineHt = tk.Entry(right_frame, textvariable=S_LblLineHt,font=f)
E_ProgFont = tk.Entry(right_frame, textvariable=S_ProgFont,font=f)
E_ProgLineHt = tk.Entry(right_frame, textvariable=S_ProgLineHt,font=f)
E_BtnFont = tk.Entry(right_frame, textvariable=S_BtnFont,font=f)
E_BtnLineHt = tk.Entry(right_frame, textvariable=S_BtnLineHt,font=f)
E_EntFont = tk.Entry(right_frame, textvariable=S_EntFont,font=f)
E_EntLineHt = tk.Entry(right_frame, textvariable=S_EntLineHt,font=f)
E_MboxFont = tk.Entry(right_frame, textvariable=S_MboxFont,font=f)
E_TkrFont = tk.Entry(right_frame, textvariable=S_TkrFont,font=f)
E_TkrLineHt = tk.Entry(right_frame, textvariable=S_TkrLineHt,font=f)


E_FontFamily.grid(row=0, column=1, pady=10, padx=20)
E_FontSize.grid(row=1, column=1, pady=10, padx=20)
C_ProxyOn.grid(row=2, column=1, pady=10, padx=20)
C_HaveGotOn.grid(row=3, column=1, pady=10, padx=20)
C_allowImport.grid(row=4, column=1, pady=10, padx=20)
C_exportTags.grid(row=5, column=1, pady=10, padx=20)
C_exportCats.grid(row=6, column=1, pady=10, padx=20)
E_orientation.grid(row=7, column=1, pady=10, padx=20)
E_minsecs.grid(row=8, column=1, pady=10, padx=20)
E_VideoTagsDisp.grid(row=9, column=1, pady=10, padx=20)
E_VideoCatsDisp.grid(row=10, column=1, pady=10, padx=20)
E_MaxDispSort.grid(row=11, column=1, pady=10, padx=20)
E_Archive_Source.grid(row=12, column=1, columnspan=30, pady=10, padx=20)
E_csvpath.grid(row=13, column=1, pady=10, columnspan=30, padx=20)
E_imagePath.grid(row=14, column=1, pady=10, columnspan=30, padx=20)
E_mpvConfig.grid(row=15, column=1, pady=10, columnspan=30, padx=20)
E_screenshotPath.grid(row=16, column=1, pady=10, columnspan=30, padx=20)
left_frame.place(x=50, y=0)

E_YDL_Archive.grid(row=0, column=1, pady=10, columnspan=30, padx=20)
E_YDL_exportPath.grid(row=1, column=1, pady=10, columnspan=30, padx=20)
E_YDL_Flags.grid(row=2, column=1, pady=10, padx=20)
E_YDL_format.grid(row=3, column=1, pady=10, padx=20)
C_YDL_ignoreerrors.grid(row=4, column=1, pady=10, padx=20)
C_YDL_no_warnings.grid(row=5, column=1, pady=10, padx=20)
C_YDL_noplaylist.grid(row=6, column=1, pady=10, padx=20)
C_YDL_quiet.grid(row=7, column=1, pady=10, padx=20)
C_YDL_UseNetrc.grid(row=8, column=1, pady=10, padx=20)
E_YDL_Options.grid(row=9, column=1, pady=10, padx=20)
E_YDL_OutStru.grid(row=10, column=1, pady=10, padx=20)
O_styleTheme.grid(row=11, column=1, pady=10, padx=20)
middle_frame.place(x=750, y=0)

E_TvFont.grid(row=0, column=1, pady=10, padx=20)
E_TvLineHt.grid(row=1, column=1, pady=10, padx=20)
E_TvDlFont.grid(row=2, column=1, pady=10, padx=20)
E_TvDlLineHt.grid(row=3, column=1, pady=10, padx=20)
E_ConsFont.grid(row=4, column=1, pady=10, padx=20)
E_ConsLineHt.grid(row=5, column=1, pady=10, padx=20)
E_CbFont.grid(row=6, column=1, pady=10, padx=20)
E_LblFont.grid(row=7, column=1, pady=10, padx=20)
E_LblLineHt.grid(row=8, column=1, pady=10, padx=20)
E_ProgFont.grid(row=9, column=1, pady=10, padx=20)
E_ProgLineHt.grid(row=10, column=1, pady=10, padx=20)
E_BtnFont.grid(row=11, column=1, pady=10, padx=20)
E_BtnLineHt.grid(row=12, column=1, pady=10, padx=20)
E_EntFont.grid(row=13, column=1, pady=10, padx=20)
E_EntLineHt.grid(row=14, column=1, pady=10, padx=20)
E_MboxFont.grid(row=15, column=1, pady=10, padx=20)
E_TkrFont.grid(row=16, column=1, pady=10, padx=20)
E_TkrLineHt.grid(row=17, column=1, pady=10, padx=20)
right_frame.place(x=1500, y=0)

save_btn.grid(row=0, column=1, pady=10, padx=20)
save_frame.place(x=850, y=800)

############################## INITIALISING PROXY #############################

############################## INITIALISING PROXY #############################
ProxyOn = AppC.ProxyOn
if ProxyOn == True:
    # Create an instance of the proxy  manager
    print("getting proxies")
    proxie = get_proxies()
    proxy = proxie[8]
    print(proxy)
    session = requests.Session()
    session.proxies = {"http": proxy, "https": proxy}



######################## START MAIN LOOP ######################################
# INITIALISES THE HUB DATABASE CLASS
if __name__ == '__main__':
    if AppC.HaveGotOn == True:
        havegot = HaveGot("Pornhub.db")
        loadhavegot()
        prochavegot()

    global Tab4app
    thumb   = Thumb("Pornhub.db")
    yvideos = Yvideos("Pornhub.db")
    ytdl = YTdl("Pornhub.db")
    if AppC.allowImport:
        noword = NoWord("Pornhub.db")
        pornstar = PornStar("Pornhub.db")
#        Nowords = NoWordsTable(master)
#        Nowords.dispTree5()
    master.tk.call('wm', 'iconphoto', master._w, tk.PhotoImage(file=AppC.imagePath+'/Hubwards-logo.svg.png'))
    master.title("Hubwards "+AppC.orientation+" Video Downloads")
    dispTree1()
    Downloader = DownloaderUI(master)
    cwd = os.getcwd()
    makeBrowseVideos()
    tk.mainloop()

