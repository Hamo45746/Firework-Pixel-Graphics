#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in vec4 color;

out vec4 vertexColor;

uniform float point_size;

void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    gl_PointSize = point_size;
    vertexColor = color;
}