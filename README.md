# PyOpenGL Pixel Firework Simulator

A 2D graphics implementation examining OpenGL rendering techniques through particle simulations. Developed as computer graphics coursework.

## Overview

This project implements a basic firework simulation utilising PyOpenGL, demonstrating progression through OpenGL rendering methodologies. The implementation transitions from immediate mode rendering to shader-based approaches with post-processing effects.

## Implementation Features
- Particle physics simulation
- Mouse-driven firework generation
- Parallax background scrolling
- Post-processing shader implementations

## Demonstration Videos
- [Sand Simulation](Captures/sand.mp4)
- [Immediate Mode Fireworks](Captures/FW_immediate_1.mp4)
- [Modern OpenGL Implementation](Captures/ModernGL_1.mp4)
- Post-Processing:
  - [Greyscale](Captures/PP_Greyscale.mp4)
  - [Colour Inversion](Captures/PP_Inverted.mp4)
  - [Contrast Enhancement](Captures/PP_Contrast.mp4)

## Project Architecture

### Development Branches
1. `sand`: Initial particle system implementation using immediate mode
2. `main`: Firework system with immediate mode rendering
3. `Modern-OpenGL`: VAO/VBO implementation with shader integration
4. `post-processing`: Framebuffer-based post-processing effects

### Core Components
- `main.py`: Program entry, window management, render loop
- `grid.py`: Particle position management system
- `particle.py`: Particle behaviour definitions
- `firework.py`: Firework particle generation logic
- `background.py`: Background rendering and scroll management
- `gl_utils.py`: OpenGL function abstractions

## Installation
```bash
git clone https://github.com/Hamo45746/Firework-Pixel-Graphics.git
cd Firework-Pixel-Graphics
pip install -r requirements.txt
```

### Execution
```bash
python main.py
```

### Input Controls
- Left Mouse: Generate firework
- Cursor at screen edges: Scroll viewport
- Window close: Terminate program

## Technical Implementation

### Rendering Methods
1. **Immediate Mode Implementation**
   - Direct OpenGL state manipulation
   - Point sprite particle representation

2. **Modern OpenGL Integration**
   - Vertex/Fragment shader implementation
   - VAO/VBO data management
   - Texture coordinate handling

3. **Post-Processing Pipeline**
   - Framebuffer implementation
   - Fragment shader effects:
     - RGB to greyscale conversion
     - Colour channel inversion
     - Contrast modification

## Notice
This project was developed as university coursework for a computer graphics course. 
This code is provided for reference and educational purposes. Any use must comply with relevant academic integrity policies.
Project completion date: 2024
