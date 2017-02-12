from math import sqrt,acos,pi,inf,isinf,fabs

def savePPM(w,h,mxCol,name,imgDat): # Code for saving rendered image in displayable format
    print("saving ppm...")
    filename = "/Users/willsumner/Desktop/Coding/My_Raytracer/Image_Test_Container/"+name+".ppm"
    with open(filename, 'w') as outFile:
        outFile.write("P3\n")
        outFile.write(str(w) + " " + str(h) + "\n"+ str(mxCol)+"\n")
        for line in imgDat:
            outFile.write(" ".join(line))
            outFile.write("\n")

def solveQuad(a,b,c): # Find roots of quadratic equation (i.e. for sphere tracing)
    det = b*b - 4*a*c
    if det > 0:
        inv = 1/(2*a)
        tt = (-1*b - sqrt(det))*inv
        if tt <= 0:
            t = (-1*b + sqrt(det))*inv
            if t > 0: return t
        else: return tt
    return False

class Vec: # Vector class
    x = 0
    y = 0
    z = 0
    def __init__ (self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self): # Useful for saving  as a file, basically str(Vec()) -> "x y z"
        return "{} {} {}".format(self.x,self.y,self.z)
    def __mul__(self,val): # Overload math operators
        return Vec(self.x*val,self.y*val,self.z*val)
    def __add__(self,other): # Same for other simple math operators
        newx = self.x+other.x
        newy = self.y+other.y
        newz = self.z+other.z
        return Vec(newx,newy,newz)
    def __sub__(self,other):
        newx = self.x-other.x
        newy = self.y-other.y
        newz = self.z-other.z
        return Vec(newx,newy,newz)
    def __div__(self,val):
        newx = self.x/val
        newy = self.y/val
        newz = self.z/val
        return Vec(newx,newy,newz)
    def dot (self,other): # Dot Product
        return (self.x*other.x)+(self.y*other.y)+(self.z*other.z)
    def ang(self,other): # Angle between two vectors
        return acos(self.dot(other)/(self.length() * other.length()))
    def length(self): # Return Length
        return sqrt((self.x**2)+(self.y**2)+(self.z**2))
    def square(self): # Square a vector
        return self.dot(self)
    def norm(self): # Normalize a vector
        l = self.length()
        if l > 0:
            self.x = self.x/l
            self.y = self.y/l
            self.z = self.z/l
        else: self.x=self.y=self.z=0
    def cross(self,other): # Cross Product
        i = (self.y*other.z - self.z*other.y)
        j = (self.x*other.z - self.z*other.x)
        k = (self.x*other.y - self.y*other.x)
        return Vec(i,j,k)

class Col: # Color Class
    r = 0
    g = 0
    b = 0
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    def __str__(self): # Useful for saving  as a file, basically str(Col()) -> "r g b"
        return "{} {} {}".format(self.r,self.g,self.b)
    def __add__(self,nCol):
        newr = min(self.r + nCol.r,255)
        newg = min(self.g + nCol.g,255)
        newb = min(self.b + nCol.b,255)
        return Col(newr,newg,newb)
    def scale(self): # Very basic pseudo - tone mapping 
        self.r = min(255,self.r)
        self.g = min(255,self.g)
        self.b = min(255,self.b)
        self.r = max(0,self.r)
        self.g = max(0,self.g)
        self.b = max(0,self.b)
    

class Sphere: # Sphere Class
    c = Vec(0,0,0)
    r = 1
    col = Col(.5,.5,.5)
    scol = Col(.5,.5,.5)
    shine = 0
    def __init__(self,origin,radius,col,scol,shine):
        self.c = origin
        self.r = radius
        self.col = col
        self.scol = scol
        self.shine = shine
    def checkHit(self,ray): # Find Intersection
        t0 = 0
        t1 = 0
        oc = ray.o - self.c
        a = ray.d.square()
        b = 2 * ray.d.dot(oc)
        c = oc.dot(oc)-(self.r**2)
        hit = solveQuad(a,b,c)
        if (not(hit)): return False
        return hit
    def normal(self,point):
        normal = self.c-point
        normal.norm()
        return normal
            
class Ray: # Ray Class
    o = Vec(0,0,0)
    t = 0
    d = Vec(1,1,1)
    def __init__(self,o,t,d):
        self.o = o
        self.t = t
        self.d = d
        self.d.norm()
    def hitPoint(self,t):
        return self.o+(self.d*t)

class Camera: # Camera Class
    o = Vec(0,0,0)
    d = Vec(1,0,0)
    ang = 0
    def __init__(self,o,d,ang):
        self.o = o
        self.d=d
        self.ang = ang
        
class Light: # Light Class
    o = Vec(0,0,0)
    brightness = 1.0
    def __init__(self,o,brightness):
        self.o = o
        self.brightness = brightness

class Scene:
    objects = []
    lights = []
    camera = 0
    def __init__(self):
        objects = []
        lights = []
        camera = 0
    def addObject(self,obj):
        self.objects.append(obj)
    def removeObject(self,obj):
        self.objects.remove(obj)
    def addLight(self,light):
        self.lights.append(light)
    def removeLight(self,light):
        self.lights.remove(light)
    def addCamera(self,camera):
        self.camera=camera

def trace(ray, objects,lights): # Trace a ray until it hits an object
    t = inf
    obj = objects[0]
    for thing in objects:
        hold = thing.checkHit(ray)
        if (hold > 0 and hold < t):
            t = hold;
            obj = thing
    if (not(isinf(t))):
        hitPoint = ray.hitPoint(t)
        normal = thing.normal(hitPoint)
        return phongshade(ray,normal,hitPoint,obj.col,obj.scol,obj.shine,lights)
    return Vec(30,30,30) # Background Color
        
def lamshade(N,P,material,lights): # Shade a pixel based on lighting
    fincol = Col(0,0,0)
    for light in lights:
        L = P-light.o
        L.norm()
        dott = max(0,N.dot(L))
        fincol.r += int(dott*material.r*light.brightness)
        fincol.g += int(dott*material.g*light.brightness)
        fincol.b += int(dott*material.b*light.brightness)
    return fincol+ambient

def phongshade(ray,N,hitpoint,dmaterial,smaterial,shine,lights): # More Advanced Shading
    if shine == 0: return lamshade(N,hitpoint,dmaterial,lights)
    fincol = Col(0,0,0)
    fincol.scale()
    shine *= 1000
    for light in lights:
        L = hitpoint-light.o
        L.norm()
        ddot = max(0,N.dot(L))
        H = L+ray.d
        H.norm()
        sdot = max(0,H.dot(N))**shine
        fincol.r += min(int(dmaterial.r*ddot*light.brightness+smaterial.r*sdot*light.brightness),255)
        fincol.g += min(int(dmaterial.g*ddot*light.brightness+smaterial.g*sdot*light.brightness),255)
        fincol.b += min(int(dmaterial.b*ddot*light.brightness+smaterial.b*sdot*light.brightness),255)
    return fincol+ambient

def render(pixels,objects,width,height,camera,lights,filename): # Main Render Function
    w = camera.d*-1  # Creating coordinate system
    u = w.cross(Vec(0,1,0))
    u.norm()
    v = u.cross(w)*-1
    v.norm() 
    for i in range(height): # For each pixel
        for j in range(width):
            dirr = camera.d*camera.ang + u*(2*(j / width)-1) + v*(1-2*(i/height)) # Find a direction
            dirr.norm() # Normalize it
            traceRay = Ray(camera.o,2,dirr) # Trace it
            pixels[i][j] = str(trace(traceRay,objects,lights)) # Shade and store it
    savePPM(width,height,255,filename,pixels) # Save it to an image file
            
            
width,height=150,150 # Image Dimensions
ambient = Col(10,10,10) # Ambient Color
image = [ [ 0 for x in range(width)] for y in range(height)] # Image Container

red = Col(180,0,0) # Setting up colors
blue = Col(40,93,226)
green = Col(39,196,39)
white = Col(255,255,255)
cyan = Col(55,221,216)

mscene = Scene() # Default Scene Setup 
SphereUno = Sphere(Vec(-1,0,3),1,red,white,0)
SphereDos = Sphere(Vec(1,0,3.5),1,blue,white,1)
LightUno = Light(Vec(-1,2,0),1)
mscene.addObject(SphereUno)
mscene.addObject(SphereDos)
mscene.addLight(LightUno)
mscene.addCamera(Camera(Vec(0,0,0),Vec(0,0,1),1))

print("Rendering...")

imgName = "image"
render(image,mscene.objects,width,height,mscene.camera,mscene.lights,imgName)

