from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from MyDef import *
import numpy as np
#
root = Tk()
root.title('AN codes')
root.geometry('460x360')
#
window_width1=20
#
BitN = IntVar() 
FindA1 = IntVar() 
N1 = IntVar() 
AN1 = IntVar() 
errorbit = IntVar() 
Mod1 = IntVar() 
Finderrorbit = IntVar()
ANc = IntVar()
Nc = IntVar()
AN12 = StringVar() 
ANe2 = StringVar() 
BitAN_A_N = StringVar() 
# def
def AList(event):
    mode=1
    if (BitN.get()!=0):
        Two_A,Two_cbit_N,One_A,One_cbit_N=FindA(mode,200)
        if Combobox_Model.current() < 3:
            findA_One,cbitN_One=AutoFindA(1,BitN.get(),One_A,One_cbit_N)
            FindA1.set(findA_One)
            strAN_A_N=str(findA_One-1)+', '+str(findA_One-1-cbitN_One)+', '+str(cbitN_One)
            BitAN_A_N.set(strAN_A_N)
            Ra_array,Ta_array=TableOne(findA_One)
        else:
            findA_Two,cbitN_Two=AutoFindA(0,BitN.get(),Two_A,Two_cbit_N)
            FindA1.set(findA_Two)
            strAN_A_N=str(int((findA_Two-1)/2))+', '+str(int((findA_Two-1)/2)-cbitN_Two)+', '+str(cbitN_Two)
            BitAN_A_N.set(strAN_A_N)
            Ra_array,Ta_array,Sa_array=TableTwo(findA_Two)
            index_R=int(len(Ra_array)/2)
            
    else:
        messagebox.showwarning("BitN Error","You should enter the bit of N!")
#
def gen():
    BitAll=(BitAN_A_N.get()).split(",")
    BitN_gen=int(BitAll[-1])
    NumN=np.random.randint(0,2**BitN_gen)
    N1.set(NumN)
    NumNxA=NumN*FindA1.get()
    AN1.set(NumNxA)
    NumNxA2=(bin(NumNxA)[2:]).zfill(int(BitAll[0]))
    Text_AN2.delete(1.0,END) 
    Text_AN2.insert(END,str(NumNxA2))
#
def AddError():
    if FindA1.get() != 0:
        index=errorbit.get()
        BitAll=(BitAN_A_N.get()).split(",")
        BitAN_e=int(BitAll[0])
        index11=BitAN_e-index-1
        AN=list(Text_AN2.get("1.0","end"))[:-1]
        if AN[index11] == "1":
            AN[index11] = "0"
        else:
            AN[index11] = "1"
        ANe22=''.join(AN)
        Text_ANe2.delete(1.0,END) 
        Text_ANe2.insert(END,str(ANe22))
        ANe22_DEC=int(ANe22,2)
        #####
        RR1=ANe22_DEC%FindA1.get()
        Mod1.set(RR1)
        # correct
        if Combobox_Model.current() == 0:
            Ra_array,Ta_array=TableOne(FindA1.get())
            Febit=Ta_array[RR1]
            Nc11_bin=CorrectHL(BitAN_e,ANe22_DEC,FindA1.get(),Ra_array,Ta_array,Sa_array)
            Nc11=Bin2Dec(BitAN_e, Nc11_bin)
            ANc11=Nc11*FindA1.get()

        if Combobox_Model.current() == 1:
            Ra_array,Ta_array=TableOne(FindA1.get())
            Febit=Ta_array[RR1]
            Nc11_bin=CorrectLH(BitAN_e,ANe22_DEC,FindA1.get(),Ra_array,Ta_array,Sa_array)
            Nc11=Bin2Dec(BitAN_e, Nc11_bin)
            ANc11=Nc11*FindA1.get()

        if Combobox_Model.current() == 2:
            Ra_array,Ta_array=TableOne(FindA1.get())
            Febit=Ta_array[RR1]
            Nc11_bin=CorrectUni(BitAN_e,ANe22_DEC,FindA1.get(),Ra_array,Ta_array,Sa_array)
            Nc11=Bin2Dec(BitAN_e, Nc11_bin)
            ANc11=Nc11*FindA1.get()

        if Combobox_Model.current() == 3:
            Ra_array,Ta_array,Sa_array=TableTwo(FindA1.get())
            Febit=Ta_array[RR1]
            Nc11_bin=CorrectBER(BitAN_e,ANe22_DEC,FindA1.get(),Ra_array,Ta_array,Sa_array)
            Nc11=Bin2Dec(BitAN_e, Nc11_bin)
            ANc11=Nc11*FindA1.get()
     
        if Combobox_Model.current() == 4:            
            Ra_array,Ta_array,Sa_array=TableTwo(FindA1.get())
            Febit=Ta_array[RR1]
            Nc11_bin=CorrectAWE(BitAN_e,ANe22_DEC,FindA1.get(),Ra_array,Ta_array,Sa_array)
            Nc11=Bin2Dec(BitAN_e, Nc11_bin)
            ANc11=Nc11*FindA1.get()
        Finderrorbit.set(Febit)
        Nc.set(Nc11)
        ANc.set(ANc11)
#

# Row0
Label_Nbit = Label(root, text="請輸入N值的位元: ",font=("微軟正黑體",12))
Label_Nbit.grid(row=0,column=0,sticky=E)

Entry_Nbit = Entry(root, textvariable=BitN,font=("微軟正黑體",12),width=window_width1)
Entry_Nbit.grid(row=0,column=1,sticky=W)
# Row1
Label_Model = Label(root, text="Error Models: ",font=("微軟正黑體",12))
Label_Model.grid(row=1,column=0,sticky=E)

Combobox_Model = ttk.Combobox(root, values=[ "Uni HL","Uni LH","Alter","BER","AWE"], state='readonly', width=(window_width1-2),font=("微軟正黑體",12))
Combobox_Model.grid(row=1,column=1,sticky=W,pady=5)
Combobox_Model.current(0)
Combobox_Model.bind('<<ComboboxSelected>>', AList)
# Row2
Label_FindA = Label(root, text="最小可適用的A值: ",font=("微軟正黑體",12))
Label_FindA.grid(row=2,column=0,sticky=E)

Entry_FindA = Entry(root, textvariable=FindA1,font=("微軟正黑體",12),width=window_width1)
Entry_FindA.grid(row=2,column=1,sticky=W)
# Row3
Label_BitAN = Label(root, text="可更正位元(AN, A, N): ",font=("微軟正黑體",12))
Label_BitAN.grid(row=3,column=0,sticky=E)

Entry_BitAN = Entry(root, textvariable=BitAN_A_N,font=("微軟正黑體",12),width=window_width1)
Entry_BitAN.grid(row=3,column=1,sticky=W)
# Row4
sep1=ttk.Separator(root,orient='horizontal')
sep1.grid(row=4,column=0,columnspan=3,sticky=W+E)
# Row5
Label_N = Label(root, text="隨機N值: ",font=("微軟正黑體",12))
Label_N.grid(row=5,column=0,sticky=E)

Entry_N = Entry(root, textvariable=N1,font=("微軟正黑體",12),width=window_width1)
Entry_N.grid(row=5,column=1,sticky=W)

Button_Gen = Button(root,text='generate',command=gen,width=10)
Button_Gen.grid(row=5,column=2,sticky=W)
# Row6
Label_AN = Label(root, text="編碼AN值(d): ",font=("微軟正黑體",12))
Label_AN.grid(row=6,column=0,sticky=E)

Entry_AN = Entry(root, textvariable=AN1,font=("微軟正黑體",12),width=window_width1)
Entry_AN.grid(row=6,column=1,sticky=W)
# Row7
# frame1=Frame(root)
# frame1.grid(row=7,column=0,columnspan=3,sticky=W+E)
Label_AN2 = Label(root, text="編碼AN值(b): ",font=("微軟正黑體",12))
Label_AN2.grid(row=7,column=0,sticky=E)

Text_AN2 = Text(root,font=("微軟正黑體",12),width=window_width1,height=1)
Text_AN2.grid(row=7,column=1,sticky=W)
# Row8
Label_errorbit = Label(root, text="錯誤位元: ",font=("微軟正黑體",12))
Label_errorbit.grid(row=8,column=0,sticky=E)

Entry_errorbit = Entry(root, textvariable=errorbit,font=("微軟正黑體",12),width=window_width1)
Entry_errorbit.grid(row=8,column=1,sticky=W)

Button_AddError = Button(root,text='Add error',command=AddError,width=10)
Button_AddError.grid(row=8,column=2,sticky=W)
# Row9
Label_ANe2 = Label(root, text="錯誤AN值(b): ",font=("微軟正黑體",12))
Label_ANe2.grid(row=9,column=0,sticky=E)

Text_ANe2 = Text(root,font=("微軟正黑體",12),width=window_width1,height=1)
Text_ANe2.grid(row=9,column=1,sticky=W)
# Row10
sep2=ttk.Separator(root,orient='horizontal')
sep2.grid(row=10,column=0,columnspan=3,sticky=W+E)
#Row11
Label_Mod = Label(root, text="餘數為: ",font=("微軟正黑體",12))
Label_Mod.grid(row=11,column=0,sticky=E)

Entry_Mod = Entry(root, textvariable=Mod1,font=("微軟正黑體",12),width=window_width1)
Entry_Mod.grid(row=11,column=1,sticky=W)
# Row12
Label_Finderrorbit = Label(root, text="對應之錯誤位元: ",font=("微軟正黑體",12))
Label_Finderrorbit.grid(row=12,column=0,sticky=E)

Entry_Finderrorbit = Entry(root, textvariable=Finderrorbit,font=("微軟正黑體",12),width=window_width1)
Entry_Finderrorbit.grid(row=12,column=1,sticky=W)
#Row13
Label_ANc = Label(root, text="更正後AN值(d): ",font=("微軟正黑體",12))
Label_ANc.grid(row=13,column=0,sticky=E)

Entry_ANc = Entry(root, textvariable=ANc,font=("微軟正黑體",12),width=window_width1)
Entry_ANc.grid(row=13,column=1,sticky=W)
#Row14
Label_Nc = Label(root, text="更正後N值(d): ",font=("微軟正黑體",12))
Label_Nc.grid(row=14,column=0,sticky=E)

Entry_Nc = Entry(root, textvariable=Nc,font=("微軟正黑體",12),width=window_width1)
Entry_Nc.grid(row=14,column=1,sticky=W)

root.mainloop() 