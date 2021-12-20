from os import stat
from tkinter import *
import sqlite3
from PIL import Image,ImageTk
from tkinter import ttk,messagebox

class CourseClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Result Management System | Course")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #title
        title=Label(self.root,text="Manage Course Details",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=10,y=15,width=1180,height=35)
        #variables
        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()
        self.var_search=StringVar()
        #label names
        lbl_courseName=Label(self.root,text="Course Name",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=60)
        lbl_duration=Label(self.root,text="Duration",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=100)
        lbl_charges=Label(self.root,text="Charges",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=140)
        lbl_description=Label(self.root,text="Description",font=("goudy old style",15,"bold"),bg="white").place(x=10,y=180)

        #entry
        self.txt_coursename=Entry(self.root,textvariable=self.var_course,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_coursename.place(x=150,y=60,width=200)
        txt_duration=Entry(self.root,textvariable=self.var_duration,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=100,width=200)
        txt_charges=Entry(self.root,textvariable=self.var_charges,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=140,width=200)
        self.txt_description=Text(self.root,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_description.place(x=150,y=180,width=500,height=130)

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
        lbl_search=Label(self.root,text="Course Name",font=("goudy old style",15,"bold"),bg="white").place(x=720,y=60)
        txt_search=Entry(self.root,textvariable=self.var_search,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=870,y=60,width=180)

        #content
        self.C_Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.C_Frame.place(x=720,y=100,width=470,height=340)
        scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
        scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
        self.CourseTable=ttk.Treeview(self.C_Frame,columns=("cid","name","duration","charges","description"),xscrollcommand=scrollx.set,
                                      yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        self.CourseTable.heading("cid",text="Course ID")
        self.CourseTable.heading("name",text="Name")
        self.CourseTable.heading("duration",text="Duration")
        self.CourseTable.heading("charges",text="Changes")
        self.CourseTable.heading("description",text="Description")
        self.CourseTable["show"]='headings'

        self.CourseTable.column("cid",width=100)
        self.CourseTable.column("name",width=100)
        self.CourseTable.column("duration",width=100)
        self.CourseTable.column("charges",width=100)
        self.CourseTable.column("description",width=100)

        self.CourseTable.pack(fill=BOTH,expand=1)
        self.CourseTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


    def add(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course name should be required",parent=self.root)
            else:
                cur.execute("Select * from course where name=?",(self.var_course.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Course name already present",parent=self.root)
                else:
                    cur.execute("Insert into course (name,duration,charges,description) values(?,?,?,?)",(self.var_course.get(),
                          self.var_duration.get(),self.var_charges.get(),self.txt_description.get("1.0",END)))
                    con.commit()
                    messagebox.showinfo("Success","Course added successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"error due to {str(ex)}")
    
    def show(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from course")
            rows=cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}")
    
    def get_data(self,ev):
        self.txt_coursename.config(state='readonly')
        r=self.CourseTable.focus()
        content=self.CourseTable.item(r)
        row=content['values']
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete('1.0',END)
        self.txt_description.insert(END,row[4])



    def update(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           if self.var_course.get()=="":
               messagebox.showerror("Error","Course name must be required",parent=self.root)
           else:
               cur.execute("Select * from course where name=?",(self.var_course.get(),))
               row=cur.fetchone()
               if row==None:
                   messagebox.showerror("Error","Invalid course Id",parent=self.root)
               else:
                   cur.execute("Update course set duration=?,charges=?,description=? where name=?",(
                       self.var_duration.get(),
                       self.var_charges.get(),
                       self.txt_description.get("1.0",END),
                       self.var_course.get(),
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
           if self.var_course.get()=="":
               messagebox.showerror("Error","Course ID must be needed",parent=self.root)
           else:
               cur.execute("Select * from course where name=?",(self.var_course.get(),))
               row=cur.fetchone()
               print(row)
               if row==None:
                   messagebox.showerror("Error","Invalid course ID",parent=self.root)
               else:
                   op=messagebox.askyesno("Confirm","Are you sure you want to delete?",parent=self.root)
                   if op==True:
                       cur.execute("Delete from course where name=?",(self.var_course.get(),))
                       con.commit()
                       messagebox.showinfo("Success","Course deleted successfully",parent=self.root)
                       self.clear()
       except Exception as ex:
           messagebox.showerror("Error",f"error due to{str(ex)}",parent=self.root)
    

    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0',END)
        self.txt_coursename.config(state=NORMAL)
        self.show()

   #search
    def search(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           cur.execute(f"Select * from course where name LIKE '%{self.var_search.get()}%'")
           rows=cur.fetchall()
           self.CourseTable.delete(*self.CourseTable.get_children())
           for row in rows:
               self.CourseTable.insert('',END,values=row)
       except Exception as ex:
           messagebox.showerror("Error",f"error due to {str(ex)}",parent=self.root)
