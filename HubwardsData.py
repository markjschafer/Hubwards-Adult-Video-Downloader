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
import sqlite3
from sqlite3 import Error
import sys



class Yvideos:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS yvideos (video_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, VideoID TEXT, VideoTitle TEXT, DateUploaded TEXT, Duration TEXT, VideoTags TEXT, VideoCats TEXT, VideoURL TEXT)")
        self.conn.commit()
#                       1         2           3            4         5          6         7          8        9
    def insert(self, VideoID, VideoTitle, DateUploaded, Duration, VideoTags, VideoCats, VideoURL):
        self.cur.execute("INSERT INTO yvideos VALUES (NULL,?,?,?,?,?,?,?)", (VideoID, VideoTitle, DateUploaded, Duration, VideoTags, VideoCats, VideoURL))
        self.conn.commit()

    def isthere(self, VidID):
        self.cur.execute("SELECT * FROM yvideos WHERE VideoID=?", (VidID,) )
        rows = self.cur.fetchall()
#        return rows
        if len(rows) > 0:
            return True
        else:
            return False

    def view(self):
        self.cur.execute("SELECT * FROM yvideos ORDER BY DateUploaded DESC" )
        rows = self.cur.fetchall()
        return rows

    def generic(self, sqlstring):
        self.cur.execute(sqlstring)
        rows = self.cur.fetchall()
        return rows

    def genericupd(self, sqlstring):
        self.cur.execute(sqlstring)
        self.conn.commit()

    def viewfor(self, sqlexpr):
        self.cur.execute("SELECT * FROM yvideos "+sqlexpr )
        rows = self.cur.fetchall()
        return rows

    def search(self, search):
        minOn = False
        pluOn = False

        if "--" in search and "++" in search:
            minOn = True
            pluOn = True
            minSt = search.find("--")
            pluSt = search.find("++")
            if minSt < pluSt:   # search --search ++search
                notword = search[minSt+2:pluSt-1]
                andword = search[pluSt+2:]
                search = search[0:minSt-1]
                search = '%' + search + '%'
                andword =  '%' + andword + '%'
                notword =  '%' + notword + '%'

            else:   # search ++search --search
                andword = search[pluSt+2:minSt-1]
                notword = search[minSt+2:]
                search = search[0:pluSt-1]
                search = '%' + search + '%'
                andword =  '%' + andword + '%'
                notword =  '%' + notword + '%'

        if "--" in search and "++" not in search: # search --search
            minOn = True
            minSt = search.find("--")
            notword = search[minSt+2:]
            search = search[0:minSt-1]
            search = '%' + search + '%'
            notword =  '%' + notword + '%'

        if "++" in search and "--" not in search : # search ++search
            pluOn = True
            pluSt = search.find("++")
            andword = search[pluSt+2:]
            search = search[0:pluSt-1]
            search = '%' + search + '%'
            andword =  '%' + andword + '%'

        if "--" not in search and "++" not in search:
            search = '%' + search + '%'


        if pluOn == True and minOn == True:
            self.cur.execute("SELECT * FROM yvideos WHERE VideoTitle LIKE ? AND VideoTitle LIKE ? AND VideoTitle NOT LIKE ? ORDER BY DateUploaded DESC", (search, andword, notword ) )
        elif pluOn == True and minOn == False:
            self.cur.execute("SELECT * FROM yvideos WHERE VideoTitle LIKE ? AND VideoTitle LIKE ? ORDER BY DateUploaded DESC", (search, andword ) )
        elif pluOn == False and minOn == True:
            self.cur.execute("SELECT * FROM yvideos WHERE VideoTitle LIKE ? AND VideoTitle NOT LIKE ? ORDER BY DateUploaded DESC", (search, notword ) )
        elif pluOn == False and minOn == False:
            self.cur.execute("SELECT * FROM yvideos WHERE VideoTitle LIKE ? OR VideoTags LIKE ? OR VideoCats LIKE ? ORDER BY DateUploaded DESC", (search, search, search ) )
        rows = self.cur.fetchall()
        return rows

    def update(self, VideoID, VideoTitle, DateUploaded, Duration, VideoTags, VideoCats, VideoURL, PornStar):
        #                                         0          1          2          3          4           5            6                 7
        self.cur.execute("UPDATE yvideos SET  VideoID=?, VideoTitle=?, DateUploaded=?, Duration=?, VideoTags=?, VideoCats=?, PornStar=? WHERE video_id=?", (VideoID, VideoTitle, DateUploaded, Duration, VideoTags, VideoCats, VideoURL, PornStar))
        self.conn.commit()
        if self.cur.rowcount < 1:
            return False
        else:
            return True

    def updatetag(self, Tag, VideoID):
        self.cur.execute("UPDATE yvideos SET VideoTags=? WHERE VideoID=?", (VideoTags, VideoID,))
        self.conn.commit()

    def viewtag(self, VideoID):
        self.cur.execute("SELECT VideoTags FROM yvideos WHERE VideoID=?", (VideoID,) )
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM yvideos WHERE Video_id=?", (id,))
        self.conn.commit()

    def deleteall(self):
        self.cur.execute("DELETE FROM yvideos WHERE Video_id > -1")
        self.conn.commit()

    def deleteVideoID(self, VideoID):
        self.cur.execute("DELETE FROM yvideos WHERE VideoID=?", (VideoID,))
        self.conn.commit()

    def showStuffIDontLike(self):
        self.cur.execute("SELECT * FROM yvideos WHERE lower(VideoTags) LIKE '%ebony%' OR lower(VideoTags) LIKE '%black%' OR lower(VideoTags) LIKE '%shemale%' OR lower(VideoTags) LIKE '%boob%' OR lower(VideoTags) LIKE '%tits%' OR lower(VideoTags) LIKE '%-pelo%' OR lower(VideoTags) LIKE '%feet%' OR lower(VideoTags) LIKE '%emo%' OR lower(VideoTags) LIKE '%sissy%' OR lower(VideoTags) LIKE '%verification-video%' OR lower(VideoTags) LIKE '%pau%'")
        rows = self.cur.fetchall()
        return rows


    def __del__(self):
        self.conn.close()

################################################
class YTdl:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS ytdl (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, VideoTitle TEXT, VideoURL, started INTEGER)")
        self.conn.commit()

    def insert(self, VideoTitle, VideoURL, started):
        self.cur.execute("INSERT INTO ytdl VALUES (NULL,?,?,?)", (VideoTitle, VideoURL, started))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM ytdl" )
        rows = self.cur.fetchall()
        return rows

    def viewOne(self):
        ans = self.cur.execute("SELECT COUNT(*) FROM ytdl WHERE started == 0")
        if ans == 0:
            return []
        else:
            self.cur.execute("SELECT * FROM ytdl WHERE started == 0 LIMIT 1" )
            rows = self.cur.fetchone()
            return rows

    def updateOne(self, started, id):
        self.cur.execute("UPDATE ytdl SET started=1 WHERE id=?", (id,))
        self.conn.commit()

    def update(self, VideoTitle, VideoURL, started):
        self.execute("UPDATE ytdl SET VideoTitle=?, VideoURL=?, started=?, WHERE id=?", (self, VideoTitle, VideoURL, started))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM ytdl WHERE id=?", (id,))
        self.conn.commit()

    def deletetitle(self, Title):
        url = ""
        Title = '%' + Title + '%'
        self.cur.execute("SELECT * FROM ytdl WHERE VideoTitle LIKE ?", (Title,))
        rows = self.cur.fetchall()
        if len(rows) > 0:
            row = rows[0]
            self.cur.execute("DELETE FROM ytdl WHERE id=?", (row[0],))
            self.conn.commit()
            url = row[2]
        return url

    def deleteall(self):
        self.cur.execute("DELETE FROM ytdl WHERE id > -1")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

#############################################################################
class NoWord:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS noword (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, noword TEXT)")
        self.conn.commit()

    def insert(self, id, noword):
        self.cur.execute("INSERT INTO noword VALUES (NULL, ?)", (id, noword))
        self.conn.commit()

    def insertlist(self, list):
        insertquery = "INSERT INTO noword (id, noword) VALUES (NULL, ?);"
        self.cur.executemany(insertquery, list)

    def view(self):
        self.cur.execute("SELECT * FROM noword" )
        rows = self.cur.fetchall()
        return rows

    def update(self, id, noword):
        self.execute("UPDATE noword SET noword=?, WHERE id=?", (self, id, noword))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM noword WHERE id=?", (id,))
        self.conn.commit()

    def deleteall(self):
        self.cur.execute("DELETE FROM noword WHERE id > -1")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

#############################################################################
class Thumb:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS thumb (thumb_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, VideoID TEXT, ThumbUrl TEXT, ThumbNail BLOB)")
        self.conn.commit()
#                       1         2           3            4         5          6         7          8        9
    def insert(self, VideoID, ThumbUrl, ThumbNail):
        self.cur.execute("INSERT INTO thumb VALUES (NULL,?,?,?)", (VideoID, ThumbUrl, ThumbNail))
        self.conn.commit()

    def isthere(self, VidID):
        self.cur.execute("SELECT * FROM thumb WHERE VideoID=?", (VidID,) )
        rows = self.cur.fetchall()
#        return rows
        if len(rows) > 0:
            return True
        else:
            return False

    def generic(self, sqlstring):
        self.cur.execute(sqlstring)
        rows = self.cur.fetchall()
        return rows

    def view(self):
        self.cur.execute("SELECT * FROM thumb" )
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()

###############################################################################
class HaveGot:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS havegot (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, VideoID TEXT, FromSite TEXT)")
        self.conn.commit()
#                       1         2           3            4         5          6         7          8        9
    def insert(self, VideoID, FromSite):
        self.cur.execute("INSERT INTO havegot VALUES (NULL,?,?)", (VideoID, FromSite))
        self.conn.commit()

    def isthere(self, VidID):
        self.cur.execute("SELECT * FROM havegot WHERE VideoID=?", (VidID,) )
        rows = self.cur.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False

    def view(self):
        self.cur.execute("SELECT * FROM havegot" )
        rows = self.cur.fetchall()
        return rows

    def viewfor(self, sqlexpr):
        self.cur.execute("SELECT * FROM havegot "+sqlexpr )
        rows = self.cur.fetchall()
        return rows

    def generic(self, sqlstring):
        self.cur.execute(sqlstring)
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()

################################################################################
class PornStar:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS pornstars (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, PornstarName TEXT, Gender TEXT )")
        self.conn.commit()
#                       1         2           3            4         5          6         7          8        9
    def insert(self, PornstarName, Gender):
        self.cur.execute("INSERT INTO pornstars VALUES (NULL,?,?)", (PornstarName, Gender))
        self.conn.commit()

    def isthere(self, PornstarName):
        self.cur.execute("SELECT * FROM pornstars WHERE PornstarName=?", (PornstarName,) )
        rows = self.cur.fetchall()
        return rows
#        if len(rows) > 0:
#            return True
#        else:
#            return False

    def view(self):
        self.cur.execute("SELECT * FROM pornstars" )
        rows = self.cur.fetchall()
        return rows

    def viewfor(self, sqlexpr):
        self.cur.execute("SELECT * FROM pornstars "+sqlexpr )
        rows = self.cur.fetchall()
        return rows

    def updateGender(self, Gender, PornstarName):
        self.cur.execute("UPDATE pornstars SET Gender=? WHERE PornstarName=?", (Gender, PornstarName,))
        self.conn.commit()


    def generic(self, sqlstring):
        self.cur.execute(sqlstring)
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
