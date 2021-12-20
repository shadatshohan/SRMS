from os import stat
from tkinter import *
import sqlite3
from PIL import Image,ImageTk
from tkinter import ttk,messagebox

class ResultClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Result Management System | Result")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #title
        title=Label(self.root,text="Add Student Results",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=10,y=15,width=1180,height=50)
        #variables
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_course=StringVar()
        self.var_marks=StringVar()
        self.var_fullmarks=StringVar()
        #labels
        lbl_select=Label(self.root,text="Select Roll",font=("goudy old style",15,"bold"),bg="white").place(x=50,y=100)
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15,"bold"),bg="white").place(x=50,y=160)
        lbl_course=Label(self.root,text="Course",font=("goudy old style",15,"bold"),bg="white").place(x=50,y=220)
        lbl_marks_ob=Label(self.root,text="Marks",font=("goudy old style",15,"bold"),bg="white").place(x=50,y=280)
        lbl_full_marks=Label(self.root,text="Full marks",font=("goudy old style",15,"bold"),bg="white").place(x=50,y=340)

        #entry
        self.roll_list=[]
        self.fetch_roll()
        self.txt_student=ttk.Combobox(self.root,values=self.roll_list,textvariable=self.var_roll,state="readonly",justify=CENTER,font=("goudy old style",15))
        self.txt_student.place(x=280,y=100,width=200)
        self.txt_student.set("Select")

        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=100,width=120,height=28)

        #entrymain
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20,"bold"),bg="lightyellow",state='readonly').place(x=280,y=160,width=320)
        txt_course=Entry(self.root,textvariable=self.var_course,font=("goudy old style",20,"bold"),bg="lightyellow",state='readonly').place(x=280,y=220,width=320)
        txt_marks=Entry(self.root,textvariable=self.var_marks,font=("goudy old style",20,"bold"),bg="lightyellow").place(x=280,y=280,width=320)
        txt_fullmarks=Entry(self.root,textvariable=self.var_fullmarks,font=("goudy old style",20,"bold"),bg="lightyellow").place(x=280,y=340,width=320)

        #buttons
        btn_add=Button(self.root,text="Add",command=self.add,font=("times new roman",15),bg="lightgreen",activebackground="lightgreen",cursor="hand2").place(x=300,y=420,width=120,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15),bg="lightgreen",activebackground="lightgray",cursor="hand2").place(x=430,y=420,width=120,height=35)

        #image
        self.bg_img=Image.open("images/result.jpg")
        self.bg_img=self.bg_img.resize((500,500),Image.ANTIALIAS)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)
        self.lbl_img=Label(self.root,image=self.bg_img).place(x=630,y=100)

    def fetch_roll(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            cur.execute("Select roll from student")
            rows=cur.fetchall()
            if len(rows)>0:
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}")
    
    def search(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           cur.execute("Select name,course from student where roll=?",(self.var_roll.get(),))
           row=cur.fetchone()
           if row!=None:
               self.var_name.set(row[0])
               self.var_course.set(row[1])
           else:
               messagebox.showerror("Error","No record found",parent=self.root)
       except Exception as ex:
           messagebox.showerror("Error",f"error due to {str(ex)}",parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r'SRM.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","please search student record",parent=self.root)
            else:
                cur.execute("Select * from resulting where roll=? and course=?",(self.var_roll.get(),self.var_course.get()))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Result already present",parent=self.root)
                else:
                    per=(int(self.var_marks.get()*100))/(int(self.var_fullmarks.get()))
                    cur.execute("Insert into resulting(roll,name,course,marks,full_marks,per) values(?,?,?,?,?,?)",
                      (self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_fullmarks.get(),
                        str(per)
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Result added successfully",parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"error due to {str(ex)}")
    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_fullmarks.set("")

if __name__=="__main__":
    root=Tk()
    obj=ResultClass(root)
    root.mainloop()