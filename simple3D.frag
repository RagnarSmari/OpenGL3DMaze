
// First light
uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform float u_mat_shininess;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;


// Second light
uniform vec4 u_light_diffuse_second;
uniform vec4 u_light_specular_second;

uniform vec4 u_mat_diffuse_second;
uniform vec4 u_mat_specular_second;
uniform float u_mat_shininess_second;

varying vec4 v_s_second;
varying vec4 v_h_second;


void main(void)
{
	
	float lambert = max(dot(v_normal, v_s), 0);
	float phong = max(dot(v_normal, v_h), 0);

	float lambert_second = max(dot(v_normal, v_s_second), 0);
	float phong_second = max(dot(v_normal, v_h_second), 0);

	// gl_FragColor = (u_light_diffuse * u_mat_diffuse) * lambert 
	// 		+ (u_light_specular * u_mat_specular) * pow(phong, u_mat_shininess);

	gl_FragColor = ((u_light_diffuse * u_mat_diffuse) * lambert 
			+ (u_light_specular * u_mat_specular) * pow(phong, u_mat_shininess)
			+ (u_light_diffuse_second * u_mat_diffuse_second) * lambert_second
			+ (u_light_specular_second * u_mat_specular_second) * pow(phong_second, u_mat_shininess_second)); 
}