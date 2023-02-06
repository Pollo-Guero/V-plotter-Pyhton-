# V-plotter-Pyhton-RPI
un programa simple de python para leer codigo-G y transformalo al movimiento de un plotter vertical o xy plotter

### Desventajas
* Solo lee cordenadas absolutas, incrementales no funcionaran.
* El escript no lee mm ni in, solamente lee pasos, si el codigo-G ordena mover 5 mm, la herramienta se movera 5 pasos;<br />
 G00 X 5.00 Y 0.00
el eje x se movera 5 pasos, no 5 milimetros
* unicamente acepta movimiento lineal G00 y G01 y no cambia la velocidad entre estos
***
### Ejecucion:
en las ultimas lineas del codigo se definen los valores importantes para el correcto funcionamiento del programa
```python
dibujo=dibujar(300,0.054006)
dibujo.Medidas()
#dibujo.leerGcode("raspberryBoard.ngc")
GPIO.output(15, 1)
```
la primera de estas lineas crea un objeto de la clase dibujar, los parametros iniciales son la separacion entre las dos cuerdas y los milimetros por paso que recorre la cuerda, este ultimo es diferente dependiendo del diametro de sus poleas y los pasos que tiene que dar el motor para commpletar una vuelta</br>
para definir las longuitudes iniciales de las cuerdas, tiene que ejecutar el metodo dibujo.Medidas(), este metodo imprimira algo asi:</br>
```
cuerdas en pasos: 3927 3927
cuerdas en mm 212 212
coordenadas iniciales de la herramienta: 2777.5 2777.5
```
los valores importantes son la cuerda en mm y las cordenadas iniciales de la herramienta, la cuerda en pasos puedes ignorarla por ahora. El primero de estos valores le dice que cuan largos deven de estar las cuerdas antes de empezar el dibujo,</br> el segundo valor indica cuales son las cordenadas de la herramienta cuando las cuerdas tienen la longuitud especificada, este valor es utilizado al hora de generar el codigo-G para pocicionarlo en estas cordenadas
