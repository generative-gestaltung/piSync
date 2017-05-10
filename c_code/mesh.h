#ifndef MESH_H
#define MESH_H

#include "GLES2/gl2.h"
#include "EGL/egl.h"
#include "EGL/eglext.h"
#include "shader.h"


typedef struct {
	GLuint buf;
	GLuint attr_vertex;
} mesh_t;

void mesh_init (mesh_t* mesh, shader_t* shader, int nvertices, GLfloat* data);

#endif

