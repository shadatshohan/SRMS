from os import stat
from tkinter import *
import sqlite3
from PIL import Image,ImageTk
from tkinter import ttk,messagebox

class StudentClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Result Management System | Student")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #title
        title=Label(self.root,text="Manage Student Details",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=10,y=15,width=1180,height=35)
        #variables
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_contact=StringVar()
        self.var_address=StringVar()
        self.var_course=StringVar()
        self.var_adate=StringVar()
        self.var_state=StringVar()
        self.var_city=StringVar()
        self.var_pin=StringVar()
        self.var_search=StringVar()
        #label names
        lbl_roll=Label(self.root,text="Roll",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=60)
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=100)
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=140)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=180)
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=260)

        lbl_state=Label(self.root,text="State",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=220)
        txt_state=Entry(self.root,textvariable=self.var_state,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=220,width=200)

        lbl_city=Label(self.root,text="City",font=("goudy old style",15,"bold"),bg="white").place(x=310,y=220)
        txt_city=Entry(self.root,textvariable=self.var_city,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=380,y=220,width=100)
        # lbl_pin=Label(self.root,text="Pin",font=("goudy old style",15,"bold"),bg="white").place(x=500,y=220)
        # entry_pin=Label(self.root,textvariable=self.var_pin,font=("goudy old style",15,"bold"),bg="white").place(x=560,y=220)
        #entry
        self.txt_roll=Entry(self.root,textvariable=self.var_roll,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_roll.place(x=150,y=60,width=200)
        self.txt_address=Entry(self.root,textvariable=self.var_address,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_address.place(x=150,y=260,width=200)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=100,width=200)
        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=140,width=200)
        self.txt_gender=ttk.Combobox(self.root,values=("Select","Male","Female","Other"),textvariable=self.var_gender,state="readonly",justify=CENTER,font=("goudy old style",15))
        self.txt_gender.place(x=150,y=180,width=200)
        self.txt_gender.current(0)

        #column2
        # lbl_dob=Label(self.root,text="dob",font=("goudy old style",15,"bold"),bg="white").place(x=360,y=60)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15,"bold"),bg="white").place(x=360,y=100)
        lbl_admission=Label(self.root,text="admission",font=("goudy old style",15,"bold"),bg="white").place(x=360,y=140)
        lbl_course=Label(self.root,text="Course",font=("goudy old style",15,"bold"),bg="white").place(x=360,y=180)

        #entry2
        self.course_list=[]
        self.fetch_course()
        # txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=480,y=100,width=200)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=480,y=140,width=200)
        txt_admission=Entry(self.root,textvariable=self.var_adate,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=480,y=100,width=200)
        self.txt_course=ttk.Combobox(self.root,values=self.course_list,textvariable=self.var_course,state="readonly",justify=CENTER,font=("goudy old style",15))
        self.txt_course.place(x=480,y=180,width=200)
        self.txt_course.set("Select")
        #buttons
        self.btn_add=Button(self.root,command=self.add,text="Save",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2")
        self.btn_add.place(x=150,y=400,width=110,height=40)
        self.btn_update=Button(self.root,command=self.update,text="Update",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2")
        self.btn_update.place(x=270,y=400,width=110,height=40)
        self.btn_delete=Button(self.root,command=self.delete,text="Delete",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2")
        self.btn_delete.place(x=390,y=400,width=110,height=40)
        self.btn_clear=Button(self.root,command=self.clear,text="Clear",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2")
        self.btn_clear.place(x=510,y=400,width=110,height=40)
        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=1070,y=60,width=120,height=28)

        #search panel
        lbl_search=Label(self.root,text="Roll No:",font=("goudy old style",15,"bold"),bg="white").place(x=720,y=60)
        txt_search=Entry(self.root,textvariable=self.var_search,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=870,y=60,width=180)

        #content
        self.C_Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.C_Frame.place(x=720,y=100,width=470,height=340)
        scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
        scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
        self.CourseTable=ttk.Treeview(self.C_Frame,columns=("roll","name","email","gender","contact","admission","course","state","city","address"),xscrollcommand=scrollx.set,
                                      yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        self.CourseTable.heading("roll",text="Roll")
        self.CourseTable.heading("name",text="Name")
        self.CourseTable.heading("email",text="Email")
        self.CourseTable.heading("gender",text="Gender")
        self.CourseTable.heading("contact",text="Contact")
        self.CourseTable.heading("admission",text="Admission")
        self.CourseTable.heading("course",text="Course")
        self.CourseTable.heading("state",text="State")
        self.CourseTable.heading("city",text="City")
        self.CourseTable.heading("address",text="Address")
        self.CourseTable["show"]='headings'

        self.CourseTable.column("roll",width=100)
        self.CourseTable.column("name",width=100)
        self.CourseTable.column("email",width=100)
        self.CourseTable.column("gender",width=100)
        self.CourseTable.column("contact",width=100)
        self.CourseTable.column("admission",width=100)
        self.CourseTable.column("course",width=100)
        self.CourseTable.column("state",width=100)
        self.CourseTable.column("city",width=100)
        self.CourseTable.column("address",width=100)

        self.CourseTable.pack(fill=BOTH,expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


    def add(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            if self.var_roll.get()=="":
                messagebox.showerror("Error","Student roll should be required",parent=self.root)
            else:
                cur.execute("Select * from student where roll=?",(self.var_roll.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Roll number already present",parent=self.root)
                else:
                    cur.execute("Insert into student (roll,name,email,gender,contact,admission,course,state,city,address) values(?,?,?,?,?,?,?,?,?,?)",
                      (self.var_roll.get(),
                       self.var_name.get(),
                       self.var_email.get(),
                       self.var_gender.get(),
                       self.var_contact.get(),
                       self.var_adate.get(),
                       self.var_course.get(),
                       self.var_state.get(),
                       self.var_city.get(),
                       self.var_address.get()))
                    con.commit()
                    messagebox.showinfo("Success","Student added successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"error due to {str(ex)}")
    
    def show(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from student")
            rows=cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}")
    
    def get_data(self,ev):
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content['values']
        self.var_roll.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_adate.set(row[5]),
        self.var_course.set(row[6]),
        self.var_state.set(row[7]),
        self.var_city.set(row[8]),
        self.var_address.set(row[9])
        self.var_course.set(row[10])

    def update(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           if self.var_roll.get()=="":
               messagebox.showerror("Error","Student name must be required",parent=self.root)
           else:
               cur.execute("Select * from student where roll=?",(self.var_roll.get(),))
               row=cur.fetchone()
               if row==None:
                   messagebox.showerror("Error","Invalid student Id",parent=self.root)
               else:
                   cur.execute("Update student set name=?,email=?,gender=?,contact=?,admission=?,course=?,state=?,city=?,address=? where roll=?",(
                       self.var_name.get(),
                       self.var_email.get(),
                       self.var_gender.get(),
                       self.var_contact.get(),
                       self.var_adate.get(),
                       self.var_course.get(),
                       self.var_state.get(),
                       self.var_city.get(),
                       self.var_address.get(),
                       self.var_roll.get(),
                   ))
                   con.commit()
                   messagebox.showinfo("Success","Updated successfully",parent=self.root)
                   self.show()
       except Exception as ex:
           messagebox.showerror("Error",f"error due to:{str(ex)}",parent=self.root)
   

    def delete(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           if self.var_roll.get()=="":
               messagebox.showerror("Error","Student ID must be needed",parent=self.root)
           else:
               cur.execute("Select * from student where roll=?",(self.var_roll.get(),))
               row=cur.fetchone()
               print(row)
               if row==None:
                   messagebox.showerror("Error","Invalid student ID",parent=self.root)
               else:
                   op=messagebox.askyesno("Confirm","Are you sure you want to delete?",parent=self.root)
                   if op==True:
                       cur.execute("Delete from student where roll=?",(self.var_roll.get(),))
                       con.commit()
                       messagebox.showinfo("Success","Student deleted successfully",parent=self.root)
                       self.clear()
       except Exception as ex:
           messagebox.showerror("Error",f"error due to{str(ex)}",parent=self.root)
    

    def clear(self):
        self.var_roll.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set(""),
        self.var_contact.set(""),
        self.var_adate.set(""),
        self.var_course.set(""),
        self.var_state.set(""),
        self.var_city.set(""),
        self.var_address.set("")
        self.var_course.set("")
        self.show()

   #search
    def search(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           cur.execute("Select * from student where roll=?",(self.var_search.get(),))
           row=cur.fetchone()
           if row!=None:
               self.CourseTable.delete(*self.CourseTable.get_children())
               self.CourseTable.insert('',END,values=row)
           else:
               messagebox.showerror("Error","No record found",parent=self.root)
       except Exception as ex:
           messagebox.showerror("Error",f"error due to {str(ex)}",parent=self.root)
    
    def fetch_course(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from course")
            rows=cur.fetchall()
            if len(rows)>0:
                for row in rows:
                    self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}")

