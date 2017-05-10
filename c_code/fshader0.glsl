uniform vec4 color;
uniform vec2 scale;
uniform vec2 centre;
uniform vec2 offset;
varying vec2 tcoord;
uniform sampler2D tex;


void main(void) {

  gl_FragColor = vec4 (texture2D(tex, tcoord).xyz, 1.0);
}

