import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import time
import secrets
import shutil
import zipfile
import re
import tkinter.messagebox

print("""
最小间隔默认为0，如要修改请在框内输入分数（不支持小数）
如果卡死了就把最小间隔改小一点
BugReport：QQ 3125998062
""")

filenamelist=[]
mczlist=[]
distance=0
Mistery=0
effectlist=[]

root=tk.Tk()
root.geometry("400x200")
root.title("MCZ Randomizer by @NENENEKO")

def GetDistance():
    global distance,Mistery,effectlist
    if SetDistanceEntry.get() != "Mistery":
        match=re.match(r"(\d+)/(\d+)",SetDistanceEntry.get())
        if match:
            distance=int(match.group(1))/int(match.group(2))
        if not match:
            tk.messagebox.showerror("error","输入的不是分数")

    elif SetDistanceEntry.get() == "Mistery":
        Mistery=1

def SelectOszFile():
    print("选择文件中......")
    global filepath
    filepath=filedialog.askopenfilenames(title="Select .mcz file",
                                        filetypes=[("mcz file","*.mcz")],
                                        multiple=True)
    for i in range(len(filepath)):
        filenamelist.append(os.path.basename(filepath[i])[0:-4])
    print("文件选择完成！")

def UnzipFile():
    global filepath
    print("文件解压中......")
    if os.path.exists("./temp"):
        shutil.rmtree("./temp")
    if os.path.exists("./output"):
        shutil.rmtree("./output")
    for file in range(len(filenamelist)):
        os.makedirs(f"./temp/{filenamelist[file]}")
        os.makedirs(f"./temp/random {filenamelist[file]}")
        with zipfile.ZipFile(filepath[file], 'r') as mczfile:
            mczfile.extractall(f"./temp/{filenamelist[file]}")
    print("文件解压完成！")

def GetFileName(i):
    mczlist.clear()
    for dirpath, dirnames, filenames in os.walk(f"./temp/{filenamelist[i]}"):
        for filename in filenames:
            if re.match(r'.*\.mc$', filename, flags=re.IGNORECASE):
                mczlist.append(filename)
        break
    for name in mczlist:
        randomize(name,i)

def randomize(mcfile,i):
    mccontent=json.load(open(f"./temp/{filenamelist[i]}/{mcfile}",encoding="utf-8"))
    notepos=[]
    lnarrdict={}
    lnpos=[]
    shutil.copyfile(f"./temp/{filenamelist[i]}/{mccontent["meta"]["background"]}",f"./temp/random {filenamelist[i]}/{mccontent["meta"]["background"]}")
    shutil.copyfile(f"./temp/{filenamelist[i]}/{mccontent["note"][-1]["sound"]}",f"./temp/random {filenamelist[i]}/{mccontent["note"][-1]["sound"]}")
    print(f"正在随机化 {os.path.basename(mcfile)} ......")
    for note in range(len(mccontent["note"])-1):#添加note位置到notepos
        notepos.append(mccontent["note"][note]["beat"][0]+mccontent["note"][note]["beat"][1]/mccontent["note"][note]["beat"][2])
        if len(mccontent["note"][note])>=3:
            lnpos.append(note)#添加ln位置到lnpos，添加ln范围，轨道到lnarrdict
            lnarrdict[note]=[[mccontent["note"][note]["beat"][0]+mccontent["note"][note]["beat"][1]/mccontent["note"][note]["beat"][2],mccontent["note"][note]["endbeat"][0]+mccontent["note"][note]["endbeat"][1]/mccontent["note"][note]["endbeat"][2]],mccontent["note"][note]["column"]]
    for j in range(len(notepos)-1):
        if j==0:
            mccontent["note"][j]["column"]=secrets.choice(list(range(mccontent["meta"]["mode_ext"]["column"])))#随机摆放第一个note。如果是ln，更新lnarrdict
            if len(mccontent["note"][j])>=3:
                lnarrdict[j]=[[mccontent["note"][j]["beat"][0]+mccontent["note"][j]["beat"][1]/mccontent["note"][j]["beat"][2],mccontent["note"][j]["endbeat"][0]+mccontent["note"][j]["endbeat"][1]/mccontent["note"][j]["endbeat"][2]],mccontent["note"][j]["column "]]

        if j==1:
            notearr=list(range(mccontent["meta"]["mode_ext"]["column"]))
            for m in lnpos:#遍历lnpos，如果第j个note在ln范围内，减小随机范围
                if notepos[j]>=lnarrdict[m][0][0] and notepos[j]<=lnarrdict[m][0][1] and (lnarrdict[m][1] in notearr):
                    notearr.remove(lnarrdict[m][1])
            #如果和上一个note距离过近，减小随机范围
            if abs(notepos[j]-notepos[j-1])<=distance and (mccontent["note"][j-1]["column"] in notearr):
                notearr.remove(mccontent["note"][j-1]["column"])
            if len(mccontent["note"][j])>=3 and notearr==[]:
                notearr.append(mccontent["note"][j]["column"])
            mccontent["note"][j]["column"]=secrets.choice(notearr)
            if len(mccontent["note"][j])>=3:
                lnarrdict[j]=[[mccontent["note"][j]["beat"][0]+mccontent["note"][j]["beat"][1]/mccontent["note"][j]["beat"][2],mccontent["note"][j]["endbeat"][0]+mccontent["note"][j]["endbeat"][1]/mccontent["note"][j]["endbeat"][2]],mccontent["note"][j]["column"]]
        
        if j == 2:
            notearr=list(range(mccontent["meta"]["mode_ext"]["column"]))
            for m in lnpos:#遍历lnpos，如果第j个note在ln范围内，减小随机范围
                if notepos[j]>=lnarrdict[m][0][0] and notepos[j]<=lnarrdict[m][0][1] and (lnarrdict[m][1] in notearr):
                    notearr.remove(lnarrdict[m][1])
            #如果和上一个note距离过近，减小随机范围
            if abs(notepos[j]-notepos[j-1])<=distance and (mccontent["note"][j-1]["column"] in notearr):
                notearr.remove(mccontent["note"][j-1]["column"])
            if abs(notepos[j]-notepos[j-2])<=distance and (mccontent["note"][j-2]["column"] in notearr):
                notearr.remove(mccontent["note"][j-2]["column"])
            if len(mccontent["note"][j])>=3 and notearr==[]:
                notearr.append(mccontent["note"][j]["column"])
            mccontent["note"][j]["column"]=secrets.choice(notearr)
            if len(mccontent["note"][j])>=3:
                lnarrdict[j]=[[mccontent["note"][j]["beat"][0]+mccontent["note"][j]["beat"][1]/mccontent["note"][j]["beat"][2],mccontent["note"][j]["endbeat"][0]+mccontent["note"][j]["endbeat"][1]/mccontent["note"][j]["endbeat"][2]],mccontent["note"][j]["column"]]

        if j == 3:
            notearr=list(range(mccontent["meta"]["mode_ext"]["column"]))
            for m in lnpos:#遍历lnpos，如果第j个note在ln范围内，减小随机范围
                if notepos[j]>=lnarrdict[m][0][0] and notepos[j]<=lnarrdict[m][0][1] and (lnarrdict[m][1] in notearr):
                    notearr.remove(lnarrdict[m][1])
            #如果和上一个note距离过近，减小随机范围
            if abs(notepos[j]-notepos[j-1])<=distance and (mccontent["note"][j-1]["column"] in notearr):
                notearr.remove(mccontent["note"][j-1]["column"])
            if abs(notepos[j]-notepos[j-2])<=distance and (mccontent["note"][j-2]["column"] in notearr):
                notearr.remove(mccontent["note"][j-2]["column"])
            if abs(notepos[j]-notepos[j-3])<=distance and (mccontent["note"][j-3]["column"] in notearr):
                notearr.remove(mccontent["note"][j-3]["column"])
            if len(mccontent["note"][j])>=3 and notearr==[]:
                notearr.append(mccontent["note"][j]["column"])
            mccontent["note"][j]["column"]=secrets.choice(notearr)
            if len(mccontent["note"][j])>=3:
                lnarrdict[j]=[[mccontent["note"][j]["beat"][0]+mccontent["note"][j]["beat"][1]/mccontent["note"][j]["beat"][2],mccontent["note"][j]["endbeat"][0]+mccontent["note"][j]["endbeat"][1]/mccontent["note"][j]["endbeat"][2]],mccontent["note"][j]["column"]]

        if j>=4:
            notearr=list(range(mccontent["meta"]["mode_ext"]["column"]))
            for m in lnpos:#遍历lnpos，如果第j个note在ln范围内，减小随机范围
                if notepos[j]>=lnarrdict[m][0][0] and notepos[j]<=lnarrdict[m][0][1] and (lnarrdict[m][1] in notearr):
                    notearr.remove(lnarrdict[m][1])
            #如果和上一个note距离过近，减小随机范围
            if abs(notepos[j]-notepos[j-1])<=distance and (mccontent["note"][j-1]["column"] in notearr):
                notearr.remove(mccontent["note"][j-1]["column"])
            if abs(notepos[j]-notepos[j-2])<=distance and (mccontent["note"][j-2]["column"] in notearr):
                notearr.remove(mccontent["note"][j-2]["column"])
            if abs(notepos[j]-notepos[j-3])<=distance and (mccontent["note"][j-3]["column"] in notearr):
                notearr.remove(mccontent["note"][j-3]["column"])
            if abs(notepos[j]-notepos[j-4])<=distance and (mccontent["note"][j-4]["column"] in notearr):
                notearr.remove(mccontent["note"][j-4]["column"])
            if len(mccontent["note"][j])>=3 and notearr==[]:
                notearr.append(mccontent["note"][j]["column"])
            mccontent["note"][j]["column"]=secrets.choice(notearr)
            if len(mccontent["note"][j])>=3:
                lnarrdict[j]=[[mccontent["note"][j]["beat"][0]+mccontent["note"][j]["beat"][1]/mccontent["note"][j]["beat"][2],mccontent["note"][j]["endbeat"][0]+mccontent["note"][j]["endbeat"][1]/mccontent["note"][j]["endbeat"][2]],mccontent["note"][j]["column"]]

    if Mistery==1:
        for mistery in range(mccontent["note"][-2]["beat"][0]):
            print("??@!#%^%?&?^&%^?*$%$@!$?~@!??*%&()")
            effectlist.append({"beat":[mistery,0,1],"scroll":secrets.randbelow(300)*0.01})
            mccontent["effect"]=effectlist
    with open(f"./temp/random {filenamelist[i]}/{mcfile}", "w", encoding="utf-8") as f:
        json.dump(mccontent, f, ensure_ascii=False,indent=None, separators=(',', ':'))
    print(f"{os.path.basename(mcfile)} 随机化完成！")

        



def CombinedFunction():
    starttime=time.time()
    SelectFileButton.config(state="disabled",text="转化中")
    SelectOszFile()
    UnzipFile()
    for i in range(len(filenamelist)): 
        GetFileName(i)
        with zipfile.ZipFile(f"./{filenamelist[i]}.mcz","w") as outputmcz:
            print(f"构建{filenamelist[i]}.mcz...")
            for dirpath, dirnames, filenames in os.walk(f"./temp/random {filenamelist[i]}"):
                for filename in filenames:
                    outputmcz.write(os.path.join(dirpath, filename),arcname=filename)
            print(f"构建{filenamelist[i]}.mcz完毕！")
    SelectFileButton.config(state="disabled",text="转化完毕！")
    endtime=time.time()
    print(f"总用时：{endtime-starttime}秒")


SelectFileButton = tk.Button(root,
                             text="Select .mcz File",
                             background='deepskyblue',
                             activebackground='royalblue',
                             command=CombinedFunction)
SelectFileButton.place(x=0, y=0)

SetDistanceTip=tk.Label(root,text="输入最小间隔：(如：1/8)")
SetDistanceTip.place(x=0,y=30)
SetDistanceEntry=tk.Entry(root)
SetDistanceEntry.place(width=75,x=0,y=50)
SetDistanceButton=tk.Button(root,text="确认",command=GetDistance)
SetDistanceButton.place(x=80,y=50)

root.mainloop()

