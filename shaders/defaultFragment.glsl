#version 330

in vec4 fragColor; 
in vec2 fragUV;
in vec3 fragNormal;
in vec3 fragPosition;

out vec4 outColor;

struct SpotLight
{
	vec3 position;
	vec3 direction;
	vec3 color;
	float intensity;

    float cutOff;
    float outerCutOff;
  
    float constant;
    float linear;
    float quadratic;

	mat4 lightView;
	mat4 lightProj;
	
	bool shadowOn;
};


struct Material
{
	vec3 ambient;
	vec3 diffuse;
	vec3 specular;
	float shininess;
};

# define NR_SPOT_LIGHTS 2

uniform SpotLight spotLights[NR_SPOT_LIGHTS];
uniform Material material;

uniform bool useSpotLightOne;
uniform bool useSpotLightTwo;

uniform sampler2D depthMapTex1;
uniform sampler2D depthMapTex2;

uniform bool blinn = true;

uniform vec3 viewPos;

uniform sampler2D tex1;

float calcShadow(vec4 fragPosLightSpace, sampler2D depthMapTex)
{
	// perform perspective divide to go to NDC
	vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;

	// Transform to [0,1] range
	projCoords = projCoords * 0.5 + 0.5;

	// Get depth of current fragment from light's perspective
	float currentDepth = projCoords.z;

	// PCF - percentage closer filtering
	// sample shadowmap multiple times at slightly offset positions
	// and take average
	float shadow = 0.0;
	vec2 texelSize = 1.0 / textureSize(depthMapTex, 0);
	int samples = 0;
	for(int x = -2; x <= 2; ++x)
	{
		for(int y = -2; y <= 2; ++y)
		{
			float pcfDepth = texture(depthMapTex, projCoords.xy + vec2(x, y) * texelSize).r;
			shadow += currentDepth > pcfDepth  ? 1.0 : 0.0;
			samples += 1;
		}
	}
	shadow /= float(samples);

	// Keep the shadow at 0.0 when outside the far_plane region of the light's frustum.
	if(projCoords.z > 2.0) {
		shadow = 0.0;
	}

	// fake ambient light by scaling shadows
	return shadow * 0.8;
}


vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDirection,bool blinn, Material material,float shadow)
{
	vec3 lightDirection = normalize(light.position - fragPos);
	
	// simple lambert diffuse shading model
	float nDotL = max(dot(normal, lightDirection), 0.0);

	//specular
	float spec = 0.0;
	if(blinn)
	{
		vec3 halfwayDirection = normalize(lightDirection + viewDirection);
		spec = pow(max(dot(halfwayDirection, normal), 0.0), material.shininess);
	}

	float distance = length(light.position - fragPos);
	float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

	vec3 ambient = material.ambient * light.color * light.intensity * attenuation;
	vec3 diffuse = material.diffuse * light.color * nDotL * light.intensity * attenuation;
	vec3 specular = material.specular * light.color * spec * light.intensity * attenuation;


	float theta = dot(lightDirection, normalize(-light.direction));
	float epsilon = light.cutOff - light.outerCutOff;
	float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);

	return ((ambient +(1-shadow)) *(diffuse + specular)) * intensity;
}




void main()
{	
	vec3 result = vec3(0.0);

	vec4 texVal = texture(tex1, fragUV);
	float ambientStrength = 0.2;
	vec3 ambient = ambientStrength * material.ambient;
	vec3 viewDirection = normalize(viewPos - fragPosition);

	vec3 normal = normalize(fragNormal);

	float shadowOne = 0.0;
	float shadowTwo = 0.0;
	
	if(useSpotLightOne)
	{

		if(spotLights[0].shadowOn)
		{
			vec4 fragPosLightSpace = spotLights[0].lightProj * spotLights[0].lightView * vec4(fragPosition.x,fragPosition.y,fragPosition.z, 1.0);
			shadowOne = calcShadow(fragPosLightSpace,depthMapTex1);
		}
		
		// If shadow not on, shadow value is 0.0

		result += CalcSpotLight(spotLights[0], normal, fragPosition, viewDirection, blinn, material,shadowOne);

	}


	if(useSpotLightTwo)
	{

		if(spotLights[1].shadowOn)
		{
			vec4 fragPosLightSpace = spotLights[1].lightProj * spotLights[1].lightView * vec4(fragPosition.x,fragPosition.y,fragPosition.z, 1.0);
			shadowTwo = calcShadow(fragPosLightSpace,depthMapTex2);
		}
		
		// If shadow not on, shadow value is 0.0

		result += CalcSpotLight(spotLights[1], normal, fragPosition, viewDirection, blinn, material,shadowTwo);

	}
	

	result += ambient;

	outColor =  vec4(result,1.0)*fragColor*texVal;
	
}

