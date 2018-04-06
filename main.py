import webapp2
import json
import re
from model import Coffee
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template


API_KEY = "WuVbkuUsCXHPx3hsQzus4SE"


class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['x-frame-options'] = 'DENY'
        self.response.out.write(template.render("home.html", {}))


class CoffeeHandler(webapp2.RequestHandler):
    def get(self):
        if valid_api_key(self.request):
            write_json_response(
                self.response,
                [c.to_json_summary_dict() for c in Coffee.query().fetch()]
            )
        else:
            write_api_error_response(self.request, self.response)

    def post(self):
        if valid_api_key(self.request):
            id = re.sub(r'\W+', '', self.request.get("id"))
            name = self.request.get("name")
            desc = self.request.get("desc")
            image_url = self.request.get("image_url")

            coffee = Coffee(id=id, name=name, desc=desc, image_url=image_url)
            coffee.put()
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(
                json.dumps(Coffee.get_by_id(id=id).to_json_full_dict())
            )
        else:
            write_api_error_response(self.request, self.response)

    def put(self):
        self.post()


class CoffeeItemHandler(webapp2.RequestHandler):
    def get(self, id):
        if valid_api_key(self.request):
            write_json_response(self.response,
                                Coffee.get_by_id(id=id).to_json_full_dict())
        else:
            write_api_error_response(self.request, self.response)

    def delete(self, id):
        if valid_api_key(self.request):

            coffee = Coffee.get_by_id(id=id)

            if (coffee is not None):
                coffee.key.delete()
                write_json_response(self.response, {"status": "done"})
            else:
                self.error(404)

        else:
            write_api_error_response(self.request, self.response)


class PrimeDBHandler(webapp2.RequestHandler):
    def get(self):
        if valid_api_key(self.request):
            ndb.delete_multi(Coffee.query().fetch(keys_only=True))
            Coffee(
                id="latte",
                name="Caffe Latte",
                desc=("Similar to the Portuguese Galao, a latte is a portion "
                      "of espresso and steamed milk, generally in a 1:3 to "
                      "1:5 ratio of espresso to milk, with a little foam on "
                      "top."),
                image_url=("http://upload.wikimedia.org/wikipedia/commons/"
                           "thumb/0/01/Latte.jpg/800px-Latte.jpg")).put()
            Coffee(
                id="americano",
                name="Caffe Americano",
                desc=("A style of coffee prepared by adding hot water to "
                      "espresso, giving a similar strength to but different "
                      "flavor from regular drip coffee."),
                image_url="").put()
            Coffee(
                id="mocha",
                name="Cafe Mocha",
                desc=("A variant of a caffe latte. Like a latte, it is "
                      "typically one third espresso and two thirds steamed "
                      "milk, but a portion of chocolate is added, typically in"
                      " the form of a chocolate syrup."),
                image_url=("http://upload.wikimedia.org/wikipedia/commons/"
                           "thumb/5/58/Mocha_Latte_Costa_Rica.JPG/"
                           "220px-Mocha_Latte_Costa_Rica.JPG")).put()
            Coffee(
                id="coldbrew",
                name="Cold Brew",
                desc=("Refers to the process of steeping coffee grounds in "
                      "room temperature or cold water for an extended "
                      "period."),
                image_url="").put()
            Coffee(
                id="cappuccino",
                name="Cappuccino",
                desc=("A coffee-based drink prepared with espresso, hot milk, "
                      "and steamed milk foam. A cappuccino differs from a "
                      "caffe latte in that it is prepared with much less "
                      "steamed or textured milk than the caffe latte with the "
                      "total of espresso and milk/foam making up between "
                      "approximately 150 and 180 millilitres (5 and 6 US "
                      "fluid ounces)."),
                image_url=("http://upload.wikimedia.org/wikipedia/commons/"
                           "thumb/1/16/Classic_Cappuccino.jpg/"
                           "800px-Classic_Cappuccino.jpg")).put()
            Coffee(
                id="decaf",
                name="Decaf",
                desc="A coffee beverage made with decaffeinated beans.",
                image_url="").put()
            Coffee(
                id="espresso",
                name="Espresso",
                desc=("Espresso is a concentrated beverage brewed by forcing "
                      "a small amount of nearly boiling water under pressure "
                      "through finely ground coffee beans."),
                image_url=("http://upload.wikimedia.org/wikipedia/commons/"
                           "thumb/4/44/Crema_espresso_Akha_Ama.jpg/"
                           "575px-Crema_espresso_Akha_Ama.jpg")).put()
            Coffee(
                id="affogato",
                name="Affogato",
                desc=("A coffee-based beverage or dessert. Usually refers to "
                      "the act of topping a drink or dessert with espresso, "
                      "may also incorporate caramel sauce or chocolate "
                      "sauce."),
                image_url=("http://upload.wikimedia.org/wikipedia/commons/"
                           "thumb/1/19/Affogato.JPG/800px-Affogato.JPG")).put()
            write_json_response(self.response, {"status": "done"})
        else:
            write_api_error_response(self.request, self.response)


def valid_api_key(request):
    return ((request.get("api_key") == API_KEY)
            or (request.headers.get('Authorization') == API_KEY))


def write_api_error_response(request, response):
    if ((request.get("api_key", None) is None)
            and (request.headers.get('Authorization', None) is None)):
        write_json_response(response, {"error": "no api key provided"})
    else:
        write_json_response(response, {"error": "invalid api key"})


def write_json_response(response, response_data):
    response.headers['Content-Type'] = 'application/json'
    response.headers['x-frame-options'] = 'DENY'
    response.out.write(json.dumps(response_data))


app = webapp2.WSGIApplication([
    ('/', HomePageHandler),
    ('/api/coffee/', CoffeeHandler),
    ('/api/coffee/([\w]+)/?', CoffeeItemHandler),
    ('/reset/', PrimeDBHandler),
], debug=True)
