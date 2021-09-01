################ proje I imports ################
#################################################
import os
import sqlite3
import datetime
import pandas as pd
from PIL import Image
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import altair as alt

################ proje I globals ################
#################################################
PATH="D:\\_Kunta_Kinte\\Streamlit\\Streamlit_Trainings\\"
#PATH="F:\\_Kunta_Kinte\\Streamlit\\Streamlit_Trainings\\"
XLSX_FILE="Streamlit_Entry_Data_Final_Output.xlsx"
JPG_FILE="logo_2.jpg"

################ sqlite3 code bloğu ################
####################################################
def Dosya_Bul(isim, yol):
    for root, dirs, files in os.walk(yol):
        if isim in files:
            return os.path.join(root, isim)
           
def DB_Mevcut_Mu(Db_Dosya='Proje_DB.db', Dosya_Yolu=PATH):
    oper = 'açıldı...'
    if Dosya_Bul(Db_Dosya, Dosya_Yolu) is None:
        oper = 'oluşturuldu...'
    conn = sqlite3.connect(Dosya_Yolu+Db_Dosya)
    cur = conn.cursor()
    #print(f'Veritabanı {oper}')
    return conn, cur, oper

def Tablo_Olustur(conn, cur, Tablo_Ismi='Proje_I'):
    comm='''
         CREATE TABLE IF NOT EXISTS 
         '''
    comm=comm+f"{Tablo_Ismi}" + \
           ''' (
           Isl_Tarih DATE NOT NULL,
           Grup TEXT NOT NULL,
           Ekip TEXT NOT NULL,
           Proje TEXT NOT NULL,
           Tam_Anket_Say INTEGER NOT NULL
           );
           '''
    cur.execute(comm); #Birşey yapma...
    return conn, cur

def DB_Kapat(conn, cur):
    try:
        #Değişiklikleri kaydet...
        conn.commit()
        #print('Değişiklikler kaydedildi...')
        conn.close()
        #print('Veritabanı kapatıldı...')
        return 1
    except sqlite3.ProgrammingError as e:
        #print('Veritabanı halihazırda kapalı !')
        #print(e)
        return 0
              
def Kayitlari_Getir(conn, cur, Isl_Tarih=None):
    if Isl_Tarih is None:
        Isl_Tarih="'"+str(datetime.datetime.now().date())+"'"
    comm = '''
           SELECT * from Proje_I
           WHERE Isl_Tarih = 
           '''
    comm = comm+f"{Isl_Tarih}"+";"
    Tum_Kayitlar=cur.execute(comm).fetchall()
    
    #print('\nGetirilen kayıtlar:')
    #for rec in Tum_Kayitlar:
        #print(rec)
     
    return conn, cur, Tum_Kayitlar

def Tum_Kayitlar(conn, cur):
    comm = '''
           SELECT * from Proje_I;
           '''
    Tum_Kayitlar=cur.execute(comm).fetchall()
    
    #print('\nGetirilen kayıtlar:')
    #for rec in Tum_Kayitlar:
        #print(rec)
     
    return conn, cur, Tum_Kayitlar

def Kayitlari_Ekle(conn, cur, Eklenecek_Liste=None):
    if Eklenecek_Liste is None:
        Isl_Tarih=datetime.datetime.now().date()
        
        #Grup="Ekonomik Araştırmalar"
        Grup="Sosyal Araştırmalar"
        #Ekip="Fiyat ve İşgücü"
        Ekip="Sektör"
        #Proje="Hanehalkı İşgücü Araştırması"
        Proje="Yazılı Medya Araştırması"
        Tam_Anket_Say=235
        Eklenecek_Liste = [(Isl_Tarih, Grup, Ekip, Proje, Tam_Anket_Say),]
    comm = '''
           INSERT OR REPLACE INTO Proje_I Values (?,?,?,?,?);
           '''            
    cur.executemany(comm, Eklenecek_Liste)
    conn.commit()
    #print(f"Eklenecek liste : {Eklenecek_Liste}")
    #print("Kayıt(lar) eklendi...")
    return conn, cur

################ sqlite3 code bloğu ################
####################################################

################ proje I fonksiyonlar ################
######################################################

#@st.cache
def Dosyalari_Oku():
    df_Proje=pd.read_excel(PATH+XLSX_FILE, parse_dates=["Baslama", "Bitis"])
    return df_Proje

def Menu_Sakla():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;} # Hide Hamburger Menu
    #if you change "Made With Streamlit"
    #footer {
    #visibility: hidden;
    #}
    #footer:after {
    #content:'goodbye'; 
    #visibility: visible;
    #display: block;
    #position: relative;
    #background-color: red;
    #padding: 5px;
    #top: 2px;
    #}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    return 0

def Tarih_Saat():
    Haf_Gunleri=["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]
    Bugun = datetime.date.today()
    Gun_Str = Bugun.strftime("%d/%m/%Y") # format : dd/mm/YY
    Gun_Str = Gun_Str + " " + Haf_Gunleri[Bugun.weekday()] # Monday = 0
    return (Gun_Str, Bugun)

def Menu_Olustur():
    Options_Tuple = ("Veri Girişi", "Raporlama", "Ana Dosyayı Yükleme")
    
    with Image.open(PATH+JPG_FILE) as Img:
        width, height = Img.size # get the image size...
        # Provide the target width and height of the image
        if ((width > 200) or (height > 200)):
            width, height = 200, 200 # (im.width // 2, im.height // 2)
            Img_Resized = Img.resize((width, height))
    
    st.sidebar.image(Img, use_column_width = True)
    st.sidebar.markdown("<h1 style='text-align: center; color: red;'>Kral Kamuoyu Araştırma</h1>", unsafe_allow_html=True)    
    st.sidebar.markdown("<h1 style='text-align: center; color: red;'>Çalışma Durum Takip</h1>", unsafe_allow_html=True)    
    
    Option = st.sidebar.selectbox(label="Seçiminiz...", options = Options_Tuple, index = 0)
    
    with st.sidebar.beta_expander('Hakkında', expanded = False):
        st.info("2021 yılında geliştirildi.")
        
    return Option, Options_Tuple
    
def file_uploaders():
    Yuklenen_Dosya = st.file_uploader("Dosya Yükleme", type = ["xlsx",])
    Dosya_Turu = st.selectbox("Dosya Türünü Seçiniz...", ["xlsx",])
    if st.button("Yükle"):
        if Yuklenen_Dosya is not None:
            if Dosya_Turu == 'xlsx':
                Islenen_Dosya = pd.read_excel(Yuklenen_Dosya)
            else:
                st.error("Dosya Türü xlsx Uzantılı Excel Dosyası Olmalıdır !")
        else:
            st.error("Dosya Seçiniz !")
            Islenen_Dosya = None
        return Islenen_Dosya

def Veri_Gir(df_Proje, df_Girilen, conn, cur): # scope !!!
    #st.text("Bugün : " + Tarih_Saat()[0])
    
    Isl_Tarih=st.date_input("Tarih Seçiniz : ", \
                            value=datetime.date.today(), \
                            min_value=datetime.date(2021, 1, 1), \
                            max_value=datetime.date(2021, 12, 31)).strftime('%Y-%m-%d')
    
    Kriter=((Isl_Tarih >= df_Proje["Baslama"]) & (Isl_Tarih <= df_Proje["Bitis"]))

    df_Kume=df_Proje[Kriter]
    
    Grouped = df_Kume.groupby("Grup")
    Grp_Tuple = tuple(Grouped.groups.keys())
    Grp_Secim = st.selectbox("Grup Ismi", Grp_Tuple)

    Grouped = df_Kume.groupby("Grup")["Ekip"].unique()
    Tak_List = tuple(Grouped[Grp_Secim])
    Tak_Secim = st.selectbox("Ekip İsmi", Tak_List)

    Proje_Dict = dict()
    Grouped = df_Kume.groupby(["Grup", "Ekip"])["Proje"]
    for group_name, group_block in Grouped:
        Proje_Dict[group_name] = tuple(group_block)

    Ara_Secim = st.selectbox("Proje İsmi", Proje_Dict[(Grp_Secim, Tak_Secim)])
    Tam_Anket_Say = st.number_input('Toplam Tamamlanmış Anket Sayısı (Doğrudan Elle Giriş Yapılabilir...)', \
                                    min_value=0, max_value=9999, value=0, step=10, format=None)

    Onay_Buton = st.button(label='Onayla')
    if Onay_Buton:
        rows=len(df_Girilen.index)+1
        
        df_Girilen.loc[rows, "Isl_Tarih"] = Isl_Tarih
        df_Girilen.loc[rows, "Grup"] = Grp_Secim
        df_Girilen.loc[rows, "Ekip"] = Tak_Secim
        df_Girilen.loc[rows, "Proje"] = Ara_Secim
        df_Girilen.loc[rows, "Tam_Anket_Say"] = Tam_Anket_Say
        st.success("Başarılı...")    
        st.dataframe(df_Girilen)
        #####
        Tek_Kayit=[(Isl_Tarih, Grp_Secim, Tak_Secim, Ara_Secim, Tam_Anket_Say),]
        _, _ = Kayitlari_Ekle(conn, cur, Eklenecek_Liste=Tek_Kayit)
        st.balloons()

def Yardimci_Dosya():
    df_Dict = {"Isl_Tarih": [], "Grup": [], "Ekip" : [], "Proje" : [], "Tam_Anket_Say" : []}
    df_Girilen = pd.DataFrame(df_Dict)
    return df_Girilen

################ proje I fonksiyonlar ################
######################################################

def main():
    Menu_Sakla()
    df_Girilen=Yardimci_Dosya()
    df_Proje=Dosyalari_Oku()
    
    conn,cur,oper=DB_Mevcut_Mu(Db_Dosya='Proje_DB_10.db', Dosya_Yolu=PATH)
    if oper == 'oluşturuldu...':
        conn,cur=Tablo_Olustur(conn, cur, Tablo_Ismi='Proje_I')
        # conn,cur=Kayitlari_Ekle(conn, cur, Eklenecek_Liste = None)
    else:
        pass
    
    Option, Options_Tuple = Menu_Olustur()

    if Option == Options_Tuple[0]: #"Veri Girişi"
        st.text("Bugün : " + Tarih_Saat()[0])
        st.header("- Veri Girişi -")
        #st.title("- Veri Girişi -")
        Veri_Gir(df_Proje, df_Girilen, conn, cur)
    elif Option == Options_Tuple[1]: #"Raporlama"
        st.text("Bugün : " + Tarih_Saat()[0])
        st.header("- Raporlama -")
        #st.title("- Raporlama -")
        ###
        # _, _, ret = Kayitlari_Getir(conn, cur, Isl_Tarih=None)
        # print(f"Getirilen : {ret}")
        
        _, _, ret = Tum_Kayitlar(conn, cur)
        df_Hepsi=pd.DataFrame(ret)
        df_Hepsi.columns=["Isl_Tarih","Grup","Ekip","Proje","Tam_Anket_Say"]
        
        #df_Tekil=df_Hepsi.drop_duplicates(subset=["Isl_Tarih","Grup","Ekip","Proje"], keep='last')
        df_Tekil=df_Hepsi.drop_duplicates(subset=["Grup","Ekip","Proje"], keep='last')

        df_Result = pd.merge(df_Tekil, df_Proje, how="left", on=["Proje", "Proje"])
        # "Proje" Proje Isimleri
        # "ToplamIsyuku" Hedef Değer,Ulasilan_Deger
        # "Tam_Anket_Say" Ulaşılan_Değer
        
        df_Result["Baslama"]=pd.to_datetime(df_Result["Baslama"]) # datetime
        df_Result["Bitis"]=pd.to_datetime(df_Result["Bitis"]) # datetime
        df_Result["Isl_Tarih"]=pd.to_datetime(df_Result["Isl_Tarih"]) # datetime
        df_Result["Beklenen_Tamamlanma"]=(df_Result["Isl_Tarih"] - df_Result["Baslama"]).dt.days * \
                                          df_Result["Kisi"] * df_Result["GunlukAnket"]
        df_Result["Proje_Durum"] = df_Result["Tam_Anket_Say"] - df_Result["Beklenen_Tamamlanma"] 
        
        #df_Grafik=df_Result[["Proje", "Beklenen_Tamamlanma"]]
        #df_Grafik.set_index("Proje", inplace=True)
        
        # col1,col2=st.beta_columns(2) 
        col1,col2=st.beta_columns([1, 3]) 
        with col1:
            with st.beta_expander("Veriseti"):
                #st.dataframe(df_Tekil)
                st.dataframe(df_Result)
        with col2:
            with st.beta_expander("Grafik"):
                # st.bar_chart(df_Grafik, use_container_width=True)
                Altair_Grafik=alt.Chart(df_Result).mark_bar().encode(
                    x='Proje_Durum', y='Proje')
                st.altair_chart(Altair_Grafik, use_container_width=True)                
                
        #fig = px.bar(df_Result, x="Proje_Durum", \
                     #y="Proje", title="Projelerde Tamamlanma Durumu", \
                     #orientation='h', width=500, height=500, barmode='group')
        #fig.show()
                
    elif Option == Options_Tuple[2]: # "Ana Dosyayı Yükleme"
        st.text("Bugün : " + Tarih_Saat()[0])
        st.header("- Dosya Yükleme -")
        #st.title("- Dosya Yükleme -")
        Islenen_Dosya = file_uploaders()
        if Islenen_Dosya is not None:
            st.write(Islenen_Dosya)

if __name__ == '__main__':
    main()    

#DB_Kapat(conn, cur):
