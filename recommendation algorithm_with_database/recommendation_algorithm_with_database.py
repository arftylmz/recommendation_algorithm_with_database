from tkinter.ttk import Combobox, Style
import recommendations
import xlrd
import sqlite3
from tkinter import *
from tkinter import filedialog
class Editor(Frame):

    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.root=parent
        self.initUI()

    def initUI(self):
        self.sozluk = dict()
        #veritabanı yaratma aşaması.
        self.conn=sqlite3.connect('kendi_degerlendirmelerim.db')
        self.islem = self.conn.cursor()
        self.islem.execute("""CREATE TABLE IF NOT EXISTS secimler(isim text,deger float)""")
        self.conn.commit()





        self.filename=("Musteri_Degerlendirmeleri.xlsx")
        self.grid()

        frame = Frame(self,bg="Beige" , width = "700", height="700",pady = "25",padx="10")
        frame.grid()
        self.Baslik = Label(frame,text="İstinye Kafetarya Öneri Sistemi", fg="Blue", bg="Beige")
        self.Baslik.config(font=("Courier", 18, "bold italic"))
        self.Baslik.grid(row=0, column = 1,columnspan = 7)
        self.bosLabel2 = Label(frame, bg="Beige")
        self.bosLabel2.grid(row=1,columnspan = 7)
        ###########################################3333
        self.Dosya_Sec = Label(frame,text="Müşteri Değerlendirmelerini Yükle",fg="Blue", bg="Beige")
        self.Dosya_Sec.config(font=("Courier", 14, "bold italic"))
        self.Dosya_Sec.grid(row = 2,column = 1,columnspan = 3)
        self.button=Button(frame,text="Dosya Seç",fg="Blue",bg ="Gold",command=self.Dosya)
        self.button.grid(row = 2,column=4)
        self.bosLabel4 = Label(frame, bg="Beige")
        self.bosLabel4.grid(row=3, columnspan=7)
        self.Kendi_Ayarlarim = Label(frame,text = "Kendi Değerlendirmelerim", fg="Blue", bg="Beige")
        self.Kendi_Ayarlarim.config(font=("Courier", 14, "bold italic"))
        self.Kendi_Ayarlarim.grid(row=4, column = 2,columnspan = 3 ,sticky=N + E + W + S)
        self.secim = StringVar()
        self.combo = Combobox(frame, width=15, textvariable=self.secim,state = "readonly")
        self.combo.grid(row = 5,column=1,sticky = E+N,padx = "20",pady="10")
        style = Style()

        style.map('TCombobox', selectbackground=[('readonly', 'Beige')])
        style.map('TCombobox', fieldforeground=[('readonly', 'black')])
        style.map('TCombobox', fieldbackground=[('readonly', 'Beige')])
        style.map('TCombobox', selectforeground=[('readonly', 'black')])

        self.label = Label(frame,text="değer giriniz", fg="Blue", bg="Beige")
        self.label.config(font=("Courier", 12, "bold italic"))
        self.label.grid(row = 5,column = 2,sticky = N,pady="5",padx ="10")
        self.deger = StringVar()
        self.degerGir = Entry(frame,textvariable = self.deger, fg="Blue", bg="Beige",width = 5)
        self.degerGir.grid(row = 5,column = 3,sticky = N,pady="10")
        self.ekleme = Button(frame, text="Ekle", fg="Blue", bg="Gold", command=self.Ekle,width ="10")
        self.ekleme.grid(row=5, column=4,sticky = N,pady="10")
        self.secileniKaldir = Button(frame, text="Seçileni Kaldır", command=self.Kaldir, fg="Blue", bg="Gold")
        self.secileniKaldir.grid(row=5, column=7, sticky=N, pady="10",padx = "10")
        #Listbox + scroll
        self.scroll=Scrollbar(frame,orient=VERTICAL,width =35)
        self.listbox = Listbox(frame,width =30 ,selectmode="EXTENDED", fg="Blue", bg="Beige",yscrollcommand=self.scroll)
        self.listbox.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox.grid(row = 5, column =5,sticky=W,pady="10")
        self.scroll.config(command=self.listbox.yview) ## AY
        self.listbox.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=5, column=6,sticky=N + S,pady="10")
        self.sozluk.setdefault("Person", {})
        self.islem.execute("""SELECT * FROM secimler""")
        # veritabanında bilgileri çekiyoruz
        for veri in self.islem:
            self.listbox.insert(END, veri)
            self.sozluk.setdefault("Person", {})
            self.sozluk["Person"][veri[0]] = float(veri[1])
        #print(self.sozluk)
        #Radiobutton tasarım.
        self.oneri_modeli = Label(frame, text="Öneri Modeli", fg="Blue", bg="Beige")
        self.oneri_modeli.config(font=("Courier", 14, "bold italic"))
        self.oneri_modeli.grid(row=7, column=4, sticky=W)
        self.benzerlik_olcutu = Label(frame, text="Benzerlik Ölçütü", fg="Blue", bg="Beige")
        self.benzerlik_olcutu.config(font=("Courier", 14, "bold italic"))
        self.benzerlik_olcutu.grid(row=10, column=4)
        self.oneri_degiskeni = StringVar()
        self.hesaplama_degiskeni = StringVar()
        self.radio1=Radiobutton(frame,text="Oklid",value=2,variable=self.oneri_degiskeni, fg="Blue", bg="Beige")
        self.radio2=Radiobutton(frame,text="Pearson",value=3,variable=self.oneri_degiskeni, fg="Blue", bg="Beige")
        self.radio3=Radiobutton(frame,text="Jaccard",value=4,variable=self.oneri_degiskeni, fg="Blue", bg="Beige")
        self.radio4=Radiobutton(frame,text="Kullanici Bazlı",value=0,variable=self.hesaplama_degiskeni, fg="Blue", bg="Beige")
        self.radio5=Radiobutton(frame,text="Urun Bazlı",value=1,variable=self.hesaplama_degiskeni, fg="Blue", bg="Beige")
        self.radio4.grid(row=8, column=4, sticky=W, padx="30")
        self.radio5.grid(row=9, column=4, sticky=W, padx="30")
        self.radio1.grid(row=11, column=4,sticky=W,padx = "30")
        self.radio2.grid(row=12, column=4,sticky=W,padx = "30")
        self.radio3.grid(row=13, column=4,sticky=W,padx = "30")
        ## AYARLAR + Öneri Adeti
        self.bosLabel1 = Label(frame, bg="Beige")
        self.bosLabel1.grid(row=5, columnspan=7)

        self.ayarlar = Label(frame,text="Ayarlar", fg="Blue", bg="Beige")
        self.ayarlar.config(font=("Courier", 14, "bold italic"))
        self.ayarlar.grid(row = 7, column = 1 , sticky = N)
        self.Sayı_Label = Label(frame,text="Toplam Öneri Adeti",fg="Blue", bg="Beige")
        self.Sayı_Label.config(font=("Courier", 12, "bold italic"))
        self.Sayı_Label.grid(row =8,column = 1,stick = E)
        self.sayi = IntVar()
        self.Sayı_Entry = Entry(frame,textvariable = self.sayi,width = "5", fg="Blue", bg="Beige")
        self.Sayı_Entry.grid(row = 8,column =2,sticky =W,padx ="10")



        self.bosLabel3 = Label(frame, bg="Beige")
        self.bosLabel3.grid(row = 14,columnspan = 7)

        #Öneri alma Butonları
        self.oneri_al = Button(frame, text="Öneri Al", fg="Blue", bg="Gold",command = self.Oneri_Ekle)  # command ekle
        self.oneri_al.grid(row=15, column=2)
        self.benzer_musteri = Button(frame, text="Benzer Musteri Listele", fg="Blue", bg="Gold",command = self.Benzer_Urun)
        self.benzer_musteri.grid(row=15, column=5)


        #Listbox + Scroll
        self.scroll_oneri = Scrollbar(frame,orient=VERTICAL,width= 35)
        self.scroll_musteri = Scrollbar(frame,orient=VERTICAL,width= 35)
        self.listbox_oneri = Listbox(frame,width =30 ,selectmode="EXTENDED", fg="Blue", bg="Beige",
                                     yscrollcommand=self.scroll_oneri)
        self.listbox_oneri.bind("<<ListboxSelect>>")
        self.listbox_musteri = Listbox(frame,width =30 ,selectmode="EXTENDED", fg="Blue", bg="Beige",
                                       yscrollcommand=self.scroll_musteri)
        self.listbox_musteri.bind("<<ListboxSelect>>")
        self.listbox_oneri.grid(row=16, column=2, sticky=N)
        self.listbox_musteri.grid(row=16, column=5, sticky=N)

        self.scroll_oneri.config(command=self.listbox_oneri.yview)  ## AY
        self.listbox_oneri.config(yscrollcommand=self.scroll_oneri.set)
        self.scroll_oneri.grid(row=16, column=3, sticky=N + S)
        self.scroll_musteri.config(command=self.listbox_musteri.yview)  ## AY
        self.listbox_musteri.config(yscrollcommand=self.scroll_musteri.set)
        self.scroll_musteri.grid(row=16, column=6, sticky=N + S)




        self.combo['values'] = ('Yemek Seçiniz','Kucuk Kahvalti Tabagi', 'Kahvalti Tabagi', 'Yumurtali Ekmek', 'Sahanda Yumurta', 'Sahanda Sucuklu Yumurta', 'Sahanda Kavurmali Yumurta', 'Sade Omlet', 'Beyaz Peynirli Omlet', 'Kasarli Omlet', 'Bahcivan Omlet', 'Karisik Omlet', 'Kavurmali Omlet', 'Menemen', 'Menemen Kasarli', 'Menemen Beyaz Peynirli', 'Kasarli Tost', 'Beyaz Peynirli Tost', 'cift Kasarli Tost', 'Karisik Tost', 'Ege Tost (Ciabata Ekmegi)', 'Kavurmali Tost', 'Sucuklu Bazlama Tost', 'Beyaz Peynirli Gozleme Tabagi', 'Kasarli Gozleme Tabagi', 'Karisik Gozleme Tabagi', 'Su Boregi', 'Patatesli Kol Boregi', 'Patates Tava', 'Izgara Tavuk Sandwic', 'Pilic Nugget', 'Kaplamali Tavuk Sandwic', 'citir Tavuk Sepeti', 'Penne Arabbiata', 'Sebzeli Tavuklu Bavetta', 'Dort Peynirli Bavetta', 'Penne Con Melenzane', 'Bonfileli Penne', 'Soya Soslu Tavuk', 'Pilic Sote', 'Taze Baharatli Izgara Tavuk', 'Tavuklu Kebap', 'Kaplamali Tavuk', 'Acili Tavuk', 'Barbeku Soslu Tavuk', 'Pesto Soslu Tavuk', 'Kori Soslu Tavuk', 'Patlicanli Kofteli Kebap', 'Izgara Kofte', 'Karisik Et Tabagi', 'cokertme Kebabi', 'Manti', 'Sosisli', 'Gorali', 'Islak Hamburger', 'Hamburger', 'Cheese Burger', 'Tavuk Burger', 'Patso', 'Kofte Durum', 'Sucuk Durum', 'citir Tavuk Durum', 'Akdeniz Salata', 'Tavuklu Sezar', 'citir Tavuk Salata', 'sis Kofte Salata', 'Ton Balikli Salata', 'Bonfile Salata', 'Kucuk Kahvalti Tabagi', 'Kahvalti Tabagi', 'Yumurtali Ekmek', 'Sahanda Yumurta', 'Sahanda Sucuklu Yumurta', 'Sahanda Kavurmali Yumurta', 'Sade Omlet', 'Beyaz Peynirli Omlet', 'Kasarli Omlet', 'Bahcivan Omlet', 'Karisik Omlet', 'Kavurmali Omlet', 'Menemen', 'Menemen Kasarli', 'Menemen Beyaz Peynirli', 'Kasarli Tost', 'Beyaz Peynirli Tost', 'cift Kasarli Tost', 'Karisik Tost', 'Ege Tost (Ciabata Ekmegi)', 'Kavurmali Tost', 'Sucuklu Bazlama Tost', 'Beyaz Peynirli Gozleme Tabagi', 'Kasarli Gozleme Tabagi', 'Karisik Gozleme Tabagi', 'Su Boregi', 'Patatesli Kol Boregi', 'Patates Tava', 'Izgara Tavuk Sandwic', 'Pilic Nugget', 'Kaplamali Tavuk Sandwic', 'citir Tavuk Sepeti', 'Penne Arabbiata', 'Sebzeli Tavuklu Bavetta', 'Dort Peynirli Bavetta', 'Penne Con Melenzane', 'Bonfileli Penne', 'Soya Soslu Tavuk', 'Pilic Sote', 'Taze Baharatli Izgara Tavuk', 'Tavuklu Kebap', 'Kaplamali Tavuk', 'Acili Tavuk', 'Barbeku Soslu Tavuk', 'Pesto Soslu Tavuk', 'Kori Soslu Tavuk', 'Patlicanli Kofteli Kebap', 'Izgara Kofte', 'Karisik Et Tabagi', 'cokertme Kebabi', 'Manti', 'Sosisli', 'Gorali', 'Islak Hamburger', 'Hamburger', 'Cheese Burger', 'Tavuk Burger', 'Patso', 'Kofte Durum', 'Sucuk Durum', 'citir Tavuk Durum', 'Akdeniz Salata', 'Tavuklu Sezar', 'citir Tavuk Salata', 'sis Kofte Salata', 'Ton Balikli Salata', 'Bonfile Salata')
        self.combo.current(0)

    def Dosya(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Dosya Seç",
                                                      filetypes=(("excel files", "*.xlsx"), ("all files", "*.*")))
        try:
            book = xlrd.open_workbook(self.filename)

            sayfa = book.sheet_by_index(0)
            for i in range(1, int(sayfa.nrows)):
                isim = str(sayfa.cell(i, 0).value)
                self.sozluk.setdefault(isim, {})
                yemek = str(sayfa.cell(i, 1).value)
                puan = round(sayfa.cell(i, 2).value, 1)
                self.sozluk[isim][yemek] = puan
            # print(recommendations.sim_distance(self.sozluk, 'Person', 'OZGE'))
            self.reverse = recommendations.transformPrefs(self.sozluk)
        except:
            print("Dosya seçiniz")
        # print(self.reverse)
        # print(self.sozluk)

    def onSelect(self, val):
        try:
            widget = val.widget
            idx = widget.curselection()
            self.value = widget.get(idx)
        except:
            print("")


    def Ekle(self):

        try:
            self.veri1 = self.secim.get()
            self.veri2 = float(self.deger.get())
            last = self.veri1,str(self.veri2)
            self.islem.execute("""INSERT INTO secimler VALUES (?,?)""",last)
            self.conn.commit()
            self.listbox.insert(END,last)
            self.sozluk.setdefault("Person",{})
            self.sozluk["Person"][self.veri1] = float(self.veri2)
        except:
            print("Doğru veri girişi yapınız.")





    def Kaldir(self):
        self.islem.execute("""DELETE FROM secimler WHERE isim = ? AND deger = ? """,self.value)
        self.conn.commit()
        self.listbox.delete(self.listbox.curselection())
        for key in self.sozluk:
            if(key == "Person"):
                for item in self.sozluk[key]:
                    if(item == self.value[0]):
                        self.sozluk[key].pop(item)
                        break
    def Oneri_Ekle(self):
        count = 0
        book = xlrd.open_workbook(self.filename)
        sayfa = book.sheet_by_index(0)
        for i in range(1, int(sayfa.nrows)):
            isim = str(sayfa.cell(i, 0).value)
            self.sozluk.setdefault(isim, {})
            yemek = str(sayfa.cell(i, 1).value)
            puan = round(sayfa.cell(i, 2).value, 1)
            self.sozluk[isim][yemek] = puan
        #print(recommendations.sim_distance(self.sozluk, 'Person', 'OZGE'))
        #self.reverse = recommendations.transformPrefs(self.sozluk)
        #print(self.reverse)
        #print(self.sozluk)
        #print(self.oneri_degiskeni.get(),self.hesaplama_degiskeni.get())
        d1 = int(self.hesaplama_degiskeni.get())
        d2 = int(self.oneri_degiskeni.get())

        if (d1==0):
            if (d2 == 2):
                deneme = recommendations.getRecommendations(self.sozluk,'Person',similarity = recommendations.sim_distance)
                self.listbox_oneri.delete(0, END)

                for veri in deneme:
                    if (self.sayi.get() == 0):
                        self.listbox_oneri.insert(END, "Adet Sayısı giriniz....")
                        break
                    else:
                        self.listbox_oneri.insert(END, veri[1] +" " +  str(round(veri[0],1)))
                        count +=1
                        if(count == self.sayi.get()):
                            count = 0
                            break

            if(d2 == 3):
                deneme = recommendations.getRecommendations(self.sozluk, 'Person',
                                                                similarity=recommendations.sim_pearson)
                self.listbox_oneri.delete(0, END)
                for veri in deneme:
                    if (self.sayi.get() == 0):
                        self.listbox_oneri.insert(END, "Adet Sayısı giriniz....")
                        break
                    else:
                        self.listbox_oneri.insert( END, veri[1] +" " +  str(round(veri[0],1)))
                        count += 1
                        if (count == self.sayi.get()):
                            count = 0
                            break
            if(d2 == 4):
                deneme = recommendations.getRecommendations(self.sozluk, 'Person',
                                                            similarity=recommendations.sim_jaccard)
                self.listbox_oneri.delete(0,END)

                for veri in deneme:
                    if (self.sayi.get() == 0):
                        self.listbox_oneri.insert(END, "Adet Sayısı giriniz....")
                        break
                    else:
                        self.listbox_oneri.insert(END, veri[1] +" " +  str(round(veri[0],1)))
                        count += 1
                        if (count == self.sayi.get()):
                            count = 0
                            break
        elif(d1==1):

            if (d2 == 2):
                self.listbox_oneri.delete(0, END)
                # Create a dictionary of items showing which other items they
                # are most similar to.
                result = {}
                # Invert the preference matrix to be item-centric
                itemPrefs = recommendations.transformPrefs(self.sozluk)
                c = 0
                for item in itemPrefs:
                    # Status updates for large datasets
                    c += 1
                    if c % 100 == 0:
                        print("%d / %d" % (c, len(self.sozluk)))
                    # Find the most similar items to this one
                    scores = recommendations.topMatches(itemPrefs, item, self.sayi.get(), similarity=recommendations.sim_distance)
                    result[item] = scores
                print(recommendations.getRecommendedItems(self.sozluk, result, 'Person'))
                deneme = recommendations.getRecommendedItems(self.sozluk, result, 'Person')
                if (len(deneme) == 0):
                    self.listbox_oneri.insert(END, "Adet Sayısı giriniz....")
                for veri in deneme:
                    self.listbox_oneri.insert( END, veri[1] + " " + str(round(veri[0], 1)))
                    count += 1
                    if (count == self.sayi.get()):
                        break
                #print(deneme)
            if(d2 == 3):
                self.listbox_oneri.delete(0, END)
                # Create a dictionary of items showing which other items they
                # are most similar to.
                result = {}
                # Invert the preference matrix to be item-centric
                itemPrefs = recommendations.transformPrefs(self.sozluk)
                c = 0
                for item in itemPrefs:
                    # Status updates for large datasets
                    c += 1
                    if c % 100 == 0:
                        print("%d / %d" % (c, len(self.sozluk)))
                    # Find the most similar items to this one
                    scores = recommendations.topMatches(itemPrefs, item, n=self.sayi.get(), similarity=recommendations.sim_pearson)
                    result[item] = scores
                print(result)
                deneme = recommendations.getRecommendedItems(self.sozluk, result, 'Person')
                if (len(deneme) == 0):
                    self.listbox_oneri.insert(END, "Adet Sayısı giriniz....")
                for veri in deneme:
                    self.listbox_oneri.insert( END, veri[1] +" " +  str(round(veri[0],1)))
                    count += 1
                    if (count == self.sayi.get()):

                        break

                print(recommendations.getRecommendedItems(self.sozluk, result, 'Person'))
            if(d2 == 4):
                self.listbox_oneri.delete(0, END)
                # Create a dictionary of items showing which other items they
                # are most similar to.
                result = {}
                # Invert the preference matrix to be item-centric
                itemPrefs = recommendations.transformPrefs(self.sozluk)
                c = 0
                for item in itemPrefs:
                    # Status updates for large datasets
                    c += 1
                    if c % 100 == 0:
                        print("%d / %d" % (c, len(self.sozluk)))
                    # Find the most similar items to this one
                    scores = recommendations.topMatches(itemPrefs, item, n=self.sayi.get(), similarity=recommendations.sim_jaccard)
                    result[item] = scores

                print(recommendations.getRecommendedItems(self.sozluk, result, 'Person'))
                deneme = recommendations.getRecommendedItems(self.sozluk, result, 'Person')
                if (len(deneme) == 0):
                    self.listbox_oneri.insert(END, "Adet Sayısı giriniz....")
                else:
                    for veri in deneme:
                        self.listbox_oneri.insert(END, veri[1] + " " + str(round(veri[0], 1)))
                        count += 1
                        if (count == self.sayi.get()):

                            break
        else:
            print("Doğru bir seçenek giriniz.")



    def Benzer_Urun(self):
        book = xlrd.open_workbook(self.filename)
        sayfa = book.sheet_by_index(0)
        for i in range(1, int(sayfa.nrows)):
            isim = str(sayfa.cell(i, 0).value)
            self.sozluk.setdefault(isim, {})
            yemek = str(sayfa.cell(i, 1).value)
            puan = round(sayfa.cell(i, 2).value, 1)
            self.sozluk[isim][yemek] = puan

        self.reverse = recommendations.transformPrefs(self.sozluk)

        d2 = int(self.oneri_degiskeni.get())
        if (d2 == 2):
            self.listbox_musteri.delete(0,END)
            deneme = recommendations.topMatches(self.sozluk, 'Person', self.sayi.get(), similarity=recommendations.sim_distance)
            for veri in deneme:
               self.listbox_musteri.insert(END, veri[1] +" " +  str(round(veri[0],1)))

        if  (d2 == 3):
            self.listbox_musteri.delete(0, END)
            deneme = recommendations.topMatches(self.sozluk, 'Person', self.sayi.get(), similarity=recommendations.sim_pearson)
            for veri in deneme:
                self.listbox_musteri.insert(END, veri[1] +" " +  str(round(veri[0],1)))
        if (d2 == 4):
            self.listbox_musteri.delete(0, END)
            deneme = recommendations.topMatches(self.sozluk, 'Person', self.sayi.get(), similarity=recommendations.sim_jaccard)
            for veri in deneme:
                self.listbox_musteri.insert(END, veri[1] +" " +  str(round(veri[0],1)))

def main():
    root= Tk()
    root.title("Excel-Reader")
    root.geometry("920x750+300+100")
    #konumu ayarlıyoruz ve ekran boyut ayarlamasını kapatıyoruz.
    root.resizable(FALSE,FALSE)
    App = Editor(root)
    root.mainloop()

if __name__ == '__main__':
    main()
