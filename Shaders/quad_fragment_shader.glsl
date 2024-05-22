#version 330 core

out vec4 FragColour;

in vec2 TexCoord;

uniform sampler2D screenTexture;
uniform float time;

void main()
{
    vec2 uv = TexCoord;
    vec3 colour = texture(screenTexture, uv).rgb;
    
    // Adjust colour channels for atmosphere
    colour.r = colour.r * 0.7;
    colour.g = colour.g * 0.4;
    colour.b = colour.b * 0.9;
    
    // Add noise
    float noise = fract(sin(dot(uv, vec2(13, 78))) * 43759);
    colour += vec3(noise * 0.1);
    
    // Darken the overall image
    colour *= 0.9;
    
    FragColour = vec4(colour, 1.0);
}