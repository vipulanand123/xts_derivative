{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "82c1955c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import flask\n",
    "from flask import request, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "09c1ac87",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n",
      "127.0.0.1 - - [15/Jan/2024 18:33:30] \"GET / HTTP/1.1\" 404 -\n"
     ]
    }
   ],
   "source": [
    "app = flask.Flask(__name__)\n",
    "app.config['DEBUG'] == True\n",
    "\n",
    "books = [\n",
    "    {'id': 0,\n",
    "     'title': 'A Fire Upon the Deep',\n",
    "     'author': 'Vernor Vinge',\n",
    "     'first_sentence': 'The coldsleep itself was dreamless.',\n",
    "     'year_published': '1992'},\n",
    "    {'id': 1,\n",
    "     'title': 'The Ones Who Walk Away From Omelas',\n",
    "     'author': 'Ursula K. Le Guin',\n",
    "     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',\n",
    "     'published': '1973'},\n",
    "    {'id': 2,\n",
    "     'title': 'Dhalgren',\n",
    "     'author': 'Samuel R. Delany',\n",
    "     'first_sentence': 'to wound the autumnal city.',\n",
    "     'published': '1975'}\n",
    "]\n",
    "\n",
    "@app.route('/', methods = ['GET'])\n",
    "def home():\n",
    "    return \"<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>\"\n",
    "\n",
    "@app.route('/api/v1/resources/books/all', methods = ['GET'])\n",
    "def api_all():\n",
    "    return jsonify(books)\n",
    "\n",
    "app.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1a64f769",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
