1. Crear el proyecto

2. Agregar los archivos de la librer�a XMLRPC
   (preferentemente en un directorio)

3. Codificar el programa deseado

Cambios a realizar sobre plataforma Windows:

4. Colocar en las primeras l�neas del programa
   principal (y en el que corresponda)
   #include <windows.h>

5. Incluir en las primeras l�neas de los archivos
   XmlRpcDispatch.cpp y XmlRpcSocket.cpp, 
   lo siguiente:
   #include <windows.h>
   #if defined(_WINDOWS_H)
   # define _WINDOWS Puma3D
   #endif  // _WINDOWS_H

6. Agregar en la l�nea de comandos de g++ 
   o configurar en el IDE, la opci�n de compilar
   usando librer�as de windows: -lws2_32

7. Compilar