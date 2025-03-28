---
layout: post
title: Godot Synth Release
date: 2025-03-19
description: First public release of the Godot Synth Plugin
title-es: Lanzamiento de Sintetizador Godot
description-es: Primera versión pública del plugin Godot Synth
tags:
  - godot
  - music
  - c++
categories: Godot
featured: true
lang: es
toc:
  sidebar: left
---

## Resumen

Hace unos días terminé la primera versión de mi plugin de sintetizador para Godot.
El objetivo de este proyecto es convertirse en un conjunto completo de características para que los desarrolladores de juegos y los diseñadores de sonido creen, modifiquen, modulen e interpreten sonidos en el juego de una manera eficiente y amigable para los programadores.

## Inicio del proyecto

Para el día de San Valentín de 2025, decidí hacerle una aplicación a mi pareja.
A ella siempre le han gustado las flores, así que hice un pequeño juego móvil de Godot donde cultivas una flor de forma procedural. El juego tiene un ciclo simple de día/noche y un sistema de música procedural.

Y si crees que he usado la palabra procedural demasiadas veces, es porque quería crear todo el contenido para su aplicación durante el tiempo de ejecución.

Así que hice algunos algoritmos, aprendí a usar LLM para el desarrollo de juegos (un proceso que aún está en curso) e hice una compilación para Android para probar.

Para mi sorpresa, la flor se veía bastante bien desde mi primer intento y todo el sistema parecía ejecutarse a una velocidad de fotogramas muy respetable (para un GDScript que se ejecuta en un teléfono Pixel antiguo) hasta que comenzó a sonar la primera nota musical generada procedimentalmente, lo que redujo mi velocidad de fotogramas a unos 5~6 fps e hizo que mi juego fuera injugable.

## GDScript vs C++

En ese momento, solo tenía unas pocas horas para entregar mi proyecto a tiempo, ya que perderme el Día de San Valentín significaría que tendría que esperar un año para entregar el proyecto y también que no tendría nada mío para regalar.

Así que hice una solución donde tocaba notas muy cortas de mi sintetizador y luego usaría reverberaciones expansivas y retrasos largos para simular sonidos más largos.

Esto me dio un rendimiento aceptable para mi proyecto, pero me dejó una inquietud en la mente, la idea central de generar sonidos de forma procedural era muy buena y funcionaba muy bien para el ambiente del juego, y sabía que esta era la forma en que quería componer música para mis próximos juegos.

Así que comencé a investigar cómo optimizar el sistema de sonido que había creado inicialmente y la respuesta obvia fue implementarlo como un plugin GDExtension.

Según DeepSeek, trasladar mi algoritmo de generación de sonido a C++ podría generar una mejora de 100 veces en el rendimiento, así que decidí hacerlo.

## Plaits

Para ser completamente honesto, esta tampoco era la primera vez que intentaba algo así, me encanta usar VCV Rack y lo consideraría mi DAW principal. Soy un gran fan de la serie de plugins de audio SurgeXT, y su implementación en VCV es simplemente sobresaliente.

SurgeXT proporciona amplias capacidades de modulación con ayudas visuales muy fáciles de seguir para mostrar lo que la modulación realmente está haciendo.

También soy un gran admirador de Emilie Gillet y sus contribuciones de código abierto a la música electrónica, no creo que esté exagerando cuando digo que probablemente sea la desarrolladora de audio más influyente de nuestra generación. Esto me lleva a [Plaits](https://pichenettes.github.io/mutable-instruments-documentation/modules/plaits/downloads/plaits_quickstart.pdf).

> Plaits es una fuente de sonido digital controlada por voltaje, capaz de
> dieciséis técnicas de síntesis diferentes. Plaits reclama la
> tierra entre todas las islas fragmentadas de sonido producidas
> por su predecesor, Braids

Para aquellos de ustedes que no lo sepan, Plaits es un módulo de sonido macro oscilador de Mutable Instruments con varios motores de sonido diferentes y 4 grandes perillas en la parte frontal para controlar:

- Frecuencia
- Armónicos
- Timbre
- Morf

Y con estos 4 simples controladores, el módulo es capaz de domar algunos algoritmos de oscilación que suelen ser muy difíciles de manejar, como la síntesis granular formante o FM.

Esto les da a los usuarios una inmensa paleta de sonido y hace que el módulo sea extremadamente flexible, permitiendo a los usuarios hacer percusiones, leads, pads acordes y mucho más con una configuración simple pero eficiente.

## Primer intento

El [código fuente](https://github.com/pichenettes/eurorack/tree/master/plaits) también tiene licencia MIT, así que mi primera idea fue simplemente llevar Plaits a Godot.

Así que, en noviembre, creé un repositorio y lo llamé Glaits, vi un montón de tutoriales sobre cómo crear extensiones de C++ para Godot y llegué al punto en que podía compilar el proyecto con los submodulos de Plaits importados, pero estos nunca fueron pensados para ejecutarse en el mismo entorno que un motor de juego.

Estos también eran algoritmos extremadamente optimizados, lo que significaba que algunos pasos críticos del código estaban escritos en ensamblador, lo que el compilador de Godot estaba teniendo muchos problemas para descifrar.

Esto puso un freno instantáneo en mi proyecto justo después de una semana de desarrollo y decidí dejarlo ahí.

## Segundo intento

Después de tomarme un descanso del intento inicial con Glaits, decidí abordar el problema desde un ángulo diferente. En lugar de portar directamente todo el módulo Plaits a Godot, me centraría en crear una versión ligera que encapsulara las funcionalidades principales que quería implementar en mi plugin de sintetizador.

### Investigación y rediseño

Revisé las funcionalidades de Plaits e identifiqué las técnicas de síntesis clave que serían más útiles para el desarrollo de juegos. Estos incluyen:

- **Formas de onda básicas**: Seno, Cuadrada, Diente de sierra y Triángulo.
- **Síntesis FM**: Para contenido armónico más complejo.
- **Síntesis granular**: Para crear texturas y paisajes sonoros evolutivos.
- **Formante**: Para crear audio con sonido de voz.
- **Generación de ruido**: Útil para sonidos y efectos de percusión.

Con estos elementos en mente, diseñé una arquitectura simplificada para mi plugin de sintetizador. Esto consistiría en componentes modulares que podrían combinarse y controlarse fácilmente en tiempo real a través del sistema de scripting de Godot.

### Pasos de implementación

1. **Configuración del marco GDExtension**:
   - Creé un nuevo proyecto GDExtension dentro de Godot 4.x.
   - Seguí las pautas sobre la configuración de los enlaces de C++ para exponer mis funciones de sintetizador a GDScript.

2. **Desarrollo del motor de sonido central**:
   - Implementé formas de onda básicas usando C++, asegurando que estuvieran optimizadas para el rendimiento.
   - Desarrollé un módulo de síntesis FM, que permite a los usuarios ajustar los parámetros de modulación de frecuencia de forma dinámica.
   - Creé un motor de formantes para la síntesis de voz.

3. **Sistema de modulación**:
   - Añadí opciones de modulación para los parámetros más importantes.

4. **Componentes de la interfaz de usuario**:
   - Integré componentes de interfaz de usuario personalizados en Godot que permiten a los usuarios interactuar con el sintetizador fácilmente.
   - Utilicé nodos Control para crear sliders, knobs y botones que representan cada parámetro del motor de sonido.

5. **Pruebas y optimización**:
   - Realicé pruebas exhaustivas en varios dispositivos (incluidos los teléfonos Android de gama baja) para garantizar que el rendimiento se mantuviera alto incluso con múltiples instancias ejecutándose simultáneamente.

### Resultados iniciales

Después de una semana de desarrollo utilizando herramientas de desarrollo impulsadas por IA, había avanzado mucho y tenía una configuración con 3 motores de oscilador con diferentes parámetros de modulación y soporte para guardar presets utilizando un recurso personalizado de Configuración de sonido.

En esta iteración temprana e ingenua, la configuración de sonido estaba a cargo de casi todo, ya que crearía un motor apropiado para producir el sonido, crearía el bus de audio específicamente para este sonido, crearía los efectos de audio definidos en el array de efectos de audio.

Las modulaciones también estaban codificadas en las variables que estaban controlando, lo que comenzó a mostrar algunos problemas de sincronización cuando algunas modulaciones se ejecutaban a un ritmo más rápido que otras.

### Problemas de buffer

La gota que colmó el vaso fue al intentar crear un efecto modulado. Como expliqué, los efectos eran manejados por el propio bus de audio, lo que significaba que audio server interno de Godot estaba a cargo de los tiempos y el buffer, lo que creó algunos problemas con mi plan.

Principalmente, mis modulaciones a los generadores de sonido se aplicaron sobre una base de **por muestra**, lo que garantizaba una alta resolución en los moduladores, pero solo podía modular los efectos sobre una base de **por buffer**, lo que provocaba algunos artefactos de sonido inesperados e incluso más desincronización.

En este punto, incluso con todo el progreso que había hecho, me sentía desesperanzado con mi proyecto hasta que tuve la idea del contexto de la nota.

## Contexto de la nota

La idea era simple: pasar una estructura de datos de contexto que el usuario pudiera usar para manipular la generación de sonido sin controlar directamente los motores.

Contiene datos sobre la frecuencia actual, la velocidad y también realiza un seguimiento de la duración actual de la nota.

Esta misma estructura ligera se pasa luego a los osciladores, las fuentes de modulación y los efectos para obtener buffers de audio actualizado.

Este nuevo enfoque era muy prometedor pero requería una reelaboración completa de mi sistema, así que eliminé todo y comencé de nuevo desde cero.

Comenzar de esta manera también permitió la creación del parámetro modulado, que puede definir un valor base flotante que puede ser modulado por cualquier fuente.

Y con este último elemento, el núcleo de mi sintetizador estaba completo.

## Conclusión

Desarrollar este proyecto fue una aventura muy gratificante e interesante. Me empujó a mis propios límites de lo que sabía sobre C++, me obligó a aprender nuevas herramientas y frameworks, y me desafió a terminar y publicar algo.

Esta publicación ya es bastante larga, haré otras publicaciones más adelante explicando la arquitectura y las opciones tomadas con más detalle y también comenzaré un pequeño tutorial sobre cómo usar eficazmente LLM con Godot.
