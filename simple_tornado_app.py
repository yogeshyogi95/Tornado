import tornado.ioloop
from tornado.routing import URLSpec
import tornado.web
import tornado.httpclient
import tornado.escape

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<a href="%s">Link to story 1</a>' %self.reverse_url("story", "1"))
    
class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("this is story %s" % story_id)

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
    
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("you wrote "+ self.get_body_argument("message"))

class AsyncMainHandler(tornado.web.RequestHandler):
    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = await http.fetch("https://www.facebook.com")
        self.write(response.body)
        # json = tornado.escape.json_decode(response.body)
        # self.write("Fetched "+str(len(json["entries"])) + " entries from the FriendFeed API")

class TemplateRenderHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item1", "Item2", "Item3"]
        self.render("item.html", title="my items", items=items)


def make_app():
    return tornado.web.Application([
        URLSpec(r"/", MainHandler),
        URLSpec(r"/story/([0-9]+)", StoryHandler, name="story"),
        URLSpec(r"/myform", FormHandler),
        URLSpec(r"/app", tornado.web.RedirectHandler,
            dict(url="http://itunes.apple.com/my-app-id")),
        URLSpec(r"/asyncreq", AsyncMainHandler),
        URLSpec(r"/render_template", TemplateRenderHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()

