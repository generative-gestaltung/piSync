#include "texture.h"

void init_texture (texture_t* tex, int w, int h) {


        glGenTextures (1, &tex->tex);
        //check();
        glBindTexture (GL_TEXTURE_2D, tex->tex);
        //check();

        // glActiveTexture(0)
        glTexImage2D (GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_SHORT_5_6_5, 0);
        //check();
        glTexParameterf (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameterf (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        //check();
        // Prepare a framebuffer for rendering
        glGenFramebuffers (1, &tex->tex_fb);
        //check();
        glBindFramebuffer (GL_FRAMEBUFFER, tex->tex_fb);
        //check();
        glFramebufferTexture2D (GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex->tex, 0);
        //check();
        glBindFramebuffer (GL_FRAMEBUFFER, 0);
        //check();
        // Prepare viewport
        glViewport (0, 0, w, h);
        //check();


}

