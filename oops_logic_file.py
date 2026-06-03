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

#--------------------

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
        new_j=(self.j-other.j)/2
        new_k=(self.k-other.k)/2
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
        new_i=(other.i-self.i)
        new_j=(other.j-self.j)
        new_k=(other.k-self.k)
        mod=math.sqrt(new_i**2+new_j**2+new_k**2)
        new=Point3d(new_i/mod,new_j/mod,new_k/mod)
        return Point3d.representation(new)