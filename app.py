import sqlite3
import os
from flask import Flask, request, render_template, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.validation import (
    validate_image,
    validate_short_link,
    validate_text_input,
    validate_url,
)
from utils.init_db import init_db


app = Flask(__name__)

# Configuration
DATABASE = "links.db"
MAX_SHORT_LINK_LENGTH = 20
MIN_SHORT_LINK_LENGTH = 3

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

if not os.path.exists(DATABASE):
    init_db(DATABASE)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
@limiter.limit("5 per minute")
def generate():
    """Generate a short link with customizable preview."""
    data = request.json

    # Required fields
    short_link = data.get("short_link")
    original_url = data.get("original_url")
    image_url = data.get("image_url")

    # Optional OG tag customization
    og_title = data.get("og_title", "Custom Link")
    og_description = data.get("og_description", "Click to view")

    # Validate required inputs
    if not short_link:
        return jsonify({"error": "Custom short link is required."}), 400

    if not validate_short_link(
        short_link, MAX_SHORT_LINK_LENGTH, MIN_SHORT_LINK_LENGTH
    ):
        return jsonify(
            {
                "error": f"Invalid short link. Must be {MIN_SHORT_LINK_LENGTH}-{MAX_SHORT_LINK_LENGTH} alphanumeric characters or hyphens."
            }
        ), 400

    if not validate_url(original_url) or not validate_url(image_url):
        return jsonify({"error": "Invalid URL format. Use full HTTP/HTTPS URLs."}), 400
    
    # Validate image
    image_valid, image_error = validate_image(image_url)
    if not image_valid:
        return render_template(
            "interface.html",
            error=f"Invalid image: {image_error}",
        )

    # Validate optional inputs
    if og_title and not validate_text_input(og_title):
        return jsonify(
            {
                "error": "Invalid OG title. Use alphanumeric characters and basic punctuation."
            }
        ), 400

    if og_description and not validate_text_input(og_description):
        return jsonify(
            {
                "error": "Invalid OG description. Use alphanumeric characters and basic punctuation."
            }
        ), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            # Check if short link already exists
            c.execute("SELECT 1 FROM links WHERE short_link=?", (short_link,))
            if c.fetchone():
                return jsonify(
                    {"error": "Short link already exists. Choose another."}
                ), 409

            # Insert link with all details
            c.execute(
                """
                INSERT INTO links 
                (short_link, original_url, image_url, og_title, og_description) 
                VALUES (?, ?, ?, ?, ?)
            """,
                (short_link, original_url, image_url, og_title, og_description),
            )
            conn.commit()

        return jsonify(
            {"message": f"Short link generated: https://shrlnk.icu/{short_link}"}
        )
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/<short_link>")
def resolve(short_link):
    """Resolve short link with custom preview."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        """
        SELECT original_url, image_url, og_title, og_description 
        FROM links 
        WHERE short_link=?
    """,
        (short_link,),
    )
    result = c.fetchone()
    conn.close()

    if result:
        original_url, image_url, og_title, og_description = result
        return render_template(
            "preview.html",
            original_url=original_url,
            image_url=image_url,
            og_title=og_title,
            og_description=og_description,
        )
    else:
        return "Link not found", 404


@app.route("/interface", methods=["GET", "POST"])
def interface():
    if request.method == "POST":
        # Required fields
        short_link = request.form.get("short_link")
        original_url = request.form.get("original_url")
        image_url = request.form.get("image_url")

        # Optional OG tag fields
        og_title = request.form.get("og_title", "")
        og_description = request.form.get("og_description", "")

        # Validate required fields
        if not short_link or not original_url or not image_url:
            return render_template(
                "interface.html",
                error="Short link, original URL, and image URL are required!",
            )

        try:
            with sqlite3.connect(DATABASE) as conn:
                c = conn.cursor()

                # Check if short link already exists
                c.execute("SELECT 1 FROM links WHERE short_link=?", (short_link,))
                if c.fetchone():
                    return render_template(
                        "interface.html",
                        error="Short link already exists. Choose another.",
                    )

                # Insert link with all details
                c.execute(
                    """
                    INSERT INTO links 
                    (short_link, original_url, image_url, og_title, og_description) 
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (short_link, original_url, image_url, og_title, og_description),
                )
                conn.commit()

            return render_template(
                "interface.html",
                success=f"Short link generated: https://shrlnk.icu/{short_link}",
            )
        except Exception as e:
            return render_template("interface.html", error=str(e))

    return render_template("interface.html")


if __name__ == "__main__":
    app.run(debug=True)
