#version 330 core

out vec4 FragColour;

in vec2 TexCoord;

uniform sampler2D screenTexture;

void main() {
    // REF: https://medium.com/@rupertontheloose/functional-shaders-a-colorful-intro-part4-gray-scale-d8595ec75601
 
    vec3 sample = texture(screenTexture, TexCoord).rgb;
    
    // Calculate luminance
    float luminance = 0.3 * sample.r + 0.59 * sample.g + 0.11 * sample.b;
    
    vec3 grayscale = vec3(luminance);
    
    FragColour = vec4(grayscale, 1.0);
}
