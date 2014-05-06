#!/usr/bin/env python
from systemofrecord.server import app
app.run(host="0.0.0.0", port=8003, debug=True, processes=3)
