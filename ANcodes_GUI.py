from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from MyDef import *
#
root = Tk()
root.title('AN codes')
root.geometry('1000x185')
# print(root.winfo_screenwidth()) #輸出螢幕寬度
# print(root.winfo_screenheight())
# root.resizable(False,False)
#
window_width1=90
#
BitN = IntVar() 
FindA1 = IntVar() 
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
            Text_R.delete(1.0,END) 
            Text_R.insert(END,str(Ra_array))
        else:
            findA_Two,cbitN_Two=AutoFindA(0,BitN.get(),Two_A,Two_cbit_N)
            FindA1.set(findA_Two)
            strAN_A_N=str(int((findA_Two-1)/2))+', '+str(int((findA_Two-1)/2)-cbitN_Two)+', '+str(cbitN_Two)
            BitAN_A_N.set(strAN_A_N)
            Ra_array,Ta_array,Sa_array=TableTwo(findA_Two)
            index_R=int(len(Ra_array)/2)
            Text_R.delete(1.0,END) 
            Text_R.insert(END,str(Ra_array[:index_R])+'\n')
            Text_R.insert(END,str(Ra_array[index_R:]))
            
        
    else:
        messagebox.showwarning("BitN Error","You should enter the bit of N!")
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
Label_R = Label(root, text="餘數表為: ",font=("微軟正黑體",12))
Label_R.grid(row=4,column=0,sticky=N+E)

Text_R = Text(root,font=("微軟正黑體",12),width=window_width1,height=2)
Text_R.grid(row=4,column=1)

scrollbarY = Scrollbar(root, orient='vertical')
scrollbarY.grid(row=4,column=2,sticky=N+S)
scrollbarY.config(command=Text_R.yview)
# Row5
scrollbarX = Scrollbar(root, orient='horizontal')
scrollbarX.grid(row=5,column=1,sticky=W+E)
scrollbarX.config(command=Text_R.xview)

#
root.mainloop() 