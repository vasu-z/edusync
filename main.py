import tkinter as tk
from tkinter import ttk , messagebox



class Student:
      def __init__( self ):
            self.window   =     tk.Tk()
            self.window.title(   "Student Panel" )
            self.window.geometry("1440x1024" )
            self.window.configure(bg= "white")
            self.window.resizable( False , False )

            self.data  = {}
            self.marks    =   {}

            self.body( )
            self.make_sidebar( )
            self.goto("Dashboard" )

            self.window.mainloop()



      def make_sidebar( self ):
            left = tk.Frame( self.window , bg="#1E293B"   )
            left.place( x=0 , y=0, width=240 , height=1024 )

            tk.Label( left, text="StudentApp" , fg="white" , bg="#1E293B" ,
                      font=( "Poppins" , 20 , "bold" )).pack(pady=(40,25) , anchor="w" , padx=20)

            menu_items = [ "Dashboard" , "Add New" , "Add Marks" , "View Marks" , "Exit" ]
            self.all_btns = {}
            for m in menu_items:
                  bb = tk.Button( left , text = m , fg="white" , bg="#1E293B" ,
                          font=("Poppins" ,13) , relief= "flat" , anchor="w" , padx=30 ,
                          activebackground="#3B82F6" , activeforeground="white" ,
                          command= lambda x = m : self.goto( x ))
                  bb.pack( fill = "x" , pady= 4 )
                  self.all_btns[ m ] = bb



      def body( self ):
            self.main = tk.Frame( self.window , bg="white"  )
            self.main.place( x=240 , y=0 , width=1200 , height=1024 )


      def clean( self ):
            for w in self.main.winfo_children():
                  w.destroy()


      def goto( self , screen ):
            if hasattr( self , "on" ):
                  self.all_btns[ self.on ].configure(bg="#1E293B"  )
            self.all_btns[screen].configure( bg="#3B82F6" )
            self.on = screen
            self.clean()

            if screen == "Dashboard":
                  self.show_home()
            elif screen == "Add New":
                  self.add_page( )
            elif screen == "Add Marks":
                  self.marks_page( )
            elif screen == "View Marks":
                  self.report( )
            elif screen == "Exit":
                  self.window.destroy()



      def show_home(self):
            tk.Label( self.main , text="Student Zone" , font=("Poppins", 19, "bold") , bg="white" ).place( x=30 , y=30 )

            stats = [
                  ( len( self.data ) , "Total Students" ),
                  ( "-" , "Class Count" ),
                  ( "-" , "Subjects" ),
                  ( sum( len(v) for v in self.marks.values() ) , "Total Marks" )
            ]

            for i , (v , l) in enumerate( stats ):
                  card = tk.Frame( self.main , bg="#3B82F6" , width=220 , height=100 )
                  card.place( x=30 + i*240 , y=80 )
                  tk.Label( card , text= v , font=("Poppins",20,"bold"), bg="#3B82F6" , fg="white" ).place( x=20 , y=10 )
                  tk.Label( card , text= l , font=("Poppins",12), bg="#3B82F6", fg="white" ).place( x=20 , y=55 )



      def add_page( self ):
            tk.Label( self.main , text="Add Student Info" , font=("Poppins", 16 , "bold" ), bg="white" ).place( x=30 , y=30 )

            fields = [ "ID" , "Name" , "DOB" , "Gender" , "Address" ]
            self.inputs = { }
            y = 80
            for f in fields:
                  tk.Label( self.main , text=f , font=("Poppins",12) , bg="white" ).place( x=30 , y=y )
                  ent = tk.Entry( self.main , font=("Poppins",12) , width=40 , bd=1 , relief="solid" )
                  ent.place( x=180 , y=y )
                  self.inputs[ f ] = ent
                  y += 50

            tk.Button( self.main , text="Save" , font=("Poppins",12) ,
                  bg="#3B82F6" , fg="white" , command=self.save_student ).place( x=180 , y= y + 10 )



      def save_student( self ):
            dat = { k: v.get().strip() for k , v in self.inputs.items() }
            sid = dat[ "ID" ]

            if sid == "":
                  return messagebox.showwarning( "Missing" , "Need ID first" )
            if sid in self.data:
                  return messagebox.showwarning( "Oops" , "ID already used" )

            self.data[ sid ] = {
                  "name": dat[ "Name" ],
                  "dob": dat[ "DOB" ],
                  "gender": dat[ "Gender" ],
                  "address": dat[ "Address" ]
            }

            messagebox.showinfo( "Saved" , f"{sid} added!" )

            for x in self.inputs.values():
                  x.delete( 0 , tk.END )



      def marks_page( self ):
            tk.Label( self.main , text="Enter Marks" , font=("Poppins", 16 , "bold") , bg="white" ).place( x=30 , y=30 )

            tk.Label( self.main , text="Student ID" , font=("Poppins",12) , bg="white" ).place( x=30 , y=80 )
            self.combo = ttk.Combobox( self.main , values=list( self.data.keys() ) , width=37 )
            self.combo.place( x=180 , y=80 )

            tk.Label( self.main , text="Subject" , font=("Poppins",12) , bg="white" ).place( x=30 , y=130 )
            self.sub = tk.Entry( self.main , font=("Poppins",12) , width=40 , bd=1 , relief="solid" )
            self.sub.place( x=180 , y=130 )

            tk.Label( self.main , text="Marks" , font=("Poppins",12) , bg="white" ).place( x=30 , y=180 )
            self.markz = tk.Entry( self.main , font=("Poppins",12) , width=40 , bd=1 , relief="solid" )
            self.markz.place( x=180 , y=180 )

            tk.Button( self.main , text="Add" , font=("Poppins",12) ,
                       bg="#3B82F6" , fg="white" , command=self.save_marks ).place( x=180 , y=230 )



      def save_marks( self ):
            sid = self.combo.get().strip()
            s = self.sub.get().strip()
            m = self.markz.get().strip()

            if sid not in self.data:
                  return messagebox.showwarning( "Wrong ID bro" , "That ID doesn't exist." )

            if not s or not m.isdigit():
                  return messagebox.showwarning( "Uhh" , "Type subject and marks (as numbers)" )

            if sid not in self.marks:
                  self.marks[ sid ] = []

            self.marks[ sid ].append( (s, int(m)) )
            messagebox.showinfo( "Done" , f"{s} → {m} added." )

            self.sub.delete( 0 , tk.END )
            self.markz.delete( 0 , tk.END )



      def report( self ):
            tk.Label( self.main , text="Student Reports" , font=("Poppins",16,"bold") , bg="white" ).place( x=30 , y=30 )

            cols = ("ID" , "Name" , "Subjects" , "Average")
            view = ttk.Treeview( self.main , columns=cols , show="headings" )

            for c in cols:
                  view.heading( c , text=c )
                  view.column( c , width=180 )

            for sid , val in self.data.items():
                  data_list = self.marks.get( sid , [] )
                  subz = ", ".join( s for s, _ in data_list ) if data_list else "-"
                  avg = f"{sum( m for _, m in data_list ) / len( data_list ):.1f}" if data_list else "-"
                  view.insert( "" , "end" , values=( sid , val["name"] , subz , avg ) )

            view.place( x=30 , y=80 , width=800 , height=400 )



if __name__ == "__main__":
      Student( )
