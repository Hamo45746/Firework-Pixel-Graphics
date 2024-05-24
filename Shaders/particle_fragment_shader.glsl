#version 330 core
// REF: https://learnopengl.com/Advanced-OpenGL/Framebuffers 
// REF: https://learnopengl.com/Getting-started/Shaders

in vec4 vertexColour;
out vec4 fragColour;

void main() {
    fragColour = vertexColour;
}
