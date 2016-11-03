import os
import jinja2
import webapp2
import time
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)
#________SONSTIGES__________________________________________________________________
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
		#string= a
		#self.response.write(z)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


#________DATABASE__________________________________________________________________
class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#________PAGES__________________________________________________________________
class MainPage(Handler):
    def render_front(self):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
		self.render("blog.html", arts=arts)

    def get(self):
        self.render_front()

class newpostPage(Handler):
	def render_newpost(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

		self.render("newpost.html", title=title, art=art, error=error, arts=arts)



	def get(self):
		#self.response.write('hhhhh')
		self.render('newpost.html')


	def post(self):
		title = self.request.get("subject")
		art = self.request.get("content")

		if title and art:
			a = Art(title = title, art = art)
			#a.put()
			#time.sleep(1)
			b_key = a.put() # Key('Blog', id)
			self.redirect("/blog/%d" % b_key.id())
			#self.redirect('/')
		else:
			error = "we brauch both a title and some artwork!"
			self.render_newpost(title, art, error)


class Permalink(Handler):
	def get(self, blog_id):
		s = Art.get_by_id(int(blog_id))
		self.render('blog.html', arts=[s])
		#self.response.out.write('arts')
app = webapp2.WSGIApplication([('/', MainPage),('/newpost', newpostPage), ('/blog/(\d+)', Permalink)], debug=True)


