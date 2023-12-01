import customtkinter

from tkinter import *

class Control:

    def __init__(self, title, render = None) -> None:
        self.render = render
        self.root = Tk()
        self.height = self.root.winfo_screenheight()
        self.width  = self.root.winfo_screenwidth()
        # self.height = 400 # TODO
        # self.width  = 400 # TODO
        self.root.title(title)
        # self.root.geometry(f"{self.width}x{self.height}")
        self.run()
        self.root.mainloop() 

    def run(self):
        self.frames = [Frame(self.root)]
        self.frames[0].grid(row=0, column=0, sticky=N+S+E+W)
        self.gridmap = [[[0 for x in range(20)] for x in range(20)] for y in range(len(self.frames))]  
        self.varmap = [[[0 for x in range(20)] for x in range(20)] for y in range(len(self.frames))]
        self.addlabel(0,0,0, "Current transformation matrix:", cspan=3)
        self.addentry(0,1,0,None, None, None, None,default="1")
        self.addentry(0,1,1,None, None, None, None,default="0")
        self.addentry(0,1,2,None, None, None, None,default="0")
        self.addentry(0,2,0,None, None, None, None,default="0")
        self.addentry(0,2,1,None, None, None, None,default="1")
        self.addentry(0,2,2,None, None, None, None,default="0")
        self.addentry(0,3,0,None, None, None, None,default="0")
        self.addentry(0,3,1,None, None, None, None,default="0")
        self.addentry(0,3,2,None, None, None, None,default="1")
        self.varmap[0][1][0].trace_add("write", lambda *args: self.modify_animation_matrix(1,0))
        self.varmap[0][1][1].trace_add("write", lambda *args: self.modify_animation_matrix(1,1))
        self.varmap[0][1][2].trace_add("write", lambda *args: self.modify_animation_matrix(1,2))
        self.varmap[0][2][0].trace_add("write", lambda *args: self.modify_animation_matrix(2,0))
        self.varmap[0][2][1].trace_add("write", lambda *args: self.modify_animation_matrix(2,1))
        self.varmap[0][2][2].trace_add("write", lambda *args: self.modify_animation_matrix(2,2))
        self.varmap[0][3][0].trace_add("write", lambda *args: self.modify_animation_matrix(3,0))
        self.varmap[0][3][1].trace_add("write", lambda *args: self.modify_animation_matrix(3,1))
        self.varmap[0][3][2].trace_add("write", lambda *args: self.modify_animation_matrix(3,2))
        self.addlabel(0,4,0, "Current animation duration:", cspan=3)
        self.addentry(0,5,0,None, None, None, None,default="10", cspan=3)
        self.varmap[0][5][0].trace_add("write", lambda *args: self.update_animation_duration(5,0))
        self.addbutton(0,6,0, 
                       "Hide coordinates" if self.render.setting["show_coordinates"] else "Show coordinates", 
                       command = lambda *arg: self.toggle_show_coordinate(), cspan=3
        )
        self.addbutton(0,7,0, 
                       "Hide basis axis" if self.render.setting["show_basis_axis"] else "Show basis axis", 
                       command = lambda *arg: self.toggle_basis_axis(), cspan=3
        )        

    def toggle_basis_axis(self):
        self.render.setting["show_basis_axis"] = not self.render.setting["show_basis_axis"]
        self.refresh_widget(0,7,0)
        self.addbutton(0,7,0, 
                       "Hide basis axis" if self.render.setting["show_basis_axis"] else "Show basis axis", 
                       command = lambda *arg: self.toggle_basis_axis(), cspan=3
        ) 


    def toggle_show_coordinate(self):
        self.render.setting["show_coordinates"] = not self.render.setting["show_coordinates"]
        self.refresh_widget(0,6,0)
        self.addbutton(0,6,0, "Hide coordinates" if self.render.setting["show_coordinates"] else "Show coordinates", lambda *arg: self.toggle_show_coordinate(), cspan=3)

    def update_animation_duration(self, row, col): 
        currentVar = self.varmap[0][row][col].get().strip()
        if(currentVar!="" and currentVar != "0"):
            try:
                self.render.setting["animation_duration"] = float(currentVar) * 1000
            except Exception as e:
                print(e)

    def modify_animation_matrix(self, row, col):
        currentVar = self.varmap[0][row][col].get().strip()
        if(currentVar!=""):
            try:
                self.render.animation[row-1][col] = int(currentVar)
            except Exception as e:
                print(e)

    def show_frame(self,frame):
        """raise the selected frame from self.frames"""
        self.frames[frame].tkraise()

    def refresh(original_function):
        """wrapper function for every "add" functions, clear the existing widget"""
        def wrapper_function(*args,**kwargs):
            self,frame,row,column = args[0:4]
            if  self.gridmap[frame][row][column]:
                self.gridmap[frame][row][column].grid_remove()
            self.gridmap[frame][row][column] = None
            original_function(*args,**kwargs)
        return wrapper_function  

    def refresh_widget(self,frame,row,column):
        """refresh selected tkinter widget"""
        if self.gridmap[frame][row][column]:
            self.gridmap[frame][row][column].grid_remove()
        self.gridmap[frame][row][column] = None  

    @refresh
    def addscale(self,frame,row,column,command,text = "",rspan = 1,cspan = 1, horizontal = False, f = 0, t = 100):
        if(horizontal):
            self.gridmap[frame][row][column] = Scale(self.frames[frame], orient=HORIZONTAL, from_=f, to=t, label=text, command=command)
        else:
            self.gridmap[frame][row][column] = Scale(self.frames[frame], from_=f, to=t, label=text, command=command)
        self.gridmap[frame][row][column].grid(row = row, column = column, padx = 2, pady = 2, sticky = NSEW, rowspan = rspan, columnspan = cspan)

    @refresh
    def addtext(self,frame,row,column, width = 0, height = 0, rspan = 1, cspan = 1):
        """add a tkinter Text widget"""
        self.gridmap[frame][row][column] = Text(self.frames[frame])
        self.gridmap[frame][row][column].grid(row = row, column = column, padx = 2, pady = 2, sticky = NSEW, rowspan = rspan, columnspan = cspan)
        if width:
            self.gridmap[frame][row][column].config(width = width)
        if height:
            self.gridmap[frame][row][column].config(height = height)

    @refresh
    def addlabel(self,frame,row,column,text,cspan = 1,rspan = 1, img = None):
        """add a tkinter label"""
        self.gridmap[frame][row][column] = Label(self.frames[frame],text = text, image = img, compound = LEFT)
        self.gridmap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)
        
    @refresh
    def addbutton(self,frame,row,column,text,command,cspan = 1,rspan = 1):
        """add a tkinter button"""
        self.gridmap[frame][row][column] = Button(self.frames[frame],text = text,command = command)
        self.gridmap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)        

    @refresh
    def addonepbutton(self,frame,row,column,text,command,p1,cspan = 1,rspan = 1):
        """add a tkinter button with one parameter"""
        self.gridmap[frame][row][column] = Button(self.frames[frame],text = text, command = lambda:command(p1))
        self.gridmap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)         

    @refresh
    def addtwopbutton(self,frame,row,column,text,command,p1,p2,cspan = 1,rspan = 1):
        """add a tkinter button with two parameter"""
        self.gridmap[frame][row][column] = Button(self.frames[frame],text = text,command = lambda:command(p1,p2))
        self.gridmap[frame][row][column].grid(row = row,column = column, padx = 2,pady = 2, sticky = NSEW, columnspan = cspan, rowspan = rspan)         

    @refresh
    def addentry(self,frame,row,column,key1,key2,command1,command2,cspan = 1,rspan = 1, default = "", width=1):
        """add a tkinter entry"""
        self.varmap[frame][row][column] = StringVar()
        self.gridmap[frame][row][column] = Entry(self.frames[frame], width=width, textvariable=self.varmap[frame][row][column])
        self.gridmap[frame][row][column].insert(END, default)
        if command1:
            self.gridmap[frame][row][column].bind(key1,command1)
        if command2:
            self.gridmap[frame][row][column].bind(key2,command2)
        self.gridmap[frame][row][column].grid(row = row, column = column, padx = 2,pady = 2, sticky=NSEW, columnspan = cspan, rowspan = rspan)    

    @refresh
    def addcombobox(self,frame,row,column,options,command): 
        """add a tkinter combobox, also generates a tkinter.StringVar() object"""
        self.varmap[frame][row][column] = StringVar()
        self.gridmap[frame][row][column] = ttk.ComboBox(self.frames[frame],values = options, variable=self.varmap[frame][row][column], command = command)
        self.gridmap[frame][row][column].grid(row = row, column = column, padx = 2,pady = 2, sticky=NSEW)  

    @refresh
    def addlistbox(self,frame,row,column, height = 10, rspan = 1, cspan = 1):
        """add a tkinter listbox"""
        self.gridmap[frame][row][column] = Listbox(self.frames[frame],height=height,yscrollcommand = self.gridmap[frame][row][column+1].set)
        self.gridmap[frame][row][column].grid(row = row,column = column, padx = 2, pady = 2, sticky=NSEW, rowspan = rspan, columnspan = cspan)
        self.gridmap[frame][row][column].config(highlightbackground="#0b5162", highlightcolor="#0b5162", highlightthickness=2, relief="solid")

    @refresh
    def addscrollbar(self,frame,row,column, rspan = 1, cspan = 1):
        """add a tkinter scrollbar"""
        self.gridmap[frame][row][column] = Scrollbar(self.frames[frame])
        self.gridmap[frame][row][column].grid(row = row,column = column, padx = 2, pady = 2, sticky=NSEW, rowspan = rspan, columnspan = cspan)

if __name__ == "__main__":
    Control("test")