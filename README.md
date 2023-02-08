# V-plotter-Python-RPI
un programa simple de python para leer codigo-G y transformarlo al movimiento de un plotter vertical o xy plotter

### Desventajas
* Solo lee coordenadas absolutas, incrementales no funcionaran.
* El escript no lee mm ni in, solamente lee pasos, si el codigo-G ordena mover 5 mm, la herramienta se moverá 5 pasos;<br />
 ```Gcode 
 G00 X 0.00 Y 0.00
 G00 X 5.00 Y 0.00
 ```
el eje x se movera 5 pasos, no 5 milímetros
* únicamente acepta movimiento lineal G00 y G01 y no cambia la velocidad entre estos
***
### Conecciones:
Este programa se diseñó para controlar dos motores bipolares a través de sus drivers tipo A4988 o DRV8825 y un servomotor, por lo que esto es lo único que debemos conectar.</br></br>
lo siguiente es la declaración de pines:

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
En los comentarios del código está directamente a que cosa deves de conectar cada pin
</br>
***
### Ejecución:
en las últimas líneas del código se definen los valores importantes para el correcto funcionamiento del programa
```python
dibujo=dibujar(300,0.054006)
dibujo.Medidas()
#dibujo.leerGcode("raspberryBoard.ngc")
GPIO.output(15, 1)
```
</br>

> dibujo=dibujar(300,0.054006)
 
la primera de estas líneas crea un objeto de la clase dibujar, los parámetros iniciales son la separación entre las dos cuerdas y los milímetros por paso que recorre la cuerda, este último es diferente dependiendo del diámetro de sus poleas y los pasos que tiene que dar el motor para completar una vuelta</br>
</br>
> dibujo.Medidas()

esta línea ejecuta el metodo Medidas(), este método imprime las coordenadas y longitudes a las que tiene que **acomodar la herramienta de forma manual antes de comenzar el dibujo**, el método imprimirá algo asi:</br>
```
cuerdas en pasos: 3927 3927
cuerdas en mm 212 212
coordenadas iniciales de la herramienta: 2777.5 2777.5
```
Los valores importantes son la cuerda en mm y las coordenadas iniciales de la herramienta, la cuerda en pasos puedes ignorarla por ahora. </br>
`cuerdas en mm 212 212` </br>
Este valor le dice la longitud a la que debe de acomodar los hilos **manualmente-antes de comenzar con el dibujo**, </br> 
`coordenadas iniciales de la herramienta: 2777.5 2777.5`
</br>
Indica cuales son las coordenadas de la herramienta cuando las cuerdas tienen la longitud especificada, este valor es utilizado al hora de generar el código-G para posicionarlo en estas coordenadas. **Es importante tomar en cuenta estas coordenadas ya que tiene que ser el punto medio del dibujo antes de generar el código-G si quiere que quede bien centrado y con la menor deformación posible** </br>
</br>
> dibujo.leerGcode("ruta/nombre.extencion")

Esta línea ejecuta el método leerGcode que a diferencia de lo que el nombre sugiere, no solo se encarga de leer el código-G sino que también lo ejecuta, al ejecutar este método, todos los demás métodos encargados de hacer funcionar toda la máquina también se ejecutarán creando el dibujo.</br>
en el script original, esta línea está comentada para que **la descomenta después de haber ejecutado el método Medidas() y acomodado las cuerdas**</br>
El parámetro que recibe es el archivo que se va a dibujar, recuerde que solo se leen los comandos G00 y G01 y que ambos moverán la herramienta a la misma velocidad 
***
# Funcinamiento:
El funcionamiento es bastante simple; el programa comprueba cada línea del archivo Gcode en busca de las líneas que comienzan con G00 o G01, si encuentra una busca las coordenadas X, Y y Z, estas coordenadas son mandadas a el algoritmo de bresenham de rasterización de linas, este regresa una lista con todos los puntos que forman la línea rasterizada, después se itera sobre estos puntos para calcular la distancia entre los puntos y los motores, pensando en un motor como la coordenada (0,0) esta distancia se resta a la distancia anterior obtenida , la diferencia será la cantidad de pasos que los motores se moverán, como la diferencia la mayor parte del tiempo tendrá puntos decimales, hay una función que los almacena hasta que la suma de un valor entero
***
# Formatos:
hay características del código-G que admite este programa que no pueden ser modificadas, como por ejemplo el uso de coordenadas absolutas, sin embargo hay otras que sí, y en estas es en las que se tiene que fijar antes de ejecutar el programa para obtener una lectura correcta del código</br>
La principal es la cantidad de decimales que tiene el codigo-G,
```python                
c=0
for i in line:
    c+=1
    if i =="X":
        self.x=float(line[c:c+6])
```
El funcionamiento de el programa es iterar en cada línea del codigo hasta encontrarse con una X,Y o Z, al encontrarla toma los 6  valores que haya enfrente de la letra y los transforma a números decimales,el problema es cuando uno de esos 6 valores es la siguiente letra, ya que las letras no pueden ser transformadas a numero, </br> 
Para asegurarse de que funcionara puede generar el código con suficientes decimales, o reducir la cantidad de valores que se leerán, (disminuya el valor que se suma a la variable `c`)</br>
*insuficientes decimales:*
```Gcode
G00 X 5.5 Y 0.0
```
O
</br>
*insuficiente separación*
```Gcode
G00 X5.50 Y0.00
```
