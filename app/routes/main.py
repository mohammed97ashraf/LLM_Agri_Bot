"""Main route blueprint.

Serves the main index page, SEO files, and static assets.
"""

import logging
import os
from datetime import datetime, timezone

from flask import (
    Blueprint, Response, current_app, render_template, send_from_directory
)

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

SITE_URL = os.getenv("SITE_URL", "https://llm-agri-bot.onrender.com")


@main_bp.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')


@main_bp.route('/favicon.ico')
def favicon():
    """Serve the favicon."""
    return send_from_directory(
        'static/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@main_bp.route('/robots.txt')
def robots_txt():
    """Serve robots.txt for search engine crawlers."""
    content = """User-agent: *
Allow: /
Disallow: /chat
Disallow: /chat/clear
Disallow: /health
Disallow: /static/audio/
Disallow: /uploads/

User-agent: GPTBot
Allow: /
Allow: /llms.txt

User-agent: Google-Extended
Allow: /
Allow: /llms.txt

User-agent: CCBot
Allow: /
Allow: /llms.txt

User-agent: anthropic-ai
Allow: /
Allow: /llms.txt

User-agent: Bytespider
Allow: /
Allow: /llms.txt

Sitemap: {}/sitemap.xml
""".format(SITE_URL)
    return Response(content, mimetype='text/plain', headers={
        'Cache-Control': 'public, max-age=86400'
    })


@main_bp.route('/sitemap.xml')
def sitemap_xml():
    """Serve sitemap.xml for search engines."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site}/</loc>
    <lastmod>{date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>""".format(site=SITE_URL, date=now)
    return Response(content, mimetype='application/xml', headers={
        'Cache-Control': 'public, max-age=86400'
    })


def _get_llms_txt_content():
    """Read llms.txt from project root."""
    try:
        project_root = os.path.dirname(current_app.root_path)
        llms_path = os.path.join(project_root, 'llms.txt')
        with open(llms_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "# llms.txt not found\n"


@main_bp.route('/llms.txt')
def llms_txt():
    """Serve llms.txt for AI crawlers."""
    content = _get_llms_txt_content()
    return Response(content, mimetype='text/plain', headers={
        'Cache-Control': 'public, max-age=86400'
    })


@main_bp.route('/.well-known/llms.txt')
def llms_txt_well_known():
    """Serve llms.txt from /.well-known/ path for AI crawlers."""
    content = _get_llms_txt_content()
    return Response(content, mimetype='text/plain', headers={
        'Cache-Control': 'public, max-age=86400'
    })