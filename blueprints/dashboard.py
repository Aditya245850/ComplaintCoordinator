import os
import time
from datetime import datetime

from quart import Blueprint, redirect, render_template, send_file, session, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from helper.download import downloadContent
from helper.graph import category_graph

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/index', methods=['GET', 'POST'])
async def index():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session.get('username')
    graph_html = await category_graph(username)
    return await render_template('index.html', graph=graph_html)


@dashboard_bp.route('/download', methods=['POST'])
async def download():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session.get('username')
    complaints = await downloadContent(username)

    timestamp = int(time.time())
    pdf_file_path = f"complaints_report_{username}_{timestamp}.pdf"

    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=16,
        leading=20,
        alignment=1,
        spaceAfter=20,
    )

    current_date = datetime.now().strftime("%Y-%m-%d")
    title = Paragraph(f"Complaints Report - {current_date}", title_style)

    pdf_content = [title, Spacer(1, 12)]
    for complaint in complaints:
        pdf_content.append(Paragraph(complaint, styles["BodyText"]))
        pdf_content.append(Spacer(1, 12))

    doc.build(pdf_content)

    response = await send_file(pdf_file_path, as_attachment=True)
    os.remove(pdf_file_path)
    return response
