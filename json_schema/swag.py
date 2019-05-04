
from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose

# load Swagger resource file into App object
app = App._create_('https://canvas.instructure.com/doc/api/courses.json')

auth = Security(app)
# auth.update_with('api_key', '9371~SNSl0krgbvfe8JYXS5NSKh7FJLcqO8yNmwZOb9ku79YGDmIXLNCjzjiOBGvfFya9') # api key
# auth.update_with('petstore_auth', '12334546556521123fsfss') # oauth2

# init swagger client
client = Client(auth)

