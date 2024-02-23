#version 330

layout(location = 0) in vec4 vertexPosition; 
layout(location = 1) in vec4 vertexColor; 
layout(location = 2) in vec2 vertexUV;
layout(location = 3) in vec3 vertexNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec4 fragColor;
out vec2 fragUV;
out vec3 fragNormal;
out vec3 fragPosition;

void main()
{
   fragPosition = vec3(model * vertexPosition);
   fragNormal = mat3(transpose(inverse(model))) * vertexNormal;
   gl_Position = proj * view * vec4(fragPosition, 1.0);
   fragColor = vertexColor;
   fragUV = vertexUV;
}