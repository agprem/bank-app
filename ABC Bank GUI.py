from tkinter import *
import tkinter.font as font
from tkinter import messagebox
import pyodbc
import PIL
from tkinter import ttk
from PIL import Image,ImageTk


#-----------------------------------CONNECTION CODE--------------------------------------------------------------------------

conn=pyodbc.connect("Driver={SQL SERVER};"
                    "Server=DESKTOP-1CKGC37;"
                    "Database=master;"
                    "Trusted_Connection=yes;")
#------------------------------------ FOR CLOSING WINDOWS------------------------------------------------------------------

def closeaddnew():
      addnewframe.destroy()
def closedeposit():
      depositframe.destroy()
def closewithdraw():
      withdrawframe.destroy()
def closemain():
      root.destroy()
def closeupdate():
      editframe.destroy()
def closeshowall():
      showally.destroy()

#-----------------------------FOR VALIDATION OF AGE------------------------------------------------------------------------------



def  validate_age(user_age):
      global flag1
      if (flag1==0):
            text2.delete(0,END)
      else:pass
      if user_age.isdigit():
            #print(type(user_age))

            age=int(user_age)
            if age>=18:
                  return True
            else:
                  messagebox.showerror("Message","You are minor less then 18")
                  return False
      elif user_age=="" or user_age=="0":
            return True
      else:
            messagebox.showerror("Enter Digits only!!!!!","You are minor")
            return False
     

#-----------------------------FOR VALIDATION OF PAN NO IN ADD RECORD WINDOW  ------------------------------------------------------------------------------


def validate_pan(input):
    global flag
    try:                                        # Code for getting correct format of PAN NO  try block for risky code of wrong PAN NO
                print("I am in of  validate pan code",input)
                #print(flag)
                if flag==0:
                      #print("cLEAR")
                      text4.delete(0,END)
                else:pass
                
                D=input
                if(len(D)==0):
                      messagebox.showinfo("Msg","Enter Data")
                      return False
                
                if(len(D) !=10):
                    messagebox.showerror("MSG","Enter PAN no again")
                    #closeaddnew()
                    return False
                else:pass
                count=0
                for i in D:
                    count=count+1
                    if(count<6):
                        if((i>='a'and i<='z') or (i>='A' and i<='Z')):
                            pass
                        else : break
                    elif(count>5 and count<10):
                        if(i>='0' and i<='9'):
                            pass
                        else : break
                    elif(count==10):
                        if((i>='a'and i<='z') or (i>='A' and i<='Z')):
                            flag=1
                            break
                        else:break
                    else:pass
                cursor=conn.cursor()
                cursor.execute("select PAN_NO from bankdb")
               
                
                for j in cursor:                # j  represents row in database
                    #print(cursor)
                    if (D in j):
                         messagebox.showerror("MSG","PAN no already in database")
                         #closeaddnew() 
                         return False
                    
                    
                    else:pass
                    
                return True
                        
                       
                conn.commit()
    except Exception as r:
           print("Wrong PAN NO",r)

#-----------------------------FOR VALIDATION OF PAN NO IN UPDATE WINDOW  ------------------------------------------------------------------------------       
        

def validate_updatepan(input):
      try:
            
            D=input
            
            if(len(D)==0):
                  messagebox.showinfo("Msg","Entering PAN_NO is must")
                  return False
            if(len(D) !=10):
                  messagebox.showerror("MSG","Enter PAN no again")
                  closeupdate()
                  return False
            else:pass
            count=0
            for i in D:
                  count=count+1
                  if(count<6):
                        if((i>='a'and i<='z') or (i>='A' and i<='Z')):
                              pass
                        else : break
                  elif(count>5 and count<10):
                        if(i>='0' and i<='9'):
                            pass
                        else : break
                  elif(count==10):
                        if((i>='a'and i<='z') or (i>='A' and i<='Z')):
                            flag=1
                            break
                        else:break
                  else:pass
            cursor=conn.cursor()
            cursor.execute("select PAN_NO from bankdb")
               
                
               
            for j in cursor:                # j  represents row in database  This code required when we update the record but don't update PAN then it will coincide with previously
                    #print(cursor)          # saved PAN so it chks whether the pan no belongs to same account no then it will allow to save
                  if (D in j):
                          
                        print("hi",j)
                        conn.commit()
                        cursor1=conn.cursor()
                         
                        cursor1.execute("select acc_no from bankdb where PAN_NO=?",(j[0]))
                        record=cursor1.fetchone()
                        print("record",record)
                        for i in record:
                              pass
                        print("Account no for pan-no present already in database ",i)
                         
                        conn.commit()
                        #cursor2=conn.cursor()
                        '''cursor2.execute("select acc_no from bankdb where name=?",(text))
                          
                        record=cursor2.fetchone()
                        for k in record:
                            pass
                        print("Account no for pan-no enteredn now  ",k)'''
                        presentaccount=int(textaccount.get())
                        if(i!=presentaccount):
                              print(type(i))
                              print(type(presentaccount))
                              print("account for edit",textaccount.get())
                              messagebox.showerror("MSG","PAN no already in database")
                              closeupdate()
                              return False
                        else:return True
            return True            
                                
      except Exception as r:
            print("Wrong validateupdate PAN NO",r)



#-----------------------------FUNCTION TO ADD NEW RECORD -----------------------------------------------------------------------------      

def addrecord():
      
    global name,age,address,PAN_NO,Aadhar_no,contact_no,balance,status1,status2,flag,flag1
    
    name=text1.get()
    flag1=1
# validation of age------
    if (flag1==1):
          reg=addnewframe.register(validate_age)
          print("I am in validate age")
          text2.config(validate="key",validatecommand=(reg,'%P'))
    
          print("I am out of  validate age")
    else:pass
    address=text3.get()

    flag=1
    
# validation of PAN_NO------
    if flag==1:
          print("I am in of  validate pan")
          reg1=addnewframe.register(validate_pan)
          text4.config(validate="key",validatecommand=(reg1,'%P'))
          print("I am out of  validate pan")
    else:pass
    Aadhar_no=text5.get()
    contact_no=text6.get()
    #balance1.set("100")
    balance=text7.get()
    print(balance)
   
    
# checking status of validation of pan no and age
    status1=validate_age(text2.get())
    status2=validate_pan(text4.get())
    print(status1,status2)
    if(status1 and status2):
        age=text2.get()
        PAN_NO=text4.get()
        print(name,age,address,PAN_NO,Aadhar_no,contact_no,balance)
        cursor=conn.cursor()
        cursor.execute("insert into bankdb values(?,?,?,?,?,?,?)",(name,age,address,PAN_NO,Aadhar_no,contact_no,balance))
        conn.commit()
        cursor=conn.cursor()
        cursor.execute("select acc_no from bankdb")
        data=cursor.fetchall()
        for i in data:
              pass
        print(i[0])
        newacc=i[0]
        print("New account no is ",newacc)
        conn.commit()
        messagebox.showinfo("Your Account-no is ",newacc)
    else:messagebox.showinfo("Msg","Data can't be Inserted")
    #closeaddnew()
    

#-----------------------------FUNCTION TO CLEAR TEXT FIELDS IN ADD RECORD WINDOW -----------------------------------------------------------------------------     

def cleartext():
      global flag,flag1
      text1.delete(0,END)
      flag1=0
      text2.delete(0,END)
      text3.delete(0,END)
      #print("hi")
      flag=0
      text4.delete(0,END)
      
      #print(flag)
      #print("Text4",text4.get())
      text5.delete(0,END)
      text6.delete(0,END)
      text7.delete(0,END)
      text1.focus()
      
    
      '''name1.set('')
      age1.set('')
      address1.set('')
      panno1.set('')
      aadharno1.set('')
      contactno1.set('')
      balance1.set('')
      text1.focus()
      print(name1.get())'''

#-----------------------------FUNCTION FOR DEPOSIT ----------------------------------------------------------------------------- ---------
      
def deposit():
      val=text8.get()
      if(text8.get()==""):
            messagebox.showinfo("Message","Enter  some value")
            return True
      else:pass
      #print(type(val))
      depositval=int(val)
      #print(depositval)
      #print(type(depositval))
      
      
      cursor=conn.cursor()
      cursor.execute("select balance from bankdb where acc_no=?",(textaccount.get()))
      record=cursor.fetchone()
      for i in record:
            #print(i)
            #print(type(i))
            depositval+=i
            #print(depositval)
      balance=depositval
      #print(balance)
      conn.commit()
      cursor=conn.cursor()
      cursor.execute("update Bankdb set Balance=? where acc_no=?",(balance,textaccount.get()))
      messagebox.showinfo("Msg","Amount Deposited")
      conn.commit()
      closedeposit()
#-----------------------------FUNCTION FOR WITHDRAWAL----------------------------------------------------------------------------     

def withdraw():
      val=text8.get()
      if(text8.get()==""):
            messagebox.showinfo("Message","Enter  some value")
            return True
      else:pass
      #print(type(val))
      withdrawval=int(val)
      #print(withdrawval)
      #print(type(depositval))
      
      
      cursor=conn.cursor()
      cursor.execute("select balance from bankdb where acc_no=?",(textaccount.get()))
      record=cursor.fetchone()
      for i in record:
            #print(i)
            if(i<withdrawval):
                  messagebox.showerror("Msg","Insufficient Amount in account")
                  closewithdraw()
                  return False
            else:i-=withdrawval
            #print(type(i))
            #print(i)
      balance=i
      #print(balance)
      conn.commit()
      cursor=conn.cursor()
      cursor.execute("update Bankdb set Balance=? where acc_no=?",(balance,textaccount.get()))
      messagebox.showinfo("Msg","Withdrawal Completed")
      conn.commit()
      closewithdraw()

#-----------------------------FUNCTION FOR EDITING ACCOUNT DETAILS-----------------------------------------------------------------------------           

def update():
      reg=editframe.register(validate_age)                         # for validation of age
      text2.config(validate="key",validatecommand=(reg,'%P'))
      reg1=editframe.register(validate_updatepan)                  # for validation of PAN no
      text4.config(validate="key",validatecommand=(reg1,'%P'))
      status1=validate_age(text2.get())
      status2=validate_updatepan(text4.get())
      if(status1 and status2):
            print(status1,status2)
            cursor=conn.cursor()
            cursor.execute(" update bankdb set name=?,age=?,address=?,PAN_NO=?,Aadhar_no=?,contact_no=? where acc_no=?",(text1.get(),text2.get(),text3.get(),text4.get(),text5.get(),text6.get(),textaccount.get()))
            messagebox.showinfo("Message"," Account Details Updated...******.")
      
      else:messagebox.showerror("Message"," Account Details cannot be Updated !!!!!.")
      conn.commit()
      closeupdate()
      
#-----------------------------FUNCTION TO DELETE A RECORD -----------------------------------------------------------------------------     

def delete():
      cursor=conn.cursor()
      cursor.execute("select * from bankdb where acc_no=?", textaccount.get())
      records=cursor.fetchall()
      #print (records)
      if(records==[]):
            messagebox.showerror("Message","Please enter a valid Account no...")
            return False
      else:pass
      conn.commit()
      
      
      cursor=conn.cursor()
      cursor.execute("delete from bankdb where acc_no=?",(textaccount.get()))
      messagebox.showinfo("Message","Data deleted Succesfully")
      conn.commit()
      



      
#-----------------------------CODE TO  NEW RECORD WINDOW -----------------------------------------------------------------------------             

def addnewframe():
    global addnewframe
    addnewframe=Tk()
    addnewframe.title("Add New Record")
    addnewframe.geometry("1500x600")
    addnewframe.configure(background="light blue");
    global name1,age1,address1,panno1,aadharno1,contactno1,balance1
    name1=StringVar()
    age1=StringVar()
    address1=StringVar()
    panno1=StringVar()
    aadharno1=StringVar()
    contactno1=StringVar()
    balance1=StringVar()
   
    labelheading1=Label(addnewframe,text="WELCOME TO ABC BANK",font=("bold",20),fg='blue',bg="light blue")
    labelheading1.grid(row=0,column=0,columnspan=5,rowspan=3,padx=400,pady=50,ipadx=30,ipady=30)

    label1=Label(addnewframe,text="Name",bg="light blue")
    label1.grid(row=7,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label2=Label(addnewframe,text="Age",bg="light blue")
    label2.grid(row=8,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label3=Label(addnewframe,text="Address",bg="light blue")
    label3.grid(row=9,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label4=Label(addnewframe,text="PAN no.",bg="light blue")
    label4.grid(row=10,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label5=Label(addnewframe,text="AADHAR no",bg="light blue")
    label5.grid(row=11,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label6=Label(addnewframe,text="Contact no..",bg="light blue")
    label6.grid(row=12,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label7=Label(addnewframe,text=" Balance",bg="light blue")
    label7.grid(row=13,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)

    global text1,text2,text3,text4,text5,text5,text6,text7
    text1=Entry(addnewframe,width=50,textvariable=name1)
    text1.grid(row=7,column=2)
    text2=Entry(addnewframe,width=50,textvariable=age1)
    text2.grid(row=8,column=2)
    text3=Entry(addnewframe,width=50,textvariable=address1)
    text3.grid(row=9,column=2)
    text4=Entry(addnewframe,width=50,textvariable=panno1)
    text4.grid(row=10,column=2)
    text5=Entry(addnewframe,width=50,textvariable=aadharno1)
    text5.grid(row=11,column=2)
    text6=Entry(addnewframe,width=50,textvariable=contactno1)
    text6.grid(row=12,column=2)
    text7=Entry(addnewframe,width=50,textvariable=balance1)
    text7.grid(row=13,column=2)

    addbutton=Button(addnewframe,text="Add Record",width=20,command=addrecord)
    addbutton.grid(row=16,column=1,padx=10,pady=10)
    clearbutton=Button(addnewframe,text="Clear Text",width=20,command=cleartext)
    clearbutton.grid(row=16,column=2,padx=10,pady=10)
    closebutton=Button(addnewframe,text="Close Window",width=20,command=closeaddnew)
    closebutton.grid(row=16,column=3,padx=10,pady=10)
    '''print("HI",name1)
    print("Hello",name1.get())
    print(text1.get())'''

    
#----------------------------- CODE FOR WITHDRAWAL WINDOW  -----------------------------------------------------------------------------     
    

def withdrawframe():
    global withdrawframe
    global text1,text2,text3,text4,text5,text5,text6,text7,text8
    withdrawframe=Tk()
    withdrawframe.title("Withdraw ")
    withdrawframe.geometry("1500x800")
    withdrawframe.configure(background="light blue");
    
    global name1,age1,address1,panno1,aadharno1,contactno1,balance1
    name1=StringVar()
    age1=StringVar()
    address1=StringVar()
    panno1=StringVar()
    aadharno1=StringVar()
    contactno1=StringVar()
    balance1=StringVar()
    withdrawamount=StringVar()
   
    labelheading1=Label(withdrawframe,text="WELCOME TO ABC BANK",font=("bold",20),fg='blue',bg="light blue")
    labelheading1.grid(row=0,column=0,columnspan=5,rowspan=3,padx=400,pady=50,ipadx=30,ipady=30)

    label1=Label(withdrawframe,text="Name",bg="light blue")
    label1.grid(row=7,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label2=Label(withdrawframe,text="Age",bg="light blue")
    label2.grid(row=8,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label3=Label(withdrawframe,text="Address",bg="light blue")
    label3.grid(row=9,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label4=Label(withdrawframe,text="PAN no.",bg="light blue")
    label4.grid(row=10,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label5=Label(withdrawframe,text="AADHAR no",bg="light blue")
    label5.grid(row=11,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label6=Label(withdrawframe,text="Contact no..",bg="light blue")
    label6.grid(row=12,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label7=Label(withdrawframe,text=" Balance",bg="light blue")
    label7.grid(row=13,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label8=Label(withdrawframe,text="Enter amount to Withdraw",bg="light blue")
    label8.grid(row=14,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)

    
    text1=Entry(withdrawframe,width=50,textvariable=name1)
    text1.grid(row=7,column=2)
    text2=Entry(withdrawframe,width=50,textvariable=age1)
    text2.grid(row=8,column=2)
    text3=Entry(withdrawframe,width=50,textvariable=address1)
    text3.grid(row=9,column=2)
    text4=Entry(withdrawframe,width=50,textvariable=panno1)
    text4.grid(row=10,column=2)
    text5=Entry(withdrawframe,width=50,textvariable=aadharno1)
    text5.grid(row=11,column=2)
    text6=Entry(withdrawframe,width=50,textvariable=contactno1)
    text6.grid(row=12,column=2)
    text7=Entry(withdrawframe,width=50,textvariable=balance1)
    text7.grid(row=13,column=2)
    text8=Entry(withdrawframe,width=50,textvariable=withdrawamount)
    text8.grid(row=14,column=2)

    addbutton=Button(withdrawframe,text="Withdraw",width=20,command=withdraw)#this calls withdraw function
    addbutton.grid(row=17,column=1,columnspan=2,padx=10,pady=10)
    clearbutton=Button(withdrawframe,text="Close Window",width=20,command=closewithdraw)
    clearbutton.grid(row=17,column=2,columnspan=2,padx=10,pady=10)
    cursor=conn.cursor()
    if(textaccount.get()==""):
          messagebox.showerror("Message","Please enter a valid  account no...")
          closewithdraw()
          return False
    cursor.execute("select * from bankdb where acc_no="+ textaccount.get())
    records=cursor.fetchall()
    #print (records)
    if(records==[]):
          messagebox.showerror("Message","Account doesn't exist")
          closewithdraw()
          return False
    else:pass
          
    
    for record in records:                          # for inserting records into text boxes from database
          text1.insert(0,record[1])
          text2.insert(0,record[2])
          text3.insert(0,record[3])
          text4.insert(0,record[4])
          text5.insert(0,record[5])
          text6.insert(0,record[6])
          text7.insert(0,record[7])
    
#----------------------------- CODE FOR DEPOSIT WINDOW  -----------------------------------------------------------------------------     
    
 


def depositframe():
    global depositframe
    global text1,text2,text3,text4,text5,text5,text6,text7,text8
    depositframe=Tk()
    depositframe.title("Deposit ")
    depositframe.geometry("1500x800")
    depositframe.configure(background="light blue");
    
    global name1,age1,address1,panno1,aadharno1,contactno1,balance1
    name1=StringVar()
    age1=StringVar()
    address1=StringVar()
    panno1=StringVar()
    aadharno1=StringVar()
    contactno1=StringVar()
    balance1=StringVar()
    depositamount=StringVar()
   
    labelheading1=Label(depositframe,text="WELCOME TO ABC BANK",font=("bold",20),fg='blue',bg="light blue")
    labelheading1.grid(row=0,column=0,columnspan=5,rowspan=3,padx=400,pady=50,ipadx=30,ipady=30)

    label1=Label(depositframe,text="Name",bg="light blue")
    label1.grid(row=7,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label2=Label(depositframe,text="Age",bg="light blue")
    label2.grid(row=8,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label3=Label(depositframe,text="Address",bg="light blue")
    label3.grid(row=9,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label4=Label(depositframe,text="PAN no.",bg="light blue")
    label4.grid(row=10,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label5=Label(depositframe,text="AADHAR no",bg="light blue")
    label5.grid(row=11,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label6=Label(depositframe,text="Contact no..",bg="light blue")
    label6.grid(row=12,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label7=Label(depositframe,text=" Balance",bg="light blue")
    label7.grid(row=13,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label8=Label(depositframe,text="Enter amount to deposit",bg="light blue")
    label8.grid(row=14,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)

    
    text1=Entry(depositframe,width=50,textvariable=name1)
    text1.grid(row=7,column=2)
    text2=Entry(depositframe,width=50,textvariable=age1)
    text2.grid(row=8,column=2)
    text3=Entry(depositframe,width=50,textvariable=address1)
    text3.grid(row=9,column=2)
    text4=Entry(depositframe,width=50,textvariable=panno1)
    text4.grid(row=10,column=2)
    text5=Entry(depositframe,width=50,textvariable=aadharno1)
    text5.grid(row=11,column=2)
    text6=Entry(depositframe,width=50,textvariable=contactno1)
    text6.grid(row=12,column=2)
    text7=Entry(depositframe,width=50,textvariable=balance1)
    text7.grid(row=13,column=2)
    text8=Entry(depositframe,width=50,textvariable=depositamount)
    text8.grid(row=14,column=2)

    addbutton=Button(depositframe,text="Deposit",width=20,command=deposit)
    addbutton.grid(row=17,column=1,columnspan=2,padx=10,pady=10)
    clearbutton=Button(depositframe,text="Close Window",width=20,command=closedeposit)
    clearbutton.grid(row=17,column=2,columnspan=2,padx=10,pady=10)
    cursor=conn.cursor()
    if(textaccount.get()==""):
          messagebox.showerror("Message","Please enter a valid  account no...")
          closedeposit()
          return False
    cursor.execute("select * from bankdb where acc_no="+ textaccount.get())
    records=cursor.fetchall()
    #print(records)
    if(records==[]):
          messagebox.showerror("Message","Account doesn't exist")
          closedeposit()
          return False
    else:pass
    for record in records:                  # for inserting records into text boxes from database
          text1.insert(0,record[1])
          text2.insert(0,record[2])
          text3.insert(0,record[3])
          text4.insert(0,record[4])
          text5.insert(0,record[5])
          text6.insert(0,record[6])
          text7.insert(0,record[7])
          
#----------------------------- CODE FOR ACCOUNT EDITING  WINDOW  -----------------------------------------------------------------------------     
    


def editframe():
    global editframe
    global text1,text2,text3,text4,text5,text5,text6,text7,text8,rbutton
    cursor=conn.cursor()
    '''accountno=textaccount.get()
    print(accountno,"jhdjkhkdhf")
    cursor.execute("select balance from bankdb where acc_no=?",(textaccount.get()))
    record=cursor.fetchall()
    print("******record)
    balancelabel=""
    for i in record:
          balancelabel=i[0]
          print("BalanceLabel---",balancelabel)
          pass'''
   
    editframe=Tk()
    editframe.title("Update Account Details ")
    editframe.geometry("1500x800")
    editframe.configure(background="light blue");
    
    global name1,age1,address1,panno1,aadharno1,contactno1,balance1
    name1=StringVar()
    age1=StringVar()
    address1=StringVar()
    panno1=StringVar()
    aadharno1=StringVar()
    contactno1=StringVar()
    balance1=StringVar()
    
    
   
    labelheading1=Label(editframe,text="WELCOME TO ABC BANK",font=("bold",20),fg='blue',bg="light blue")
    labelheading1.grid(row=0,column=0,columnspan=5,rowspan=3,padx=400,pady=50,ipadx=30,ipady=30)

    label1=Label(editframe,text="Name",bg="light blue")
    label1.grid(row=7,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label2=Label(editframe,text="Age",bg="light blue")
    label2.grid(row=8,column=0,columnspan=2,padx=5,pady=5,ipadx=10,ipady=10)
    label3=Label(editframe,text="Address",bg="light blue")
    label3.grid(row=9,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label4=Label(editframe,text="PAN no.",bg="light blue")
    label4.grid(row=10,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label5=Label(editframe,text="AADHAR no",bg="light blue")
    label5.grid(row=11,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label6=Label(editframe,text="Contact no..",bg="light blue")
    label6.grid(row=12,column=0,padx=5,pady=5,ipadx=10,ipady=10,columnspan=2)
    label7=Label(editframe,text="Balance for the account no." ,bg="light blue",font=("bold",12),fg="black")
    label7.grid(row=13,column=0,padx=5,pady=5,ipadx=10,ipady=10)
    label8=Label(editframe,text=accountno ,bg="light blue",font=("bold",12),fg="black")
    label8.grid(row=13,column=1,padx=5,pady=5,ipadx=10,ipady=10)
    label9=Label(editframe,text=balancelabel,bg="light blue",font=("bold",12),fg="blue")
    label9.grid(row=13,column=2,padx=5,pady=5,ipadx=10,ipady=10)
    

    
    text1=Entry(editframe,width=50,textvariable=name1)
    text1.grid(row=7,column=2)
    text2=Entry(editframe,width=50,textvariable=age1)
    text2.grid(row=8,column=2)
    text3=Entry(editframe,width=50,textvariable=address1)
    text3.grid(row=9,column=2)
    text4=Entry(editframe,width=50,textvariable=panno1)
    text4.grid(row=10,column=2)
    text5=Entry(editframe,width=50,textvariable=aadharno1)
    text5.grid(row=11,column=2)
    text6=Entry(editframe,width=50,textvariable=contactno1)
    text6.grid(row=12,column=2)
    
    
    

    updatebutton=Button(editframe,text=" Update Account Details ",width=20,command=update)
    updatebutton.grid(row=17,column=1,columnspan=2,padx=10,pady=10)
    closebutton=Button(editframe,text="Close Window",width=20,command=closeupdate)
    closebutton.grid(row=17,column=2,columnspan=2,padx=10,pady=10)
    cursor=conn.cursor()
    if(textaccount.get()==""):
          messagebox.showerror("Message","Please enter a valid  account no...")
          closeupdate()
          return False
    cursor.execute("select * from bankdb where acc_no="+ textaccount.get())
    records=cursor.fetchall()
    #print(records)
    if(records==[]):
          messagebox.showerror("Message","Account doesn't exist")
          closeupdate()
          return False
    else:pass
    for record in records:                     # for inserting records into text boxes from database
          text1.insert(0,record[1])
          text2.insert(0,record[2])
          text3.insert(0,record[3])
          text4.insert(0,record[4])
          text5.insert(0,record[5])
          text6.insert(0,record[6])
          
    conn.commit()

#----------------------------- CODE FOR SHOWING ALL ACCOUNT INFORMATION WINDOW  -----------------------------------------------------------------------------     
    


def showall():
    global showally
    showally=Tk()
    showally.geometry("1500x800")
    showally.resizable(width = 1, height = 1) 
    showally.title("Show Accounts")
    
    #showall.configure(background="light blue");
    
    cursor=conn.cursor()
    cursor.execute("select * from bankdb")

    # Using treeview widget 
    tv = ttk.Treeview(showally, selectmode ='browse') 
        
    # Calling pack method w.r.to treeview 
    tv.pack(side ='right') 
        
    # Constructing vertical scrollbar 
    # with treeview 
    verscrlbar = ttk.Scrollbar(showally,orient ="vertical",command = tv.yview) 
        
    # Calling pack method w.r.to verical  
    # scrollbar 
    verscrlbar.pack(side ='right', fill ='x') 
        
    # Configuring treeview 
    tv.configure(xscrollcommand = verscrlbar.set) 
       
    tv["columns"] = ("1","2","3","4","5","6","7","8")
    tv['show'] = 'headings'
    tv.column("1", width = 165,anchor='c' ) 
    tv.column("2", width = 165 ,anchor='c')
    tv.column("3", width = 165,anchor='c')
    tv.column("4", width =165,anchor='c')
    tv.column("5", width = 165,anchor='c')
    tv.column("6", width = 165,anchor='c')
    tv.column("7", width = 165,anchor='c')
    tv.column("8", width = 165,anchor='c')
    tv.heading(1,text="Account-no..")
    tv.heading(2,text='Name')
    tv.heading(3,text="Age")
    tv.heading(4,text="Address")
    tv.heading(5,text="PAN_NO")
    tv.heading(6,text="Aadhar_No")
    tv.heading(7,text="Contact_no")
    tv.heading(8,text="Balance")
    printdt=""
    for data in cursor:
          tv.insert("",'end',values=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))
          
    tv.pack()
  
    label1=Label(showally,text="ALL ACCOUNT DETAILS",font=("bold",20))
    label1.place(x=500,y=100)
    buttonclose=Button(showally,text="Close",width='20',command=closeshowall)
    buttonclose.place(x=550,y=600)
                 
          
          

        

#----------------------------- CODE FOR MAIN WINDOW  -----------------------------------------------------------------------------     
    


root=Tk()
root.title("ABC BANK")
root.geometry("1500x800")
root.configure(background="light blue");
myimage=ImageTk.PhotoImage(Image.open("bg3.jpg"))  
mylabel=Label(root,image=myimage)
mylabel.pack()
'''canvas = Canvas(root, width = 2000, height = 1500)              ######## ITS NOT WORKING
canvas.pack()
myimage=ImageTk.PhotoImage(Image.open("bg.jpg"))
canvas.create_image(1000, 1000, image=myimage)'''

global textaccount
myFont= font.Font(family='Helvetica', size=20, weight='bold',underline='True')
labelheading=Label(root,text="WELCOME TO ABC BANK",fg="blue",bg="light blue")
labelheading['font']=myFont
labelheading.place(x=450,y=50)
#labelheading.grid(row=10,column=40,rowspan=3,columnspan=3,ipadx=10,ipady=10)
button1=Button(root,text="Add New Account",width=50,command=addnewframe)
button1.place(x=450,y=130)
#button1.grid(row=16,column=40,columnspan=3,ipadx=10,ipady=10)
button2=Button(root,text="Show all Accounts",width=50,command=showall)
button2.place(x=450,y=180)
myFont1= font.Font(family='Helvetica', size=10, weight='bold',underline='True')
labelaccount=Label(root,text="Enter Account no.",bg="light blue",fg="blue")
labelaccount['font']=myFont1
labelaccount.place(x=450,y=230)
textaccount=Entry(root,width=38)
textaccount.place(x=578,y=230)
#button2.grid(row=17,column=40,columnspan=3,ipadx=10,ipady=10)
button3=Button(root,text="Click to Deposit",width=50,command=depositframe)
button3.place(x=450,y=280)
#button3.grid(row=18,column=40,columnspan=3,ipadx=10,ipady=10)
button4=Button(root,text="Click to Withdraw",width=50,command=withdrawframe)
button4.place(x=450,y=330)
#button4.grid(row=19,column=40,columnspan=3,ipadx=10,ipady=10)
button5=Button(root,text="Edit Account details",width=50,command=editframe)
button5.place(x=450,y=380)
#button5.grid(row=20,column=40,columnspan=3,ipadx=10,ipady=10)
button6=Button(root,text="Delete Account details",width=50,command=delete)
button6.place(x=450,y=430)
button7=Button(root,text="Exit",width=50,command=closemain)
button7.place(x=450,y=480)
#button6.grid(row=21,column=40,columnspan=3,ipadx=10,ipady=10)



root.mainloop()



'''mainwindow=Toplevel() ######                    ITS NOT WORKING       
mainwindow.title("Welcome to ABC Bank ")
mainwindow.geometry("1500x800")
canvas = Canvas(mainwindow, width = 300, height = 300)
canvas.pack()
myimage=ImageTk.PhotoImage(Image.open("bg.jpg"))
canvas.create_image(200, 200, anchor=NW, image=myimage)
mybutton=Button(mainwindow,text="Login",command=openroot)
mybutton.place(x=500,y=500)'''


