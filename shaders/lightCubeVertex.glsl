#version 330 core
layout(location = 0) in vec4 vertexPosition; 
layout(location = 1) in vec4 vertexColor; 
layout(location = 2) in vec2 vertexUV;
layout(location = 3) in vec3 vertexNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main()
{

   gl_Position = proj * view * model * vertexPosition;
}
