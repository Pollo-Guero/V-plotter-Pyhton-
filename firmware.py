""" al crear al objeto dibujar, especificas el nombre del arcivo que quieres dibujar,
al crearse la clase se lee el archivio, y comienza solo el programa,
en la inicializacion, se ejecuta la funcion de leerGcode, con el archivo como parametro,
esta funcion lee linea por linea y extrae los valores de x,y,z de cada una de estas,

cada que extrae una nueva cordenada,se la pasa a la funcion de bresenham que al terminar, # la funcion bresenham resive las cordenadas talcual fueron extraidas, sin hacer diferencias
llamara a  la funcion moverLinea,

la funcion moverLinea recibe como parametro una lista de puntos en cordenadas absolutas,
por cada punto calculara la longitud de las cuerdas,
se resta la longuitud de la cuerda con la anterior, y se le dice al motor que mueva esa diferencia,
si la diferencia es muy pequeña(menor a 1 paso),no se hace nada y se guarda para sumarla a la siguiente diferencia

cuando se juntans suficientes diferencias para formar enteros, se mueve el entero que forma, y se sige guardando el decimal que sobro


la cosa es como hcaer eso




"""
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
    def __init__(self,nombre,separacion):
        self.Z=10
        self.Za=self.Z
        #ajustamos las cuerdas hasta que ambas tomen la medifa de:
        self.ancho=separacion/0.054006#calcula los pasos de separacion entre las cuerdas
        self.x,self.y,self.z=self.ancho/2,self.ancho/2,0#aqui se define la pocicion inicial de la herramienta
        #print("x,y",self.x,self.y)
        
        

        self.xa,self.ya,self.za=self.ancho/2,self.ancho/2,0
        
        # tenogo que encontrar la forma de definir las longuitufes iniciales
        self.cuerdaXa,self.cuerdaYa=sqrt(self.x**2+ self.y **2),sqrt((self.ancho-self.x)**2+self.y**2)#la longuitud inicial de las cuerdas, se calcula en base a la pocicion inicial de las cuerdas
        #print("cuerdas en pasos:",self.cuerdaXa,self.cuerdaYa)
        #print("cuerdas  en mm?:",self.cuerdaXa*0.054006,self.cuerdaYa*0.054006)
        print(self.cuerdaXa*0.054006,self.cuerdaYa*0.054006)
#cuerdas  en mm?: 212.13203435596427 212.13203435596427

        time.sleep(1)
        self.decimal_acumuladoX,self.decimal_acumuladoY=0,0
        
        self.nombre=nombre
        self.archivo= open(self.nombre,mode="r")
        
    def moverLinea(self,puntos):#"una lista de puntos en cordenadas absolutas :[[-2, 1], [-2, 2], [-1, 3], [0, 4], [0, 5], [1, 6], [2, 7], [2, 8], [3, 9], [4, 10], [4, 11], [5, 12], [6, 13]]
        #print(puntos)
        for punto in puntos:
            x=punto[0]
            y=punto[1]
            #print(x,y)#estos serian cada punto de la escalerita de puntos
         #   print("cuerda ante",self.cuerdaXa,self.cuerdaYa)
            
            cuerdaX=sqrt(x**2+y**2) # la trigonometria aqui
            cuerdaY=sqrt((self.ancho-x)**2+y**2)
            
            #print("cuerdasxy:",cuerdaY,cuerdaX)
            diferenciax = cuerdaX - self.cuerdaXa + self.decimal_acumuladoX
            if diferenciax >= 1 or diferenciax <= -1 :
                motor_moveX = int(diferenciax)
               # print(motor_move)
                self.decimal_acumuladoX = diferenciax - motor_moveX
            else:
                motor_moveX = 0
                self.decimal_acumuladoX = diferenciax
            
            
            diferenciay = cuerdaY - self.cuerdaYa + self.decimal_acumuladoY
            if diferenciay >= 1 or diferenciay <= -1 :
                motor_moveY = int(diferenciay)
                #print(motor_moveY)
                self.decimal_acumuladoY = diferenciay - motor_moveY
            else:
                motor_moveY = 0
                self.decimal_acumuladoY = diferenciay
          #  print("decimal",self.decimal_acumuladoY,self.decimal_acumuladoY)
           # print("motor",motor_moveX,motor_moveY)
            self.girarMotorX(motor_moveX)
            self.girarMotorY(motor_moveY)
            
           # print("girarMotorx(",motor_moveX,")")
           # print("girarMotory(",motor_moveY,")")
                #return motor_move, decimal_acumulado
            #print(diferenciax)
            
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
 #           print("X")        
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
#            print("Y")
            time.sleep(0.003)
            GPIO.output(8, 1)
            time.sleep(0.003)
            GPIO.output(8, 0)
        

    def mover_motor(cuerda1, cuerda2, decimal_acumulado=0):#esta funcion es la que escribio chatgpt3
        diferencia = cuerda1 - cuerda2 + decimal_acumulado
        if diferencia >= 1:
            motor_move = int(diferencia)
            decimal_acumulado = diferencia - motor_move
        else:
            motor_move = 0
            decimal_acumulado = diferencia
        return motor_move, decimal_acumulado
        
        
    
    def bresenham(self,x0,y0,x1,y1):#uno introduce los parametros cada que se llama a la funcion, esta se llama cada lectura de gcode
        self.puntos=[]
        #print("bren",x0,y0,x1,y1)
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
        #print(x,y)
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
                #print(x,y)
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
                #print(x,y)
                self.puntos.append([x,y])
        
  #      print(self.puntos)
        #print("puntos array",self.puntos,"\n")
        self.moverLinea(self.puntos)
        #print("bresneham")
        #return(self.puntos)
        
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
        
    def leerGcode(self):
        con=0
        for line in self.archivo:
            con+=1
            
            l=line[0:3]
            if l == "G00"or l =="G01":
                print(line)
                
                c=0
                for i in line:#extrae los valores de x e y actuales
                    c+=1
                    if i =="Z":
                        self.z=float(line[c+1:c+4])
                        self.zeta(self.z)
#                        print("z",self.z)

                    if i =="Y":
                        self.y=float(line[c+1:c+6])
                       # print("y",self.y)
                    if i =="X":
                        self.x=float(line[c+1:c+6])
 #                       print("x",self.x)
            #desde aqui indica para moverse
            self.bresenham(round(self.xa),round(self.ya),round(self.x),round(self.y))
            self.xa=self.x
            self.ya=self.y
            self.za=self.z
            
            
print("start")
nuevo=dibujar("raspberryBoard.ngc",300)
nuevo.leerGcode()
GPIO.output(15, 1)