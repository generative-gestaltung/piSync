#ifndef TEXTURE_H

#include "GLES2/gl2.h"
#include "EGL/egl.h"
#include "EGL/eglext.h"
#include <stdio.h>

typedef struct {
	GLuint tex_fb;
	GLuint tex;
} texture_t;

void init_texture (texture_t* tex, int w, int h);

#endif




