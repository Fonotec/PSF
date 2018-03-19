import tkinter as tk

class Interface:
    
    def __init__(self, master, win_size = (1024,784)):
        self.master = master
        master.title("PSF Dwingeloo bende you know")
        master.geometry('%dx%d+%d+%d' % (win_size[0], win_size[1], 0, 0))
        master.resizable(width=False, height=False)
        
        self.Header = HeaderFrame(master)
        self.Header.grid(row=0, column=0)
        self.Header.build()
        
        self.Menu = MenuFrame(master)
        self.Menu.grid(row=1, column=0, sticky='nw')
        
        self.Plots = PlotFrame(master)
        self.Plots.grid(row=1, sticky='e')
                
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
        self.Label_Status_Value = tk.Label(self, text="IDLE", bg='#99FF99', font=('Courier New', 22), padx=8, pady=8)
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
        self.configure(bd=0, width=512, height=720, bg="#FF0000")
        self.grid_propagate(0)
        self.master = master
        
        self.MenuAButton = tk.Button(self, text='STANDARD', command=self.A_button, width=14, padx=12, pady=10)
        self.MenuBButton = tk.Button(self, text='EVERYTHING EVER', command=self.B_button, width=14, padx=12, pady=10)
        self.MenuCButton = tk.Button(self, text='LESS OPTIONS', command=self.C_button, width=14, padx=12, pady=10)
        self.MenuDButton = tk.Button(self, text='FRANS', command=self.D_button, width=14, padx=12, pady=10)
        
        self.ActiveFrame = MenuAFrame(self.master)
        self.ActiveButton = self.MenuAButton
        self.ActiveButton.config(relief="sunken")
        
        self.ActiveFrame.grid(row=1, column=0, sticky='sw')
        self.ActiveFrame.build()
        self.build_Buttons() 
        self.ActiveButton.invoke()
        
    def build_Buttons(self):
        self.MenuAButton.grid(row=0, column=0)
        self.MenuBButton.grid(row=0, column=1)
        self.MenuCButton.grid(row=0, column=2)
        self.MenuDButton.grid(row=0, column=3)
        
    def A_button(self):
        if self.ActiveButton == self.MenuAButton:
            pass
        else:
            self.ActiveButton.config(relief="raised")
            self.ActiveFrame.destroy()
        
            self.ActiveFrame = MenuAFrame(self.master)
            self.ActiveButton = self.MenuAButton
        
            self.ActiveButton.config(relief="sunken")            
            self.ActiveFrame.grid(row=1, column=0, sticky='sw')   

            self.ActiveFrame.build()
   
        
    def B_button(self):
        if self.ActiveButton == self.MenuBButton:
            pass
        else:        
            self.ActiveButton.config(relief="raised")
            self.ActiveFrame.destroy()
            
            self.ActiveFrame = MenuBFrame(self.master)
            self.ActiveButton = self.MenuBButton
            
            self.ActiveButton.config(relief="sunken")
            self.ActiveFrame.grid(row=1, column=0, sticky='sw')    

            self.ActiveFrame.build()
        
    def C_button(self):
        if self.ActiveButton == self.MenuCButton:
            pass
        else:         
            self.ActiveButton.config(relief="raised")
            self.ActiveFrame.destroy()
            
            self.ActiveFrame = MenuCFrame(self.master)
            self.ActiveButton = self.MenuCButton
            
            self.ActiveButton.config(relief="sunken")
            self.ActiveFrame.grid(row=1, column=0, sticky='sw')  

            self.ActiveFrame.build()
            
    def D_button(self):
        if self.ActiveButton == self.MenuDButton:
            pass
        else:         
            self.ActiveButton.config(relief="raised")
            self.ActiveFrame.destroy()
            
            self.ActiveFrame = MenuDFrame(self.master)
            self.ActiveButton = self.MenuDButton
            
            self.ActiveButton.config(relief="sunken")
            self.ActiveFrame.grid(row=1, column=0, sticky='sw')        

            self.ActiveFrame.build()
            
class MenuAFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=680)
        self.grid_propagate(0)
        self.columnconfigure(0, minsize=200)
        var = tk.StringVar(master)
        
        self.FilenameLabel = tk.Label(self, text="Output name (.fits)", font=('Courier New', 14), padx=30, pady=20)
        self.FilenameEntry = tk.Entry(self, font=("Arial", 14))
        
        self.ObjectnameLabel = tk.Label(self, text="Object name", font=("Courier New", 14), padx=30, pady=20)
        self.ObjectnameEntry = tk.Entry(self, font=("Arial", 14))
        
        self.ObservationTimeLabel = tk.Label(self, text="Observation time (s)", font=('Courier New', 14), padx=30, pady=20)
        self.ObservationTimeEntry = tk.Entry(self, font=("Arial", 14))
        
        self.CentralFrequencyLabel = tk.Label(self, text="Central freq. (MHz)", font=("Courier New", 14), padx=30, pady=20)
        self.CentralFrequencyEntry = tk.Entry(self, font=("Arial", 14))

    def build(self):
        
        self.FilenameLabel.grid(row=0, column=0, sticky='w')
        self.FilenameEntry.grid(row=0, column=1)
        
        self.ObjectnameLabel.grid(row=1, column=0, sticky='w')
        self.ObjectnameEntry.grid(row=1, column=1)
        
        self.ObservationTimeLabel.grid(row=2, column=0, sticky='w')
        self.ObservationTimeEntry.grid(row=2, column=1)
        self.ObservationTimeEntry.insert(0, "600")
        
        self.CentralFrequencyLabel.grid(row=3, column=0, sticky='w')
        self.CentralFrequencyEntry.grid(row=3, column=1)
        self.CentralFrequencyEntry.insert(0, "405")
class MenuBFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=680, bg="#00FF00")
        self.grid_propagate(0)
        
        self.FilenameLabel = tk.Label(self, text="FileName")
        
    def build(self):
        self.FilenameLabel.grid(row=1, column=0)  
        
class MenuCFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=680, bg="#0000FF")
        self.grid_propagate(0)
        
        self.FilenameLabel = tk.Label(self, text="FileName")
        
    def build(self):
        self.FilenameLabel.grid(row=1, column=0)
        
class MenuDFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=680)
        self.grid_propagate(0) 
        
        self.GoImage = tk.PhotoImage(file="./tkinter_start.gif")
        self.StopImage = tk.PhotoImage(file="./tkinter_stop.gif")
        
        self.GOBUTTON = tk.Button(self, image=self.GoImage, border=0, command=self.switchon)
        self.STOPBUTTON = tk.Button(self, image=self.StopImage)
        
    def build(self):
        self.GOBUTTON.grid(sticky='ns')
        self.GOBUTTON.config(activebackground=self.GOBUTTON.cget('background'))
        
    def switchon(self):
        self.GOBUTTON.destroy()
        self.STOPBUTTON = tk.Button(self, image=self.StopImage, border=0, command=self.switchoff)        
        self.STOPBUTTON.grid(sticky='ns')
        self.STOPBUTTON.config(activebackground=self.STOPBUTTON.cget('background'))        
        
    def switchoff(self):
        self.STOPBUTTON.destroy()
        self.GOBUTTON = tk.Button(self, image=self.GoImage, border=0, command=self.switchon)
        self.GOBUTTON.grid(sticky='ns')
        self.GOBUTTON.config(activebackground=self.GOBUTTON.cget('background'))        
class PlotFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=0, width=512, height=720, bg="#000FF0")
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