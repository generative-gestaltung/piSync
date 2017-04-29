uniform vec4 color;
uniform vec2 scale;
uniform vec2 centre;
varying vec2 tcoord;

void main(void) {

  gl_FragColor = vec4 (sin(tcoord.x*55.0)*0.5+0.5, 1.0, sin(tcoord.y*65.0)*0.5+0.5, 1.0);
}
