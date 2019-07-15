from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import ImageTk, Image
import bs4
import requests
import datetime
import socket
import requests
import cx_Oracle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2

root = Tk()
root.title("Welcome Screen")
root.geometry("1200x1000+200+10")
root.iconbitmap('welcome.ico')
#root.configure(background='blue')

dt = datetime.datetime.now().date()
lblTim = Label(root,text = "Date: " + str(dt), fg = 'grey', font=("Times New Roman",16,'bold'),relief=RAISED)
lblTim.pack(padx=0,pady=0,side=TOP)

#for getting location Weather
try:
	socket.create_connection( ("www.google.com",80))
	res = requests.get("https://ipinfo.io/")
	#print("Sucessful",res)
	data = res.json()   #converted data in json and stored it into variable
	#print(data)
	city = data['city']
	#print("Your current city: ",city)
	city_1 = city
	socket.create_connection(("www.google.com",80))
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_1
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address = a1 + a2 + a3
	res1 = requests.get(api_address)
	#print(res1)
	wdata = res1.json()
	#print(wdata)
	main = wdata['main']
	#print(main)
	temp = main['temp']
	lbltem = Label(root, text = "Current City " + city_1 + " - Temperature: "+ str(temp),fg='brown',font=("Times New Roman",18))
	#print("Temperaure: ", temp)
except OSError:
	print("Check internet")
lbltem.pack()


explanation_1 = 'Quote of the Day'
lblDis = Label(root, text=explanation_1,fg='red',font=("Times New Roman",24,'bold','underline'))
lblDis.pack(pady=10)

#for quote of the day
res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup = bs4.BeautifulSoup(res.text,'lxml')
quote = soup.find('img',{"class":"p-qotd"})
print("Quote: ",quote)
print(quote['alt'])
print("https://www.brainyquote.com/" + quote['data-img-url'])
im = "https://www.brainyquote.com/" + quote['data-img-url']
r= requests.get(im)
with open("quote.jpg",'wb') as f:  # quote is the name of img jo download hoga uska
	f.write(r.content)

# for resizing and displaying on tkinter screen
img = Image.open("quote.jpg")
img = img.resize((1000,600), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(root, image = img)
panel.pack(side = "top", expand = "yes")

'''
# display the quote in label
explanation_2 = quote['alt']
lblDis1 = Label(root, text=explanation_2,font=("Times New Roman",24,'bold'))
lblDis1.pack()
'''
def sl():
        root_op.deiconify()
        root.withdraw()
root.after(10000,sl)

#for new operation window
root_op = Toplevel(root)
root_op.title("Student-Management-System")
root_op.geometry("400x400+200+200")
root_op.iconbitmap('stu.ico')
root_op.configure(background='dark grey')
root_op.withdraw()

def f1():                       #for add button
	adSt.deiconify()  # window upar ane ke lie
	root_op.withdraw()	   # window back per rahane ke lie

def f3():                       # for view button
	viSt.deiconify()
	root_op.withdraw()
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg = ""
		for d in data:
			msg = msg + "Roll no: " + str(d[0])+ " | " + " Name: " + str(d[1])+ " | " + " Marks: " + str(d[2]) + "\n"
		stData.insert(INSERT,msg)
	except cx_Oracle.DatabaseError as e:
		msgbox.showinfo("Some Issue ", e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

def f6():                       # for update button
    upDt.deiconify()
    root.withdraw()

def f8():                       # for delete button
        deLt.deiconify()
        root_op.withdraw()

def f11():                   # for graph button
        con = None
        cursor = None
        try:
                con = cx_Oracle.connect("system/abc123")
                cursor = con.cursor()
                sql = "select * from student"
                cursor.execute(sql)
                data = cursor.fetchall()
                name_List = []
                marks_List = []
                for d in data:
                        name_List.append(d[1])
                        marks_List.append(d[2])
                plt.bar(name_List,marks_List)
                plt.title("Student Database")
                plt.xlabel('Names')
                plt.ylabel('Marks')
                plt.legend(loc="upper right", shadow=True)
                plt.show()
        except cx_Oracle.DatabaseError as e:
                msgbox.showinfo("Some Issue ", e)
        finally:
                if cursor is not None:
                        cursor.close()
                if con is not None:
                        con.close()


btnAdd = Button(root_op, text = "Add", font=("arial",16,"bold"),width = 10, command=f1)
btnView = Button(root_op, text = "View", font=("arial",16,"bold"),width = 10, command=f3)
btnUpdate = Button(root_op, text = "Update", font=("arial",16,"bold"),width = 10, command=f6)
btnDelete = Button(root_op, text = "Delete", font=("arial",16,"bold"),width = 10,command=f8)
btnGraph = Button(root_op, text = "Graph", font=("arial",16,"bold"),width = 10,command=f11)
btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnGraph.pack(pady = 10)



# for new add insert window
adSt = Toplevel(root_op)
adSt.title("Add Student")
adSt.geometry("400x400+200+200")
adSt.iconbitmap('ad.ico')
adSt.withdraw()


def f2():               # for back button
	root_op.deiconify()
	adSt.withdraw()

def f5():
        con = None
        cursor = None
        try:
                con = cx_Oracle.connect("system/abc123")
                srno = entAddRno.get()
                if srno.isdigit() and int(srno) > 0:
                        rno = int(srno)
                else:
                        messagebox.showerror("Mistake", "Invalid Input")
                        entAddRno.focus()
                        return
                sname = entAddName.get()
                if sname.isalpha():
                        name = sname
                else:
                        messagebox.showerror("Mistake", "Name contains only Alphabets")
                        entAddName.focus()
                        return		
                smarks = entAddMarks.get()
                if smarks.isdigit() and int(smarks) > 0 and int(smarks)< 100:
                        marks = int(smarks)
                else:
                        messagebox.showerror("Mistake", "Enter Valid Marks")
                        entAddRno.focus()
                        return
                cursor = con.cursor()
                sql = "insert into student values('%d','%s','%d')"
                args = (rno,name,marks)
                cursor.execute(sql % args)
                con.commit()
                msg = str(cursor.rowcount) + " Row inserted: "
                messagebox.showinfo("Success ", msg)
        except cx_Oracle.DatabaseError as e:
                con.rollback()
                messagebox.showerror('Failure ', e)
        finally:
                if cursor is not None:
                        cursor.close()
                if con is not None:
                        con.close()

lblAddRno = Label(adSt, text="Enter Roll No: ")
lblAddName = Label(adSt, text="Enter Name: ")
lblAddMarks = Label(adSt, text="Marks: ")
entAddRno = Entry(adSt, bd = 5 )
entAddName = Entry(adSt, bd = 5 )
entAddMarks = Entry(adSt, bd = 5 )
btnAddSave = Button(adSt, text="Save",command=f5)
btnAddBack = Button(adSt, text="Back",command=f2)
lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddMarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

# for view window
viSt = Toplevel(root)           
viSt.title("View Student")
viSt.geometry("400x400+200+200")
viSt.withdraw()
viSt.iconbitmap('vie.ico')
viSt.withdraw()

def f4():               # for going back to main operation window
        root_op.deiconify()
        viSt.withdraw()


stData = scrolledtext.ScrolledText(viSt, width=45, height=5)
btnViewBack = Button(viSt, text="Back",command=f4)

stData.pack(pady=10)
btnViewBack.pack(pady=10)


# for update window
upDt = Toplevel(root_op)
upDt.title("Update Student Data")
upDt.geometry("400x400+200+200")
upDt.iconbitmap('up.ico')
upDt.withdraw()


def f12():
    root_op.deiconify()
    upDt.withdraw()

def f7():
        con = None
        cursor = None
        try:
                con = cx_Oracle.connect("system/abc123")
                srno = entupdateRno.get()
                if srno.isdigit() and int(srno) > 0:
                        rno = int(srno)
                else:
                        messagebox.showerror("Mistake", "Invalid Input")
                        entAddRno.focus()
                        return
                sname = entupdateName.get()
                if sname.isalpha():
                        name = sname
                else:
                        messagebox.showerror("Mistake", "Name contains only Alphabets")
                        entAddName.focus()
                        return
                smarks = entupdateMarks.get()
                if smarks.isdigit() and int(smarks) > 0 and int(smarks)< 100:
                        marks = int(smarks)
                else:
                        messagebox.showerror("Mistake", "Enter Valid Marks")
                        entAddRno.focus()
                        return
                cursor = con.cursor()
                sql = "update student set NAME = '%s', MARKS='%d' where RNO='%d'"
                args = (name,marks,rno)
                cursor.execute(sql%args)
                con.commit()
                msg = str(cursor.rowcount) + 'Row Updated...'
                messagebox.showinfo("Succesfully " + msg)
        except cx_Oracle.DatabaseError as e:
                con.rollback()
                messagebox.showerror('Failure', e)
        finally:
                if cursor is not None:
                        cursor.close()
                if con is not None:
                        con.close()

lblupdateRno = Label(upDt, text="Enter New Roll No: ")
lblupdateName = Label(upDt, text="Enter New Name: ")
lblupdateMarks = Label(upDt, text="New Marks: ")
entupdateRno = Entry(upDt, bd = 5 )
entupdateName = Entry(upDt, bd = 5 )
entupdateMarks = Entry(upDt, bd = 5 )
btnupdateSave = Button(upDt, text="Save",command=f7)
btnupdateBack = Button(upDt, text="Back",command=f12)
lblupdateRno.pack(pady=10)
entupdateRno.pack(pady=10)
lblupdateName.pack(pady=10)
entupdateName.pack(pady=10)
lblupdateMarks.pack(pady=10)
entupdateMarks.pack(pady=10)
btnupdateSave.pack(pady=10)
btnupdateBack.pack(pady=10)

# for delete window
deLt = Toplevel(root_op)
deLt.title("For Deleting a Student Data")
deLt.geometry("400x400+200+200")
deLt.iconbitmap('del.ico')
deLt.withdraw()

def f9():
        root_op.deiconify()
        deLt.withdraw()

def f10():
        con = None
        cursor = None
        try:
                con = cx_Oracle.connect("system/abc123")
                srno = entdeleteRno.get()
                if srno.isdigit() and int(srno)>0:
                        rno = int(srno)
                else:
                     messagebox.showerror("Mistake", "Invalid Input")
                     entdeleteRno.focus()
                     return
                
                cursor = con.cursor()
                sql = "delete from student where RNO='%d'"
                args = (rno)
                cursor.execute(sql%args)
                con.commit()
                msg = str(cursor.rowcount) + 'Row Deleted...'
                messagebox.showinfo("Successfully " +  '', msg)
        except cx_Oracle.DatabaseError as e:
                con.rollback()
                messagebox.showerror('Failure', e)
        finally:
                if cursor is not None:
                        cursor.close()
                if con is not None:
                        con.close()

lbldeleteRno = Label(deLt, text="Enter Roll No to delete Student Data: ")
entdeleteRno = Entry(deLt, bd = 5 )
btndeleteSave = Button(deLt, text="Delete",command=f10)
btndeleteBack = Button(deLt, text="Back",command=f9)
lbldeleteRno.pack(pady=10)
entdeleteRno.pack(pady=10)
btndeleteSave.pack(pady=10)
btndeleteBack.pack(pady=10)

root.mainloop()
