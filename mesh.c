#include "mesh.h"



void mesh_init (mesh_t* mesh, shader_t* shader, int nVertices, GLfloat* data) {

	printf("%d\n", nVertices);
	mesh->attr_vertex = glGetAttribLocation (shader->program, "vertex");
	glGenBuffers (1, &mesh->buf);
	glBindBuffer (GL_ARRAY_BUFFER, mesh->buf);
	glBufferData (GL_ARRAY_BUFFER, nVertices*4*sizeof(GLfloat), data, GL_STATIC_DRAW);
	glVertexAttribPointer (mesh->attr_vertex, 4, GL_FLOAT, 0, nVertices*4, 0);
	glEnableVertexAttribArray (mesh->attr_vertex);
}
