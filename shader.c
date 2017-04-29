#include "shader.h"


int load_file (char* name, char* buf) {
	FILE* pFile = fopen(name, "r");
	fseek(pFile, 0, SEEK_END);
	long len = ftell(pFile);
	rewind (pFile);

	fread(buf, 1, len, pFile);
	fclose(pFile);

	return len;
}


#define FILE_LEN 1024*1024

void shader_load (shader_t* state, char* vname, char* fname) {


	GLchar* fshader = (GLchar*)malloc(FILE_LEN);
	GLchar* vshader = (GLchar*)malloc(FILE_LEN);

	memset(fshader, 0, FILE_LEN);
	memset(vshader, 0, FILE_LEN);

	load_file (vname, vshader);
	load_file (fname, fshader);

	GLchar* vshader_source = vshader;
	GLchar* fshader_source = fshader;



        state->vshader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(state->vshader, 1, &vshader_source, 0);
        glCompileShader(state->vshader);
        //check();

        //if (state->verbose)
        //    showlog(state->vshader);

        state->fshader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(state->fshader, 1, &fshader_source, 0);
        glCompileShader(state->fshader);
        //check();

        //if (state->verbose)
        //    showlog(state->fshader);


        state->program = glCreateProgram();
        glAttachShader(state->program, state->vshader);
        glAttachShader(state->program, state->fshader);
        glLinkProgram(state->program);

        //check();

        //if (state->verbose)
        //    showprogramlog(state->program);
}

GLuint create_uniform (shader_t* state, char* name) {

        return glGetUniformLocation (state->program, name);
}


void showlog(GLint shader) {
   // Prints the compile log for a shader
   char log[1024];
   glGetShaderInfoLog(shader,sizeof log,NULL,log);
   printf("%d:shader:\n%s\n", shader, log);
}

void showprogramlog(GLint shader) {
   // Prints the information log for a program object
   char log[1024];
   glGetProgramInfoLog(shader,sizeof log,NULL,log);
   printf("%d:program:\n%s\n", shader, log);
}
