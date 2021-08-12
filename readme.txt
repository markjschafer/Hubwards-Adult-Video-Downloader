
First off, I am NOT a python developer, I'm 58 year old and due to covid, I'm no longer working. I was a programmer/developer in another life, but that was using CA-Clipper in the MS-DOS environment. I started playing with python just over 6 months ago. My genetic preferences are towards men, not women, so the below code is a reflection of that. It will be easy to adjust the code to your genetic preference.

The pornhub import csv file is HUGE. Currently there are over 500 000 references to just the gay videos, which is a fraction of the hetrosexual references and that takes a while to load. I'm using sqlite3 database structure. The database will be created when you run the application.

PornhubConst.py - This is where the system holds all of its settings and constants. You  will need to put /your/path/names/ in for your customisations The reference to where the pornhub csv file may be downloaded is in this file

PornhubMst is the main file. I've set it up as a notebook with 5 pages. Page 1 is my import from CSV. It's a mostly blanket import with few validations. I found it was quicker to install most of what I wanted, then strip out the stuff I didn't want.

Prior to importing, you need to setup a No-word table. These are words that must not be included in your import. my genetic preference is gay, so mine will typically only include links with gay and exclude any reference to hetrosexual videos and pornstars. You need to adjust yours acordingly.

I found it easier and a LOT quicker to mildly modify the CSV file then get pandas to place it into a sqlite3 database, then delete the records I don't want.

Tab2. This is where you make your video selection from atreeview. There are 2 combo-boxes and a test search to thin your selection. To do a search, enter a key word with a --key-word to exclude that key word from the search and a ++key word to add a second key word to the search. This is how to thin your search down. You can click on any of the treeview's column headings to sort via the columns

You can select one video or several by clicling with your mouse and shift, to select a block or actl to select scattered. Once you have narrowed your selection, use the "Copy Selected" to the downloader on Tab3.

Tab3. This is where the videos will be downloaded. The ones that you selected on Tab 2 will show here. They are in a table, waiting for you to download them.

I use Youtube_dl as my downloader. It's a clever piece of software that enables you do download videos and clips, using threading. Youtube_dl utalises a "Downloaded.txt" file to keep a record of all the films and clips you have previously downloaded.

Because I use a "blanket upload", a some of these videos will be private and youtube_dl will not download them. if the video does not download, just highlight the video and click the remove button. You can remove all the videos from the scheduled table by clicking the "Clear Videos" button.

Select the "Add" button to add the next video into the download sequence. You can add as many downloads as your bandwidth can handle. Once the download has completed, the systen will remove it of the pending list and stor it in the output folder (pornhubConst). If your selection doesnt download, This could be because it was previously downloaded or it's private, just highlight the video on the treeview and select remove button.

On the RHS of the screen, there is a console mimic, that displays STDOUT console messages. To see your STDERR messages you will need to look at the console screen you used to start the application.

At all times, you can move between tabs without halting or interrupting functionality.

Tab 4 is a list of your output folder. Highlight the video you want to watch and use the Enter key to activate the MPV video plsyer. You can select many, using the shift or ctrl keys with the mouse pointer or click on the subfolder to play all in that subfolder.

I wrote this software as an educational project to learn python and GUI programming. It is not intended as a commercial application.

There will be sections of code that are likely to make your toes curl and suggestions to correct those areas will bw welcomed. Be warned, I am not tollerant of millenials who have neen spoonfed their entire lives. I am not a developer. Most of the code has been adapted and customised from various sources on the web. If you see any code that is yours, Thankyou for letting me modify it.

if you have a standard free pornhub account, do the following (linux)

change YDL_UseNetrc to True in PornhubConst, then enter the following into your command prompt

touch $HOME/.netrc
chmod a-rwx,u+rw $HOME/.netrc
```
After that you can add credentials for an extractor in the following format, where *extractor* is the name of the extractor in lowercase:
```
machine pornhub login <yourlogin> password <yourpassword>
