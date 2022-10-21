import numpy as np
import os
import time
####---------------------------------------------------------####
def Bin2Dec(bit, Bin):
    A=0
    Bin=list(Bin)
    Bin.reverse()
    for i in range(0,bit):
        A=Bin[i]*2**(i)+A
    return A
####----------------------####
def Dec2Bin(bit, Dec):
    binrandom0 = bin(Dec)
    d1=binrandom0[2:]                   #ex.1111
    h2=d1.zfill(bit)                    #ex.00001111
    data=list(h2)                       #turn to list: ex.['0', '0', '0', '0', '1', '1', '1', '1']
    arrayh=np.array(data)               #ex.['0' '0' '0' '0' '1' '1' '1' '1']
    arrayh=arrayh.astype(int)           #del'' ex.[0 0 0 0 1 1 1 1]
    return arrayh
####-----------------------table-----------------------------####
#One-way error:Uni or Alter
def TableOne(module):  
    Ra=[0]*(module-1) #R:1-46
    Ta=[0]*module
    Ra_array=np.array(Ra)
    Ta_array=np.array(Ta)
    Ra_array[0]=1  #R:1
    for i in range(1,module-1):#1-45(<-扣掉R:1)
        Ra_array[i]=(Ra_array[i-1]*2) % module
        Ta_array[Ra_array[i]]=i
    return Ra_array,Ta_array
####----------------------####
#Two-way error:AWE or BER
def TableTwo(module):  
    Ra=[0]*(module-1) #R:1-46
    Ta=[0]*module
    Sa=[0]*module
    Ra_array=np.array(Ra)
    Ta_array=np.array(Ta)
    Sa_array=np.array(Sa)
    Ra_array[0]=1
    for i in range(1,module-1): #1-45(<-扣掉R:1)
        Ra_array[int((module-1)/2)]=(module-1)
        #Ra_array[23]=46
        Ra_array[i]=(Ra_array[i-1]*2) % module
        if(i<((module-1)/2)):
            Ta_array[Ra_array[i]]=i
            Sa_array[Ra_array[i]]=0
        else:
            Ta_array[Ra_array[i]]=i-((module-1)/2)
            Sa_array[Ra_array[i]]=1
    Sa_array[1]=0
    Sa_array[(module-1)]=1
    return Ra_array,Ta_array,Sa_array
####------------------Auto-Find-A----------------------------####
def FindA(mode,rang2):
    Two_A=[]
    Two_A_bit=[]
    Two_cbit=[]
    Two_cbit_N=[]
    One_A=[]
    One_A_bit=[]
    One_cbit=[]
    One_cbit_N=[]    
    rang1=8
    for module in range(rang1,(rang2+1)):
            Ra_array,Ta_array,Sa_array=TableTwo(module)
            Ra2_array,Ta2_array=TableOne(module)
            module_2=bin(module)[2:]
            module_len=len(module_2)
            count=0
            for i in range(1, module):
                if i in Ra_array:
                    count+=1
            check=set(Ra_array)
            if count == (module-1) and len(Ra_array) == len(check):
                Two_A.append(module)
                maxT=max(Ta_array)
                cbit=maxT+1
                Two_cbit.append(cbit)
                cbitN=cbit-module_len
                Two_cbit_N.append(cbitN)
                Two_A_bit.append(module_len)         
            count2=0
            for i2 in range(1, module):
                if i2 in Ra2_array:
                    count2+=1
            check2=set(Ra2_array)
            if count2 == (module-1) and len(Ra2_array) == len(check2):
                One_A.append(module)
                maxT2=max(Ta2_array)
                cbit2=maxT2+1
                One_cbit.append(cbit2)
                cbitN2=cbit2-module_len
                One_cbit_N.append(cbitN2)
                One_A_bit.append(module_len)
    #################################################
    #the same bit of A select which can correct more 
    bitA=Two_A_bit[-1] +1
    Two_A_bit_len=len(Two_A_bit)
    Two_A_most=[]
    for j in range(0,bitA): #Value content
        t1=[]
        for k in range(0,Two_A_bit_len):#Array position    
            if Two_A_bit[k]==j:
                t1.append(Two_A[k])
        if len(t1) > 1:
            t1max=max(t1)
            Two_A_most.append(t1max)
        elif len(t1) == 1:
            Two_A_most.append(t1[0])
    Two_A_most_cbitN=[]
    for g in range(0,len(Two_A_most)):
        t2=Two_A_most[g]
        Two_most_index=Two_A.index(t2)
        t3=Two_cbit_N[Two_most_index]
        Two_A_most_cbitN.append(t3)
    #################################################
    bitA_One=One_A_bit[-1] +1
    One_A_bit_len=len(One_A_bit)
    One_A_most=[]
    for j1 in range(0,bitA_One):
        t1One=[]
        for k1 in range(0,One_A_bit_len):   
            if One_A_bit[k1]==j1:
                t1One.append(One_A[k1])
        if len(t1One) > 1:
            t1maxOne=max(t1One)
            One_A_most.append(t1maxOne)
        elif len(t1One) == 1:
            One_A_most.append(t1One[0])
    One_A_most_cbitN=[]
    for g1 in range(0,len(One_A_most)):
        t2One=One_A_most[g1]
        One_most_index=One_A.index(t2One)
        t3One=One_cbit_N[One_most_index]
        One_A_most_cbitN.append(t3One)
    #################################################
    if mode == 1:
        return Two_A,Two_cbit_N,One_A,One_cbit_N
    #################################################
    else:
        return Two_A_most,Two_A_most_cbitN,One_A_most,One_A_most_cbitN
####----------------------####
def Show_A_TEXT(rang2, show_correct_bit):
    txt_A=""
    Two_A=[]
    Two_A_bit=[]
    Two_cbit=[]
    Two_cbit_N=[]
    One_A=[]
    One_A_bit=[]
    One_cbit=[]
    One_cbit_N=[]    
    rang1=8
    for module in range(rang1,(rang2+1)):
            Ra_array,Ta_array,Sa_array=TableTwo(module)
            Ra2_array,Ta2_array=TableOne(module)
            module_2=bin(module)[2:]
            module_len=len(module_2)
            count=0
            for i in range(1, module):
                if i in Ra_array:
                    count+=1
            check=set(Ra_array)
            if count == (module-1) and len(Ra_array) == len(check):
                Two_A.append(module)
                maxT=max(Ta_array)
                cbit=maxT+1
                Two_cbit.append(cbit)
                cbitN=cbit-module_len
                Two_cbit_N.append(cbitN)
                Two_A_bit.append(module_len)         
            count2=0
            for i2 in range(1, module):
                if i2 in Ra2_array:
                    count2+=1
            check2=set(Ra2_array)
            if count2 == (module-1) and len(Ra2_array) == len(check2):
                One_A.append(module)
                maxT2=max(Ta2_array)
                cbit2=maxT2+1
                One_cbit.append(cbit2)
                cbitN2=cbit2-module_len
                One_cbit_N.append(cbitN2)
                One_A_bit.append(module_len)
    #################################################
    bitA=Two_A_bit[-1] +1
    Two_A_bit_len=len(Two_A_bit)
    Two_A_most=[]
    for j in range(0,bitA):
        t1=[]
        for k in range(0,Two_A_bit_len):  
            if Two_A_bit[k]==j:
                t1.append(Two_A[k])
        if len(t1) > 1:
            t1max=max(t1)
            Two_A_most.append(t1max)
        elif len(t1) == 1:
            Two_A_most.append(t1[0])
    Two_A_most_cbitN=[]
    for g in range(0,len(Two_A_most)):
        t2=Two_A_most[g]
        Two_most_index=Two_A.index(t2)
        t3=Two_cbit_N[Two_most_index]
        Two_A_most_cbitN.append(t3)
    #################################################
    bitA_One=One_A_bit[-1] +1
    One_A_bit_len=len(One_A_bit)
    One_A_most=[]
    for j1 in range(0,bitA_One):
        t1One=[]
        for k1 in range(0,One_A_bit_len):   
            if One_A_bit[k1]==j1:
                t1One.append(One_A[k1])
        if len(t1One) > 1:
            t1maxOne=max(t1One)
            One_A_most.append(t1maxOne)
        elif len(t1One) == 1:
            One_A_most.append(t1One[0])
    One_A_most_cbitN=[]
    for g1 in range(0,len(One_A_most)):
        t2One=One_A_most[g1]
        One_most_index=One_A.index(t2One)
        t3One=One_cbit_N[One_most_index]
        One_A_most_cbitN.append(t3One)
    #################################################
    txt_A=txt_A+'-------------Find an available A-------------\n'\
    +'雙向錯誤可用的A(%d~%d)=%s\n'%(rang1,rang2,Two_A)\
    +'單向錯誤可用的A(%d~%d)=%s\n'%(rang1,rang2,One_A)\
    +'-------------Find the most appropriate A-------------\n'\
    +"雙向錯誤最合適的A=%s\n"%Two_A_most\
    +"單向錯誤最合適的A=%s\n"%One_A_most
    txt_A_split=txt_A.split("\n")
    if show_correct_bit == 1:
        txt_A_split.insert(2,"可更正bit數(N)=%s"%Two_cbit_N)
        txt_A_split.insert(4,"可更正bit數(N)=%s\n"%One_cbit_N)
        txt_A_split.insert(7,"可更正bit數(N)=%s"%Two_A_most_cbitN)
        txt_A_split.insert(9,"可更正bit數(N)=%s"%One_A_most_cbitN)
    final_string = '\n'.join(txt_A_split)
    print(final_string)
####----------------------####
def AutoFindA(model,BitN_input,A,cbitN):    
    if model == 1 :
        print('----------Single R Ring----------') #取名取相反了one<=>two
        Two_A=A
        Two_cbit_N=cbitN
        if BitN_input in Two_cbit_N: #剛好有對應的樹
            x_Two=Two_cbit_N.index(BitN_input)
            findA_Two=Two_A[x_Two]
            print('適合的A=',findA_Two)
            print('可更正的bit數(N)=',Two_cbit_N[x_Two])
            return findA_Two,Two_cbit_N[x_Two]
        else:   #大於Nbit的最小數
            Two_cbit_N_a=np.array(Two_cbit_N)
            index_Two=(np.abs(Two_cbit_N_a-BitN_input)).argmin()
            findA2_Two=Two_A[index_Two]
            if BitN_input < index_Two :
                print('適合的A=',findA2_Two)
                print('可更正的bit數(N)=',Two_cbit_N[index_Two])
                return findA2_Two,Two_cbit_N[index_Two]
            else:
                findA3_Two=Two_A[(index_Two+1)]
                print('適合的A=',findA3_Two)
                print('可更正的bit數(N)=',Two_cbit_N[(index_Two+1)])
                return findA3_Two,Two_cbit_N[(index_Two+1)]
    else :
        print('----------Double R Ring----------')
        One_A=A
        One_cbit_N=cbitN
        if BitN_input in One_cbit_N: #剛好有對應的樹
            x_One=One_cbit_N.index(BitN_input)
            findA_One=One_A[x_One]
            print('適合的A=',findA_One)
            print('可更正的bit數(N)=',One_cbit_N[x_One])
            return findA_One,One_cbit_N[x_One]
        else:   #大於Nbit的最小數
            One_cbit_N_a=np.array(One_cbit_N)
            index_One=(np.abs(One_cbit_N_a-BitN_input)).argmin()
            findA2_One=One_A[index_One]
            if BitN_input < index_One :
                print('適合的A=',findA2_One)
                print('可更正的bit數(N)=',One_cbit_N[index_One])
                return findA2_One,One_cbit_N[index_One]
            else:
                findA3_One=One_A[(index_One+1)]
                print('適合的A=',findA3_One)    
                print('可更正的bit數(N)=',One_cbit_N[(index_One+1)])
                return findA3_One,One_cbit_N[(index_One+1)]
####------------------Error-----------------------------####
def errorGenTwo(bitAN,module,N):
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    ebit=np.random.randint(0,bitAN)
    ebitp=bitAN-(ebit+1)
    if AN2_0List[ebit] == '0':
        AN2_0List[ebit] = '1'
    else:
        AN2_0List[ebit] = '0'
    ANe2=''.join(AN2_0List)
    ANe=int(ANe2,2)
    R=ANe%module
    print('---------Original Data-------------')
    print("A\tN\tAN\tAN2\n%d\t%d\t%d\t%s\t"%(module,N,AN,AN2_0))
    print('------Random error generation------')
    print("R\tebit\tANe\tANe2\n%d\t%d\t%d\t%s\t"%(R,ebitp,ANe,ANe2))
    return ANe,ANe2,ebit
####----------------------####
def TestforAllErrorAWE(bitAN,module,N):
    ANe_list=[]
    ebit_list=[]
    R_list=[]
    AN=module*N
    for i in range(bitAN):
        ANe_num=AN+2**i
        ANe_list.append(ANe_num)
        ebit_list.append(i)
        R_list.append(ANe_num%module)
    for j in range(bitAN):
        ANe_num=AN-2**j
        ANe_list.append(ANe_num)
        ebit_list.append(j)
        R_list.append(ANe_num%module)
    # 應該要確認位元是否只有一位變化? # 好像不引響 # 去除負數
    return ANe_list,ebit_list,R_list
####----------------------####
def TestforAllErrorBER(bitAN,module,N):
    ANe_list=[]
    ebit_list=[]
    R_list=[]
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    for i in range(bitAN-1,-1,-1): # 0->1
        AN2_0List_e=AN2_0List.copy()
        if AN2_0List[i] == '0':
            AN2_0List_e[i] = '1'
            ANe2=''.join(AN2_0List_e)
            ANe_num=int(ANe2,2)
            ANe_list.append(ANe_num)
            ebit_list.append(bitAN-i-1)
            R_list.append(ANe_num%module)
    for j in range(bitAN-1,-1,-1): # 1->0
        AN2_0List_e=AN2_0List.copy()
        if AN2_0List[j] == '1':
            AN2_0List_e[j] = '0'
            ANe2=''.join(AN2_0List_e)
            ANe_num=int(ANe2,2)
            ANe_list.append(ANe_num)
            ebit_list.append(bitAN-j-1)
            R_list.append(ANe_num%module)
    return ANe_list,ebit_list,R_list
####----------------------####
def TestforAllErrorAlter(bitAN,module,N): #verilog未寫出error bit #效果不好
    ANe_list=[]
    ebit_list=[]
    R_list=[]
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    for i in range(bitAN-1,-1,-1):
        AN2_0List_e=AN2_0List.copy()
        if AN2_0List[i] == '0':
            AN2_0List_e[i] = '1'
            ANe2=''.join(AN2_0List_e)
            ANe_num=int(ANe2,2)
            ANe_list.append(ANe_num)
            ebit_list.append(bitAN-i-1)
            R_list.append(ANe_num%module)
    for j in range(bitAN-1,-1,-1):
        AN2_0List_e=AN2_0List.copy()
        if AN2_0List[j] == '1':
            AN2_0List_e[j] = '0'
            ANe2=''.join(AN2_0List_e)
            ANe_num=int(ANe2,2)
            ANe_list.append(ANe_num)
            ebit_list.append(bitAN-j-1)
            R_list.append(ANe_num%module)
    return ANe_list,ebit_list,R_list
####----------------------####
def TestforAllErrorHL(bitAN,module,N): 
    ANe_list=[]
    ebit_list=[]
    R_list=[]
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    for j in range(bitAN-1,-1,-1):
        AN2_0List_e=AN2_0List.copy()
        if AN2_0List[j] == '1':
            AN2_0List_e[j] = '0'
            ANe2=''.join(AN2_0List_e)
            ANe_num=int(ANe2,2)
            ANe_list.append(ANe_num)
            ebit_list.append(bitAN-j-1)
            R_list.append(ANe_num%module)
    return ANe_list,ebit_list,R_list
####----------------------####
def TestforAllErrorLH(bitAN,module,N): 
    ANe_list=[]
    ebit_list=[]
    R_list=[]
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    for i in range(bitAN-1,-1,-1):
        AN2_0List_e=AN2_0List.copy()
        if AN2_0List[i] == '0':
            AN2_0List_e[i] = '1'
            ANe2=''.join(AN2_0List_e)
            ANe_num=int(ANe2,2)
            ANe_list.append(ANe_num)
            ebit_list.append(bitAN-i-1)
            R_list.append(ANe_num%module)
    return ANe_list,ebit_list,R_list
####----------------------#### 
def errorGenLH(bitAN,module,N):
    cnt=0
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    while cnt < 1:
        ebit=np.random.randint(0,bitAN)
        ebitp=bitAN-(ebit+1)
        if AN2_0List[ebit] == '0':
            AN2_0List[ebit] = '1'
            cnt+=1
    ANe2=''.join(AN2_0List)
    ANe=int(ANe2,2)
    R=ANe%module
    print('---------Original Data-------------')
    print("A\tN\tAN\tAN2\n%d\t%d\t%d\t%s\t"%(module,N,AN,AN2_0))
    print('------Random error generation------')
    print("R\tebit\tANe\tANe2\n%d\t%d\t%d\t%s\t"%(R,ebitp,ANe,ANe2))
    return ANe,ANe2,ebit
####----------------------####
def errorGenHL(bitAN,module,N):
    cnt=0
    AN=module*N
    AN2=bin(AN)[2:]
    AN2_0=AN2.zfill(bitAN)
    AN2_0List=list(AN2_0)
    while cnt < 1:
        ebit=np.random.randint(0,bitAN)
        ebitp=bitAN-(ebit+1)
        if AN2_0List[ebit] == '1':
            AN2_0List[ebit] = '0'
            cnt+=1
    ANe2=''.join(AN2_0List)
    ANe=int(ANe2,2)
    R=ANe%module
    print('---------Original Data-------------')
    print("A\tN\tAN\tAN2\n%d\t%d\t%d\t%s\t"%(module,N,AN,AN2_0))
    print('------Random error generation------')
    print("R\tebit\tANe\tANe2\n%d\t%d\t%d\t%s\t"%(R,ebitp,ANe,ANe2))
    return ANe,ANe2,ebit   
####------------------correction-----------------------------#### 
def CorrectAWE(bit,data,module,Ra_array,Ta_array,Sa_array):
    ErrorWay=""
    bitAN=int((module-1)/2)# 13->13-1=12, 12/2=6
    R=data % module
    print('-----------Correct AWE---------------------------')
    for i in range(1,bit):
        databin=Dec2Bin(bit, data)
        bitint=int(bit)        #if no int(bit) #when bit=36, 2^bit=0 #I do not know why.
        pow2Bit=pow(2,bitint)
        if data < pow2Bit:              
            if(R==0):
                final_answer=int(data/module)
                final_answer_bin=Dec2Bin(bit, final_answer)
                print('There is no error.')
                return final_answer_bin
            elif R in Ra_array:   
                errorbit=Ta_array[R]
                data_B2D=Bin2Dec(bit,databin)
                errValue=2**(errorbit)
                if(Sa_array[R]==0):
                    if(errValue>data_B2D):
                        print('Error cannot be detected.')
                        return databin
                    else:
                        ErrorWay="Addition"
                        dec_data=data_B2D-errValue
                else:
                    if(data_B2D+errValue > 2**bit):
                        print('Error cannot be detected.')
                        return databin
                    else:
                        ErrorWay="Subtraction"
                        dec_data=data_B2D+errValue
                #############################
                if(dec_data % module==0):
                    ANc2=(bin(dec_data)[2:]).zfill(bitAN)
                    final_answer=int(dec_data/module)
                    final_answer_bin=Dec2Bin(bit, final_answer)
                    print("R\tebit\tANc\tANc2\t\tNc\tError way\n%d\t%d\t%d\t%s\t%d\t%s"%(R,errorbit,dec_data,ANc2,final_answer,ErrorWay))
                    return final_answer_bin
                else:
                    print('Error cannot be detected.')
                    return databin
        else:                                   #超過範圍直接輸出
                print('Error cannot be detected')
                return databin
####----------------------####
def CorrectBER(bit,data,module,Ra_array,Ta_array,Sa_array):
    bitAN=int((module-1)/2)# 13->13-1=12, 12/2=6
    R=data % module
    print('-----------Correct BER---------------------------')
    for i in range(1,bit):
        databin=Dec2Bin(bit, data)
        bitint=int(bit)        #if no int(bit) #when bit=36, 2^bit=0 #I do not know why.
        pow2Bit=pow(2,bitint)
        if data < pow2Bit:              
            if(R==0):
                final_answer=int(data/module)
                final_answer_bin=Dec2Bin(bit, final_answer)
                print('There is no error.')
                return final_answer_bin
            elif R in Ra_array:   
                errorbit=Ta_array[R]
                data_B2D=Bin2Dec(bit,databin)
                errValue=2**(errorbit)
                if(Sa_array[R]==0):
                    if(errValue>data_B2D):
                        print('Error cannot be detected.')
                        return databin
                    else:
                        ErrorWay="Addition"
                        dec_data=data_B2D-errValue
                else:
                    if(data_B2D+errValue > 2**bit):
                        print('Error cannot be detected.')
                        return databin
                    else:
                        ErrorWay="Subtraction"
                        dec_data=data_B2D+errValue
                #############################
                if(dec_data % module==0):
                    ANc2=(bin(dec_data)[2:]).zfill(bitAN)
                    final_answer=int(dec_data/module)
                    final_answer_bin=Dec2Bin(bit, final_answer)
                    print("R\tebit\tANc\tANc2\t\tNc\n%d\t%d\t%d\t%s\t%d"%(R,errorbit,dec_data,ANc2,final_answer))
                    return final_answer_bin
                else:
                    print('Error cannot be detected.')
                    return databin
        else:                                   #超過範圍直接輸出
                print('Error cannot be detected')
                return databin
####----------------------#### direction: 1->LH ,others->HL # Bug, No USE!
def CorrectUni(bit,data,module,Ra_array,Ta_array,direction):
    bitAN=module-1# 13->13-1=12
    if direction == 1:
        R=data % module
        print('-----------CorrectLH---------------------------')
    else:
        R=module-(data % module)
        print('-----------CorrectHL---------------------------')
    for i in range(1,bit):
        databin=Dec2Bin(bit, data)
        bitint=int(bit)        #if no int(bit) #when bit=36, 2^bit=0 #I do not know why.
        pow2Bit=pow(2,bitint)
        if data < pow2Bit:              
            if(R==0):
                final_answer=int(data/module)
                final_answer_bin=Dec2Bin(bit, final_answer)
                print('There is no error.')
                return final_answer_bin
            elif R in Ra_array:   
                errorbit=Ta_array[R]
                # print("R\tebit\n%d\t%d"%(R,errorbit))
                errorbit_computer=bit-(errorbit+1)
                if databin[errorbit_computer]==1:
                    databin[errorbit_computer]=0
                else:
                    databin[errorbit_computer]=1
                dec_data=Bin2Dec(bit, databin)
                #############################
                if(dec_data % module==0):
                    ANc2=(bin(dec_data)[2:]).zfill(bitAN)
                    final_answer=int(dec_data/module)
                    # print('final_answer=',final_answer)
                    final_answer_bin=Dec2Bin(bit, final_answer)
                    print("R\tebit\tANc\tANc2\tNc\n%d\t%d\t%d\t%s\t%d"%(R,errorbit,dec_data,ANc2,final_answer))
                    return final_answer_bin
                else:
                    print('Error cannot be detected.')
                    return databin
        else:                                   #超過範圍直接輸出
                print('Error cannot be detected')
                return databin
####----------------------####
def CorrectLH(bit,data,module,Ra_array,Ta_array):
    R=data % module
    bitAN=module-1# 13->13-1=12
    print('----------CorrectLH----------------')
    # print("R=%d"%R)
    for i in range(1,bit):
        databin=Dec2Bin(bit, data)
        bitint=int(bit)        #if no int(bit) #when bit=36, 2^bit=0        #I do not know why.
        pow2Bit=pow(2,bitint)
        if data < pow2Bit:              
            if(R==0):
                final_answer=int(data/module)
                final_answer_bin=Dec2Bin(bit, final_answer)
                print('There is no error.')
                return final_answer_bin
            elif R in Ra_array:   
                errorbit=Ta_array[R]
                # print('Error is in',errorbit,'bit')
                errorbit_computer=bit-(errorbit+1)
                if databin[errorbit_computer]==1:
                    databin[errorbit_computer]=0
                else:
                    databin[errorbit_computer]=1
                dec_data=Bin2Dec(bit, databin)
                #############################
                if(dec_data % module==0):
                    ANc2=(bin(dec_data)[2:]).zfill(bitAN)
                    final_answer=int(dec_data/module)
                    # print('final_answer=',final_answer)
                    final_answer_bin=Dec2Bin(bit, final_answer)
                    print("R\tebit\tANc\tANc2\tNc\n%d\t%d\t%d\t%s\t%d"%(R,errorbit,dec_data,ANc2,final_answer))
                    return final_answer_bin
                else:
                    print('Error cannot be detected.')
                    return databin
        else:                                   #超過範圍直接輸出
                print('---Error cannot be detected')
                return databin
####----------------------####
def CorrectHL(bit,data,module,Ra_array,Ta_array):
    bitAN=module-1# 13->13-1=12
    Re=data % module
    #print('餘數=',Re)
    R=module -  Re
    #print('模數-餘數=',R)
    print('----------CorrectHL----------------')
    # print("R=%d"%R)
    for i in range(1,bit):
        databin=Dec2Bin(bit, data)
        bitint=int(bit)        #if no int(bit) #when bit=36, 2^bit=0        #I do not know why.
        pow2Bit=pow(2,bitint)
        if data < pow2Bit:              
            if(R==0):
                final_answer=int(data/module)
                final_answer_bin=Dec2Bin(bit, final_answer)
                print('There is no error.')
                return final_answer_bin
            elif R in Ra_array:   
                errorbit=Ta_array[R]
                # print('Error is in',errorbit,'bit')
                errorbit_computer=bit-(errorbit+1)
                if databin[errorbit_computer]==1:
                    databin[errorbit_computer]=0
                else:
                    databin[errorbit_computer]=1
                dec_data=Bin2Dec(bit, databin)
                #############################
                if(dec_data % module==0):                    
                    ANc2=(bin(dec_data)[2:]).zfill(bitAN)
                    final_answer=int(dec_data/module)
                    # print('final_answer=',final_answer)
                    print("R\tebit\tANc\tANc2\tNc\n%d\t%d\t%d\t%s\t%d"%(R,errorbit,dec_data,ANc2,final_answer))
                    final_answer_bin=Dec2Bin(bit, final_answer)
                    return final_answer_bin
                else:
                    print('Error cannot be detected.')
                    return databin
        else:                                   #超過範圍直接輸出
                print('---Error cannot be detected---')
                return databin
####------------------txt-or-verilog-------------------------#### 
def AWE_veri(N,module,Ta_array,Sa_array):
    fver= time.strftime("%Y%m%d_%H%M", time.localtime())
    AWEFolder='files\\AWE_'+fver
    Path=autoCreatFolder(AWEFolder)
    module_str=str(module)
    Nstr=str(N)
    Pathlist=Path.split('\\')
    lenPath=len(Pathlist)
    Rpath='./'+Pathlist[lenPath-2]+'/'+Pathlist[lenPath-1]
    fn=Rpath+'/ANdecoder_AWE_'+module_str+'_for_N_'+Nstr+'.v'
    bitIN=int((module-1)/2)      #可更正bit數
    bitMod=len(bin(module)[2:])  #mod的bit數
    bit1=bitIN*2 # and gate output +1 output
    bitN=bitIN-bitMod
    print('---------------開始寫檔案---------------')
    print('可更正AN的bit數=',bitIN,'\nmod的bit數=',bitMod,'\nand gate數=',bit1,'\n可更正N的bit數=',bitN)
    f = open(fn, "w")
    f.write("// File Name: %s/ANdecoder_AWE_%s_for_N_%s.v\n"%(Rpath,module_str,Nstr))
    f.write("// module= %d\n// 可更正AN的bit數= %d\n// mod的bit數= %d\n// 可更正N的bit數= %d\n"%(module,bitIN,bitMod,bitN))
    f.write("\nmodule ANdecoder(ANe, Nc);\n")
    f.write("input [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f.write("output Nc;\n")
    else:
        f.write("output [%d:0] Nc;\n" %(bitN-1))  
    f.write("wire [%d:0] mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] not_mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] error_bit;\n"%(bitIN-1))
    f.write("wire [%d:0] and_out;\n"%(bit1-1))
    f.write("wire add;\n" )
    
    f.write("wire [%d:0] ANc;\n"%(bitIN-1))
    # mod R
    f.write("\nassign mod_tri = ANe %% %d;\n"%module)
    #Inv
    f.write("\n//not gate")
    for j in range(0,bitMod):
        f.write("\nnot not_%d(not_mod_tri[%d], mod_tri[%d]);"%(j,j,j) )
    #And
    f.write("\n//and gate")
    for k in range(1,module):
       iLen=len(str(bin(module)[2:]))
       f.write("\nand and_%d("%k)
       f.write("and_out[%d], "%(k-1))
       k2=bin(k)[2:]
       k2_0=k2.zfill(iLen)
       ############
       k2_arr=list(str(k2_0))
       k2_arr.reverse()
       k2Tran=[]
       for x in range(0, iLen):
           if k2_arr[x] == '1' :
                k2Tran.append('mod_tri[%d],'%x)
           else :
                k2Tran.append('not_mod_tri[%d],'%x)
       k2Tran2=" ".join(k2Tran)
       k2Tran3=k2Tran2[:-1]
       f.write("%s);"%k2Tran3)
       ##############
    #Or
    f.write("\n//or gate")
    err2=[0]*bitIN
    for y in range(0,bitIN):
        f.write("\nor or_%d(error_bit[%d], "%(y,y))
        orList=[]
        err1=[] #-1 =>S=1
        for t in range(1,module):
            #and gate編碼從0開始
            if  Ta_array[t] == y:
                 orList.append('and_out[%d],'%(t-1))
                 orList2=" ".join(orList)
                 if  Sa_array[t] == 1:
                #bit對應   #順序其實沒差              
                     err2[y]=(t-1)
        orList3=orList2[:-1]
        f.write("%s);"%orList3)
    #Or=>-1 => output=1 => +errbit ; if not => -errbit
    f.write("\nor or_%d(add, "%bitIN)
    for ebit in range(0,bitIN): #0-5
        err1.append('and_out[%d],'%err2[ebit])
        err1_2=" ".join(err1)
    err1t=err1_2[:-1]
    f.write("%s);"%err1t)        
    f.write("\n\nassign ANc = (add==0) ? ANe-error_bit : ANe+error_bit;\n" )
    f.write("\nassign Nc = ANc / %d;\n"%module)
    f.write("\nendmodule")
    f.close()
    #tb
    fn2=Rpath+'/ANdecoder_AWE_'+module_str+'_tb_for_N_'+Nstr+'.v'
    f2 = open(fn2, "w")
    f2.write("// File Name: %s\n"%fn2)
    f2.write("// module= %d\n// N= %d\n"%(module,N))
    f2.write("\nmodule ANdecoder_tb;\n")
    f2.write("reg [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f2.write("wire Nc;\n")
    else:
        f2.write("wire [%d:0] Nc;\n" %(bitN-1))
    f2.write("\nANdecoder D0(ANe, Nc);\ninitial begin\n")
    f2.write("$dumpfile(\"%s/A%dN%d.vcd\"); \n$dumpvars(0, ANdecoder_tb);\n"%(Rpath,module,N))  
    f2.write("\nANe=%d'd0;\n"%bitIN)
    #error
    ANe_list,ebit_list,R_list=TestforAllErrorAWE(bitIN,module,N)
    for t1 in range(len(ANe_list)):
        tANe=ANe_list[t1]
        tebit=ebit_list[t1]
        tR=R_list[t1]
        if tANe < 0:
            f2.write("\n//ANe=%s(負數), R=%s, error bit=%s"%(tANe,tR,tebit))
        else:
            if t1 > 0:
                f2.write("\n#10 ANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
            else:
                f2.write("\nANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
    f2.write("\n#10 $finish;\nend\nendmodule\n")
    f2.close()
    print('---------------寫檔案完成---------------')
    print('%s has been generated.'%fn)
    print('%s has been generated.'%fn2) 
    fvcd=Path+'\\A'+module_str+'N'+Nstr+'.vcd'
    fo=Path+'\\A'+module_str+'N'+Nstr+'.out'
    return fn,fn2,fvcd,fo
####----------------------####
def BER_veri(N,module,Ta_array,Sa_array):
    fver= time.strftime("%Y%m%d_%H%M", time.localtime())
    BERFolder='files\\BER_'+fver
    Path=autoCreatFolder(BERFolder)
    module_str=str(module)
    Nstr=str(N)
    Pathlist=Path.split('\\')
    lenPath=len(Pathlist)
    Rpath='./'+Pathlist[lenPath-2]+'/'+Pathlist[lenPath-1]
    fn=Rpath+'/ANdecoder_BER_'+module_str+'_for_N_'+Nstr+'.v'
    bitIN=int((module-1)/2)      #可更正bit數
    bitMod=len(bin(module)[2:])  #mod的bit數
    bit1=bitIN*2 # and gate output +1 output
    bitN=bitIN-bitMod
    print('---------------開始寫檔案---------------')
    print('可更正AN的bit數=',bitIN,'\nmod的bit數=',bitMod,'\nand gate數=',bit1,'\n可更正N的bit數=',bitN)
    f = open(fn, "w")
    f.write("// File Name: %s\n"%fn)
    f.write("// module= %d\n// 可更正AN的bit數= %d\n// mod的bit數= %d\n// 可更正N的bit數= %d\n"%(module,bitIN,bitMod,bitN))
    f.write("\nmodule ANdecoder(ANe, Nc);\n")
    f.write("input [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f.write("output Nc;\n")
    else:
        f.write("output [%d:0] Nc;\n" %(bitN-1))
    f.write("wire [%d:0] mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] not_mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] error_bit;\n"%(bitIN-1))
    f.write("wire [%d:0] and_out;\n"%(bit1-1))
    
    f.write("wire [%d:0] ANc;\n"%(bitIN-1))
    
    # mod R
    f.write("\nassign mod_tri = ANe %% %d;\n"%module)
    #Inv
    f.write("\n//not gate")
    for j in range(0,bitMod):
        f.write("\nnot not_%d(not_mod_tri[%d], mod_tri[%d]);"%(j,j,j) )
    #And
    f.write("\n//and gate")
    for k in range(1,module):
       iLen=len(str(bin(module)[2:]))
       f.write("\nand and_%d("%k)
       f.write("and_out[%d], "%(k-1))
       k2=bin(k)[2:]
       k2_0=k2.zfill(iLen)
       ############
       k2_arr=list(str(k2_0))
       k2_arr.reverse()
       k2Tran=[]
       for x in range(0, iLen):
           if k2_arr[x] == '1' :
                k2Tran.append('mod_tri[%d],'%x)
           else :
                k2Tran.append('not_mod_tri[%d],'%x)
       k2Tran2=" ".join(k2Tran)
       k2Tran3=k2Tran2[:-1]
       f.write("%s);"%k2Tran3)
       ##############
    #Or
    f.write("\n//or gate")
    err2=[0]*bitIN
    for y in range(0,bitIN):
        f.write("\nor or_%d(error_bit[%d], "%(y,y))
        orList=[]
        # err1=[] #-1 =>S=1
        for t in range(1,module):
            #and gate編碼從0開始
            if  Ta_array[t] == y:
                 orList.append('and_out[%d],'%(t-1))
                 orList2=" ".join(orList)
                 if  Sa_array[t] == 1:
                #bit對應   #順序其實沒差              
                     err2[y]=(t-1)
        orList3=orList2[:-1]
        f.write("%s);"%orList3)     
    f.write("\n//xor gate")
    for xo in range(0,bitIN):
        f.write('\nxor xor_%d(ANc[%d],error_bit[%d],ANe[%d]);'%(xo,xo,xo,xo))
    f.write("\nassign Nc = ANc / %d;\n"%module)
    f.write("\nendmodule")
    f.close()  
    #tb
    fn2=Rpath+'/ANdecoder_BER_'+module_str+'_tb_for_N_'+Nstr+'.v'
    f2 = open(fn2, "w")
    f2.write("// File Name: %s\n"%fn2)
    f2.write("// module= %d\n// N= %d\n"%(module,N))
    f2.write("\nmodule ANdecoder_tb;\n")
    f2.write("reg [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f2.write("wire Nc;\n")
    else:
        f2.write("wire [%d:0] Nc;\n" %(bitN-1))
    
    f2.write("\nANdecoder D0(ANe, Nc);\ninitial begin\n")
    f2.write("$dumpfile(\"%s/A%dN%d.vcd\"); \n$dumpvars(0, ANdecoder_tb);\n"%(Rpath,module,N))  
    # f2.write("\nANe=%d'd0;\n"%bitIN)
    #error
    ANe_list,ebit_list,R_list=TestforAllErrorBER(bitIN,module,N)
    for t1 in range(len(ANe_list)):
        tANe=ANe_list[t1]
        tebit=ebit_list[t1]
        tR=R_list[t1]
        if t1 > 0:
            f2.write("\n#10 ANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
        else:
            f2.write("\nANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
    f2.write("\n#10 $finish;\nend\nendmodule\n")
    f2.close()
    print('---------------寫檔案完成---------------')
    print('%s has been generated.'%fn)
    print('%s has been generated.'%fn2) 
    fvcd=Path+'\\A'+module_str+'N'+Nstr+'.vcd'
    fo=Path+'\\A'+module_str+'N'+Nstr+'.out'
    return fn,fn2,fvcd,fo   
####----------------------####
def Alter_veri(N,module,Ta_array):
    fver= time.strftime("%Y%m%d_%H%M", time.localtime())
    AlterFolder='files\\Alter_'+fver
    Path=autoCreatFolder(AlterFolder)
    module_str=str(module)
    Nstr=str(N)
    Pathlist=Path.split('\\')
    lenPath=len(Pathlist)
    Rpath='./'+Pathlist[lenPath-2]+'/'+Pathlist[lenPath-1]
    fn=Rpath+'/ANdecoder_Alter_'+module_str+'_for_N_'+Nstr+'.v'
    bitIN=(module-1)     #可更正bit數
    bitMod=len(bin(module)[2:])  #mod的bit數
    bitN=bitIN-bitMod
    print('---------------開始寫檔案---------------')
    print('可更正AN的bit數=',bitIN,'\tmod的bit數=',bitMod,'\t可更正N的bit數=',bitN)
    f = open(fn, "w")
    f.write("// File Name: %s\n"%fn)
    f.write("// module= %d\n// 可更正AN的bit數= %d\n// mod的bit數= %d\n// 可更正N的bit數= %d\n"%(module,bitIN,bitMod,bitN))
    f.write("\nmodule ANdecoder(ANe, Nc);\n")
    f.write("input [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f.write("output Nc;\n")
    else:
        f.write("output [%d:0] Nc;\n" %(bitN-1))  
    
    f.write("wire [%d:0] mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] not_mod_tri;\n"%(bitMod-1))
    #f.write("wire [%d:0] error_bit1;\n"%(bitIN-1))
    f.write("wire [%d:0] R;\n"%(bitIN-1))
    f.write("wire [%d:0] notR;\n"%(bitIN-1))
    f.write("wire [%d:0] ANc1;\n"%(bitIN-1))
    
    #f.write("wire [%d:0] error_bit2;\n"%(bitIN-1))
    f.write("wire [%d:0] ANc2;\n"%(bitIN-1))
    f.write("wire [%d:0] check;\n"%(bitMod-1))
    
    f.write("wire [%d:0] ANc;\n" %(bitIN-1))    
    
    # mod R
    f.write("\nassign mod_tri = ANe %% %d;\n"%module)
    # Inv
    f.write("\n//not0 gate")
    for j1 in range(0,bitMod):
        f.write("\nnot not0_%d(not_mod_tri[%d], mod_tri[%d]);"%(j1,j1,j1) )
    # And
    f.write("\n//and gate")
    for k in range(1,module): #EX: i=13 => 1-12
       iLen=len(str(bin(module)[2:]))
       f.write("\nand and0_%d(R[%d], "%(k,(k-1)))
       ebit=Ta_array[k]
       #f.write("error_bit1[%d], "%ebit)
       k2=bin(k)[2:]
       k2_0=k2.zfill(iLen)
       k2_arr=list(str(k2_0))
       k2_arr.reverse()
       k2Tran=[]
       for x in range(0, iLen):
           if k2_arr[x] == '1' :
                k2Tran.append('mod_tri[%d],'%x)
           else :
                k2Tran.append('not_mod_tri[%d],'%x)
       k2Tran2=" ".join(k2Tran)
       k2Tran3=k2Tran2[:-1]
       f.write("%s);"%k2Tran3)
    # Not
    f.write("\n//not1 gate")
    for j0 in range(0,bitIN):
        f.write("\nnot not1_%d(notR[%d], R[%d]);"%(j0,j0,j0) ) 
    # And1 # R&ANe對應
    f.write("\n//and1 gate")
    for j3 in range(0,bitIN):
        ebit=Ta_array[(j3+1)]
        f.write("\nand and1_%d(ANc1[%d], notR[%d], ANe[%d]);"%(ebit,ebit,j3,ebit))
    # xor1 
    #0727 改or gate
    f.write("\n//or gate")
    for x1 in range(0,bitIN):
        xxx=module-(x1+1)
        ebit2=Ta_array[xxx]
        f.write("\nor or_%d(ANc2[%d], "%(ebit2,ebit2))
        f.write("R[%d], "%x1)
        f.write("ANe[%d]);"%ebit2)
    
    f.write("\n//check")
    f.write("\nassign check = ANc1 %% %d;"%module)
    f.write("\nassign ANc = (check == %d'd0) ? ANc1 : ANc2;"%bitMod)
    f.write("\nassign Nc = ANc / %d;"%module)
    f.write("\nendmodule")
    f.close()    
    #tb
    fn2=Rpath+'/ANdecoder_Alter_'+module_str+'_tb_for_N_'+Nstr+'.v'
    f2 = open(fn2, "w")
    f2.write("// File Name: %s\n"%fn2)
    f2.write("// module= %d\n// N= %d\n"%(module,N))
    f2.write("\nmodule ANdecoder_tb;\n")
    f2.write("reg [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f2.write("wire Nc;\n")
    else:
        f2.write("wire [%d:0] Nc;\n" %(bitN-1))
 
    f2.write("\nANdecoder D0(ANe, Nc);\ninitial begin\n")
    f2.write("$dumpfile(\"%s/A%dN%d.vcd\"); \n$dumpvars(0, ANdecoder_tb);\n"%(Rpath,module,N))  
    #error
    ANe_list,ebit_list,R_list=TestforAllErrorAlter(bitIN,module,N)
    for t1 in range(len(ANe_list)):
        tANe=ANe_list[t1]
        tebit=ebit_list[t1]
        tR=R_list[t1]
        if t1 > 0:
            f2.write("\n#10 ANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
        else:
            f2.write("\nANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
    f2.write("\n#10 $finish;\nend\nendmodule\n")
    f2.close()
    print('---------------寫檔案完成---------------')
    print('%s has been generated.'%fn)
    print('%s has been generated.'%fn2) 
    fvcd=Path+'\\A'+module_str+'N'+Nstr+'.vcd'
    fo=Path+'\\A'+module_str+'N'+Nstr+'.out'
    return fn,fn2,fvcd,fo
####----------------------####
def Uni_LH_veri(N,module,Ta_array):
    fver= time.strftime("%Y%m%d_%H%M", time.localtime())
    UniLHFolder='files\\Uni_LH_'+fver
    Path=autoCreatFolder(UniLHFolder)
    module_str=str(module)
    Nstr=str(N)
    Pathlist=Path.split('\\')
    lenPath=len(Pathlist)
    Rpath='./'+Pathlist[lenPath-2]+'/'+Pathlist[lenPath-1]
    fn=Rpath+'/ANdecoder_Uni_LH_'+module_str+'_for_N_'+Nstr+'.v'
    bitIN=module-1      #可更正bit數
    bitMod=len(bin(module)[2:])  #mod的bit數
    bitN=bitIN-bitMod
    print('---------------開始寫檔案---------------')
    print('可更正AN的bit數=',bitIN,'\tmod的bit數=',bitMod,'\t可更正N的bit數=',bitN)
    f = open(fn, "w")
    f.write("// File Name: %s\n"%fn)
    f.write("// module= %d\n// 可更正AN的bit數= %d\n// mod的bit數= %d\n// 可更正N的bit數= %d\n"%(module,bitIN,bitMod,bitN))
    f.write("\nmodule ANdecoder(ANe, Nc);\n")
    f.write("input [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f.write("output Nc;\n")
    else:
        f.write("output [%d:0] Nc;\n" %(bitN-1))
    f.write("wire [%d:0] mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] not_mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] error_bit;\n"%(bitIN-1))
    f.write("wire [%d:0] not_error_bit;\n"%(bitIN-1))
    f.write("wire [%d:0] ANc;"%(bitIN-1))
    
    # mod R
    f.write("\nassign mod_tri = ANe %% %d;\n"%module)
    #Inv
    f.write("\n//not0 gate")
    for j1 in range(0,bitMod):
        f.write("\nnot not0_%d(not_mod_tri[%d], mod_tri[%d]);"%(j1,j1,j1) )
    #And
    f.write("\n//and0 gate")
    for k in range(1,module): #EX: i=13 => 1-12
       iLen=len(str(bin(module)[2:]))
       f.write("\nand and0_%d("%k)
       ebit=Ta_array[k]
       f.write("error_bit[%d], "%ebit)
       k2=bin(k)[2:]
       k2_0=k2.zfill(iLen)
       k2_arr=list(str(k2_0))
       k2_arr.reverse()
       k2Tran=[]
       for x in range(0, iLen):
           if k2_arr[x] == '1' :
                k2Tran.append('mod_tri[%d],'%x)
           else :
                k2Tran.append('not_mod_tri[%d],'%x)
       k2Tran2=" ".join(k2Tran)
       k2Tran3=k2Tran2[:-1]
       f.write("%s);"%k2Tran3)
    # xor
    #f.write("\n//XOR gate")
    #for x1 in range(0,bitIN):
    #    f.write("\nxor xor_%d(ANc[%d],error_bit[%d], ANe[%d]);"%(x1,x1,x1,x1) )
    
    # not
    f.write("\n//not1 gate")
    for x1 in range(0,bitIN):
        f.write("\nnot not1_%d(not_error_bit[%d],error_bit[%d]);"%(x1,x1,x1) )
    # and
    f.write("\n//and1 gate")
    for x2 in range(0,bitIN):
        f.write("\nand and1_%d(ANc[%d],not_error_bit[%d], ANe[%d]);"%(x2,x2,x2,x2) )
    f.write("\n\nassign Nc = ANc / %d;\n"%module)
    f.write("\nendmodule")
    f.close()
    #tb
    fn2=Rpath+'/ANdecoder_Uni_LH_'+module_str+'_tb_for_N_'+Nstr+'.v'
    f2 = open(fn2, "w")
    f2.write("// File Name: %s\n"%fn2)
    f2.write("// module= %d\n// N= %d\n"%(module,N))
    f2.write("\nmodule ANdecoder_tb;\n")
    f2.write("reg [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f2.write("wire Nc;\n")
    else:
        f2.write("wire [%d:0] Nc;\n" %(bitN-1))
    f2.write("\nANdecoder D0( ANe, Nc);\ninitial begin\n")
    f2.write("$dumpfile(\"%s/A%dN%d.vcd\"); \n$dumpvars(0, ANdecoder_tb);\n"%(Rpath,module,N))  
    f2.write("\nANe=%d'd0;\n"%bitIN)
    #error
    ANe_list,ebit_list,R_list=TestforAllErrorLH(bitIN,module,N)
    for t1 in range(len(ANe_list)):
        tANe=ANe_list[t1]
        tebit=ebit_list[t1]
        tR=R_list[t1]
        if t1 > 0:
            f2.write("\n#10 ANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
        else:
            f2.write("\nANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
    f2.write("\n#10 $finish;\nend\nendmodule\n")
    f2.close()
    print('---------------寫檔案完成---------------')
    print('%s has been generated.'%fn)
    print('%s has been generated.'%fn2) 
    fvcd=Path+'\\A'+module_str+'N'+Nstr+'.vcd'
    fo=Path+'\\A'+module_str+'N'+Nstr+'.out'
    return fn,fn2,fvcd,fo
####---------------------------------------------------------####
def Uni_HL_veri(N,module,Ta_array):
    fver= time.strftime("%Y%m%d_%H%M", time.localtime())
    UniHLFolder='files\\Uni_HL_'+fver
    Path=autoCreatFolder(UniHLFolder)
    module_str=str(module)
    Nstr=str(N)
    Pathlist=Path.split('\\')
    lenPath=len(Pathlist)
    Rpath='./'+Pathlist[lenPath-2]+'/'+Pathlist[lenPath-1]
    fn=Rpath+'/ANdecoder_Uni_HL_'+module_str+'_for_N_'+Nstr+'.v'
    bitIN=module-1      #可更正bit數
    bitMod=len(bin(module)[2:])  #mod的bit數
    bitN=bitIN-bitMod
    print('---------------開始寫檔案---------------')
    print('可更正AN的bit數=',bitIN,'\tmod的bit數=',bitMod,'\t可更正N的bit數=',bitN)
    f = open(fn, "w")
    f.write("// File Name: %s\n"%fn)
    f.write("// module= %d\n// 可更正AN的bit數= %d\n// mod的bit數= %d\n// 可更正N的bit數= %d\n"%(module,bitIN,bitMod,bitN))
    f.write("\nmodule ANdecoder(ANe, Nc);\n")
    f.write("input [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f.write("output Nc;\n")
    else:
        f.write("output [%d:0] Nc;\n" %(bitN-1))
    f.write("wire [%d:0] mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] not_mod_tri;\n"%(bitMod-1))
    f.write("wire [%d:0] error_bit;\n"%(bitIN-1))
    
    f.write("wire [%d:0] ANc;"%(bitIN-1))
    
    # mod R
    f.write("\nassign mod_tri = ANe %% %d;\n"%module)
    #Inv
    f.write("\n//not gate")
    for j1 in range(0,bitMod):
        f.write("\nnot not_%d(not_mod_tri[%d], mod_tri[%d]);"%(j1,j1,j1) )
    #And
    f.write("\n//and gate")
    for k in range(1,module): #EX: i=13 => 1-12
       iLen=len(str(bin(module)[2:]))
       f.write("\nand and_%d("%k)
       ebit=Ta_array[(module-k)]
       f.write("error_bit[%d], "%ebit)
       k2=bin(k)[2:]
       k2_0=k2.zfill(iLen)
       k2_arr=list(str(k2_0))
       k2_arr.reverse()
       k2Tran=[]
       for x in range(0, iLen):
           if k2_arr[x] == '1' :
                k2Tran.append('mod_tri[%d],'%x)
           else :
                k2Tran.append('not_mod_tri[%d],'%x)
       k2Tran2=" ".join(k2Tran)
       k2Tran3=k2Tran2[:-1]
       f.write("%s);"%k2Tran3)
    # xor #0727 改成or gate(驗證成功)
    f.write("\n//or gate")
    for x1 in range(0,bitIN):
        f.write("\nor or_%d(ANc[%d],error_bit[%d], ANe[%d]);"%(x1,x1,x1,x1) )
    f.write("\nassign Nc = ANc / %d;\n"%module)
    f.write("\nendmodule")
    f.close()
    #tb
    fn2=Rpath+'/ANdecoder_Uni_HL_'+module_str+'_tb_for_N_'+Nstr+'.v'
    f2 = open(fn2, "w")
    f2.write("// File Name: %s\n"%fn2)
    f2.write("// module= %d\n// N= %d\n"%(module,N))
    f2.write("\nmodule ANdecoder_tb;\n")
    f2.write("reg [%d:0] ANe;\n"%(bitIN-1))
    if (bitN-1) == 0:
        f2.write("wire Nc;\n")
    else:
        f2.write("wire [%d:0] Nc;\n" %(bitN-1))
    f2.write("\nANdecoder D0(ANe, Nc);\ninitial begin\n")
    f2.write("$dumpfile(\"%s/A%dN%d.vcd\"); \n$dumpvars(0, ANdecoder_tb);\n"%(Rpath,module,N))  
    f2.write("\nANe=%d'd0;\n"%bitIN)
    #error
    ANe_list,ebit_list,R_list=TestforAllErrorHL(bitIN,module,N)
    for t1 in range(len(ANe_list)):
        tANe=ANe_list[t1]
        tebit=ebit_list[t1]
        tR=R_list[t1]
        if t1 > 0:
            f2.write("\n#10 ANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
        else:
            f2.write("\nANe=%d'd%d; //R=%s, error bit=%s"%(bitIN,tANe,tR,tebit))
    f2.write("\n#10 $finish;\nend\nendmodule\n")
    f2.close()
    print('---------------寫檔案完成---------------')
    print('%s has been generated.'%fn)
    print('%s has been generated.'%fn2) 
    fvcd=Path+'\\A'+module_str+'N'+Nstr+'.vcd'
    fo=Path+'\\A'+module_str+'N'+Nstr+'.out'
    return fn,fn2,fvcd,fo
####------------------iverilog-------------------------------####
def autoVCD(fn,ftb,fvcd,fo,ErrorModels):
    if ErrorModels == 2:
        tclName="auto_Alter"
    else:
        tclName="auto"

    os.system('iverilog -o %s %s %s'%(fo,fn,ftb))
    os.system('vvp -n %s'%fo)
    os.system('gtkwave -T %s.tcl %s'%(tclName,fvcd))
####---------------------------------------------------------####
def autoCreatFolder(newFolder):
    path = os.path.abspath('.')
    newPath = path + '\\' + newFolder
    if not os.path.isdir(newPath):
        os.mkdir(newPath)
    return newPath
######