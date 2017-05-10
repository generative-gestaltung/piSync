import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import json
from audiothread import AudioThread


audioT = AudioThread (0, "audio", 0, "wav")


class MainHandler(tornado.web.RequestHandler):

    def get(self):        
        self.write("Hello, world")


class WSHandler(tornado.websocket.WebSocketHandler):
 

    def open (self):
        print "WS connection open"

    def on_message (self, message):
        
        message_dict = json.loads(message)
        audioT.cmd(message_dict)




favicon_path = '.'
static_path = './static'

handlers = [
            (r'/favicon.ico', MainHandler), #tornado.web.StaticFileHandler, {'path': favicon_path}),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
            (r'/', MainHandler),
            (r'/ws', WSHandler)
]



if __name__ == "__main__":

    audioT.start()

    app = tornado.web.Application(handlers)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


