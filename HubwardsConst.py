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
# -o '%(uploader)s.%(id)s.%(title)s.%(ext)s'
# https://www.pornhub.com/files/pornhub.com-db.zip
#https://www.pornhub.com/webmasters
import os
from easysettings import EasySettings

settings = EasySettings("PornConfigFile.conf")

def setsettings():
    settings.set("FontFamily", 'arial')
    settings.set("FontSize", 16)
    settings.set("ProxyOn", True)
    settings.set("HaveGotOn", False)
    settings.set("allowImport", True)
    settings.set("exportTags", False)
    settings.set("exportCats", False)
    settings.set("orientation", 'Gay')
    settings.set("minsecs", 300)
    settings.set("VideoTagsDisp", 300)
    settings.set("VideoCatsDisp", 600)
    settings.set("MaxDispSort", 9000)
    settings.set("Archive_Source", 'https://www.pornhub.com/files/pornhub.com-db.zip')
    settings.set("csvpath", '/path/to/your/CSV/')
    settings.set("imagePath", './images/')
    settings.set("mpvConfig", '--config-dir=/home/yourname/.config/mpv/')
    settings.set("screenshotPath", "/path/to/your/Snapshots/")
    settings.set("YDL_Archive", "/path/to/your/downloaded.txt")
    settings.set("YDL_exportPath", '/path/to/your/Video/')
    settings.set("YDL_Flags", "-ciw")
    settings.set("YDL_format", 'bestvideo[height<=?720]+bestaudio/best[height<=?720]')
    settings.set("YDL_ignoreerrors", True)
    settings.set("YDL_no_warnings", True)
    settings.set("YDL_noplaylist",  True)
    settings.set("YDL_quiet", False)
    settings.set("YDL_UseNetrc", True)
    settings.set("YDL_Options", "./images/")
    settings.set("YDL_OutStru", '%(id)s.%(title)s.%(ext)s')
    settings.set("TvFont", 22)
    settings.set("TvLineHt", 44)
    settings.set("TvDlFont", 14)
    settings.set("TvDlLineHt", 20)
    settings.set("ConsFont", 16)
    settings.set("ConsLineHt", 26)
    settings.set("CbFont",  20)
    settings.set("LblFont",  20)
    settings.set("LblLineHt", 28)
    settings.set("ProgFont",  18)
    settings.set("ProgLineHt", 28)
    settings.set("BtnFont",  24)
    settings.set("BtnLineHt", 32)
    settings.set("EntFont",  20)
    settings.set("EntLineHt", 28)
    settings.set("MboxFont",  20)
    settings.set("TkrFont",  24)
    settings.set("TkrLineHt", 44)
    settings.set("styleTheme", 'blue')
    settings.save()


setsettings()

FontFamily = settings.get("FontFamily")
FontSize = settings.get("FontSize")
ProxyOn = settings.get("ProxyOn")
HaveGotOn = settings.get("HaveGotOn")
allowImport = settings.get("allowImport")
exportTags = settings.get("exportTags")
exportCats = settings.get("exportCats")
orientation = settings.get("orientation")
minsecs = settings.get("minsecs")
VideoTagsDisp = settings.get("VideoTagsDisp")
VideoCatsDisp = settings.get("VideoCatsDisp")
MaxDispSort = settings.get("MaxDispSort")
Archive_Source = settings.get("Archive_Source")
csvpath = settings.get("csvpath")
imagePath = settings.get("imagePath")
mpvConfig = settings.get("mpvConfig")
screenshotPath = settings.get("screenshotPath")
YDL_Archive = settings.get("YDL_Archive")
YDL_exportPath = settings.get("YDL_exportPath")
YDL_Flags = settings.get("YDL_Flags")
YDL_format = settings.get("YDL_format")
YDL_ignoreerrors = settings.get("YDL_ignoreerrors")
YDL_no_warnings = settings.get("YDL_no_warnings")
YDL_noplaylist = settings.get("YDL_noplaylist")
YDL_quiet = settings.get("YDL_quiet")
YDL_UseNetrc = settings.get("YDL_UseNetrc")
YDL_Options = settings.get("YDL_Options")
YDL_OutStru = settings.get("YDL_OutStru")

TvFont = ('arial', settings.get("TvFont"),'bold')
TvDlFont = ('arial', settings.get("TvDlFont"),'bold')
ConsFont = ('arial', settings.get("ConsFont"),'bold')
CbFont = ('arial', settings.get("CbFont"),'bold')
LblFont = ('arial', settings.get("LblFont"),'bold')
ProgFont = ('arial', settings.get("ProgFont"),'bold')
BtnFont = ('arial', settings.get("BtnFont"),'bold')
EntFont = ('arial', settings.get("EntFont"),'bold')
MboxFont = ('arial', settings.get("MboxFont"),'bold')
TkrFont = ('arial', settings.get("TkrFont"),'bold')

TvFontSz = settings.get("TvFont")
TvDlFontSz = settings.get("TvDlFont")
ConsFontSz = settings.get("ConsFont")
CbFontSz = settings.get("CbFont")
LblFontSz = settings.get("LblFont")
ProgFontSz = settings.get("ProgFont")
BtnFontSz = settings.get("BtnFont")
EntFontSz = settings.get("EntFont")
MboxFontSz = settings.get("MboxFont")
TkrFontSz = settings.get("TkrFont")


TvLineHt = settings.get("TvLineHt")
TvDlLineHt = settings.get("TvDlLineHt")
ConsLineHt = settings.get("ConsLineHt")
LblLineHt = settings.get("LblLineHt")
ProgLineHt = settings.get("ProgLineHt")
BtnLineHt = settings.get("BtnLineHt")
EntLineHt = settings.get("EntLineHt")
TkrLineHt = settings.get("TkrLineHt")
styleTheme = settings.get("styleTheme")





