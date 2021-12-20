from os import stat
from tkinter import *
import sqlite3
from PIL import Image,ImageTk
from tkinter import ttk,messagebox

class ReportClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Result Management System | Result")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #title
        title=Label(self.root,text="View Student Results",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=10,y=15,width=1180,height=50)
        #variables
        self.var_search=StringVar()
        self.var_id=""
        #labels
        lbl_search=Label(self.root,text="Search By Roll No.",font=("goudy old style",15,"bold"),bg="white").place(x=280,y=100)
        txt_search=Entry(self.root,textvariable=self.var_search,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=520,y=100,width=150)
        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=680,y=100,width=100,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15),bg="gray",fg="white",cursor="hand2").place(x=800,y=100,width=100,height=35)

        #lables
        lbl_roll=Label(self.root,text="Roll",font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white").place(x=150,y=230,width=150,height=50)
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white").place(x=300,y=230,width=150,height=50)
        lbl_course=Label(self.root,text="Course",font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white").place(x=450,y=230,width=150,height=50)
        lbl_marks=Label(self.root,text="Marks",font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white").place(x=600,y=230,width=150,height=50)
        lbl_fullmarks=Label(self.root,text="Full Marks",font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white").place(x=750,y=230,width=150,height=50)
        lbl_per=Label(self.root,text="Percentage",font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white").place(x=900,y=230,width=150,height=50)

        # anslabels
        self.roll=Label(self.root,font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white")
        self.roll.place(x=150,y=280,width=150,height=50)
        self.name=Label(self.root,font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white")
        self.name.place(x=300,y=280,width=150,height=50)
        self.course=Label(self.root,font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white")
        self.course.place(x=450,y=280,width=150,height=50)
        self.marks=Label(self.root,font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white")
        self.marks.place(x=600,y=280,width=150,height=50)
        self.fullmarks=Label(self.root,font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white")
        self.fullmarks.place(x=750,y=280,width=150,height=50)
        self.per=Label(self.root,font=("goudy old style",15,"bold"),bd=2,relief=GROOVE,bg="white")
        self.per.place(x=900,y=280,width=150,height=50)

        #button delete
        btn_delete=Button(self.root,command=self.delete,text="Delete",font=("goudy old style",15,"bold"),bg="red",fg="white",cursor="hand2").place(x=500,y=350,width=150,height=35)
    def search(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           if self.var_search.get()=="":
               messagebox.showerror("Error","Roll number should be required",parent=self.root)
           else:
               cur.execute("Select * from resulting where roll=?",(self.var_search.get(),))
               row=cur.fetchone()
               if row!=None:
                   self.var_id=row[0]
                   self.roll.config(text=row[1])
                   self.name.config(text=row[2])
                   self.course.config(text=row[3])
                   self.marks.config(text=row[4])
                   self.fullmarks.config(text=row[5])
                   self.per.config(text=row[6])
               else:
                   messagebox.showerror("Error","No record found",parent=self.root)
       except Exception as ex:
           messagebox.showerror("Error",f"error due to {str(ex)}",parent=self.root)
    def clear(self):
        self.var_id("")
        self.roll.config("")
        self.name.config("")
        self.course.config("")
        self.marks.config("")
        self.fullmarks.config("")
        self.per.config("")
    

    def delete(self):
       con=sqlite3.connect(database=r'SRM.db')
       cur=con.cursor()
       try:
           if self.var_id=="":
               messagebox.showerror("Error","Search student result first",parent=self.root)
           else:
               cur.execute("Select * from resulting where rid=?",(self.var_id,))
               row=cur.fetchone()
               if row==None:
                   messagebox.showerror("Error","Invalid course ID",parent=self.root)
               else:
                   op=messagebox.askyesno("Confirm","Are you sure you want to delete?",parent=self.root)
                   if op==True:
                       cur.execute("Delete from resulting where rid=?",(self.var_id,))
                       con.commit()
                       messagebox.showinfo("Success","Result deleted successfully",parent=self.root)
                       self.clear()
       except Exception as ex:
           messagebox.showerror("Error",f"error due to{str(ex)}",parent=self.root)
if __name__=="__main__":
    root=Tk()
    obj=ReportClass(root)
    root.mainloop()