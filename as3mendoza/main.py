# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from google.appengine.api import oauth
import json
from google.appengine.ext import ndb

app = webapp2.WSGIApplication([
	('/illness','classes.IllnessHandler'),
], debug=True)
#app.router.add(webapp2.Route(r'/illness','classes.IllnessHandler'))
app.router.add(webapp2.Route(r'/illness/<id:[0-9]+><:/?>','classes.IllnessHandler'))
app.router.add(webapp2.Route(r'/patient','classes.patientHandler'))
app.router.add(webapp2.Route(r'/patient/<cid:[0-9]+>/illness/<mid:[0-9]+><:/?>','classes.patientIllness'))





