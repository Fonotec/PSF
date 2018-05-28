import tkinter as tk
import matplotlib
#matplotlib.use("TKAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.widgets import RadioButtons
import time as time
from line_profiler import LineProfiler


class Interface:
    
    def __init__(self, master, win_size = (1024,784)):
        self.master = master
        self.Built = False
        self.PlotreScaled = False
        master.title("PSF Dwingeloo bende you know")
        master.geometry('%dx%d+%d+%d' % (win_size[0], win_size[1], 0, 0))
        master.resizable(width=True, height=True)
        master.minsize(win_size[0], win_size[1])
        master.bind("<Configure>", self.config)
        
        self.Menu = MenuFrame(self.master)
        self.Header = HeaderFrame(self.master)
        self.Info = FillerFrame(self.master)
        self.Plots = PlotFrame(self.master)
        self.Plots.grid(row=1, sticky='e')
        self.prevtime = time.time()
        
        self.FPSList = np.zeros(10)
        
        self.update_plot()
        
    def config(self, event):
        wwidth = self.master.winfo_width()
        wheight= self.master.winfo_height()
        if not self.Built:
            self.build()
        else:
            self.Header.configure(width = wwidth)
            self.Info.configure(width = wwidth)
            self.Plots.configure(width = wwidth-512, height=wheight-64)
            self.Plots.fwidth = wwidth-512
            self.Plots.fheight = wheight-64
            self.PlotreScaled = True
            self.Menu.ActiveFrame.configure(height=wheight-104)
            
    def build(self):
        self.Built=True
        self.Header.grid(row=0, column=0)
        self.Header.build()
        self.Info.grid(row=2)
        self.Menu.grid(row=1, column=0, sticky='nw')
     
    def update_plot(self):
        self.Plots.animate2(reScaled = self.PlotreScaled)
        self.PlotreScaled = False
        ct = time.time()
        self.FPSList[0] = (1/(ct - self.prevtime))
        self.FPSList = np.roll(self.FPSList,1)
        self.Info.updateFPS(np.mean(self.FPSList), ct)
        self.prevtime = ct
        self.master.after(0, self.update_plot)
         
         
class HeaderFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=4, width=1024, height=40, relief='flat')
        self.grid_propagate(0)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.Label_Status = tk.Label(self, text='Status IDLE', font=('Courier New', 22),padx=2, pady=8)
        self.Label_Observate_Status = tk.Label(self, text="Pulsar observing mode",font=('Courier New', 22), padx=8, pady=8)
        self.Label_Target_Name = tk.Label(self, text="No object in view",font=('Courier New', 22), padx=2, pady=8)
        
    def build(self):
        self.Label_Status.grid(row=0, column=0, sticky='nesw', padx=(0, 10))
        self.Label_Observate_Status.grid(row=0, column=1, columnspan=1, sticky='nesw')
        self.Label_Target_Name.grid(row=0, column=2, sticky='nesw', padx=(10,0))
        
        
class MenuFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=2, width=512, height=720, relief='sunken')
        self.grid_propagate(0)
        self.master = master
        
        self.MenuAButton = tk.Button(self, text='MAIN', command=self.A_button, width=14, padx=12, pady=10)
        self.MenuBButton = tk.Button(self, text='PLUS', command=self.B_button, width=14, padx=12, pady=10)
        self.MenuCButton = tk.Button(self, text='SAVED DATA', command=self.C_button, width=14, padx=12, pady=10)
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
        self.configure(bd=2, width=512, height=680, relief='sunken')
        self.grid_propagate(0)
        self.columnconfigure(0, minsize=200)
        var = tk.StringVar(master)
        
        self.FilenameLabel = tk.Label(self, text="Output name (.fits)", font=('Courier New', 14), padx=30, pady=20)
        self.FilenameEntry = tk.Entry(self, font=('Courier New', 14), width=18)
        
        self.ObjectnameLabel = tk.Label(self, text="Object name", font=("Courier New", 14), padx=30, pady=20)
        self.ObjectnameEntry = tk.Entry(self, font=('Courier New', 14), width=18)
        
        self.ObservationTimeLabel = tk.Label(self, text="Observation time (s)", font=('Courier New', 14), padx=30, pady=20)
        self.ObservationTimeEntry = tk.Entry(self, font=('Courier New', 14), width=18)
        
        self.CentralFrequencyLabel = tk.Label(self, text="Mixing freq. (MHz)", font=("Courier New", 14), padx=30, pady=20)
        self.CentralFrequencyEntry = tk.Entry(self, font=('Courier New', 14), width=18)

        self.BeginButton = tk.Button(self, text='Start', font=("Courier New", 20), command=self.RunMain(), width=15, height=3)
    
    def RunMain(self):
        pass
    
    def build(self):
        
        self.FilenameLabel.grid(row=0, column=0, sticky='w')
        self.FilenameEntry.grid(row=0, column=1, sticky='w')
        
        self.ObjectnameLabel.grid(row=1, column=0, sticky='w')
        self.ObjectnameEntry.grid(row=1, column=1)
        
        self.ObservationTimeLabel.grid(row=2, column=0, sticky='w')
        self.ObservationTimeEntry.grid(row=2, column=1)
        self.ObservationTimeEntry.insert(0, "600")
        
        self.CentralFrequencyLabel.grid(row=3, column=0, sticky='w')
        self.CentralFrequencyEntry.grid(row=3, column=1)
        self.CentralFrequencyEntry.insert(0, "405")
        
        self.BeginButton.grid(row=4, sticky='ns', columnspan=2)
        
        
class MenuBFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.configure(bd=2, width=512, height=680, relief='sunken')
        self.grid_propagate(0)
        
        self.FilenameLabel = tk.Label(self, text="Output name (.fits)", font=('Courier New', 14), padx=30, pady=20)
        self.FilenameEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.ObjectnameLabel = tk.Label(self, text="Object name", font=("Courier New", 14), padx=30, pady=20)
        self.ObjectnameEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.ObservationTimeLabel = tk.Label(self, text="Observation time (s)", font=('Courier New', 14), padx=30, pady=20)
        self.ObservationTimeEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.CentralFrequencyLabel = tk.Label(self, text="Mixing freq. (MHz)", font=("Courier New", 14), padx=30, pady=20)
        self.CentralFrequencyEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.PeriodLabel = tk.Label(self, text="Period (s)", font=('Courier New', 14), padx=30, pady=20)
        self.PeriodEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.DispersionMeasureLabel = tk.Label(self, text="Dispersion Measure", font=("Courier New", 14), padx=30, pady=20)
        self.DispersionMeasureEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.BinsAmountLabel = tk.Label(self, text="Number of bins", font=('Courier New', 14), padx=30, pady=20)
        self.BinsAmountEntry = tk.Entry(self, font=('Courier New', 14))      

        self.BeginButton = tk.Button(self, text='Start', font=("Courier New", 20), command=self.BeginButtonFunc, width=10, height=2, padx=10, pady=5)
        self.StopButton = tk.Button(self, text='Stop', font=("Courier New", 20), command=self.StopButtonFunc, width=10, height=2, padx=10, pady=5)
        
        self.ResetGraphButton = tk.Button(self, text='Reset Plot', font=("Courier New", 20), command=self.RunMain, width=10, height=2, padx=10, pady=5)
        self.StopGraphButton = tk.Button(self, text='Stop Plot', font=("Courier New", 20), command=self.RunMain, width=10, height=2, padx=10, pady=5)
        
        self.PauseButton = tk.Button(self, text='Start', font=("Courier New", 20), command=self.RunMain, width=5, height=2)
        #self.ResetGraphButton = tk.Button(self, text='Start', font=("Courier New", 20), command=self.RunMain(), width=5, height=2)
        
        
    def BeginButtonFunc(self):
        print("Begin")
        if self.getEntries():
            self.BeginButton.grid_forget()
            self.StopButton.grid(row=7, column=0)
        pass
    
    def StopButtonFunc(self):
        print("Stop")
        self.StopButton.grid_forget()
        self.BeginButton.grid(row=7, column=0)
        
        
    def RunMain(self, name):
        print(True, name)
        
        pass   
    
    def getEntries(self):
        FileName = self.FilenameEntry.get()
        ObjectName = self.ObjectnameEntry.get()
        ObservationTime = self.ObservationTimeEntry.get()
        MixingFrequency= self.CentralFrequencyEntry.get()
        Period = self.PeriodEntry.get()
        DispersionMeasure = self.DispersionMeasureEntry.get()
        BinsAmount = self.BinsAmountEntry.get()
        
        VariableNames = np.array(["FileName", "ObjectName", "ObservationTime", "MixingFrequency", "Period", "DispersionMeasure", "BinsAmount"])
        Variables = np.array([FileName, ObjectName, ObservationTime, MixingFrequency, Period, DispersionMeasure, BinsAmount])
        
        MissingVariables = VariableNames[Variables=='']
        
        if len(MissingVariables):
            print(MissingVariables)
            popUp = tk.Toplevel()
            popUp.geometry('%dx%d+%d+%d' % (400, 200, 500, 400))
            popUp.minsize(375, 100)
            popUp.maxsize(375, 100)
            popUp.title("Missing Parameters")
            
            self.popUpLabel = tk.Label(popUp, text="Please fill in empty entry fields", font=("Courier New", 14), padx=5)
            self.popUpOK = tk.Button(popUp, text="Okay", font=("Courier New", 14), width=12, height=2)
            self.popupDIFM = tk.Button(popUp, text="Do it for me!", font=("Courier New", 14), width=12, height=2)
            
            self.popUpLabel.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=10)
            self.popUpOK.grid(row=1, column=0)
            self.popupDIFM.grid(row=1, column=1)
            popUp.grab_set()
            return False
        return True
    
    
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

        self.PeriodLabel.grid(row=4, column=0, sticky='w')
        self.PeriodEntry.grid(row=4, column=1)
        
        self.DispersionMeasureLabel.grid(row=5, column=0, sticky='w')
        self.DispersionMeasureEntry.grid(row=5, column=1)
        
        self.BinsAmountLabel.grid(row=6, column=0, sticky='w')
        self.BinsAmountEntry.grid(row=6, column=1)
       
        self.BeginButton.grid(row=7, column=0, sticky='ns')
        #self.StopButton.grid(row=7, column=1)
        
        self.StopGraphButton.grid(row=8, column=0, sticky='ns', pady=8)
        self.ResetGraphButton.grid(row=8, column=1, pady=8)
        
        
class MenuCFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=2, width=512, height=680, bg="#0000FF", relief='sunken')
        self.grid_propagate(0)
        
        self.FilenameLabel = tk.Label(self, text="FileName")
        
    def build(self):
        self.FilenameLabel.grid(row=1, column=0)

        self.FilenameLabel = tk.Label(self, text="Output name (.fits)", font=('Courier New', 14), padx=30, pady=20)
        self.FilenameEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.ObjectnameLabel = tk.Label(self, text="Object name", font=("Courier New", 14), padx=30, pady=20)
        self.ObjectnameEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.ObservationTimeLabel = tk.Label(self, text="Observation time (s)", font=('Courier New', 14), padx=30, pady=20)
        self.ObservationTimeEntry = tk.Entry(self, font=('Courier New', 14))
        
        self.CentralFrequencyLabel = tk.Label(self, text="Central freq. (MHz)", font=("Courier New", 14), padx=30, pady=20)
        self.CentralFrequencyEntry = tk.Entry(self, font=('Courier New', 14))
        
        
class MenuDFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=2, width=512, height=680, relief='sunken')
        self.grid_propagate(0) 
        
        self.GoImage = tk.PhotoImage(file="./images/tkinter_start.gif")
        self.StopImage = tk.PhotoImage(file="./images/tkinter_stop.gif")
        
        self.GOBUTTON = tk.Button(self, image=self.GoImage, border=0, command=self.switchon)
        self.STOPBUTTON = tk.Button(self, image=self.StopImage)
        
    def build(self):
        self.GOBUTTON.grid(sticky='ns', pady=75)
        self.GOBUTTON.config(activebackground=self.GOBUTTON.cget('background'))
        
    def switchon(self):
        self.GOBUTTON.destroy()
        self.STOPBUTTON = tk.Button(self, image=self.StopImage, border=0, command=self.switchoff)        
        self.STOPBUTTON.grid(sticky='ns', pady=75)
        self.STOPBUTTON.config(activebackground=self.STOPBUTTON.cget('background'))        
        
    def switchoff(self):
        self.STOPBUTTON.destroy()
        self.GOBUTTON = tk.Button(self, image=self.GoImage, border=0, command=self.switchon)
        self.GOBUTTON.grid(sticky='ns', pady=75)
        self.GOBUTTON.config(activebackground=self.GOBUTTON.cget('background'))
        
        
class PlotFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.fwidth  = 512
        self.fheight = 720
        self.configure(bd=2, width=self.fwidth, height=self.fheight, relief='sunken')
        self.grid_propagate(0)   
        self.dpi = 100  
        self.f = Figure(figsize = (self.fwidth/self.dpi, self.fheight/self.dpi), dpi=self.dpi, facecolor=(1, 1, 1, 0))
        self.canvas = FigureCanvasTkAgg(self.f, self)
 
        self.top = self.f.add_subplot(311)
        self.middle = self.f.add_subplot(312)
        self.bottom = self.f.add_subplot(313)

        self.xData = np.linspace(0, 100*np.pi, 1000, endpoint=False)
        self.yDataB = np.sin(self.xData)
        self.yDataM = np.sin(self.xData)*np.sin(self.xData*0.5+.4)
        self.yDataT = np.sin(self.xData)**2 + np.cos(self.xData*1.1 + 0.15)
        
        self.startTime = time.time() 
        self.canvas.draw()       
        self.backgroundB = self.canvas.copy_from_bbox(self.bottom.bbox)
        self.backgroundT = self.canvas.copy_from_bbox(self.top.bbox)
        self.backgroundM = self.canvas.copy_from_bbox(self.middle.bbox)
        self.pointsB = self.bottom.plot(self.xData, self.yDataB)[0]            
        self.pointsM = self.middle.plot(self.xData, self.yDataM)[0]  
        self.pointsT = self.top.plot(self.xData, self.yDataT)[0]  
            
    def animate2(self, reScaled):
        scale = True
        
        if reScaled:
            self.f.clf()
            self.showCanvas.grid_forget()
            self.f = Figure(figsize = (self.fwidth/self.dpi, self.fheight/self.dpi), dpi=self.dpi, facecolor=(1, 1, 1, 0))
            self.canvas = FigureCanvasTkAgg(self.f, self)
            
            self.top = self.f.add_subplot(311)
            self.middle = self.f.add_subplot(312)
            self.bottom = self.f.add_subplot(313)
            
            self.canvas.draw()            
            
            self.backgroundB = self.canvas.copy_from_bbox(self.bottom.bbox)
            self.backgroundT = self.canvas.copy_from_bbox(self.top.bbox)
            self.backgroundM = self.canvas.copy_from_bbox(self.middle.bbox)
            
            self.pointsB = self.bottom.plot(self.xData, self.yDataB)[0]            
            self.pointsM = self.middle.plot(self.xData, self.yDataM)[0]  
            self.pointsT = self.top.plot(self.xData, self.yDataT)[0]  
            scale=False
            
        if scale:
            t = time.time()-self.startTime
            N = len(self.xData)
            currentIdx = int(N*((t/4)%1))
            scalingNumber = N*0.1
            waveShape = np.exp(-np.arange(N)/scalingNumber)[::-1]            

            colorArray = np.array([(1, 0, 0, a) for a in np.roll(waveShape, currentIdx)])      

            self.yDataB = np.roll(self.yDataB, 1)
            self.yDataT = np.roll(self.yDataT, 1)
            self.yDataM = np.roll(self.yDataM, 1)
            
            self.pointsB.set_data(self.xData, self.yDataB)
            self.pointsT.set_data(self.xData, self.yDataT)
            self.pointsM.set_data(self.xData, self.yDataM)
            
            self.canvas.restore_region(self.backgroundB)
            self.canvas.restore_region(self.backgroundT)
            self.canvas.restore_region(self.backgroundM)
            
            self.bottom.draw_artist(self.pointsB)
            self.middle.draw_artist(self.pointsM)
            self.top.draw_artist(self.pointsT)
            
            self.canvas.blit(self.bottom.bbox)
            self.canvas.blit(self.top.bbox)
            self.canvas.blit(self.middle.bbox)
            
            self.showCanvas = self.canvas.get_tk_widget()
            self.showCanvas.grid()

            
    
class FillerFrame(tk.Frame):
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(bd=2, width=1024, height=26, relief="sunken")
        self.grid_propagate(0)
        
        self.FPSLabel = tk.Label(self, text="FPS: ", font=("Courier New", 14))
        self.FPSValueLabel = tk.Label(self, text="{}".format(int(0)), font=("Courier New", 14))
        
        self.build()
        self.i = 0
        
        self.prevtime = time.time()
        
    def updateFPS(self, FPS, current_time):
        if current_time - self.prevtime > 0.3:
            
            self.FPSValueLabel.grid_forget()
            self.i += 1
            self.FPSValueLabel = tk.Label(self, text="{}".format(int(FPS)), font=("Courier New", 14))
            self.FPSValueLabel.grid(row=0, column=1)
            self.prevtime = current_time
        else:
            pass
        
    def build(self):
        self.FPSLabel.grid(row=0, column=0)
        self.FPSValueLabel.grid(row=0, column=1)
        
        #self.CentralFrequencyLabel = tk.Label(self, text="Central freq. (MHz)", font=("Courier New", 14), padx=30, pady=20)
if __name__ == "__main__":
    root = tk.Tk()
    Interface(root)
    root.mainloop()
