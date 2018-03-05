import tkinter as tk

class Interface:
    
    def __init__(self, master, win_size = (1024,786)):
        self.master = master
        master.title("PSF Dwingeloo bende you know")
        master.geometry('%dx%d+%d+%d' % (win_size[0], win_size[1], 0, 0))
        master.resizable(width=False, height=False)
        
        self.Header = HeaderFrame(master)
        self.Header.grid(row=0, column=0)
        self.Header.build()
        
        self.Menu = MenuFrame(master)
        self.Menu.grid(row=1, column=0, sticky='nw')
        self.Menu.build()
        
        self.Plots = PlotFrame(master)
        self.Plots.grid(row=1, sticky='e')
        
        self.OptionsA = OptionsFrame(master)
        self.OptionsA.grid(row=1, sticky='sw')
        
        self.Info = FillerFrame(master)
        self.Info.grid(row=2)
class HeaderFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=1024, height=40)
        self.grid_propagate(0)
        
        self.columnconfigure(0, minsize=145)
        self.columnconfigure(1, minsize=145)
        self.columnconfigure(2, minsize=414)
        self.columnconfigure(3, minsize=290)
        
        self.Label_Status = tk.Label(self, text='Status', bg='#99FF99', font=('Courier New', 22),padx=8, pady=8)
        self.Label_Status_Value = tk.Label(self, text="IDLE", bg='#99FF99',font=('Courier New', 22), padx=8, pady=8)
        self.Label_Observate_Status = tk.Label(self, text="Pulsar observing mode", bg='#99FF99',font=('Courier New', 22), padx=8, pady=8)
        self.Label_Target_Name = tk.Label(self, text="Rolo's projectquasar", bg='#99FF99',font=('Courier New', 22), padx=10, pady=8)
        
    def build(self):
        self.Label_Status.grid(row=0, column=0, sticky='nesw')
        self.Label_Status_Value.grid(row=0, column=1, rowspan=2, sticky='nesw')
        self.Label_Observate_Status.grid(row=0, column=2, rowspan=2, sticky='nesw')
        self.Label_Target_Name.grid(row=0, column=3, sticky='nesw')
        
class MenuFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=40, bg="#FF0000")
        self.grid_propagate(0)

        self.MenuA = tk.Button(self, text='STANDARD', command=self.A_button, width=14, padx=12, pady=10)
        self.MenuB = tk.Button(self, text='EVERYTHING EVER', command=self.B_button, width=14, padx=12, pady=10)
        self.MenuC = tk.Button(self, text='LESS OPTIONS', command=self.C_button, width=14, padx=12, pady=10)
        self.MenuD = tk.Button(self, text='FRANS', command=self.D_button, width=14, padx=12, pady=10)
        
    def build(self):
        self.MenuA.grid(row=0, column=0)
        self.MenuB.grid(row=0, column=1)
        self.MenuC.grid(row=0, column=2)
        self.MenuD.grid(row=0, column=3)
        
    def A_button(self):
        RestButtons = [self.MenuB, self.MenuC, self.MenuD]
        self.MenuA.config(relief="sunken")
        for i in RestButtons:
            i.config(relief="raised")

    def B_button(self):
        RestButtons = [self.MenuA, self.MenuC, self.MenuD]
        self.MenuB.config(relief="sunken")
        for i in RestButtons:
            i.config(relief="raised")

    def C_button(self):
        RestButtons = [self.MenuA, self.MenuB, self.MenuD]
        self.MenuC.config(relief="sunken")
        for i in RestButtons:
            i.config(relief="raised")
            
    def D_button(self):
        RestButtons = [self.MenuA, self.MenuB, self.MenuC]
        self.MenuD.config(relief="sunken")
        for i in RestButtons:
            i.config(relief="raised")            
class PlotFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=720, bg="#000FF0")
        self.grid_propagate(0)

class OptionsFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=680, bg="#0F0F0F")
        self.grid_propagate(0)

class FillerFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=1024, height=26, bg="#00FFFF")
        self.grid_propagate(0)
        
if __name__ == "__main__":
    root = tk.Tk()
    Interface(root)
    root.mainloop()