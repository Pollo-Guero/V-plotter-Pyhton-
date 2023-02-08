from math import sqrt,sin,cos
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)   #
GPIO.setwarnings(False)

GPIO.setup(13, GPIO.OUT) #direccion 1 s
GPIO.setup(11, GPIO.OUT) #pasos  1 s
GPIO.setup(15, GPIO.OUT) #enable s
GPIO.setup(33, GPIO.OUT) #servo motor 
GPIO.setup(8, GPIO.OUT) # pasos 2
GPIO.setup(10, GPIO.OUT) #direccion 2

servo=GPIO.PWM(33,50)
servo.start(0)

GPIO.output(15, 0)

class dibujar:
    def __init__(self,separacion,ppmm):
        self.Z=10
        self.Za=self.Z
        self.ppmm=ppmm
        
        self.ancho=separacion/self.ppmm
        self.x,self.y,self.z=self.ancho/2,self.ancho/2,0
        self.xa,self.ya,self.za=self.x,self.y,0
        self.cuerdaXa,self.cuerdaYa=sqrt(self.x**2+ self.y **2),sqrt((self.ancho-self.x)**2+self.y**2)

        time.sleep(1)
        self.decimal_acumuladoX,self.decimal_acumuladoY=0,0
        
        
    def Medidas(self):
        print("cuerdas en pasos:",int(self.cuerdaXa),int(self.cuerdaYa))
        print("cuerdas en mm",int(self.cuerdaXa*self.ppmm),int(self.cuerdaYa*self.ppmm))
        print("coordenadas iniciales de la herramienta:",round(self.x,1),round(self.y,1))
        
        
    def moverLinea(self,puntos):
        for punto in puntos:
            x=punto[0]
            y=punto[1]
            
            cuerdaX=sqrt(x**2+y**2)
            cuerdaY=sqrt((self.ancho-x)**2+y**2)
            diferenciax = cuerdaX - self.cuerdaXa + self.decimal_acumuladoX
            if diferenciax >= 1 or diferenciax <= -1 :
                motor_moveX = int(diferenciax)
                self.decimal_acumuladoX = diferenciax - motor_moveX
            else:
                motor_moveX = 0
                self.decimal_acumuladoX = diferenciax
            
            
            diferenciay = cuerdaY - self.cuerdaYa + self.decimal_acumuladoY
            if diferenciay >= 1 or diferenciay <= -1 :
                motor_moveY = int(diferenciay)
                self.decimal_acumuladoY = diferenciay - motor_moveY
            else:
                motor_moveY = 0
                self.decimal_acumuladoY = diferenciay
            self.girarMotorX(motor_moveX)
            self.girarMotorY(motor_moveY)

            
            self.cuerdaXa=cuerdaX
            self.cuerdaYa=cuerdaY

    def girarMotorX(self,pasos):
        if pasos<0:
            Direccion=0
        else:
            Direccion=1
        GPIO.output(10,Direccion)
        GPIO.output(13,Direccion)
        
        for i in range(abs(pasos)):
            time.sleep(0.003)
            GPIO.output(11, 1)
            time.sleep(0.003)
            GPIO.output(11, 0)
        
    def girarMotorY(self,pasos):
        if pasos<0:
            Direccion=0
        else:
            Direccion=1
        GPIO.output(10,Direccion)
        GPIO.output(13,Direccion)
        for i in range(abs(pasos)):
            time.sleep(0.003)
            GPIO.output(8, 1)
            time.sleep(0.003)
            GPIO.output(8, 0)
        
    
    def bresenham(self,x0,y0,x1,y1):
        self.puntos=[]
        c=0
        dx=x1-x0
        dy=y1-y0
        if dy<0:
            dy=-dy
            stepy=-1
        else:
            stepy=1
        if dx<0:
            dx=-dx
            stepx=-1
        else:
            stepx=1
        x=x0
        y=y0
        self.puntos.append([x,y])
        if dx>dy:
            p=dy-dx
            incE=2*dy
            incNE=2*(dy-dx)
            while x!= x1:
                x=x+stepx
                if p<0:
                    p=p+incE
                else:
                    y=y+stepy
                    p=p+incNE
                self.puntos.append([x,y])
        else:
            p=2*(dx-dy)
            incE=2*dx
            incNE=2*(dx-dy)
            while y!=y1:
                y=y+stepy
                if p<0:
                    p=p+incE
                else:
                    x=x+stepx
                    p=p+incNE
                self.puntos.append([x,y])
        
        self.moverLinea(self.puntos)
        
    def zeta(self,zeta):
        self.Z=zeta
        if self.Z!=self.Za:
            if self.Z<0:
                servo.ChangeDutyCycle(3)
                time.sleep(.5)
                servo.ChangeDutyCycle(0)
            elif self.Z>0:
                servo.ChangeDutyCycle(7)
                time.sleep(.5)
                servo.ChangeDutyCycle(0)
                #levanta
        self.Za=self.Z
        
    def leerGcode(self,nombre):
        self.nombre=nombre
        self.archivo= open(self.nombre,mode="r")
        con=0
        for line in self.archivo:
            con+=1
            
            l=line[0:3]
            if l == "G00"or l =="G01":
                print(line)
                
                c=0
                for i in line:
                    c+=1
                    if i =="Z":
                        self.z=float(line[c:c+4])
                        self.zeta(self.z)
                    if i =="Y":
                        self.y=float(line[c:c+6])
                    if i =="X":
                        self.x=float(line[c:c+6])

            self.bresenham(round(self.xa),round(self.ya),round(self.x),round(self.y))
            self.xa=self.x
            self.ya=self.y
            self.za=self.z
            
            
print("start")
dibujo=dibujar(300,0.054006)
dibujo.Medidas()
dibujo.leerGcode("raspberryBoard.ngc")
GPIO.output(15, 1)
