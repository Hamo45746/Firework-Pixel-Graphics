#version 330 core
out vec4 FragColour;
in vec2 TexCoord;
uniform sampler2D screenTexture;
void main()
{
FragColour = texture(screenTexture, TexCoord);
}