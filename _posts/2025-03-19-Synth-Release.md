---
layout: post
title: Godot Synth Release
date: 2025-03-19
description: First public release of the Godot Synth Plugin
tags:
  - godot
  - music
  - c++
categories: Godot
featured: true
toc:
  sidebar: left
---

## Overview

A few days ago I finished the first version of my synthesizer plugin for Godot.
This project is meant now to become a full set of features for game developers and sound designers to create, modify, modulate and perform sounds in game in a programmer friendly and efficient way.

## Project Start

For valentine's day in 2025 I decided to make my partner an app.
She's always liked flowers, so I made a small Godot mobile game where you procedurally grow a flower, the game has a simple day/night cycle and a procedural music system.

And if you think that I have used the word procedural too many times, it is because I wanted to make all the content for her app during runtime.

So I made a few algorithms, learned how to use LLMs for game development (a process which is still ongoing) and made an android build to test.

To my surprise, the flower looked kinda nice from my very first attempt and the whole system seemed to run at a very respectable frame rate (for a GDScript running on an old Pixel phone) until the first procedurally generated music note started playing, which dropped my frame rate to about 5~6 fps and made my game unplayable.

## GDScript vs C++

At that point I only had a few hours to deliver my project in time, as missing Valentine's Day would mean I should wait a year to deliver the project and also that I would have nothing of mine to give.

So I hacked a solution where I played very small short notes from my synth and then would use expansive reverbs and long delays to fake longer sounds.

This got me to an acceptable performance for my project but left an itch at the back of my mind, the core idea of procedurally generating the sounds was very good and worked really well for the game ambiance, and I knew that this was the way I wanted to compose music for my next games.

So I started looking into how to optimize the sound system I had made initially and the obvious answer was implementing it as a GDExtension plugin.

According to DeepSeek, moving my sound generation algorithm to C++ could make a 100x improvement in performance, so I decided to do it.

## Plaits

To be completely honest, this was not the first time I tried something like this either, I love using VCV Rack and would consider it my main DAW. I am a big fan of the SurgeXT series of audio plugins, and their implementation in VCV is just outstanding.

SurgeXT provides extensive modulation capabilities with very easy to follow visual aids to showcase what the modulation is actually doing.

I am also a big fan of Emilie Gillet and her open source contributions to electronic music, I don't think I am exaggerating when I say that she's probably the most influential audio developer of our generation. This brings me to [Plaits](https://pichenettes.github.io/mutable-instruments-documentation/modules/plaits/downloads/plaits_quickstart.pdf).

> Plaits is a digital voltage-controlled sound source capable of
sixteen different synthesis techniques. Plaits reclaims the
land between all the fragmented islands of sound produced
by its predecessor, Braids

For those of you who don't know, Plaits is a macro oscillator sound module by Mutable Instruments with several different sound engines and 4 large knobs on the front to control:

- Frequency
- Harmonics
- Timbre
- Morph

And with these 4 simple controllers, the module is able to tame some oscillation algorithms that are usually very difficult to manage, like granular formant or FM synthesis.

This gives users an immense sound palette and makes the module extremely flexible, allowing users to do percussions, leads, pads chords and a lot more with a simple but efficient setup.

## First attempt

The [source code](https://github.com/pichenettes/eurorack/tree/master/plaits) for it is also MIT license, so my first idea was to simply bring Plaits into Godot.

So back in November, I made a repository and named it Glaits, watched a bunch of tutorials on how to create C++ extensions for Godot and got up to the point where I could compile the project with the imported Plaits submodules, but these were never meant to run on the same environment as a game engine.

These were also extremely heavily optimized algorithms, which meant that some critical steps of the code were actually written in assembler, which the Godot compiler was having a lot of trouble figuring out.

This put a instant brake into my project just after a week of development and I decided to leave it there.

## Second Attempt

After taking a break from the initial attempt with Glaits, I decided to approach the problem from a different angle. Instead of directly porting the entire Plaits module into Godot, I would focus on creating a lightweight version that encapsulated the core functionalities I wanted to implement in my synthesizer plugin.

### Research and Redesign

I revisited the functionalities of Plaits and identified the key synthesis techniques that would be most useful for game development. These included:

- **Basic Waveforms**: Sine, Square, Sawtooth, and Triangle.
- **FM Synthesis**: For more complex harmonic content.
- **Granular Synthesis**: To create evolving textures and soundscapes.
- **Formant**: To create speech sounding audio.
- **Noise Generation**: Useful for percussive sounds and effects.

With these elements in mind, I designed a simplified architecture for my synthesizer plugin. This would consist of modular components that could be easily combined and controlled in real-time through Godot’s scripting system.

### Implementation Steps

1. **Setting Up the GDExtension Framework**:
   - I created a new GDExtension project within Godot 4.x.
   - Followed guidelines on setting up C++ bindings to expose my synthesizer functions to GDScript.

2. **Core Sound Engine Development**:
   - Implemented basic waveforms using C++, ensuring they were optimized for performance.
   - Developed an FM synthesis module, allowing users to adjust frequency modulation parameters dynamically.
   - Created a formant engine for voice synthesis.

3. **Modulation System**:
   - Added modulation options for the most important parameters

4. **User Interface Components**:
   - Integrated custom UI components in Godot that allow users to interact with the synthesizer easily.
   - Used Control nodes to create sliders, knobs, and buttons representing each parameter of the sound engine.

5. **Testing and Optimization**:
   - Conducted extensive testing on various devices (including lower-end Android phones) to ensure performance remained high even with multiple instances running simultaneously.
   - Profiled code regularly using Godot's built-in debugging tools to identify any bottlenecks.

### Early Results

After a week of development on this using AI powered development tools I had made a lot of progress and had a setup with 3 oscillator engines with different modulation parameters and support for saving presets by using a Sound Configuration custom resource.

In this early and naive iteration the sound configuration was in charge of almost everything, as it would create an appropriate engine to produce the sound, create the audio bus specifically for this sound, create the audio effects defined in the audio effect array.

The modulations were also hardcoded into the variables they were controlling which started showing some synchronization issues when some modulations were running at a faster pace than others.

### Buffer issues

The last straw came when trying to create a modulated effect. Like I explained the effects were handled by the audio bus itself, which meant that the Godot internal audio server was in charge of the timings and the buffer which created a few issues with my plan.

Mainly, my modulations to the sound generators were applied on a **per-sample** basis, ensuring high resolution on the modulators, but I could only modulate the effects on a **per-buffer** basis, causing some unexpected sound artifacts and even more desynchronization.

At this point, even with all the progress I had made, I was feeling hopeless about my project until I had the idea of the note context.

## Note context

The idea was simple: to pass a context data structure that the user could use to manipulate the sound generation without directly controlling the engines.

It contains data about the current frequency, velocity and also keeps track of the current note duration.

This same lightweight structure then gets passed around the oscillators, modulation sources and effects in order to obtain updated audio buffers.

This new approach was very promising but required a complete rework of my system, so I deleted everything and started again from scratch.

Starting this way also allowed for the creation of the modulated parameter, which can define a float base value that can be modulated by any source.

And with this last element the core of my synthesizer was complete.

## Conclusion

Developing this project was a very rewarding and interesting adventure. It pushed me to my own limits of what I knew about C++, forced me to learn new tools and frameworks, and challenged me to actually finish and publish something.

This post is long enough as it is right now, I'll make some more other post later explaining the architecture and the choices made in more detail and will also start a small tutorial on how to effectively use LLMs with Godot.
