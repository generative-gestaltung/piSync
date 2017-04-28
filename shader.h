#ifndef SHADER_H
#define SHADER_H

#include "GLES2/gl2.h"
#include "EGL/egl.h"
#include "EGL/eglext.h"
#include <stdio.h>

#define N_UNIFORMS 128

typedef struct {

	GLuint vshader;
	GLuint fshader;
	GLuint program;
} shader_t;


int load_file (char* name, char* buf);
void shader_load (shader_t* s, char* vname, char* fname);
GLuint create_uniform (shader_t* state, char* name);

#endif




