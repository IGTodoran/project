import logging

import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort


NB_DB_CONNECTIONS = 0
app = Flask(__name__)


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post


def get_post_title(post_id):
    """Function to get the post title for a given post_id"""
    connection = get_db_connection()
    post = connection.execute('SELECT title FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post[0]


def get_number_posts():
    """Function to get the number of posts."""
    connection = get_db_connection()
    nb_posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()
    return nb_posts[0]


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    global NB_DB_CONNECTIONS
    post = get_post(post_id)
    if post is None:
        app.logger.info("Page does not exist, returned 404.")
        return render_template('404.html'), 404
    else:
        NB_DB_CONNECTIONS += 1
        post_title = get_post_title(post_id=post_id)
        app.logger.info(f"Article {post_title} retrieved!.")
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("Page About Us is accessed.")
    return render_template('about.html')


# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            app.logger.info("Article not created because the title is missing.")
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f"Created a new article having as title: {title}.")
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def status():
    """Endpoint returning the status of the app."""
    response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info("Status successfully returned.")
    return response


@app.route('/metrics')
def metrics():
    """Endpoint returning some useful metrics of the app."""
    nb_posts = get_number_posts()
    response = app.response_class(
            response=json.dumps(
                {"status": "success",  
                 "data": {
                    "db_connection_count": NB_DB_CONNECTIONS,
                    "post_count": nb_posts}
                    }
                ),
            status=200,
            mimetype='application/json'
    )
    app.logger.info("Metrics successfully returned.")
    return response


# start the application on port 3111
if __name__ == "__main__":

    # stream logs to app.log file
    # logging.basicConfig(filename='app.log', level=logging.INFO)

    app.run(host='0.0.0.0', debug=True, port='3111')
