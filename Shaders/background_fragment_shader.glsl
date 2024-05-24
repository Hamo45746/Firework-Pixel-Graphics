#version 330 core
// REF: https://learnopengl.com/Getting-started/Shaders
// REF: https://learnopengl.com/Advanced-OpenGL/Framebuffers

out vec4 FragColour;
in vec2 TexCoord;

uniform sampler2D texture1;

void main() {
    FragColour = texture(texture1, TexCoord);
}
