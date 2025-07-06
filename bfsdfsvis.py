import tkinter as tk
import queue

root=tk.Tk()
root.title("BFS Visualization")

buttons=[]
mode=1
greenbtn=-1
redbtn=-1
q=queue.Queue()
s=[]
fromm=[0]*400
algoactive=False
pathIsVisible=False
l=tk.Label(root,height=2,width=40,text="Welcome to the BFS and DFS visualizer!", font=("Arial",14,"bold"))

def toggle(idx):
    if (algoactive or pathIsVisible):
        l.config(text="You can't do that right now!")
        return
    global greenbtn, redbtn, mode
    currcolor=buttons[idx]["bg"]
    if mode==1:
        if currcolor=="white":
            buttons[idx]["bg"]="black"
        else:
            buttons[idx]["bg"]="white"
    elif mode==2 and currcolor=="white":
        if greenbtn!=-1:
            buttons[greenbtn]["bg"]="white"
        buttons[idx]["bg"]="green"
        greenbtn=idx
    elif mode==3 and currcolor=="white":
        if redbtn!=-1:
            buttons[redbtn]["bg"]="white"
        buttons[idx]["bg"]="red"
        redbtn=idx
            
def change(num):
    if (algoactive or pathIsVisible):
        l.config(text="You can't do that right now!")
        return
    global mode
    mode=num
    if (mode==1):
        l.config(text="You are now drawing black squares.")
    elif (mode==2):
        l.config(text="You are now selecting a starting point.")
    elif (mode==3):
        l.config(text="You are now selecting a finishing point.")

def bfs():
    global algoactive, pathIsVisible
    if (algoactive or pathIsVisible):
        l.config(text="You can't do that right now!")
        return
    if (greenbtn==-1 or redbtn==-1):
        l.config(text="Please select a starting and a finishing point!")
        return
    l.config(text="BFS Visualization is in progress.")
    algoactive=True
    pathIsVisible=True
    global q
    q.put(greenbtn)
    doQueue()

def doQueue():
    global q, fromm, algoactive
    att=q.get()
    if (att!=greenbtn):
        buttons[att]["bg"]="blue"
    if att%20!=0 and att-1>=0 and att-1<400 and (buttons[att-1]["bg"]=="white" or buttons[att-1]["bg"]=="red"):
        q.put(att-1)
        fromm[att-1]=att
        if (buttons[att-1]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="BFS Visualization has finished.")
            return
        buttons[att-1]["bg"]="purple"
    if (att+1)%20!=0 and att+1>=0 and att+1<400 and (buttons[att+1]["bg"]=="white" or buttons[att+1]["bg"]=="red"):
        q.put(att+1)
        fromm[att+1]=att
        if (buttons[att+1]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="BFS Visualization has finished.")
            return
        buttons[att+1]["bg"]="purple"
    if att>19 and att-20>=0 and att-20<400 and (buttons[att-20]["bg"]=="white" or buttons[att-20]["bg"]=="red"):
        q.put(att-20)
        fromm[att-20]=att
        if (buttons[att-20]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="BFS Visualization has finished.")
            return
        buttons[att-20]["bg"]="purple"
    if att<380 and att+20>=0 and att+20<400 and (buttons[att+20]["bg"]=="white" or buttons[att+20]["bg"]=="red"):
        q.put(att+20)
        fromm[att+20]=att
        if (buttons[att+20]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="BFS Visualization has finished.")
            return
        buttons[att+20]["bg"]="purple"
    if (q.empty()):
        algoactive=False
        l.config(text="BFS Visualization has finished.")
        return
    root.after(20,doQueue)

def dfs():
    global algoactive, pathIsVisible
    if (algoactive or pathIsVisible):
        l.config(text="You can't do that right now!")
        return
    if (greenbtn==-1 or redbtn==-1):
        l.config(text="Please select a starting and a finishing point!")
        return
    l.config(text="DFS Visualization is in progress.")
    algoactive=True
    pathIsVisible=True
    global s
    s.append(greenbtn)
    doStack()

def doStack():
    global s, fromm, algoactive
    att=s.pop()
    if (att!=greenbtn):
        buttons[att]["bg"]="blue"
    if att%20!=0 and att-1>=0 and att-1<400 and (buttons[att-1]["bg"]=="white" or buttons[att-1]["bg"]=="red"):
        s.append(att-1)
        fromm[att-1]=att
        if (buttons[att-1]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="DFS Visualization has finished.")
            return
        buttons[att-1]["bg"]="purple"
    if (att+1)%20!=0 and att+1>=0 and att+1<400 and (buttons[att+1]["bg"]=="white" or buttons[att+1]["bg"]=="red"):
        s.append(att+1)
        fromm[att+1]=att
        if (buttons[att+1]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="DFS Visualization has finished.")
            return
        buttons[att+1]["bg"]="purple"
    if att>19 and att-20>=0 and att-20<400 and (buttons[att-20]["bg"]=="white" or buttons[att-20]["bg"]=="red"):
        s.append(att-20)
        fromm[att-20]=att
        if (buttons[att-20]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="DFS Visualization has finished.")
            return
        buttons[att-20]["bg"]="purple"
    if att<380 and att+20>=0 and att+20<400 and (buttons[att+20]["bg"]=="white" or buttons[att+20]["bg"]=="red"):
        s.append(att+20)
        fromm[att+20]=att
        if (buttons[att+20]["bg"]=="red"):
            drawPath()
            algoactive=False
            l.config(text="DFS Visualization has finished.")
            return
        buttons[att+20]["bg"]="purple"
    if (not s):
        algoactive=False
        l.config(text="DFS Visualization has finished.")
        return
    root.after(20,doStack)

def drawPath():
    global fromm, redbtn
    att=fromm[redbtn]
    while (att!=greenbtn):
        buttons[att]["bg"]="orange"
        att=fromm[att]

def clearPath():
    global algoactive, pathIsVisible
    if (algoactive):
        l.config(text="You can't do that right now!")
        return
    global q,s,fromm
    q.queue.clear()
    s.clear()
    fromm=[0]*400
    for i in range(400):
        if buttons[i]["bg"]=="blue" or buttons[i]["bg"]=="orange" or buttons[i]["bg"]=="purple":
            buttons[i]["bg"]="white"
    pathIsVisible=False
    l.config(text="The path has been cleared.")

def reset():
    global algoactive, pathIsVisible
    if (algoactive):
        l.config(text="You can't do that right now!")
        return
    global fromm, q, greenbtn, redbtn
    for i in range(400):
        buttons[i]["bg"]="white"
    q.queue.clear()
    fromm=[0]*400
    greenbtn=-1
    redbtn=-1
    algoactive=False
    pathIsVisible=False
    l.config(text="The canvas has been cleared.")

for i in range(20):
    for j in range(20):
        btn=tk.Button(
            root,
            bg="white",
            width=2,
            height=1,
            command=lambda num=20*i+j:toggle(num)
        )
        btn.grid(row=i,column=j)
        buttons.append(btn)

btn1 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Draw black (unvisitable) squares", command=lambda num=1: change(num))
btn1.grid(row=20, column=0, columnspan=20, sticky="w")

btn2 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Pick a starting point (green square)", command=lambda num=2: change(num))
btn2.grid(row=21, column=0, columnspan=20, sticky="w")

btn3 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Pick a finishing point (red square)", command=lambda num=3: change(num))
btn3.grid(row=22, column=0, columnspan=20, sticky="w")

btn4 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Visualize the BFS Algorithm", command=bfs)
btn4.grid(row=23, column=0, columnspan=20, sticky="w")

btn5 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Visualize the DFS Algorithm", command=dfs)
btn5.grid(row=24, column=0, columnspan=20, sticky="w")

btn6 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Clear path", command=clearPath)
btn6.grid(row=25, column=0, columnspan=20, sticky="w")

btn7 = tk.Button(root, height=1, width=70, bg="black", fg="white", text="Clear canvas", command=reset)
btn7.grid(row=26, column=0, columnspan=20, sticky="w")

l.grid(row=27,column=0,columnspan=20)

root.mainloop()