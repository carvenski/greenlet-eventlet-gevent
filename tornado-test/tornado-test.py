

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        import time 
        print '-------------hander: ', id(self) 
        print time.time() 
        time.sleep(1)
        print time.time() 
        print '--------------------------------'
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
