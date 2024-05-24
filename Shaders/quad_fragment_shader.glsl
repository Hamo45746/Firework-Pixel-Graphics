#version 330 core

out vec4 FragColour;
in vec2 TexCoord;

uniform sampler2D screenTexture;

void main() {
    vec3 sample = texture(screenTexture, TexCoord).rgb;
    //REF: https://stackoverflow.com/questions/944713/help-with-pixel-shader-effect-for-brightness-and-contrast
    // Increase contrast
    vec3 contrast = (sample - 0.5) * 2.0 + 0.5;
    
    FragColour = vec4(contrast, 1.0);
}

