struct DirectionalLight
{
	vec3 direction;
	vec3 color;
	float intensity;
};

struct PointLight
{
	vec3 position;
	vec3 color;
	float intensity;

	float constant;
    float linear;
    float quadratic;
};

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
  
};


vec3 CalcDirectionalLight(DirectionalLight light, vec3 normal, vec3 viewDirection);
vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDirection);
vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDirection);


uniform DirectionalLight dirLight;
uniform PointLight pointLight;
uniform SpotLight spotLight;





vec3 CalcDirectionalLight(DirectionalLight light, vec3 normal, vec3 viewDirection)
{
	vec3 lightDirection = normalize(-light.direction);
	
	// simple lambert diffuse shading model
	float nDotL = max(dot(normal, lightDirection), 0.0);

	//specular
	vec3 halfwayDirection = normalize(lightDirection + viewDirection);
	float spec = pow(max(dot(halfwayDirection, normal), 0.0), 64);


	return light.color * light.intensity * (spec + nDotL);
}

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDirection)
{
	vec3 lightDirection = normalize(light.position - fragPos);
	
	// simple lambert diffuse shading model
	float nDotL = max(dot(normal, lightDirection), 0.0);

	//specular
	vec3 halfwayDirection = normalize(lightDirection + viewDirection);
	float spec = pow(max(dot(halfwayDirection, normal), 0.0), 64);

	float distance = length(light.position - fragPos);
	float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

	return light.color * light.intensity * attenuation * (spec + nDotL);
}

vec3 CalcSpotLight(SpotLight light, vec3 normal, vec3 fragPos, vec3 viewDirection)
{
	vec3 lightDirection = normalize(light.position - fragPos);
	
	// simple lambert diffuse shading model
	float nDotL = max(dot(normal, lightDirection), 0.0);

	//specular
	vec3 halfwayDirection = normalize(lightDirection + viewDirection);
	float spec = pow(max(dot(halfwayDirection, normal), 0.0), 64);

	float distance = length(light.position - fragPos);
	float attenuation = 1.0 / (light.constant + light.linear * distance + light.quadratic * (distance * distance));

	float theta = dot(lightDirection, normalize(-light.direction));
	float epsilon = light.cutOff - light.outerCutOff;
	float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);

	return light.color * light.intensity * attenuation * intensity * (spec + nDotL);
}
