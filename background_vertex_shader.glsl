#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 aTexCoord;

uniform vec2 translation; // Translation (x, y)
uniform vec2 scale; // Scale (x, y)

out vec2 TexCoord;

void main()
{
    vec2 pos = (aPos * scale) + translation; // Apply scaling and translation
    gl_Position = vec4(pos, 0.0, 1.0);
    TexCoord = aTexCoord;
}
