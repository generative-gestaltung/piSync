#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>

#include "bcm_host.h"
#include "GLES2/gl2.h"
#include "EGL/egl.h"
#include "EGL/eglext.h"
#include "shader.h"
#include "mesh.h"
#include "texture.h"

typedef struct
{
   uint32_t screen_width;
   uint32_t screen_height;

   EGLDisplay display;
   EGLSurface surface;
   EGLContext context;

   GLuint verbose;
   GLuint tex_fb;
   GLuint tex;
   GLuint unif_color, unif_scale, unif_offset, unif_tex, unif_centre;
   GLuint attr_vertex2, unif_scale2, unif_offset2, unif_centre2;
} CUBE_STATE_T;

static CUBE_STATE_T _state, *state=&_state;
static mesh_t mesh0;
static shader_t s0;
static shader_t s1;
texture_t tex0;

#define check() assert(glGetError() == 0)



static void init_ogl (CUBE_STATE_T *state) {
   int32_t success = 0;
   EGLBoolean result;
   EGLint num_config;

   static EGL_DISPMANX_WINDOW_T nativewindow;

   DISPMANX_ELEMENT_HANDLE_T dispman_element;
   DISPMANX_DISPLAY_HANDLE_T dispman_display;
   DISPMANX_UPDATE_HANDLE_T dispman_update;
   VC_RECT_T dst_rect;
   VC_RECT_T src_rect;

   static const EGLint attribute_list[] =
   {
      EGL_RED_SIZE, 8,
      EGL_GREEN_SIZE, 8,
      EGL_BLUE_SIZE, 8,
      EGL_ALPHA_SIZE, 8,
      EGL_SURFACE_TYPE, EGL_WINDOW_BIT,
      EGL_NONE
   };

   static const EGLint context_attributes[] =
   {
      EGL_CONTEXT_CLIENT_VERSION, 2,
      EGL_NONE
   };
   EGLConfig config;

   // get an EGL display connection
   state->display = eglGetDisplay(EGL_DEFAULT_DISPLAY);
   assert(state->display!=EGL_NO_DISPLAY);
   check();

   // initialize the EGL display connection
   result = eglInitialize(state->display, NULL, NULL);
   assert(EGL_FALSE != result);
   check();

   // get an appropriate EGL frame buffer configuration
   result = eglChooseConfig(state->display, attribute_list, &config, 1, &num_config);
   assert(EGL_FALSE != result);
   check();

   // get an appropriate EGL frame buffer configuration
   result = eglBindAPI(EGL_OPENGL_ES_API);
   assert(EGL_FALSE != result);
   check();

   // create an EGL rendering context
   state->context = eglCreateContext(state->display, config, EGL_NO_CONTEXT, context_attributes);
   assert(state->context!=EGL_NO_CONTEXT);
   check();

   // create an EGL window surface
   success = graphics_get_display_size(0 /* LCD */, &state->screen_width, &state->screen_height);
   assert( success >= 0 );

   dst_rect.x = 0;
   dst_rect.y = 0;
   dst_rect.width = state->screen_width;
   dst_rect.height = state->screen_height;

   src_rect.x = 0;
   src_rect.y = 0;
   src_rect.width = state->screen_width << 16;
   src_rect.height = state->screen_height << 16;

   dispman_display = vc_dispmanx_display_open( 0 /* LCD */);
   dispman_update = vc_dispmanx_update_start( 0 );

   dispman_element = vc_dispmanx_element_add ( dispman_update, dispman_display,
      0/*layer*/, &dst_rect, 0/*src*/,
      &src_rect, DISPMANX_PROTECTION_NONE, 0 /*alpha*/, 0/*clamp*/, 0/*transform*/);

   nativewindow.element = dispman_element;
   nativewindow.width = state->screen_width;
   nativewindow.height = state->screen_height;
   vc_dispmanx_update_submit_sync( dispman_update );

   check();

   state->surface = eglCreateWindowSurface( state->display, config, &nativewindow, NULL );
   assert(state->surface != EGL_NO_SURFACE);
   check();

   // connect the context to the surface
   result = eglMakeCurrent(state->display, state->surface, state->surface, state->context);
   assert(EGL_FALSE != result);
   check();

   // Set background color and clear buffers
   glClearColor(0.15f, 0.25f, 0.35f, 1.0f);
   glClear( GL_COLOR_BUFFER_BIT );

   check();
}


void init_shaders(CUBE_STATE_T *state) {


	GLfloat vertex_data[] = {
		-0.5,-0.5,1.0,1.0,
		0.5,-0.5,1.0,1.0,
		0.5,0.5,1.0,1.0,
		-0.5,0.5,1.0,1.0
	};


	shader_load (&s0, "vshader.glsl", "fshader0.glsl");
	shader_load (&s1, "vshader.glsl", "fshader1.glsl");

        state->unif_color  = create_uniform (&s0, "color");
        state->unif_scale  = create_uniform (&s0, "scale");
        state->unif_offset = create_uniform (&s0, "offset");
        state->unif_tex    = create_uniform (&s0, "tex");
        state->unif_centre = create_uniform (&s0, "centre");


        //if (state->verbose)
        //    showprogramlog(state->program2);
        //state->attr_vertex2 = create_uniform (&s1, "vertex");
        state->unif_scale2  = create_uniform (&s1, "scale");
        state->unif_offset2 = create_uniform (&s1, "offset");
        state->unif_centre2 = create_uniform (&s1, "centre");
        check();

        glClearColor (0.0, 1.0, 1.0, 1.0);
        //glGenBuffers(1, &state->buf);
        check();

	mesh_init (&mesh0, &s0, 4, vertex_data);

}



static void draw_texture (CUBE_STATE_T *state, GLfloat cx, GLfloat cy, GLfloat scale) {

        glBindFramebuffer (GL_FRAMEBUFFER, tex0.tex_fb);
        check();
        glBindBuffer (GL_ARRAY_BUFFER, mesh0.buf);

        glUseProgram (s1.program);
        check();

        glUniform2f (state->unif_scale2, scale, scale);
        glUniform2f (state->unif_centre2, cx, cy);
        check();
        glDrawArrays (GL_TRIANGLE_FAN, 0, 4);
        check();

        glFlush();
        glFinish();
        check();
}

static void draw_screen (CUBE_STATE_T *state, GLfloat cx, GLfloat cy, GLfloat scale, GLfloat x, GLfloat y) {

        glBindFramebuffer(GL_FRAMEBUFFER,0);
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
        check();

        glBindBuffer (GL_ARRAY_BUFFER, mesh0.buf); //state->buf);
        check();

        glUseProgram (s0.program);
        check();

        glBindTexture (GL_TEXTURE_2D, tex0.tex);
        check();

        glUniform4f (state->unif_color, 0.5, 0.5, 0.8, 1.0);
        glUniform2f (state->unif_scale, scale, scale);
        glUniform2f (state->unif_offset, x, y);
        glUniform2f (state->unif_centre, cx, cy);
        glUniform1i (state->unif_tex, 0);
        check();

        glDrawArrays (GL_TRIANGLE_FAN, 0, 4);
        check();

        glBindBuffer(GL_ARRAY_BUFFER, 0);

        glFlush();
        glFinish();
        check();

        eglSwapBuffers(state->display, state->surface);
        check();
}



int main ()
{

	int terminate = 0;

	GLfloat cx, cy;
	bcm_host_init();

	memset (state, 0, sizeof(*state));

	init_ogl(state);
	init_shaders(state);


	init_texture (&tex0, state->screen_width, state->screen_height);
	cx = state->screen_width/2;
	cy = state->screen_height/2;

	draw_texture(state, cx, cy, 0.003);

	while (!terminate) {
		int x, y, b;
		draw_screen(state, cx, cy, 0.003, x, y);
	}

	return 0;
}

