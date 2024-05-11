#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in vec4 colour;

out vec4 vertexColour;

uniform float scaling_factor;

void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    gl_PointSize = scaling_factor;
    vertexColour = colour;
}