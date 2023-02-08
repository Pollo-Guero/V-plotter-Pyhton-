# V-plotter-Python-RPI
un programa simple de python para leer codigo-G y transformalo al movimiento de un plotter vertical o xy plotter

### Desventajas
* Solo lee cordenadas absolutas, incrementales no funcionaran.
* El escript no lee mm ni in, solamente lee pasos, si el codigo-G ordena mover 5 mm, la herramienta se movera 5 pasos;<br />
 ```Gcode 
 G00 X 0.00 Y 0.00
 G00 X 5.00 Y 0.00
 ```
el eje x se movera 5 pasos, no 5 milimetros
* unicamente acepta movimiento lineal G00 y G01 y no cambia la velocidad entre estos
***
### Conecciones:
Este programa se diseño para controlar dos motores bipolares a travez de sus drivers tipo A4988 o DRV8825 y un servomotor, por lo que esto es lo unico que debemos de conectar.</br></br>
lo siguiente es la declaracion de pines:

```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)   #
GPIO.setwarnings(False)

GPIO.setup(13, GPIO.OUT) #direccion motor1
GPIO.setup(11, GPIO.OUT) #pasos  motor1
GPIO.setup(15, GPIO.OUT) #enable ambos motores
GPIO.setup(33, GPIO.OUT) #servo motor 
GPIO.setup(8, GPIO.OUT) # pasos motor2
GPIO.setup(10, GPIO.OUT) #direccion motor2

servo=GPIO.PWM(33,50)
servo.start(0)
```
En los comentarios del codigo esta directamente a que cosa deves de conectar cada pin
</br>
***
### Ejecucion:
en las ultimas lineas del codigo se definen los valores importantes para el correcto funcionamiento del programa
```python
dibujo=dibujar(300,0.054006)
dibujo.Medidas()
#dibujo.leerGcode("raspberryBoard.ngc")
GPIO.output(15, 1)
```
</br>

> dibujo=dibujar(300,0.054006)
 
la primera de estas lineas crea un objeto de la clase dibujar, los parametros iniciales son la separacion entre las dos cuerdas y los milimetros por paso que recorre la cuerda, este ultimo es diferente dependiendo del diametro de sus poleas y los pasos que tiene que dar el motor para commpletar una vuelta</br>
</br>
> dibujo.Medidas()

esta linea ejecuta el metodo Medidas(), este metodo imprime las cordenadas y longuitudes a las que tiene que **acomodar la herramienta de forma manual antes de comenzar el dibujo**, el metodo imprimira algo asi:</br>
```
cuerdas en pasos: 3927 3927
cuerdas en mm 212 212
coordenadas iniciales de la herramienta: 2777.5 2777.5
```
los valores importantes son la cuerda en mm y las cordenadas iniciales de la herramienta, la cuerda en pasos puedes ignorarla por ahora. </br>
`cuerdas en mm 212 212` </br>
Este valor le dice la longuitud a la que deve de acomodar los hilos **manualmente-antes de comenzar con el dibujo**, </br> 
`coordenadas iniciales de la herramienta: 2777.5 2777.5`
</br>
Indica cuales son las cordenadas de la herramienta cuando las cuerdas tienen la longuitud especificada, este valor es utilizado al hora de generar el codigo-G para pocicionarlo en estas cordenadas. **Es importante tomar en cuenta estas cordenadas ya que tiene que ser el punto medio del dibujo antes de generar el codigo-G si quiere que quede bien centrado y con la menor deformacion posible** </br>
</br>
> dibujo.leerGcode("ruta/nombre.extencion")

esta linea ejecuta el metodo leerGcode que a diferencia de lo que el nombre sugiere, no solo se encarga de leer el codigo-G sino que tambien lo ejecuta, al ejecutar este metodo, todos los demas metodos encargados de hacer funcionar toda la maquina tambien se ejecutaran creando el dibujo.</br>
en el escript original, esta linea esta comentada para que **la descomente despues de haber ejecutado el metodo Medidas() y acomodado las cuerdas**</br>
El parametro que recibe es el archivo que se va a dibujar, recuerde que solo se leen los comandos G00 y G01 y que ambos moveran la herramienta a la misma velocidad 
***
# Funcinamiento:
El funcionamiento es bastante simple; el programa comprueba cada linea del archivo Gcode en busca de las lineas que comienzan con G00 o G01, si encuentra una busca las cordenadas X, Y y Z, estas cordenadas son mandadas a el algoritmo de bresenham de rasterizacion de linas, este regresa una lista con todos los puntos que forman la linea rasterizada,despues se itera sobre estos puntos para calcular la distancia entre los puntos y los motores, penzando en un motor como la cordenada (0,0) esta distancia se resta a la distancia anterior obtenida , la diferencia sera la cantidad de pasos que los motores se moveran, como la diferencia la mayor parte del timepo tendra puntos decimales, hay una funcion que los almacena hasta que la suma de un valor entero
***
# Formatos:
hay caracteristicas del codigo-G que admite este programa que no pueden ser modificadas, como por ejemplo el uso de cordenadas absolutas, sin embargo hay otras que si, y en estas es en las que se tiene que figar antes de ejecutar el programa para obtener una lectura correcta del codigo</br>
Lo principal es la cantidad de decimales que tiene el codigo-G,
```python                
for i in line:
    c+=1
    if i =="X":
        self.x=float(line[c:c+6])
```
El funcionamiento de el programa es iterar en cada lina del codigo hazta encontrarse con una X,Y o Z, al encontrarla toma los 6  valores que haya enfrente de la letra y los tranforma a numeros decimales,el problema es cuando uno de esos 6 valores es la siguiente letra, ya que las letras no pueden ser trasformadas a numero, </br> 
Para asegurarce de que funcionara puede generar el codigo con suficientes decimales, o reducir la cantidad de valores que se leeran, (disminulla el valor que se suma a la variable **_c_**)
