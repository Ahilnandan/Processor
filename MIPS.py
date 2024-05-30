import math
import sys
import time
first=1
dm=[]
SL=["FETCH","DECODE","EXECUTE","MEMORY","WRITEBACK"]
instruction_memory=[]
def convert_str_to_decimal(a):#It converts binary to decimal
  if(a[0]=='0'):
      return int(a,2)
  else:
      num=-2**(len(a)-1)
      a=a[1:]
      a=a[::-1]
      k=0
      for j in a:
          if(j=='1'):
              num+=2**(k)
          k+=1
      return num
def convert_str_to_decimal1(a):#It converts binary to decimal
    return int(math.fabs(int(a,2)))
def ALU(a,b,signal):
  #print('************************')
  #print(a)
  #print(b)
  if(signal=='000'):
    return a and b
  elif(signal=='010'):
    return a + b
  elif(signal=='011'):
    return a-b 
  elif(signal=="100"):
    return int(a<b)
  elif(signal=="001"):
    return int(a or b)
def sign_extender(a):
  if(a[0]=='0'):
    return '0000000000000000'+a
  else:
    return '1111111111111111'+a

def bin_to_int(a):#cnverts integer to binary to binary
  if a.isdecimal():
    a = bin(int(a))[2:].zfill(40)
  else:
    jj = int(math.fabs(int(a)))
    pa = bin(jj)[2:].zfill(40)
    new = ''.join('1' if j == '0' else '0' for j in pa)
    p = '1'
    a = bin(int(new, 2) + int(p, 2))[2:].zfill(40)
  return a
class control_mux:
  def __init__(self,signal):
    self.signal=signal
  def branch(self,value,PC,branch):
    if(self.signal==0):
      PC=PC+4
      return PC
    elif(self.signal==1 and branch==1):
      PC=PC+4+value
      return PC
    else:
      return PC+4
  def branch_checker(self,value,branch):
    if(value==0 and branch==1):
      return 1
    else:
      return 0


  def Jump(self,value,PC):
    if(self.signal==0):
      #PC=PC+4
      return 0
    else:
      return value
  def RegDst(self,value1,value2):
    if(self.signal==0):
      return (value1,0)
    else:
      return (value2,1)
  def ALU_SRC(self,value1,value2):
    if(self.signal==0):
      return value2
    else:
      return value1
  def Mem_To_Reg(self,value1,value2):
    if(self.signal==0):
      return value1
    else:
      return value2
def Control(opcode,reg):
  opcode_left=opcode[0:3]
  #print(opcode_left)
  #print("kunju")
  opcode_right=opcode[3:6]
  #print(opcode_left,opcode_right)
  opcode_left=convert_str_to_decimal1(opcode_left)
  #print(opcode_left)
  opcode_right=convert_str_to_decimal1(opcode_right)
  if(reg=='RegDst'):
    if(opcode_left==0 and opcode_right==0):
      return 1
    else:
      return 0
  elif(reg=='Mem_To_Reg'):
    if(opcode_left in range(4,8) and opcode_right in range(0,8)):
      return 1
    else:
      return 0
  elif(reg=='ALU_SRC'):
    if(opcode_left==0 and opcode_right==0 or (opcode_right in range(1,8) and opcode_left==0)):
      return 1
    else:
      return 0
  elif(reg=='Jump'):
    if(opcode_left==0 and opcode_right in range(2,4)):
      return 1
    else:
      return 0
  elif(reg=='Branch'):
    if(opcode_left==0 and opcode_right in range(4,8)):
      return 1
    else:
      return 0
  elif(reg=='ALU_OP'):
    if(opcode_left==0 and opcode_right==0):
      return '10'
    elif(opcode_left==0 and opcode_right in range(4,8)):
      return '01'
    elif(opcode_left in range(4,8) and opcode_right in range(0,8)):
      return '00'
  elif(reg=='MemWrite'):
    if(opcode_left==5 and opcode_right in range(0,8)):
      return 1
    else:
      return 0
  elif(reg=='MemRead'):
    if(opcode_left==4 and opcode_right in range(0,8)):
      return 1
    else:
      return 0
  elif(reg=='RegWrite'):
    if(opcode_left==1 or (opcode_left==0 and opcode_right==0) or (opcode_left==4)):
      return 1
    else:
      return 0

def ALU_Control(ALU_OP,func_code):
  if(ALU_OP=='00'):
    return '010'
  elif(ALU_OP=='01'):
    return '011'
  elif(ALU_OP=='10' and func_code=='100000'):
    return '010'
  elif(ALU_OP=='10' and func_code=='100010'):
    return '011'
  elif(ALU_OP=='10' and func_code=='100100'):
    return '000'
  elif(ALU_OP=='10'and func_code=='100101'):
    return '001'
  elif(ALU_OP=='10' and func_code=='101010'):
    return '100'
def clock(stage,count):
  #print(stage,count)
  #print(SL)
  #time.sleep(1)
  ch=SL.index(stage)
  print("clock cycle=",count+1)
  #print(ch)
  if(ch<4):
    ch=ch+1
  else:
    ch=0
  count=count+1
  return (SL[ch],count)
class Instruction_memory:
  def __init__ (self):
    self.PC=0
  def set_instruction_memory(self):
    f = open("instruction_memory.txt", "r")
    k=f.readlines()
    kii=[]
    for i in k:
      text=i.strip()
      kii.append(text)
    list=[]
    m=''
    for i in kii:
      for j in i:
        m=j+m
      list.append(m)
      m=''
    c=8
    for i in list:
      c=8
      for p in range(0,4):
        instruction_memory.append(i[c-8:c])
        c=c+8
  def fetch(self,PC):
    s=''
    for i in range(0,4):
      if(i+PC)<len(instruction_memory)-4:
        s=s+instruction_memory[i+PC]
      else:
        print('Implementation done')
        sys.exit()
    return s
class register_manager:
  def __init__(self):
    self.rs=0
    self.at=0
    self.v0=0
    self.v1=0
    self.a0=0
    self.a1=0
    self.a2=0
    self.a3=0
    self.t0=0
    self.t1=0
    self.t2=0
    self.t3=0
    self.t4=0
    self.t5=0
    self.t6=0
    self.t7=0
    self.s0=0
    self.s1=0
    self.s2=0
    self.s3=0
    self.s4=0
    self.s5=0
    self.s6=0
    self.s7=0
    self.t8=0
    self.t9=0
    self.k0=0
    self.k1=0
    self.gp=0
    self.sp=0
    self.fp=0
    self.ra=0
    self.IF=0
    self.ID=0
    self.MEM=0
    self.zero=0
    self.dict={0:self.zero,1:self.at,2:self.v0,3:self.v1,4:self.a0,5:self.a1,6:self.a2,7:self.a3,8:self.t0,9:self.t1,10:self.t2,11:self.t3,12:self.t4,13:self.t5,14:self.t6,15:self.t7,16:self.s0,17:self.s1,18:self.s2,19:self.s3,20:self.s4,21:self.s5,22:self.s6,23:self.s7,24:self.t8,25:self.t9,26:self.k0,27:self.k1,28:self.gp,29:self.sp,30:self.fp,31:self.ra}
    self.write_choice=0
  def load(self,value):
    self.IF=value
    return self.IF
  def set_register(self,rs,rd,rt="00000"):
    self.temp=convert_str_to_decimal1(rs)
    self.rs=self.temp
    self.temp=convert_str_to_decimal1(rt)
    if(rt!=0):
      self.rt=self.temp
    self.temp=convert_str_to_decimal1(rd)
    self.rd=self.temp
  def read_register(self):
    return (self.dict[self.rs],self.dict[self.rd])
  def choose_write_register(self,choice):
    if(choice==0):
      self.write_choice=self.rd
    else:
      self.write_choice=self.rt
  def write_register(self,value):
    self.dict[self.write_choice]=value
    print("reigster file after writeback = ",self.dict)
class data_memory:
  def __init__(self):
    self.dm_index=0
  def set_data_memory(self):
    f = open("data_memory.txt", "r")
    k=f.readlines()
    kii=[]
    for i in k:
      st=i.strip()
      kii.append(st)
    list=[]
    m=''
    for i in kii:
      for j in i:
        m=j+m
      list.append(m)
      m=''
    c=8
    for i in kii:
      c=8
      for p in range(0,4):
        dm.append(i[c-8:c])
        c=c+8
  def read_data_memory(self,index):
    s=''
    for i in range(0,4):
      s=s+dm[i+4*index]
    return s
  def write_data_memory(self,value,index):
    c=8
    for i in range(0,4):
      dm[index+i]=value[c-8:c]
      c=c+8
class data_path:
  def __init__(self,state):
    self.a=0
    self.state=state
    self.alu_result=0
    self.mem_result=0
    self.write_data=0
    self.mem_write=0
    self.mem_read=0
    self.write_enable=0
    self.alu_op=0
    self.mem_to_reg=0
    self.count=0
    self.PC=0
    self.stage="FETCH"
    self.Funcode=0
    control_keys=['Mem_To_Reg', 'ALU_SRC', 'ALU_OP', 'RegWrite', 'MemWrite', 'Branch', 'Jump', 'RegDst','MemRead']
    self.control_signals=dict.fromkeys(control_keys)
    self.IF=[]
    self.temp=0
    self.AlU_control=0
    self.ALU_result=0
    self.memory_access=0
    self.reg=0
    self.a=register_manager()
  def stage_caller(self,stage,first):
    print(stage)
 
    time.sleep(1)
    if(first==1):
      data_path.fetch(self)
    else:
      a,b=clock(self.stage,self.count)
      self.count=b
      self.stage=a
      if(a=="FETCH"):
        data_path.fetch(self)
      elif(a== "DECODE"):
        data_path.decode(self)
      elif(a=="EXECUTE"):
        data_path.execute(self)
      elif(a=="MEMORY"):
        data_path.memory(self)
      elif(a=="WRITEBACK"):
        data_path.writeback(self)
  def fetch(self):
    if (len(instruction_memory)-4 < self.PC):
      print("Implementation done")
      sys.exit()
    first=0
    data=Instruction_memory()
    temp=data.fetch(self.PC)
    self.IF=temp
    self.a.load(temp)
    data_path.stage_caller(self,"FETCH",first=0)
  def decode(self):
    print("IF=",self.IF)
    print("Control_signals",self.control_signals)
    for i in self.control_signals:
      self.control_signals[i]=Control(self.IF[31:25:-1],i)
    temp=self.control_signals['RegDst']
    a=control_mux(temp)
    h,b=a.RegDst(self.IF[20:15:-1],self.IF[15:10:-1])
    self.a.set_register(self.IF[25:20:-1],self.IF[20:15:-1],h)
    self.a.choose_write_register(b)
    self.temp=sign_extender(self.IF[15:0:-1]+self.IF[0])
    self.Funcode=self.IF[5:0:-1]+self.IF[0]
    temp=self.control_signals['ALU_OP']
    self.AlU_control=ALU_Control(temp,self.Funcode)
    self.stage='DECODE'
    data_path.stage_caller(self,"DECODE",first=0)

  def execute(self):
    temp=self.control_signals['Jump']
    a=control_mux(temp)
    a=a.Jump(self.temp,self.PC)
    if(a==0):
      a1,a2=self.a.read_register()
      temp=self.control_signals['ALU_SRC']
      b=control_mux(temp)
      ac=convert_str_to_decimal(self.temp)
      choice=b.ALU_SRC(a2,ac)
      self.ALU_result=ALU(a1,choice,self.AlU_control)
      self.state="EXECUTE"
      data_path.stage_caller(self,"EXECUTE",first=0)
    else:
      self.temp=self.temp+'00'
      self.temp='0000'+self.temp
      self.PC=self.temp
      data_path.stage_caller(self,"WRITEBACK",first=0)


  def memory(self):
    temp=self.control_signals['Branch']
    k=control_mux(temp)
    temp12=k.branch_checker(self.ALU_result,temp)
    print("ALU=",self.ALU_result)
    if(temp12!=1):
      value=0
      self.PC=k.branch(value,self.PC,temp)
      print("PC",self.PC)
    elif(temp12==1):
      value=convert_str_to_decimal(self.temp)
      value=value<<2
      print("PC",self.PC)
      self.PC=k.branch(value,self.PC,temp)
    if(self.control_signals['MemRead']==1):
      a=data_memory()
      self.memory_access=a.read_data_memory(self.ALU_result)
      self.memory_access=convert_str_to_decimal(self.memory_access)

    if(self.control_signals['MemWrite']==1):
      a=data_memory()
      a1,a2=self.a.read_register()
      a.write_data_memory(a1,self.ALU_result)
    data_path.stage_caller(self,"MEMORY",first=0)
  def writeback(self):
    temp=self.control_signals['Mem_To_Reg']
    a=control_mux(temp)
    a=a.Mem_To_Reg(self.ALU_result,self.memory_access)
    temp=self.control_signals['RegWrite']
    if(temp==1):
      self.a.write_register(a)
    data_path.stage_caller(self,"WRITEBACK",first=0)
b=Instruction_memory()
b.set_instruction_memory()
print("Instruction memory = ",instruction_memory)
b=data_memory()
b.set_data_memory()
print("Data_memory=",dm)
a=data_path("FETCH")
a.stage_caller("FETCH",first)

      
    





