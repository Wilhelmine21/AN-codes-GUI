"""
Copyright © 2022 Ting-Yu Chen. All rights reserved.
###
Project: GUI_ALL.py
Version: v1.0
Author:  Ting-Yu Chen
Company: Test Lab, Electronic Engineering, National Changhua University of Education 
Work:    GUI for My Research
###
"""
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import os
import numpy as np
import math
import time
# from MyLib_ANcodes import *
# from MyLib_ANRCAM import *
import MyLib_ANcodes as MyAN
import MyLib_ANRCAM as MyANR
root = Tk()
root.title('My Research --- v1.0')
# root.title('Error Correctable Range-Addressable Lookup for Any Activation Function of Neural Networks')
root.geometry('600x280')
root.resizable(False,False)
###
#具有副視窗
def Openfile():
    filetypes1 = (("verilog design files","*.v"),("all files","*.*"))
    f = filedialog.askopenfile(filetypes=filetypes1)
    # print(f)
    if f == None:
        messagebox.showwarning("No File","You should select a file!")
    else:
        # #簡化路徑顯示
        f2=str(f).split(" ")
        f3=str(f2[1]).split("/")
        f4="Open file --- ./"+ f3[-2] +"/"+f3[-1][:-1]
        # #絕對路徑顯示
        # print(f2[1])
        # f3=str(f2[1]).split("'")
        # f4="Open file --- "+f3[1]
        str_vfile=""
        for line in f.readlines():
            str_vfile=str_vfile+line
        new1=Toplevel(root)
        # new1.iconbitmap("./TY2022_16x16.ico")
        new1.title(f4)
        #new1.geometry('400x400')
        Text_new1 = Text(new1,height=10,width=60,wrap=NONE)
        Text_new1.insert(END, str_vfile)
        
        scrollbarY = Scrollbar(new1, orient="vertical", command=Text_new1.yview)
        scrollbarX = Scrollbar(new1, orient="horizontal", command=Text_new1.xview)
        Text_new1.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
        
        Text_new1.grid(row=0, column=0, sticky="nsew")
        scrollbarY.grid(row=0, column=1, sticky="ns")
        scrollbarX.grid(row=1, column=0, sticky="ew")
        new1.grid_rowconfigure(0, weight=1)
        new1.grid_columnconfigure(0, weight=1)
#
#未寫
def Help():
    messagebox.showinfo("Info","Help.")
#
def about():
    note_about="Project: GUI_ALL.py\n\
Version: v1.0\n\
Author: Ting-Yu Chen\n\
Company: Test Lab, Electronic Engineering, NCUE\n\
----------------------------------------------------\n\
Work: GUI for My Research"
    messagebox.showinfo("Information",note_about)
#
def UseChrome(web):
    #指定你的chrome路徑
    Path1='C:\Program Files\Google\Chrome\Application\chrome.exe'
    Path2="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    if os.path.exists(Path1):
        # Lab
        chromePath = Path1 
    elif os.path.exists(Path2):
        chromePath = Path2
        # Home
        # chromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    else:
        messagebox.showwarning("Path Error","Can Not found Google Chrome")
        filetypes2 = (("exe files","*.exe"),("all files","*.*"))
        f22 = filedialog.askopenfile(filetypes=filetypes2)
        if f22 == None:
            messagebox.showwarning("No File","You should select a file!")
        else:
            chromePath = f22
    #註冊Chrome
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
    #指定Chrome開啟網頁
    webbrowser.get('chrome').open(web,new=2) 
#
def Video():
    #指定Chrome開啟網頁
    web = 'https://youtu.be/WHrd4GVcBvY'
    UseChrome(web)
# Call AN codes
def GUIANcodes():
    win_AN = Toplevel()
    win_AN.title('AN Codes and Decoder --- v2.1')
    win_AN.geometry('400x400')
    win_AN.resizable(False,False)
    #
    Range2 = IntVar() 
    Range2.set(100)
    selA = IntVar() 
    #
    #
    # ####按鈕功能def####
    def AList(event):
        Text_show_A.delete(1.0,END)
        if Entry_Range.get()!="" and Range2.get()>10:
            Two_A,Two_cbit_N,One_A,One_cbit_N=MyAN.FindA(1,int(Range2.get()))
            if Combobox_Mode.current() < 3:
                str1=str(One_A[0])
                for i in range(1,len(One_A)):
                    str1=str1+", "+str(One_A[i])
                Text_show_A.insert(END,str1)
            else:
                str1=str(Two_A[0])
                for i in range(1,len(Two_A)):
                    str1=str1+", "+str(Two_A[i])
                Text_show_A.insert(END,str1)
        else:
            messagebox.showwarning("Something Error","You should enter a number and it need > 10!")
    # #
    def Gen(newPath_Name1):
        if Entry_Range.get()!="" and Range2.get()>10:
            Two_A,Two_cbit_N,One_A,One_cbit_N=MyAN.FindA(1,int(Range2.get()))
            k=int(Entry_selA.get())
            if Combobox_Mode.current() < 3:
                if k in One_A:
                    if Combobox_Mode.current() == 0: #HL
                        fn="./"+newPath_Name1+"/Uni_HL_"+str(k)+".v"
                        fn2,fvcd,fo=MyAN.Uni_HL_veri(fn,k,newPath_Name1)
                    elif Combobox_Mode.current() == 1: #LH
                        fn="./"+newPath_Name1+"/Uni_LH_"+str(k)+".v"
                        fn2,fvcd,fo=MyAN.Uni_LH_veri(fn,k,newPath_Name1)
                    else: # 2 Alter
                        fn="./"+newPath_Name1+"/Alter_"+str(k)+".v"
                        fn2,fvcd,fo=MyAN.Alter_veri(fn,k,newPath_Name1)
                else:
                    messagebox.showwarning("Value Error1","You should enter a number in range.")
                    Entry_selA.delete(1.0,END)
            else:
                if k in Two_A:
                    k=int(Entry_selA.get())
                    if Combobox_Mode.current() == 3: #BER
                        fn="./"+newPath_Name1+"/BER_"+str(k)+".v"
                        fn2,fvcd,fo=MyAN.BER_veri(fn,k,newPath_Name1)
                    else: # 4 AWE
                        fn="./"+newPath_Name1+"/AWE_"+str(k)+".v"
                        fn2,fvcd,fo=MyAN.AWE_veri(fn,k,newPath_Name1)
                else:
                    messagebox.showwarning("Value Error2","You should enter a number in range.")
                    Entry_selA.delete(1.0,END)
            fR=open(fn,'r')
            file_str=""
            for line in fR.readlines():
                file_str=file_str+line
            fR.close()
            Text_txt.delete(1.0,END)
            Text_txt.insert('1.0', file_str)
        else:
            messagebox.showwarning("Something Error","You should enter a number!")
    #
    def clear():
        Entry_Range.delete(0,END)
        Text_show_A.delete(1.0,END)
        Entry_selA.delete(0,END)
        Text_txt.delete(1.0,END)
        Combobox_Mode.current(0)
    #
    def VCD(newPath_Name1):
        if Entry_selA.get()!="":
            if Combobox_Mode.current() == 0:
                fn="./"+newPath_Name1+"/Uni_HL_"+Entry_selA.get()+".v"
            elif Combobox_Mode.current() == 1:
                fn="./"+newPath_Name1+"/Uni_LH_"+Entry_selA.get()+".v"
            elif Combobox_Mode.current() == 2:
                fn="./"+newPath_Name1+"/Alter_"+Entry_selA.get()+".v"
            elif Combobox_Mode.current() == 3:  
                fn="./"+newPath_Name1+"/BER_"+Entry_selA.get()+".v"
            else:
                fn="./"+newPath_Name1+"/AWE_"+Entry_selA.get()+".v"     
            if os.path.isfile(fn):
                ftb=fn[:-2]+"_tb.v" #BER_13_tb.v
                fo="./"+newPath_Name1+"/A"+Entry_selA.get()+".out" #A13.out
                fvcd="./"+newPath_Name1+"/A"+Entry_selA.get()+".vcd" #A13.vcd
                os.system('iverilog -o %s %s %s'%(fo,fn,ftb))
                os.system('vvp -n %s'%fo)
                if os.path.isfile(fvcd):
                    os.system('gtkwave -T %s %s'%(ftcl,fvcd))
                else:
                    messagebox.showwarning("VCD File Error","The VCD file doesn't exist!")
            else:
                messagebox.showwarning("File Error","The file doesn't exist!")
        else:
            messagebox.showwarning("Something Error","Please enter the A value!")
    #具有副視窗
    def Openfile():
        filetypes1 = (("verilog design files","*.v"),("all files","*.*"))
        f = filedialog.askopenfile(filetypes=filetypes1)
        # print(f)
        if f == None:
            messagebox.showwarning("No File","You should select a file!")
        else:
            # #簡化路徑顯示
            f2=str(f).split(" ")
            f3=str(f2[1]).split("/")
            f4="Open file --- ./"+ f3[-2] +"/"+f3[-1][:-1]
            # #絕對路徑顯示
            # print(f2[1])
            # f3=str(f2[1]).split("'")
            # f4="Open file --- "+f3[1]
            str_vfile=""
            for line in f.readlines():
                str_vfile=str_vfile+line
            new1=Toplevel(win_AN)
            new1.title(f4)
            #new1.geometry('400x400')
            Text_new1 = Text(new1,height=10,width=60,wrap=NONE)
            Text_new1.insert(END, str_vfile)
            
            scrollbarY = Scrollbar(new1, orient="vertical", command=Text_new1.yview)
            scrollbarX = Scrollbar(new1, orient="horizontal", command=Text_new1.xview)
            Text_new1.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
            
            Text_new1.grid(row=0, column=0, sticky="nsew")
            scrollbarY.grid(row=0, column=1, sticky="ns")
            scrollbarX.grid(row=1, column=0, sticky="ew")
            new1.grid_rowconfigure(0, weight=1)
            new1.grid_columnconfigure(0, weight=1)

    #具有副視窗
    def Help():
        messagebox.showinfo("Info","The description will change based on your selection in \"Error Model\".")
        str_mode1="# 1st Error Model\n    # Unidirectional Fully Asymmetric Channel Model(完全非對稱模型)\n        # Error will only occur in uni-direction.事先知道哪一個1->0/0->1\n        #左圖為HL,右圖為LH\n"
        str_mode2="# 2nd Error Model\n    # Alternative-direction Fully Asymmetric Channel Model\n        # There is no way to know ahead of time that the error will go from 1 to 0 or from 0 to 1.\n"
        str_mode3="# 3rd Error Model\n    # Bit Error Rate Model(BER)\n        # bit 0->1 or 1->0, 各有機率\n"
        str_mode4="# 4nd Error Model\n    # Arithmetic Weight Error Model(AWE)\n        # The error comes from addition or subtraction."  

        global fig_decoder0,fig_decoder1,fig_decoder2,fig_decoder3,fig_decoder4
        fig_decoder0=PhotoImage(file="./fig/0.png")
        fig_decoder1=PhotoImage(file="./fig/1.png")
        fig_decoder2=PhotoImage(file="./fig/2.png")
        fig_decoder3=PhotoImage(file="./fig/3.png")
        fig_decoder4=PhotoImage(file="./fig/4.png")
        
        new1=Toplevel(win_AN)
        new1.title('Error Model 說明')
        if Combobox_Mode.current() < 2: #0,1
            Label_new1 = Label(new1, text = str_mode1, justify=LEFT)
            Label_new1.grid(row=0,column=0,columnspan=2,sticky=W)
            Label_fig0 = Label(new1, image=fig_decoder0)
            Label_fig0.grid(row=1,column=0,sticky=W,padx=5)
            Label_fig1 = Label(new1, image=fig_decoder1)
            Label_fig1.grid(row=1,column=1,sticky=W,padx=5)
        elif Combobox_Mode.current() == 2:
            Label_new2 = Label(new1, text = str_mode2, justify=LEFT)
            Label_new2.grid(row=0,column=0,columnspan=2,sticky=W)
            Label_fig2 = Label(new1, image=fig_decoder2)
            Label_fig2.grid(row=1,column=0,sticky=NS,padx=5,pady=5)
        elif Combobox_Mode.current() == 3:
            Label_new3 = Label(new1, text = str_mode3, justify=LEFT)
            Label_new3.grid(row=0,column=0,columnspan=2,sticky=W)
            Label_fig3 = Label(new1, image=fig_decoder3)
            Label_fig3.grid(row=1,column=0,sticky=NS,padx=5,pady=5)
        else:
            Label_new4 = Label(new1, text = str_mode4, justify=LEFT)
            Label_new4.grid(row=0,column=0,columnspan=2,sticky=W)
            Label_fig4 = Label(new1, image=fig_decoder4)
            Label_fig4.grid(row=1,column=0,sticky=NS,padx=5,pady=5)

    '''
    1st error model, for the situation where it is impossible to know in advance that the error will change from 1 to 0 or from 0 to 1, at this time, the remainder ring corresponding to modulo A is a single ring, and the remainder ring will appear like a Möbius ring. According to the error The orientation corresponds to the wrong location. Assuming that the modulus A is n bits, the number of (n-1) bits can be corrected. Taking modulus A=13 as an example, the number of bits that can be corrected is 12 (including modulus A itself), and the correctable range is a number between 0 and 255 (excluding modulus A), but because it is an unknown error direction, so the corresponding remainder is more, and its decoding circuit has the largest area among the four models.
    2nd error model is based on the situation that it is known in advance that the error will change from 1 to 0 or from 0 to 1. At this time, the remainder ring corresponding to the modulus A is a single ring. Assuming that the modulus A is n bits, the number of (n-1) bits can be corrected. Taking modulus A=13 as an example, the number of bits that can be corrected is 12 (including modulus A itself), and the correctable range is a number from 0 to 255 (excluding modulus A). Due to the known wrong direction, So the corresponding remainder is only half of the 1st error model.
    3rd error model is based on the situation that the circuit is disturbed and an error occurs. It changes from 1 to 0 or 0 to 1, and each has a probability. At this time, the remainder ring corresponding to the modulus A is a double ring. Assuming that the modulus A is n bits, the number of ((n-1))/2 bits can be corrected. Taking modulus A=13 as an example, the number of bits it can correct is 6 (including modulus A itself), and the correctable range is a number from 0 to 3 (excluding modulus A).
    4th error model, for the case that the error comes from addition or subtraction, at this time, the remainder ring corresponding to the modulus A is a double ring. Through the correspondence of the remainder in Table 3, we can know that when s=0, it means that the error comes from addition; when s=1, it means that the error comes from subtraction. Assuming that the modulus A is n bits, the number of ((n-1))/2 bits can be corrected. Taking modulo A=13 as an example, the number of bits that can be corrected is 6 (including modulo A itself), and the correctable range is a number from 0 to 3 (excluding modulo A). Its decoder circuit is shown in the figure 7. Unlike the BER model, AWE has "add" to check that the error comes from addition or subtraction.
    '''
    #
    def about():
        messagebox.showinfo("Information","Project: GUI_ANcodes.py\nVersion: v2.0\nAuthor: Ting-Yu Chen\nCompany: Test Lab, Electronic Engineering, NCUE\nWork: GUI for AN codes and Decoder")
    #
    #
    def UseChrome(web):
        #指定你的chrome路徑
        Path1='C:\Program Files\Google\Chrome\Application\chrome.exe'
        Path2="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        if os.path.exists(Path1):
            # Lab
            chromePath = Path1 
        elif os.path.exists(Path2):
            chromePath = Path2
            # Home
            # chromePath = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        else:
            messagebox.showwarning("Path Error","Can Not found Google Chrome")
            filetypes2 = (("exe files","*.exe"),("all files","*.*"))
            f22 = filedialog.askopenfile(filetypes=filetypes2)
            if f22 == None:
                messagebox.showwarning("No File","You should select a file!")
            else:
                chromePath = f22
        #註冊Chrome
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
        #指定Chrome開啟網頁
        webbrowser.get('chrome').open(web,new=2) 
    #
    #
    def Video():
        #指定Chrome開啟網頁
        web = 'https://youtu.be/WHrd4GVcBvY'
        UseChrome(web)

    def iVer():
        #指定Chrome開啟網頁
        web = 'http://iverilog.icarus.com'
        UseChrome(web)

    def GTK():
        web = 'http://gtkwave.sourceforge.net/'
        UseChrome(web)

    menu = Menu(win_AN)              
    win_AN.config(menu=menu)
    filemenu = Menu(menu,tearoff=0)               
    menu.add_cascade(label="File",menu=filemenu)
    filemenu.add_command(label="Open File...",command=Openfile)
    filemenu.add_separator() 
    filemenu.add_command(label="Exit",command=win_AN.destroy)
    #
    helpmenu = Menu(menu,tearoff=0)
    menu.add_cascade(label="Help",menu=helpmenu)
    helpmenu.add_command(label="What is iVerilog?",command=iVer)
    helpmenu.add_command(label="What is GTKwave?",command=GTK)
    helpmenu.add_separator() 
    helpmenu.add_command(label="Error Model Description",command=Help)
    helpmenu.add_command(label="Video",command=Video)
    helpmenu.add_separator() 
    helpmenu.add_command(label="About",command=about)

    #1. 輸入參數######################################################################################################
    # Label_Notes1 = Label(root, text='1. 顯示可用的A', justify=LEFT)
    Label_Notes1 = Label(win_AN, text='1. Show available A', justify=LEFT)
    Label_Notes1.grid(row=0,columnspan=2,sticky=W)

    Label_Range = Label(win_AN, text='Range:')
    Label_Range.grid(row=1,column=0,sticky=E,pady=5)

    Entry_Range = Entry(win_AN, textvariable=Range2)
    Entry_Range.grid(row=1,column=1,sticky=W)

    Label_Mode = Label(win_AN, text='Error Model:')
    Label_Mode.grid(row=2,column=0,sticky=E,pady=5)

    Combobox_Mode = ttk.Combobox(win_AN, values=[ "Uni HL","Uni LH","Alter","BER","AWE"], state='readonly', width=18)
    Combobox_Mode.grid(row=2,column=1,sticky=W,pady=5)
    Combobox_Mode.current(0)
    Combobox_Mode.bind('<<ComboboxSelected>>', AList)

    Label_A = Label(win_AN, text='A maybe:', justify=LEFT)
    Label_A.grid(row=3,column=0,sticky=E,pady=5)

    Text_show_A = Text(win_AN,height=2,width=20,wrap=WORD)
    Text_show_A.grid(row=3,column=1,sticky=W,pady=5)

    scrollbar = Scrollbar(win_AN, orient="vertical", command=Text_show_A.yview)
    Text_show_A.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=3,column=2,sticky=W)
    win_AN.grid_rowconfigure(0, weight=1)

    # 2. 輸出verilog檔案 Generate verilog file############################################################################
    newPath_Name1="ANcodes_files"
    newPath_files=MyAN.autoCreatFolder(newPath_Name1)
    Label_Notes2 = Label(win_AN, text='2. Generate verilog file', justify=LEFT)
    Label_Notes2.grid(row=4,columnspan=4,sticky=W)

    Label_selA = Label(win_AN, text='Select A:')
    Label_selA.grid(row=5,column=0,sticky=E,pady=5)

    Entry_selA = Entry(win_AN, textvariable=selA)
    Entry_selA.grid(row=5,column=1,sticky=W)

    Label_txt = Label(win_AN, text='The content of the generated file:')
    Label_txt.grid(row=6,column=0,columnspan=2,sticky=W,pady=5)

    Text_txt = Text(win_AN,height=5,width=52,wrap=NONE)
    Text_txt.grid(row=7,column=0,columnspan=4,sticky=NSEW,pady=5,padx=3)

    scrollbar2 = Scrollbar(win_AN, orient="vertical", command=Text_txt.yview)
    Text_txt.config(yscrollcommand=scrollbar2.set)
    scrollbar2.grid(row=7,column=4,sticky=NS)
    win_AN.grid_rowconfigure(0, weight=1)
    ######################################################
    Button_GenShow = Button(win_AN, text='Gen & Show', bg="LightBlue",command=lambda: Gen(newPath_Name1), width=20)
    Button_GenShow.grid(row=8,column=1,sticky=W,pady=5)

    Button_Clear = Button(win_AN, text='Clear', bg="Gold", command=clear, width=20)
    Button_Clear.grid(row=8,column=2,sticky=W,pady=5)

    # 3. Verilog verification (using iverilog+GTKwave)############################################################################
    PinName="D0.numX D0.out"
    DataFormat="Decimal"
    wPDF=0
    ftcl=MyAN.AutoVerilogTcl(newPath_Name1,PinName,DataFormat,wPDF)
    # Label_Notes3 = Label(root, text='3. Verilog驗證(使用iverilog+GTKwave)', justify=LEFT)
    Label_Notes3 = Label(win_AN, text='3. Verilog verification( Using iverilog + GTKwave )', justify=LEFT)
    Label_Notes3.grid(row=9,columnspan=4,sticky=W)

    Button_VCD = Button(win_AN, text='VCD', bg="LightBlue", command=lambda: VCD(newPath_Name1), width=20)
    Button_VCD.grid(row=10,column=1,sticky=W,pady=5)

    Button_Exit = Button(win_AN, text='Exit', bg="pink", command=win_AN.destroy, width=20)
    Button_Exit.grid(row=10,column=2,sticky=W,pady=5)
    #
# Call ANRCAM
def GUIANRCAM():
    win_ANRCAM = Toplevel(root)
    win_ANRCAM.title('ANRCAM --- v3.1')
    win_ANRCAM.geometry('600x430')
    win_ANRCAM.resizable(False,False)
    #
    NumA = IntVar()
    InBit = IntVar()
    in1 = IntVar()
    in2 = IntVar()
    error = DoubleVar()
    setXSign = IntVar()
    setXInt = IntVar()
    setXDec = IntVar()
    setbSign = IntVar()
    setbInt = IntVar()
    setbDec = IntVar()
    Lstart = IntVar()
    Lshift = IntVar()
    lightnumbers = IntVar()
    mode = IntVar()
    finish_mode = IntVar()
    run_mode = IntVar()
    verilog_mode = IntVar()
    #########Python def###########################
    def CheckBit():
        # print("--- Check Bit ---\n")
        kk=InBit.get()-setXSign.get()-setXInt.get()
        if setXDec.get()!=kk:
            strXDec="*set* set_x1_dec= "+str(kk)
            messagebox.showwarning("Reset X dec bit",strXDec)
            setXDec.set(kk)
        # if (setbInt.get()-setXInt.get()-Lstart.get()) < 0:
        #     k1=setbInt-(setbInt.get()-setXInt.get()-Lstart.get())
        #     strbInt="*set* set_b1_int= "+str(k1)
        #     messagebox.showwarning("Reset b int bit",strbInt)
        #     setbInt.set(k1)
        set_shift_pow = 2**Lshift.get()
        # if (setbDec.get()-setXDec.get()+Lstart.get()-set_shift_pow+1) < 0:
        #     k2=setbDec.get()-(setbDec.get()-setXDec.get()+Lstart.get()-set_shift_pow+1)
        #     strbDec="*set* set_b1_dec= "+str(k2)
        #     messagebox.showwarning("Reset b dec bit",strbDec)
        #     setbDec.set(k2)
        set_stop=Lstart.get()-set_shift_pow
        in_num=(2**setXDec.get())+1
        in_length=1/(in_num-1)
        return set_shift_pow,set_stop,in_num,in_length
    #呼叫CheckBit()檢查 setXDec=InBit-setXSign-setXInt
    def BasicParameters():
        global x,y,a1,b1,fig_fileName,fig_Name,figName1,figName2,figName3,figName4,set_shift_pow,set_stop
        set_shift_pow,set_stop,in_num,in_length=CheckBit()
        x = np.linspace(in1.get(), in2.get(), num=(int)((in2.get()-in1.get())/in_length)+1)
        y = []
        #***(產生x與函式)***
        if Combobox_Funct.current() == 0:
            # tanh
            for i in range(0,len(x)):
                y.append(math.tanh(x[i]))
        elif Combobox_Funct.current() == 1:
            #sigmoid
            for i in range(0,len(x)):
                y.append(1/(1+math.exp(-x[i])))
        else:
            #sin
            for i in range(0,len(x)):
                y.append((math.asin(2*x[i]-1)/math.pi)+1/2)
        ####
        fig_fileName=Combobox_Funct.get()[:-3]
        fig_Name=Combobox_Funct.get()
        a1,b1,figName1,figName2,figName3,figName4=MyANR.ShowFigBeforeTheAlgorithm(x,y,in_length,setbDec.get(),Lstart.get(),set_shift_pow,lightnumbers.get(),mode.get(),run_mode.get(),fig_Name,figPathName)
    #
    def AutoSelectA():
        NBitNeed=InBit.get()+setbDec.get()-setXDec.get()
        Two_A,Two_cbit_N,One_A,One_cbit_N=MyANR.FindA(1,rang2=100)
        if Combobox_ErrorModel.current() < 3: #Uni,Alter
            NumA1,BitN1=MyANR.AutoFindA(NBitNeed,0,One_A,One_cbit_N)
        else: #3 #4 BER AWE
            NumA1,BitN1=MyANR.AutoFindA(NBitNeed,1,Two_A,Two_cbit_N)
        if NumA.get()!=NumA1:
            noteA="A should be "+str(NumA1)+"\nIt can correct "+str(BitN1)+" bits(N)."
            messagebox.showinfo("Check A",noteA)
            NumA.set(NumA1)
        return NumA1,BitN1
    # ########Button def###########################
    #
    def clear():
        # Text.delete(1.0,END)
        Entry_A.delete(0,END)
        Entry_InBit.delete(0,END)
        Entry_in1.delete(0,END)
        Entry_in2.delete(0,END)
        Entry_error.delete(0,END)
        Entry_setXSign.delete(0,END)
        Entry_setXDec.delete(0,END)
        Entry_setXInt.delete(0,END)
        Entry_setbSign.delete(0,END)
        Entry_setbDec.delete(0,END)
        Entry_setbInt.delete(0,END)
        Entry_Lstart.delete(0,END)
        Entry_Lshift.delete(0,END)
        Entry_LN.delete(0,END)
        Entry_mode.delete(0,END)
        Entry_run_mode.delete(0,END)
        Entry_finish_mode.delete(0,END)
        Entry_verilog_mode.delete(0,END)
        Combobox_Funct.current(0)
        Combobox_ErrorModel.current(0)
    #
    def default():
        NumA.set(47)
        InBit.set(12)
        in1.set(-8)
        in2.set(8)
        error.set(0.001)
        setXSign.set(1)
        setXInt.set(3)
        setXDec.set(8)
        setbSign.set(1)
        setbInt.set(0)
        setbDec.set(16)
        Lstart.set(0)
        Lshift.set(3)
        lightnumbers.set(3)
        mode.set(3)
        ###
        finish_mode.set(0) 
        run_mode.set(0) 
        verilog_mode.set(1)
        ####
        Combobox_Funct.current(0)
        Combobox_ErrorModel.current(3)
    #
    def ShowFig():
        if Entry_InBit.get() != "" and Entry_setXSign.get()!="" and Entry_setXInt.get()!="" and Entry_setXDec.get()!="" and Entry_setbSign.get()!="" and Entry_setbInt.get()!="" and Entry_setbDec.get()!="" and Entry_Lstart.get()!="" and Entry_Lshift.get()!="" and Entry_LN.get()!="" and Entry_mode.get()!="" and Entry_finish_mode.get()!="" and Entry_run_mode.get()!="" and Entry_verilog_mode.get()!="":
            if InBit.get()==0 or (in1.get()== 0 and in2.get()== 0) or setXDec.get()== 0 or setbDec.get()==0:
                messagebox.showwarning("Value error","You should check the values!")
            else:
                BasicParameters()
                ######### GUI plt #######
                figWin=Toplevel(win_ANRCAM)
                figWin.title("Show fig")
                figWin.resizable(False,False)
                #
                global fig1,fig2,fig3,fig4
                fig1 = PhotoImage(file=("./"+figPathName+"/"+figName1))
                fig2 = PhotoImage(file=("./"+figPathName+"/"+figName2))
                fig3 = PhotoImage(file=("./"+figPathName+"/"+figName3))
                fig4 = PhotoImage(file=("./"+figPathName+"/"+figName4))
                #
                Label_fig1 = Label(figWin, image=fig1)
                Label_fig1.grid(row=0,column=0)
                Label_fig2 = Label(figWin, image=fig2)
                Label_fig2.grid(row=0,column=1)
                Label_fig3 = Label(figWin, image=fig3)
                Label_fig3.grid(row=1,column=0)
                Label_fig4 = Label(figWin, image=fig4)
                Label_fig4.grid(row=1,column=1)
        else:
            messagebox.showwarning("No Value","You should enter the all values!")     
    #
    def Gen():
        if Entry_InBit.get() != "" and Entry_setXSign.get()!="" and Entry_setXInt.get()!="" and Entry_setXDec.get()!="" and Entry_setbSign.get()!="" and Entry_setbInt.get()!="" and Entry_setbDec.get()!="" and Entry_Lstart.get()!="" and Entry_Lshift.get()!="" and Entry_LN.get()!="" and Entry_mode.get()!="" and Entry_finish_mode.get()!="" and Entry_run_mode.get()!="" and Entry_verilog_mode.get()!="":
            if InBit.get()==0 or (in1.get()== 0 and in2.get()== 0) or setXDec.get()== 0 or setbDec.get()==0:
                messagebox.showwarning("Value error","You should check the values!")
            else:
                Button_Gen["state"] = "disabled"
                # OutBit=in_bit+set_b1_dec-set_x1_dec
                # pool = multiprocessing.Pool()
                time0=time.time()
                BasicParameters()
                NumA1,BitN1=AutoSelectA()
                time1=time.time()
                # LS_PWL_RALUT_old(Path,x,a1,b1,error,in_bit,set_b1_dec,set_shift,set_lightnumbers)
                arr3=MyANR.LS_PWL_RALUT_old(filePathName,x,a1,b1,error.get(),InBit.get(),setbDec.get(),Lshift.get(),lightnumbers.get())
                time2=time.time()
                # pool.close()
                # pool.join()
                note1="* len(arr3)="+str(len(arr3))+"\n"+"It cost %.2f sec."%(time2-time1)
                messagebox.showwarning("search done",note1)
                ymax, yavg,figName11,figName12=MyANR.ShowFigAfterA(x,y,arr3,fig_Name,figPathName)
                #呼叫匯出
                MyANR.fpattern_xA(filePathName,NumA.get(),arr3,InBit.get(),setXInt.get(),setXDec.get(),setXSign.get())
                MyANR.fver_xA(filePathName,NumA.get(),arr3,setbInt.get(),setbDec.get(),setbSign.get(),lightnumbers.get(),Lshift.get(),set_shift_pow,Lstart.get(),mode.get())
                
                if(run_mode.get()==0):
                    global fnV,ftb,fvcd,f_vData
                    fnV=MyANR.ANRCAM(filePathName,NumA.get(),Combobox_ErrorModel.current(),lightnumbers.get(),InBit.get(),setbDec.get(),setXDec.get())
                    ftb,fvcd,f_vData=MyANR.ANRCAM_tb(filePathName,InBit.get(), setXDec.get(), setbDec.get(), wPDF, printData, FullData)
                if(run_mode.get()==1):
                    MyANR.fverilog_RALUT(filePathName,InBit.get())
                    # EDA #
                str1=MyANR.pri(arr3,fig_fileName,InBit.get(),in1.get(),in2.get(),error.get(),setbInt.get(),setbDec.get(),Lstart.get(),set_stop,Lshift.get(),set_shift_pow,lightnumbers.get(),mode.get(),finish_mode.get())
                tEnd = time.time()
                AllTime=("It cost %f sec" % (tEnd - time0))
                EndText="max "+str(ymax)+'\n'+"avg "+str(yavg)+'\n'+str1+"\n"+AllTime
                messagebox.showinfo("All done",EndText)
                ######### GUI plt #######
                figWinA=Toplevel(win_ANRCAM)
                figWinA.title("Show fig After Algorithm")
                figWinA.resizable(False,False)
                #
                global fig11,fig12
                fig11 = PhotoImage(file=("./"+figPathName+"/"+figName11))
                fig12 = PhotoImage(file=("./"+figPathName+"/"+figName12))
                #
                Label_fig11 = Label(figWinA, image=fig11)
                Label_fig11.grid(row=0,column=0)
                Label_fig12 = Label(figWinA, image=fig12)
                Label_fig12.grid(row=0,column=1)
                Button_Gen["state"] = "normal"
        else:
            messagebox.showwarning("No Value","You should enter the all values!")
    #
    def Openfile():
        filetypes1 = (("verilog design files","*.v"),("all files","*.*"))
        f = filedialog.askopenfile(filetypes=filetypes1)
        # print(f)
        if f == None:
            messagebox.showwarning("No File","You should select a file!")
        else:
            f2=str(f).split(" ")
            f3=str(f2[1]).split("/")
            f4="Open file --- ./"+ f3[-2] +"/"+f3[-1][:-1]
            str_vfile=""
            for line in f.readlines():
                str_vfile=str_vfile+line
            new1=Toplevel(win_ANRCAM)
            new1.title(f4)
            Text_new1 = Text(new1,height=10,width=60,wrap=NONE)
            Text_new1.insert(END, str_vfile)
            
            scrollbarY = Scrollbar(new1, orient="vertical", command=Text_new1.yview)
            scrollbarX = Scrollbar(new1, orient="horizontal", command=Text_new1.xview)
            Text_new1.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
            
            Text_new1.grid(row=0, column=0, sticky="nsew")
            scrollbarY.grid(row=0, column=1, sticky="ns")
            scrollbarX.grid(row=1, column=0, sticky="ew")
            new1.grid_rowconfigure(0, weight=1)
            new1.grid_columnconfigure(0, weight=1)
    #
    def VCD(Path):
        ftcl=MyANR.AutoVerilogTcl(Path,PinName,DataFormat,wPDF)  
        fo="./"+Path+"/ANRCAM.out"
        if os.path.isfile(fnV):
            os.system('iverilog -o %s %s %s'%(fo,fnV,ftb))
            os.system('vvp -n %s'%fo)
            if os.path.isfile(fvcd):
                os.system('gtkwave -T %s %s'%(ftcl,fvcd))
            else:
                messagebox.showwarning("VCD File Error","The VCD file doesn't exist!")
        else:
                messagebox.showwarning("File Error","The file doesn't exist!")
    #
    def Pltfig(Path):
        OutBit=InBit.get()+setbDec.get()-setXDec.get()
        if os.path.isfile(f_vData) and FullData == 1:
            InBinArr,InDecArr,OutBinArr,OutDecArr=MyANR.ImpDataVerilog(f_vData)
            xVeri,yVeri,figName21=MyANR.ReadData(Path,InBit.get(),setXDec.get(),OutBit,setbDec.get(),InDecArr,OutDecArr)
        else:
            messagebox.showwarning("Files Problem","The txt file doesn't exist!\n or The data is incomplete!")
        ######### GUI plt #######
        figWin2=Toplevel(win_ANRCAM)
        figWin2.title("Plt fig")
        figWin2.resizable(False,False)
        #
        global fig21
        fig21 = PhotoImage(file=("./"+figPathName+"/"+figName21))
        Label_fig21 = Label(figWin2, image=fig21)
        Label_fig21.grid(row=0,column=0)
    #
    #具有副視窗
    def Help():
        new1=Toplevel(win_ANRCAM)
        new1.title('Mode說明')
        str_mode="#-------- 輕數設定 --------#\n\
        1) start 輕數從0次方開始\n\
        2) shift 輕數一組有幾bits\n\
        3) set_lightnumbers 輕數是由幾組組成(weight)\n\n\
    #-------- mode設定 --------#\n\
        1) mode 0 light number的每一組都支援0\n\
        2) mode 1 light number的每一組都不支援0，\n\
            因此如果需要為0，會用互補的方式處理\n\
            (light number為奇數時，會容易互補不了)\n\
        3) mode 2 保留\n\
        4) mode 3 light number僅最後一組支援0\n\n\
    #-------- finish_mode設定 --------#\n\
        1) finish_mode 0 快速，通常與完整掃描的一樣，\n\
            但不保證結果最佳\n\
        2) finish_mode 1 完整掃描，數據大容易很慢，\n\
            很慢時請先用mode0試\n\
        3) finish_mode 2 測試\n\n\
    #-------- run_mode設定 --------#\n\
        1) run_mode 0 正常運行\n\
        2) run_mode 1 RALUT模式\n\n\
    #-------- verilog_mode設定 --------#\n\
        1) verilog_mode 0 verilog中使用IN+1\n\
        2) verilog_mode 1 verilog中使用IN\n\
    "
        Label_new1 = Label(new1, text = str_mode, justify=LEFT)
        Label_new1.grid(row=0,column=0,sticky=W)
    #
    global figPathName,filePathName
    filePathName="ANRCAM_files"
    filePath=MyANR.autoCreatFolder(filePathName)
    figPathName=filePathName+"/ANRCAM_fig"
    figPath=MyANR.autoCreatFolder(figPathName)
    #
    global wPDF, printData, FullData,PinName,DataFormat
    wPDF=0
    printData=1
    FullData=1
    PinName="t0.in t0.out_xA_e t0.out_xA_e_unsigned t0.out_xA_e_unsigned_zfill0 t0.out_unsigned t0.out"
    DataFormat="Decimal"
    #1. 輸入參數######################################################################################################
    Label_Notes1 = Label(win_ANRCAM, text='1. Basic Parameter Settings', justify=LEFT)
    Label_Notes1.grid(row=0,column=0,columnspan=2,sticky=W)

    #in_bit
    Label_InBit = Label(win_ANRCAM, text='Input Bit:')
    Label_InBit.grid(row=1,column=0,sticky=E,pady=5)
    Entry_InBit = Entry(win_ANRCAM,width=15,textvariable=InBit)
    Entry_InBit.grid(row=1,column=1,sticky=W)

    Label_in1 = Label(win_ANRCAM, text='Left Range:')
    Label_in1.grid(row=1,column=2,sticky=E,pady=5)
    Entry_in1 = Entry(win_ANRCAM,width=15,textvariable=in1)
    Entry_in1.grid(row=1,column=3,sticky=W)

    Label_in2 = Label(win_ANRCAM, text='Right Range:')
    Label_in2.grid(row=1,column=4,sticky=E,pady=5)
    Entry_in2 = Entry(win_ANRCAM,width=15,textvariable=in2)
    Entry_in2.grid(row=1,column=5,sticky=W)

    #X
    Label_X = Label(win_ANRCAM, text='X',width=85, fg="blue",bg="lightgray")
    Label_X.grid(row=2,column=0,columnspan=6,sticky=W,pady=5)

    Label_setXSign = Label(win_ANRCAM, text='X Sign Bit:', fg="blue")
    Label_setXSign.grid(row=3,column=0,sticky=E,pady=5)
    Entry_setXSign = Entry(win_ANRCAM,width=15,textvariable=setXSign)
    Entry_setXSign.grid(row=3,column=1,sticky=W)

    Label_setXInt = Label(win_ANRCAM, text='X Int Bit:', fg="blue")
    Label_setXInt.grid(row=3,column=2,sticky=E,pady=5)
    Entry_setXInt = Entry(win_ANRCAM,width=15,textvariable=setXInt) 
    Entry_setXInt.grid(row=3,column=3,sticky=W)

    Label_setXDec = Label(win_ANRCAM, text='X Dec Bit:', fg="blue")
    Label_setXDec.grid(row=3,column=4,sticky=E,pady=5)
    Entry_setXDec = Entry(win_ANRCAM,width=15,textvariable=setXDec)
    Entry_setXDec.grid(row=3,column=5,sticky=W)
    #b
    Label_b = Label(win_ANRCAM, text='b',width=85, fg="green",bg="lightgray")
    Label_b.grid(row=4,column=0,columnspan=6,sticky=W,pady=5)

    Label_setbSign = Label(win_ANRCAM, text='b Sign Bit:', fg="green")
    Label_setbSign.grid(row=5,column=0,sticky=E,pady=5)
    Entry_setbSign = Entry(win_ANRCAM,width=15,textvariable=setbSign) 
    Entry_setbSign.grid(row=5,column=1,sticky=W)

    Label_setbInt = Label(win_ANRCAM, text='b Int Bit:', fg="green")
    Label_setbInt.grid(row=5,column=2,sticky=E,pady=5)
    Entry_setbInt = Entry(win_ANRCAM,width=15,textvariable=setbInt)
    Entry_setbInt.grid(row=5,column=3,sticky=W)

    Label_setbDec = Label(win_ANRCAM, text='b Dec Bit:', fg="green")
    Label_setbDec.grid(row=5,column=4,sticky=E,pady=5)
    Entry_setbDec = Entry(win_ANRCAM,width=15,textvariable=setbDec)
    Entry_setbDec.grid(row=5,column=5,sticky=W)
    # Light Number
    Label_Light = Label(win_ANRCAM, text='Light Number',width=85, fg="sienna",bg="lightgray")
    Label_Light.grid(row=6,column=0,columnspan=6,sticky=W,pady=5)

    Label_Lstart = Label(win_ANRCAM, text='Start:', fg="sienna")
    Label_Lstart.grid(row=7,column=0,sticky=E,pady=5)
    Entry_Lstart = Entry(win_ANRCAM,width=15,textvariable=Lstart)
    Entry_Lstart.grid(row=7,column=1,sticky=W)

    Label_Lshift = Label(win_ANRCAM, text='Shift:', fg="sienna")
    Label_Lshift.grid(row=7,column=2,sticky=E,pady=5)
    Entry_Lshift = Entry(win_ANRCAM,width=15,textvariable=Lshift)
    Entry_Lshift.grid(row=7,column=3,sticky=W)

    Label_LN = Label(win_ANRCAM, text='Lignt Numbers:', fg="sienna")
    Label_LN.grid(row=7,column=4,sticky=E,pady=5)
    Entry_LN = Entry(win_ANRCAM,width=15,textvariable=lightnumbers)
    Entry_LN.grid(row=7,column=5,sticky=W)
    #2. 輸入mode######################################################################################################
    Label_Notes2 = Label(win_ANRCAM, text='2. Mode Settings', justify=LEFT)
    Label_Notes2.grid(row=8,column=0,columnspan=2,sticky=W)

    Button_Help = Button(win_ANRCAM, text='Help', width=10, command=Help)#bg="LightBlue",
    Button_Help.grid(row=8,column=1,sticky=E)
    # mode
    Label_mode = Label(win_ANRCAM, text='Mode:')
    Label_mode.grid(row=9,column=0,sticky=E,pady=5)
    Entry_mode = Entry(win_ANRCAM,width=15,textvariable=mode)
    Entry_mode.grid(row=9,column=1,sticky=W)
    # finish_mode
    Label_finish_mode = Label(win_ANRCAM, text='Finish mode:')
    Label_finish_mode.grid(row=9,column=2,sticky=E,pady=5)
    Entry_finish_mode = Entry(win_ANRCAM,width=15,textvariable=finish_mode)
    Entry_finish_mode.grid(row=9,column=3,sticky=W)
    # error
    Label_error = Label(win_ANRCAM, text='Targe Error:')
    Label_error.grid(row=9,column=4,sticky=E,pady=5)
    Entry_error = Entry(win_ANRCAM,width=15,textvariable=error)
    Entry_error.grid(row=9,column=5,sticky=W)
    # run_mode
    Label_run_mode = Label(win_ANRCAM, text='Run mode:')
    Label_run_mode.grid(row=10,column=0,sticky=E,pady=5)
    Entry_run_mode = Entry(win_ANRCAM,width=15,textvariable=run_mode)
    Entry_run_mode.grid(row=10,column=1,sticky=W)
    # verilog_mode
    Label_verilog_mode = Label(win_ANRCAM, text='Verilog mode:')
    Label_verilog_mode.grid(row=10,column=2,sticky=E,pady=5)
    Entry_verilog_mode = Entry(win_ANRCAM,width=15,textvariable=verilog_mode)
    Entry_verilog_mode.grid(row=10,column=3,sticky=W)
    # Button
    Button_default = Button(win_ANRCAM, text='Default', bg="LightBlue", width=10, command=default) # , bg="LightBlue", width=15
    Button_default.grid(row=10,column=4,sticky=E,pady=5)

    Button_clear = Button(win_ANRCAM, text='Clear', bg="Gold", width=10, command=clear) # bg="LightBlue", width=15
    Button_clear.grid(row=10,column=5,sticky=W,pady=5,padx=5)#columnspan=2,
    #3. Activation Funct.######################################################################################################
    Label_Notes3 = Label(win_ANRCAM, text='3. Select Activation Function', justify=LEFT)
    Label_Notes3.grid(row=11,column=0,columnspan=2,sticky=W)

    frame3=Frame(win_ANRCAM)
    frame3.grid(row=12,column=0,columnspan=6,sticky=W)

    Label_ActivationFunction = Label(frame3, text='Function:')
    Label_ActivationFunction.grid(row=0,column=0,sticky=E,pady=5)
    # 選單:tanh,sigmoid,sin
    Combobox_Funct = ttk.Combobox(frame3, values=[ "tanh(x)","sigmoid(x)","sin(x)"], state='readonly', width=18)
    Combobox_Funct.grid(row=0,column=1,columnspan=2,sticky=W,pady=5,padx=5)
    Combobox_Funct.current(0)

    # command=lambda:threadit(ShowFig,figPathName)/command=lambda:ShowFig(figPathName)
    Button_ShowFig = Button(frame3, text='Show Fig', bg="LightBlue", width=10, command=lambda:ShowFig())
    Button_ShowFig.grid(row=0,column=3,sticky=E,pady=5)

    Button_Gen = Button(frame3, text='Generate', bg="LightBlue", width=10, command=Gen)
    Button_Gen.grid(row=0,column=4,sticky=W,pady=5,padx=5)

    Button_VCD = Button(frame3, text='VCD', bg="LightBlue", command=lambda: VCD(filePathName), width=10)
    Button_VCD.grid(row=0,column=5,sticky=W,pady=5)

    Button_plt = Button(frame3, text='Plt fig', bg="LightBlue", command=lambda:Pltfig(figPathName), width=10)
    Button_plt.grid(row=0,column=6,sticky=W,pady=5,padx=5)

    # #win_ANRCAM(row=12,column=0
    Label_ErrorModel = Label(frame3, text='Error Model:')
    Label_ErrorModel.grid(row=1,column=0,sticky=E,pady=5)

    Combobox_ErrorModel = ttk.Combobox(frame3, values=["Uni HL","Uni LH","Alter","BER","AWE"], state='readonly', width=18)
    Combobox_ErrorModel.grid(row=1,column=1,columnspan=2,sticky=W,pady=5,padx=5)
    Combobox_ErrorModel.current(0)
    #
    Label_A = Label(frame3, text='A should be:')
    Label_A.grid(row=1,column=3,sticky=E,pady=5)

    Entry_A = Entry(frame3,width=11,textvariable=NumA)
    Entry_A.grid(row=1,column=4,sticky=W,pady=5,padx=5)
    #
    Button_Openfile = Button(frame3, text='Open File', bg="LightBlue", command=Openfile, width=10)
    Button_Openfile.grid(row=1,column=5,sticky=E,pady=5)
    #
    Button_Exit = Button(frame3, text='EXIT', bg="pink", width=10, command=win_ANRCAM.destroy) #關閉GUI and 退出TCL #正常大小 (win_ANRCAM.destroy#只關閉GUI)
    Button_Exit.grid(row=1,column=6,sticky=W,pady=5,padx=5) #正常大小
    #
# Call EDA
def EDA():
    print("EDA")
# ##
menu = Menu(root)              
root.config(menu=menu)
filemenu = Menu(menu,tearoff=0)               
menu.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="Open File...",command=Openfile)
filemenu.add_separator() 
filemenu.add_command(label="Exit",command=root.destroy)
filemenu.add_command(label="Quit",command=root.quit)
#
helpmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Help",menu=helpmenu)
# helpmenu.add_command(label="Help",command=Help)
helpmenu.add_command(label="Demo Video",command=Video)
helpmenu.add_separator() 
helpmenu.add_command(label="About",command=about)
###
Label_Notes0 = Label(root, text='Error Correctable Range-Addressable Lookup for Any Activation Function of Neural Networks',bg="LightSkyBlue")
Label_Notes0.pack(fill=X)
Label_Author = Label(root, text='Ting-Yu Chen')
Label_Author.pack()
Label_Lab = Label(root, text='Test Lab, Electronic Engineering, NCUE')
Label_Lab.pack()
# global fig_Note1
# fig_Notes1=PhotoImage(file="./001.png")
# Label_Notes1 = Label(root, image=fig_Notes1)
# Label_Notes1.pack(pady=5)
Note_abs="　　隨著科技的發展，人工智慧對人類越來越重要，\
而神經網路是其中最重要的一種計算模型，在這個計算模型中，\
激勵函數是不可或缺的函數，若沒有它，將會使其計算出來的數據為線性的組合，\
無法貼近現實。\n\n　　在本篇論文中，我們提出了輕數斜率線性分段範圍可尋址查表\
(Light-Slope Piecewise-Linear Range-Addressable Lookup Table, LS-PWL-RALUT)，\
讓其得以在激勵函數中去進行有效率的近似計算，並且我們提出一種使用AN codes的在線糾錯算法\
和電路，來提升神經網路的可靠度。\n\n　　我們使用BLER/SNR模擬實驗去證明我們提出的AN codes編碼\
神經元的單一錯誤更正(SEC)能力。與其他最先進及類似的工作的比較，可以得知\
在 8-12 bits中等分辨率的任何激勵函數下，我們所提出的技術是最有效且可糾錯的查表方式。"
frame1=Frame(root)
frame1.pack(pady=5)
Text_Notes1 = Text(frame1,height=12,wrap=CHAR)
Text_Notes1.insert(END,Note_abs)
scrollbarY = Scrollbar(frame1)
Text_Notes1.config(yscrollcommand=scrollbarY.set)
Text_Notes1.pack(side=LEFT,fill=Y)
scrollbarY.pack(side=RIGHT,fill=Y)
#
frame2=Frame(root)
frame2.pack()
Button_Proj1 = Button(frame2, text='AN codes', command=GUIANcodes, bg="Lightskyblue", width=20)
Button_Proj1.pack(side=LEFT,pady=5,padx=10)

Button_Proj2 = Button(frame2, text='ANRCAM', command=GUIANRCAM, bg="Lightskyblue", width=20)
Button_Proj2.pack(side=LEFT,pady=5,padx=10)

Button_Proj3 = Button(frame2, text='EDA', command=EDA, bg="Lightskyblue", width=20)
Button_Proj3.pack(side=LEFT,pady=5,padx=10)

root.mainloop()
