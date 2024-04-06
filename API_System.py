import json 
import requests
import re
import tkinter as tk
from tkinter import messagebox
import random
import time

pencere = tk.Tk()
pencere.title("yeni")
pencere.geometry("1000x1000")

def change_background_color():
    colors = ["red", "green", "blue", "yellow", "orange", "purple"]
    new_color = random.choice(colors)
    pencere.configure(bg=new_color)
    pencere.after(2000, change_background_color)


left = tk.Frame(pencere)
left.pack(side="left")
pencere.configure(bg="white")
pencere.after(2000, change_background_color)



label6= tk.Label(pencere,text="")
label6.pack()

lefttext_widget = tk.Text(left, width=40, height=30)
lefttext_widget.pack() 
 
label3 = tk.Label(pencere, text="sicil no:")
label3.pack()
label3.config(bg="pink")

no = tk.Entry(width=30)
no.pack()

label2 = tk.Label(pencere, text="")
label2.pack()

label4 = tk.Label(pencere, text="")
label4.pack()

label5 = tk.Label(pencere, text="")
label5.pack()



url='http://pdks-server:8081/jwt-api-token-auth/' 

data ={     
         
           "username":"",
           "password":""
}


response=requests.post(url, json=data)  

if response.status_code == 200:
    token = response.json().get("token")
    if token:
        print("Oturum açıldı. token:", token)
    else:
        print("token alınamadı.")
else:
    print("Oturum açma başarısız. Hata kodu:", response.status_code)

    print("Hata mesajı:", response.text)



url1= 'http://pdks-server:8081/personnel/api/employees/?emp_code='

headers ={ 
            "Content-Type":"application/json",
            "Authorization":"JWT " + token
            

    }


personal_id = None 

personal_area_ids= []

int_personal_area_idss=[]
 


eklenenler = set()
def giriş():
 
 global lefttext_widget
 lefttext_widget.delete("1.0",tk.END)
 sicil_numarasi = no.get()  
 if sicil_numarasi: 
          
    response1 = requests.get(url1 +no.get() ,headers=headers)
    if response1.status_code == 200:    
        data1=response1.json()
        print(data1)
        if 'data' in data1:
            for a in data1['data']:
                if 'id' in a:
                    global personal_id
                    personal_id = a['id']
                    print("personel id=",str(personal_id))
                else:
                    print("personel id yok.")
        else:
            print("data yok")      
                                                    
        countsonuc=data1['count']
        if countsonuc == 0:
                                        
            label5 = tk.Label(pencere, text="böyle bir personel kayıtlı değildir.")
            label5.pack()

        else:
            personal_area_ids =[]
            
            
            if 'data' in data1:
                for i in data1['data']:
                    if 'area' in i:
                        for j in i['area']:
                             if 'id' in j and'area_code' in j and 'area_name' in j:
                                global int_personal_area_idss
                                global eklenenler
                                personal_area_id = j['id']
                                eklenenler.add(personal_area_id)
                               
                                personal_area_ids .append(personal_area_id)
                                personal_area_idss = ', '.join(map(str, personal_area_ids))
                                int_personal_area_idss = [int(value) for value in personal_area_idss.split(', ')]
                                
                                area_code = j['area_code']
                                area_name = j['area_name']
                                                            
                               
                                lefttext_widget.insert(tk.END,  str(personal_area_id) +'  ||||  '+ area_code +'  ||||  ' + area_name +'\n') 
                                                        
                             else:
                                print("area anahtarının içinde area_name ve area_code yok.")
                    else:
                        print("data içinde area anahtarı yok.")
            else:
                print("data anahtarı yok.")
    else:
      print("Hata kodu 200 değil.") 

    label2.config(text="Giriş yapıldı: " + sicil_numarasi)
    
    lefttext_widget.insert(tk.END ,' \n' * 3)
 else:
  label2.config("Sicil numarası girilmedi.")

         

buton1 = tk.Button(pencere, text="GİRİŞ",command=lambda:giriş())
buton1.pack()
buton1.config(bg="pink")


genel_area_id =None
list = tk.Listbox(pencere,width=40, height=40)
url2 = 'http://pdks-server:8081/personnel/api/areas/?page='
i=1

while(True):
      url3=(url2 + str(i))
      response2 = requests.get(url3 , headers=headers) 
      data2=response2.json()
      print(data2)
      if 'data' in data2:
            for x in data2['data']:
                if 'id'in x and 'area_code' in x and 'area_name' in x:
                 
                 genel_area_id = str(x['id'])
                 area_code = x['area_code']
                 area_name = x['area_name']
                 
                 list.insert(tk.END,  genel_area_id  +'  ||||  ' +area_code + '  ||||  ' + area_name +'\n' )
                 list.configure(selectmode=tk.MULTIPLE)
                 list.config(width=30, height=30)
                 list.pack()
                else:
                  print("data içinde id ,area_code ve area_name yok.")
      else:
           print("data yok.")

      nextsonuc=data2['next']
      print("next:",nextsonuc)
      if nextsonuc is None:
        break
      i += 1   
          

url4='http://pdks-server:8081/personnel/api/employees/'
toplam1=[]
int_sec_ids=[]



def ekle():
     
   
    sec_item = list.curselection()
   

    if sec_item:
      
      sec_ids = []
      sec_idsss=[]
        
      for l in sec_item:
            sec = list.get(l) 
            sec_id = sec.split(' |||| ')[0].strip()
            sec_ids.append(sec_id)
            sec_idsss = ', '.join(sec_ids)

            
                    
           
            
      for sec_id in sec_ids:
            
            int_sec_id = int(sec_id) 
            int_sec_ids.append(int_sec_id)

            if int_sec_id in eklenenler:
                
                messagebox.showinfo("HATA", "Seçtiğiniz areaya kayıtlısınız!!!")
               
                
            else :
                label4.config(text="Eklenen ID'ler: "+ sec_idsss)
             
                eklenenler.add(int_sec_id)
     
            
           
    else:
     label4.config(text="Hiçbir area seçilmedi.")
     



    global toplam1
    toplam1 =(int_personal_area_idss) + (int_sec_ids)
    

    Body = {
                     "area": 
                                 (toplam1)
                              
                       
                  
                 }
     
    print(url4 + str(personal_id) + '/')
    response4 = requests.patch(url4 + str(personal_id) + '/', json=Body, headers=headers)
    
    if response4.status_code == 200:
          data3 = response4.json()
          print("Güncellenmiş veri:", data3)
    elif response4.status_code == 404:
          print("Kaynak bulunamadı.")
    else:
          print("API isteği başarısız. HTTP Hata Kodu:", response4.status_code)
  
    giriş()
    for index in sec_item:
     list.select_clear(index)

buton2 = tk.Button(pencere, text="EKLE",command=lambda:ekle() )
buton2.pack()
buton2.config(bg="pink")





def sil():
    
    toplam2=[]
    
    sec_item = list.curselection()
    if sec_item:
        sec_ids = []
        for l in sec_item:
            sec = list.get(l)
            sec_id = sec.split(' |||| ')[0].strip()
            sec_ids.append(int(sec_id)) 

        sec_ids = [int(sec_id) for sec_id in sec_ids] 
        toplam2=(int_personal_area_idss)
        print("toplam2" , str (toplam2))

        for sec_id in sec_ids:

            if sec_id in toplam2:
                toplam2.remove(sec_id)
                eklenenler.remove(sec_id)
                print("güncel id1 ", str(toplam2))
           
            else:
                messagebox.showinfo("HATA", "Seçtiğiniz areaya kayıtlı değilsiniz!!!")


        sec_idsss = ', '.join(map(str, sec_ids))
        label5.config(text="Silinen ID'ler: " + sec_idsss)
    else:
        label5.config(text="Hiçbir ID seçilmedi.")

    
    Body2 = {
                     "area": 
                                toplam2
                              
                       
                  
                 }
    response5 = requests.patch(url4 + str(personal_id) + '/', json=Body2, headers=headers)
    
    

    
    if response5.status_code == 200:
          data3 = response5.json()
          print("Güncellenmiş veri:", data3)
    elif response5.status_code == 404:
          print("Kaynak bulunamadı.")
    else:
          print("API isteği başarısız. HTTP Hata Kodu:", response5.status_code)
    

    
    giriş()
    for index in sec_item:
     list.select_clear(index)

buton3 = tk.Button(pencere, text="SİL",command=lambda:sil())
buton3.pack()
buton3.config(bg="pink")

pencere.mainloop()
