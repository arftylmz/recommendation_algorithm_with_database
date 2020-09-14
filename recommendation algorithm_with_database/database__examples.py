import sqlite3
from tkinter import *

vt = sqlite3.connect('demebe.db')
islem=vt.cursor()
tablo = """CREATE TABLE IF NOT EXISTS secimler(isim text,puan float)"""
islem.execute(tablo)
cemalll= ('cemal','4,2')


islem.executemany("""INSERT INTO secimler VALUES (?,?)""",[cemalll])
vt.commit()
islem.execute("""SELECT * FROM secimler""")
y = cemalll[0]
islem.execute("""DELETE FROM secimler WHERE isim = ?"""[y])
for veri in islem:
    print(veri)



master = Tk()

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(master, yscrollcommand=scrollbar.set)
for i in range(1000):
    listbox.insert(END, str(i))
listbox.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=listbox.yview)

mainloop()
