#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in vec4 colour;

out vec4 vertexColour;

uniform float scroll_position;

void main() {
    gl_Position = vec4(position.x + scroll_position, position.y, 0.0, 1.0);
    vertexColour = colour;
}
