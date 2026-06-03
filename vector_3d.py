from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#----------------------------------------
import math
def simplify_square_root(n):
    if n==0:
        return 0,0
    a=1
    b=n
    d=2
    while (d*d)<=b:
        while b%(d*d)==0:
            a*=d
            b//=(d*d)
        d+=1
    return a,b
def format_radical_latex(n):
    a,b=simplify_square_root(n)
    if a==0:
        return "0"
    if b==1:
        return f"{a}"
    if a==1:
        return f"√{b}"
    return f"{a}√{b}"

class Point3d:
    def __init__(self,i,j,k):
        self.i=i
        self.j=j
        self.k=k
    def representation(self):
        if(self.i>0 and self.j>0 and self.k>0):
            return ("{}i +{}j +{}k".format(self.i,self.j,self.k))
        elif(self.i>0 and self.j>0 and self.k<0):
            return ("{}i +{}j {}k".format(self.i,self.j,self.k))
        elif(self.i>0 and self.j<0 and self.k>0):
            return ("{}i {}j +{}k".format(self.i,self.j,self.k))
        elif(self.i<0 and self.j>0 and self.k>0):
            return ("{}i +{}j +{}k".format(self.i,self.j,self.k))
        elif(self.i>0 and self.j<0 and self.k<0):
            return ("{}i {}j {}k".format(self.i,self.j,self.k))
        elif(self.i<0 and self.j>0 and self.k<0):
            return ("{}i +{}j {}k".format(self.i,self.j,self.k))
        elif(self.i<0 and self.j<0 and self.k>0):
            return ("{}i {}j +{}k".format(self.i,self.j,self.k))
        else:
            return ("{}i {}j {}k".format(self.i,self.j,self.k))
    def __add__(self,other):
        new_i=self.i+other.i
        new_j=self.j+other.j
        new_k=self.k+other.k
        new=Point3d(new_i,new_j,new_k)
        return Point3d.representation(new)
    def __sub__(self,other):
        new_i=self.i-other.i
        new_j=self.j-other.j
        new_k=self.k-other.k
        new=Point3d(new_i,new_j,new_k)
        return Point3d.representation(new)
    def distance(self,other):
        new_i=self.i-other.i
        new_j=self.j-other.j
        new_k=self.k-other.k
        dis_squared=((new_i**2)+(new_j**2)+(new_k**2))
        radical_form=format_radical_latex(dis_squared)
        dis=math.sqrt(dis_squared)
        return "{} units or {} units".format(dis,radical_form)
    def mid_point(self,other):
        new_i=(self.i+other.i)/2
        new_j=(self.j+other.j)/2
        new_k=(self.k+other.k)/2
        new=Point3d(new_i,new_j,new_k)
        return Point3d.representation(new)
    def divide_section_internal(self,other,m,n):
        total=m+n
        new_i=(other.i*m+self.i*n)/total
        new_j=(other.j*m+self.j*n)/total
        new_k=(other.k*m+self.k*n)/total
        new=Point3d(new_i,new_j,new_k)
        return Point3d.representation(new)
    def divide_section_external(self,other,m,n):
        total=m-n
        new_i=(other.i*m-self.i*n)/total
        new_j=(other.j*m-self.j*n)/total
        new_k=(other.k*m-self.k*n)/total
        new=Point3d(new_i,new_j,new_k)
        return Point3d.representation(new)
    def line_equation(self,other):
        new_i=other.i-self.i
        new_j=other.j-self.j
        new_k=other.k-self.k
        new=Point3d(new_i,new_j,new_k)
        return "r={} + l({})".format(Point3d.representation(self),Point3d.representation(new))
    def unit_vector(self,other=None):
        if other==None:
            new_i=self.i
            new_j=self.j
            new_k=self.k
        else:
            new_i=(other.i-self.i)
            new_j=(other.j-self.j)
            new_k=(other.k-self.k)
        mod=math.sqrt(new_i**2+new_j**2+new_k**2)
        if mod == 0:
            return "0i +0j +0k"
        new=Point3d(new_i/mod,new_j/mod,new_k/mod)
        return Point3d.representation(new)


#-----------------------------------
root=Tk()
root.title("Vector3D")
root.geometry("1100x800")
root.configure(background="black")
root.iconbitmap("favicon.ico")
img=Image.open("vector_3d.png")
resized_img=img.resize((400,200))
img=ImageTk.PhotoImage(resized_img)
img_label=Label(root,image=img,background="black")
img_label.pack(pady=(10,10))

left_panel=Frame(root,bg="black")
left_panel.pack(side=LEFT,fill=Y,padx=20,pady=20)
right_panel=Frame(root,bg="black")
right_panel.pack(side=RIGHT,fill=BOTH,expand=True,padx=20,pady=20)

text_label=Label(left_panel,text="Vector3D",bg="black",fg="white",font=("verdana",30,"bold"))
text_label.pack(anchor="w",pady=(0, 20))

points_frame=Frame(left_panel,bg="black")
points_frame.pack(anchor="w",pady=10)

Label(points_frame,text="Enter number of points to insert(1/2):",bg="black",fg="white",font=("Helvetica", 11)).pack()
points_input=Entry(points_frame,width=5,justify="center")
points_input.pack(side=LEFT,padx=3)

vector_entries=[]
vector_container=Frame(left_panel,bg="black")
vector_container.pack(pady=10)

action_frame=Frame(left_panel,bg="black")
action_frame.pack(pady=10)

ratio_frame=Frame(left_panel,bg="black")

result_label=Label(left_panel,text="",bg="black",fg="green")
result_label.pack(pady=20)

fig=Figure(figsize=(5,5),dpi=100,facecolor="black")
ax=fig.add_subplot(111,projection="3d")
ax.set_facecolor("black")

def style_3d_axes():
    ax.tick_params(colors='orange')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.xaxis.line.set_color('green')
    ax.yaxis.line.set_color('green')
    ax.zaxis.line.set_color('green')
style_3d_axes()

canvas = FigureCanvasTkAgg(fig, master=right_panel)
canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def generate_inputs():
    global vector_entries
    for widget in vector_container.winfo_children():
        widget.destroy()
    for widget in action_frame.winfo_children():
        widget.destroy()
    for widget in ratio_frame.winfo_children():
        widget.destroy()
    result_label.config(text="")
    vector_entries=[]
    try:
        num_points=int(points_input.get())
        if num_points not in [1, 2]:
            result_label.config(text="Please choose either 1 or 2 points!",fg="red")
            return
        for i in range(1, num_points + 1):
            box=Frame(vector_container,bg="#111",bd=1,relief=RIDGE,padx=10,pady=10)
            box.pack(side=LEFT,padx=5)
            Label(box,text=f"Vector {i}",bg="#111",fg="orange",font=("Helvetica",10,"bold")).pack()           
            xyz_frame=Frame(box,bg="#111")
            xyz_frame.pack(pady=2)          
            entries={}
            for ax_name in ['i','j','k']:
                f=Frame(xyz_frame,bg="#111")
                f.pack(pady=2)
                Label(f,text=f"{ax_name}:",bg="#111",fg="white",width=2).pack(side=LEFT)
                e=Entry(f,width=5,justify="center")
                e.pack(side=LEFT)
                entries[ax_name]=e           
            vector_entries.append(entries)
        function_ui(num_points)
    except ValueError:
        result_label.config(text="Please enter a valid integer!",fg="red")

def function_ui(num_points):
    if num_points==1:
        choices=['Representation','Unit Vector']
    else:
        choices=['Add','Subtract','Distance','Mid-Point','Divide Section (Internal)','Divide Section (External)','Line Equation','Unit Vector']
    Label(action_frame,text="Operation:",bg="black",fg="white").pack(side=LEFT,padx=5)
    dropdown=ttk.Combobox(action_frame,values=choices,state="readonly",width=22)
    dropdown.pack(side=LEFT,padx=5)
    dropdown.set(choices[0])

    calc_btn=Button(action_frame,text="Calculate & Plot",bg="green",fg="white",command=lambda: execute_and_plot(dropdown, num_points))
    calc_btn.pack(side=LEFT,padx=5)
    
    def on_dropdown_change(event):
        for widget in ratio_frame.winfo_children():
            widget.destroy()
        ratio_frame.pack_forget()
        if "Divide Section" in dropdown.get():
            ratio_frame.pack(anchor="w",pady=2)
            Label(ratio_frame,text="Ratio (m:n):",bg="black",fg="white").pack(side=LEFT)
            m_input=Entry(ratio_frame,width=3,justify="center")
            m_input.pack(side=LEFT,padx=2)
            Label(ratio_frame,text=":",bg="black",fg="white").pack(side=LEFT)
            n_input=Entry(ratio_frame,width=3,justify="center")
            n_input.pack(side=LEFT,padx=2)
            dropdown.m_ref=m_input
            dropdown.n_ref=n_input
    dropdown.bind("<<ComboboxSelected>>",on_dropdown_change)

def execute_and_plot(dropdown,num_points):
    try:
        pts=[]
        for entries in vector_entries:
            pts.append(Point3d(
                float(entries['i'].get()),
                float(entries['j'].get()),
                float(entries['k'].get())
            ))
        
        operation=dropdown.get()
        result=""
        ax.clear()
        style_3d_axes()
        
        if num_points==1:
            p1=pts[0]
            if operation=='Representation':
                result=p1.representation()
            elif operation=='Unit Vector':
                result=p1.unit_vector()
            ax.quiver(0,0,0,p1.i,p1.j,p1.k,color='cyan',arrow_length_ratio=0.1,label='Vector 1')
            ax.scatter(p1.i,p1.j,p1.k,color='red',s=30)
        else:
            p1,p2=pts[0],pts[1]
            if operation=='Add':
                result=p1 + p2
            elif operation=='Subtract':
                result=p1 - p2
            elif operation=='Distance':
                result=p1.distance(p2)
            elif operation=='Mid-Point':
                result=p1.mid_point(p2)
            elif operation=='Line Equation':
                result=p1.line_equation(p2)
            elif operation=='Unit Vector':
                result=p1.unit_vector(p2)
            elif "Divide Section" in operation:
                try:
                    m,n=int(dropdown.m_ref.get()),int(dropdown.n_ref.get())
                    if "Internal" in operation:
                        result=p1.divide_section_internal(p2,m,n)
                    else:
                        if m!=n:
                            result=p1.divide_section_external(p2,m,n)
                        else:
                            result_label.config(text="Error: Enter valid Ratios!",fg="red")
                            return
                except (AttributeError,ValueError):
                    result_label.config(text="Error: Enter valid Integer Ratios!",fg="red")
                    return
            ax.quiver(0,0,0,p1.i,p1.j,p1.k,color='cyan',arrow_length_ratio=0.1,label='Vector 1')
            ax.quiver(0,0,0,p2.i,p2.j,p2.k,color='orange',arrow_length_ratio=0.1,label='Vector 2')
            ax.plot([p1.i,p2.i],[p1.j,p2.j],[p1.k,p2.k],color='magenta',linestyle='--',label='Path A->B')
            ax.scatter([p1.i,p2.i],[p1.j,p2.j],[p1.k,p2.k], color='white', s=25)
        ax.legend(facecolor='black',edgecolor='white',labelcolor='white')
        all_i=[0,pts[0].i] + ([pts[1].i] if num_points==2 else [])
        all_j=[0,pts[0].j] + ([pts[1].j] if num_points==2 else [])
        all_k=[0,pts[0].k] + ([pts[1].k] if num_points==2 else [])
        ax.set_xlim3d(min(all_i)-1, max(all_i)+1)
        ax.set_ylim3d(min(all_j)-1, max(all_j)+1)
        ax.set_zlim3d(min(all_k)-1, max(all_k)+1)
        canvas.draw()
        result_label.config(text=f"Result:\n{result}", fg="cyan")
    except ValueError:
        result_label.config(text="Error: Ensure all vector parameters are numeric!", fg="red")


submit_btn=Button(points_frame,text="Submit",command=generate_inputs,bg="sky blue",fg="black")
submit_btn.pack(side=LEFT,padx=5)


root.mainloop()
