# Informe Lab08 con plantilla UNSAReport

Plantilla oficial: @unsareport/epis-lab. Archivo principal: lab-08/main.typ.
El informe usa los tres cuadros: I. RESULTADOS, II. CUESTIONARIO y III. CONCLUSIONES. El texto es de 11 puntos; las tablas de síntesis están dentro del cuadro de resultados. Se conservan el membrete y los logos. El desarrollo extenso sigue en los anexos.
Contenido editable: lab-08/sections/. Imágenes: lab-08/assets/.

En PowerShell, desde esta carpeta:
```powershell
$env:TYPST_FONT_PATHS="$PWD/fonts"
unsarep docs build lab-08
```
También puedes abrir Compilar-informe.cmd. Requiere unsarep y Typst en PATH.
El PDF compilado está en lab-08/main.pdf y se copia al nombre CS - LAB08 - QUISPE-CARBAJAL.pdf.
La hora real de presentación no fue informada, por eso se indica "No consignada".
