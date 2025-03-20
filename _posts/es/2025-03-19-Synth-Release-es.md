---
categories: Godot
date: 2025-03-19
description: First public release of the Godot Synth Plugin
description-es: 'Primera versión pública del plugin Godot Synth.

  '
featured: true
layout: post
tags:
- godot
- music
- c++
title: Godot Synth Release
title-es: 'Lanzamiento de Godot Synth

  '
toc:
  sidebar: left
---
## Resumen

Hace unos días terminé la primera versión de mi plugin de sintetizador para Godot.
Este proyecto está destinado ahora a convertirse en un conjunto completo de características para que los desarrolladores de juegos y diseñadores de sonido creen, modifiquen, modulen e interpreten sonidos en el juego de una manera eficiente y amigable para los programadores.

## Inicio del Proyecto

Para el día de San Valentín de 2025, decidí hacerle una aplicación a mi pareja.
Siempre le han gustado las flores, así que hice un pequeño juego móvil de Godot donde se cultiva una flor de forma procedural, el juego tiene un simple ciclo día/noche y un sistema de música procedural.

Y si piensas que he usado la palabra procedural demasiadas veces, es porque quería hacer todo el contenido para su aplicación durante el tiempo de ejecución.

Así que hice algunos algoritmos, aprendí a usar LLMs para el desarrollo de juegos (un proceso que aún está en curso) e hice una compilación de Android para probar.

Para mi sorpresa, la flor se veía bastante bien desde mi primer intento y todo el sistema parecía funcionar a una velocidad de fotogramas muy respetable (para un GDScript que se ejecuta en un viejo teléfono Pixel) hasta que comenzó a sonar la primera nota musical generada proceduralmente, lo que redujo mi velocidad de fotogramas a alrededor de 5 ~ 6 fps e imposibilitó jugar mi juego.

## GDScript vs C++

En ese momento, solo me quedaban unas pocas horas para entregar mi proyecto a tiempo, ya que perderme el Día de San Valentín significaría que tendría que esperar un año para entregar el proyecto y también que no tendría nada mío para regalar.

Así que hackeé una solución donde tocaba notas muy pequeñas de mi sintetizador y luego usaba reverbs expansivas y delays largos para fingir sonidos más largos.

Esto me llevó a un rendimiento aceptable para mi proyecto, pero dejó una inquietud en mi mente, la idea central de generar sonidos de forma procedural era muy buena y funcionaba realmente bien para el ambiente del juego, y sabía que esta era la forma en que quería componer música para mis próximos juegos.

Así que empecé a investigar cómo optimizar el sistema de sonido que había hecho inicialmente y la respuesta obvia fue implementarlo como un plugin de GDExtension.

Según DeepSeek, mover mi algoritmo de generación de sonido a C++ podría mejorar el rendimiento en 100 veces, así que decidí hacerlo.

## Plaits

Para ser completamente honesto, esta tampoco era la primera vez que intentaba algo así, me encanta usar VCV Rack y lo consideraría mi DAW principal. Soy un gran fan de la serie de plugins de audio SurgeXT, y su implementación en VCV es simplemente excepcional.

SurgeXT proporciona amplias capacidades de modulación con ayudas visuales muy fáciles de seguir para mostrar lo que realmente está haciendo la modulación.

También soy un gran fan de Emilie Gillet y sus contribuciones de código abierto a la música electrónica, no creo que esté exagerando cuando digo que probablemente sea la desarrolladora de audio más influyente de nuestra generación. Esto me lleva a [Plaits](https://pichenettes.github.io/mutable-instruments-documentation/modules/plaits/downloads/plaits_quickstart.pdf).

> Plaits es una fuente de sonido digital controlada por voltaje capaz de
dieciséis técnicas de síntesis diferentes. Plaits reclama la
tierra entre todas las islas fragmentadas de sonido producidas
por su predecesor, Braids.

Para aquellos que no lo sepan, Plaits es un módulo de sonido de macro oscilador de Mutable Instruments con varios motores de sonido diferentes y 4 perillas grandes en la parte frontal para controlar:

- Frecuencia
- Armónicos
- Timbre
- Morfología

Y con estos 4 controladores simples, el módulo es capaz de domar algunos algoritmos de oscilación que suelen ser muy difíciles de manejar, como la síntesis de formantes granulares o FM.

Esto proporciona a los usuarios una inmensa paleta de sonido y hace que el módulo sea extremadamente flexible, lo que permite a los usuarios hacer percusiones, leads, pads, acordes y mucho más con una configuración simple pero eficiente.

## Primer Intento

El [código fuente](https://github.com/pichenettes/eurorack/tree/master/plaits) también tiene licencia MIT, así que mi primera idea fue simplemente llevar Plaits a Godot.

Así que en noviembre, hice un repositorio y lo llamé Glaits, vi un montón de tutoriales sobre cómo crear extensiones C++ para Godot y llegué hasta el punto en que podía compilar el proyecto con los submódulos Plaits importados, pero estos nunca fueron pensados para ejecutarse en el mismo entorno que un motor de juego.

Estos eran también algoritmos extremadamente optimizados, lo que significaba que algunos pasos críticos del código estaban escritos en ensamblador, lo que provocaba muchos problemas al compilador de Godot para entenderlos.

Esto frenó instantáneamente mi proyecto justo después de una semana de desarrollo y decidí dejarlo ahí.

## Segundo Intento

Después de tomarme un descanso del intento inicial con Glaits, decidí abordar el problema desde un ángulo diferente. En lugar de portar directamente todo el módulo Plaits a Godot, me centraría en crear una versión ligera que encapsulara las funcionalidades principales que quería implementar en mi plugin de sintetizador.

### Investigación y Rediseño

Revisité las funcionalidades de Plaits e identifiqué las técnicas de síntesis clave que serían más útiles para el desarrollo de juegos. Estos incluían:

- **Formas de Onda Básicas**: Seno, Cuadrada, Diente de Sierra y Triángulo.
- **Síntesis FM**: Para contenido armónico más complejo.
- **Síntesis Granular**: Para crear texturas y paisajes sonoros en evolución.
- **Formantes**: Para crear audio con sonido de habla.
- **Generación de Ruido**: Útil para sonidos y efectos de percusión.

Con estos elementos en mente, diseñé una arquitectura simplificada para mi plugin de sintetizador. Esto consistiría en componentes modulares que podrían combinarse y controlarse fácilmente en tiempo real a través del sistema de scripts de Godot.

### Pasos de Implementación

1. **Configuración del Framework GDExtension**:
   - Creé un nuevo proyecto GDExtension dentro de Godot 4.x.
   - Seguí las directrices sobre cómo configurar los bindings de C++ para exponer mis funciones de sintetizador a GDScript.

2. **Desarrollo del Motor de Sonido Central**:
   - Implementé formas de onda básicas usando C++, asegurándome de que estuvieran optimizadas para el rendimiento.
   - Desarrollé un módulo de síntesis FM, permitiendo a los usuarios ajustar los parámetros de modulación de frecuencia dinámicamente.
   - Creé un motor de formantes para la síntesis de voz.

3. **Sistema de Modulación**:
   - Añadí opciones de modulación para los parámetros más importantes.

4. **Componentes de la Interfaz de Usuario**:
   - Integré componentes de interfaz de usuario personalizados en Godot que permiten a los usuarios interactuar con el sintetizador fácilmente.
   - Usé nodos Control para crear deslizadores, perillas y botones que representan cada parámetro del motor de sonido.

5. **Pruebas y Optimización**:
   - Realicé pruebas exhaustivas en varios dispositivos (incluyendo teléfonos Android de gama baja) para asegurar que el rendimiento se mantuviera alto incluso con múltiples instancias ejecutándose simultáneamente.

### Resultados Iniciales

Después de una semana de desarrollo en esto usando herramientas de desarrollo impulsadas por IA, había hecho un montón de progreso y tenía una configuración con 3 motores de oscilador con diferentes parámetros de modulación y soporte para guardar presets usando un recurso personalizado de Sound Configuration.

En esta iteración temprana e ingenua, la configuración de sonido estaba a cargo de casi todo, ya que crearía un motor apropiado para producir el sonido, crearía el bus de audio específicamente para este sonido, crearía los efectos de audio definidos en la matriz de efectos de audio.

Las modulaciones también estaban codificadas en las variables que estaban controlando, lo que comenzó a mostrar algunos problemas de sincronización cuando algunas modulaciones se ejecutaban a un ritmo más rápido que otras.

### Problemas de Buffer

La gota que derramó el vaso fue al intentar crear un efecto modulado. Como expliqué, los efectos eran manejados por el propio bus de audio, lo que significaba que el servidor de audio interno de Godot estaba a cargo de los tiempos y el buffer, lo que creó algunos problemas con mi plan.

Principalmente, mis modulaciones a los generadores de sonido se aplicaban **por muestra**, asegurando una alta resolución en los moduladores, pero solo podía modular los efectos **por buffer**, causando algunos artefactos de sonido inesperados e incluso más desincronización.

En este punto, incluso con todo el progreso que había hecho, me sentía desesperanzado con mi proyecto hasta que tuve la idea del contexto de la nota.

## Contexto de la Nota

La idea era simple: pasar una estructura de datos de contexto que el usuario pudiera usar para manipular la generación de sonido sin controlar directamente los motores.

Contiene datos sobre la frecuencia actual, la velocidad y también realiza un seguimiento de la duración actual de la nota.

Esta misma estructura ligera se pasa a los osciladores, las fuentes de modulación y los efectos para obtener buffers de audio actualizados.

Este nuevo enfoque era muy prometedor, pero requería una reelaboración completa de mi sistema, así que borré todo y volví a empezar desde cero.

Comenzar de esta manera también permitió la creación del parámetro modulado, que puede definir un valor base float que puede ser modulado por cualquier fuente.

Y con este último elemento, el núcleo de mi sintetizador estaba completo.

## Conclusión

Desarrollar este proyecto fue una aventura muy gratificante e interesante. Me empujó a mis propios límites de lo que sabía sobre C++, me obligó a aprender nuevas herramientas y frameworks, y me desafió a terminar y publicar algo.

Esta publicación ya es bastante larga, haré algunas otras publicaciones más adelante explicando la arquitectura y las elecciones hechas con más detalle y también comenzaré un pequeño tutorial sobre cómo usar eficazmente los LLMs con Godot.
