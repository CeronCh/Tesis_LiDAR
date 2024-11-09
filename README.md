
# Evaluación de sensores de distancia para aplicaciones de mapeo de entornos con agentes robóticos móviles
<h2 align="center"><em>Autor: Jorge Ricardo Cerón Cheley</em></h2>
<h3 align="center"><em>Universidad del Valle de Guatemala</em></h3>
<h3 align="center"><em>Departamento de Ingeniería Electrónica, Mecatrónica y Biomédica</em></h3>

---

<h3 align="center">
  <br>
  <a href="https://drive.google.com/uc?export=view&id=1JX5E3psndADwoQ3_kOWw1g9pJEo1_Qra">
    <img src="https://drive.google.com/uc?export=view&id=1JX5E3psndADwoQ3_kOWw1g9pJEo1_Qra" alt="Plataforma de pruebas para LiDAR FHL-LD20" width="400">
  </a>
  <br>
  Plataforma de pruebas para LiDAR FHL-LD20
  <br>
</h3>

Este trabajo se desarrolló con el objetivo de evaluar y seleccionar opciones de sensores de distancia que permitan la futura validación física de los algoritmos de exploración y mapeo de entornos en agentes robóticos móviles. Para ello, se realizó un *trade study* en el que se analizaron diversos parámetros y especificaciones técnicas de cada alternativas evaluada: el módulo VL53L0X, el LiDAR FHL-LD20 y el YLIDAR Tmini Pro. Estos sensores fueron seleccionados estratégicamnet para analizar dos tecnologías de medición diferente: triangulación y tiempo de vuelo (ToF). Los resultados del análisis demostraron que el LiDAR FHL-LD20 era la opción más adecuada, por lo que se seleccionó para futuras investigaciones con robots móviles dentro del ecosistema Robotat. Junto a esto, para facilitar su futura integración en agentes móviles disponibles en la Universidad del Valle de Guatemala, se desarrolló una herramienta en Python para obtener e interpretar los datos generados del sensor. También, se detalló la caracterización y calibración del sensor, con el objetivo de comprender mejor sus parámetros de incertidumbre y limitaciones, permitiendo así evaluar con precisión la confiabilidad de sus mediciones en condiciones reales de operación. Finalmente, se propuso una disposición para integrar el sensor en los agentes robóticos Pololu 3Pi+ para dotarlos con capacidades adicionales para el mapeo de entornos.

### Contenido del repositorio
* El firmware para la obtención y transmisión de los datos del LiDAR.
* La herramienta en Python para la interpretación y visualización de los datos del LiDAR.
* Manual de conexión del sensor y su correcta disposición dentro de la plataforma de pruebas.
* Videos que documentan algunas de las pruebas realizadas.
* Enlaces a las pruebas utilizadas para la caracterización y calibración del sensor.

## Plataformas de trabajo

La integración de microcontroladores y software de análisis es crucial para el desarrollo de sistemas de captura y procesamiento de datos en aplicaciones de sensores. En el caso del sensor FHL-LD20, se utilizó un microcontrolador ESP32 junto con plataformas de software como Matlab y Python para el proceso de lectura y decodificación de los datos. El ESP32 se encargó de recolectar la información a través de la conexión UART proporcionada por el sensor. Además, se desarrolló una aplicación en Python para la interpretación y visualizaciòn de los datos, proporcionando una herramienta útil para evaluar la precisión y confiabilidad del sensor en diversos escenarios. Python 3.11 fue seleccionado como el lenguaje de programación debido a su flexibilidad y eficiencia en el manejo de datos. En conjunto, se desarrolló una herramienta que mejorara la experiencia del usuario al interactuar con el sensor FHL-LD20.

Para diseñar elementos físicos, como las plataformas de prueba y el soporte para el LiDAR FHL-LD20, se utilizó el software Autodesk Inventor 2024. Este programa facilita la creación y manipulación de modelos 3D detallados, lo que permitió optimizar el diseño y ajuste de los componentes necesarios para las pruebas, asegurando precisión y estabilidad en la instalación del sensor en los entornos fabricados. La elección de esta herramienta no solo contribuyó a alcanzar los objetivos de diseño con mayor rapidez, sino que también permitió minimizar el tiempo de desarrollo, ya que se aprovechó la experiencia previa en el uso de esta plataforma. Esta familiaridad facilitó un flujo de trabajo eficiente y una rápida iteración en las etapas de diseño y ajuste, aumentando significativamente el tiempo destinado en la calidad de los resultados.

## Repositorios disponibles

[App]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/App
[Arduino]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/App/Arduino
[Matlab]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/App/Matlab
[Python]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/App/Python
[Documento]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Documento
[Modelos]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Modelos
[Pruebas]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Pruebas
[Angulos]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Pruebas/Angulos
[Radios]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Pruebas/Radios
[Recursos]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Recursos
[Multimedia]: https://github.com/CeronCh/Tesis_LiDAR/tree/main/Multimedia
1. **[App]**: Contiene los archivos de firmware en Arduino para la obtención y transmisión de datos del LiDAR, así como los archivos en MATLAB y Python para la interpretación y visualización de los datos recibidos.
  * [Arduino]
  * [Matlab]
  * [Python]
2. **[Documento]**: Incluye la plantilla de redacción de la tesis, la tesis presentada y las figuras utilizadas en el documento.
3. **[Modelos]**: Contiene los archivos necesarios para la fabricación e impresión de piezas empleadas en este trabajo, tanto para entornos de prueba como para soportes del LiDAR.
4. **[Multimedia]**: Incluye imágenes y videos no listados de YouTube que muestran el funcionamiento del LiDAR, la transmisión de datos, la aplicación desarrollada y diversas pruebas realizadas.
5. **[Pruebas]**: Contiene las hojas de datos utilizadas para la evaluación de la caracterización y calibración del sensor en mediciones radiales y angulares.
  * [Angulos]
  * [Radios]
6. **[Recursos]**: Contiene las fuentes bibliográficas empleadas en la redacción de la tesis.

