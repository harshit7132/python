############################################## New Code #########################################################
# import os
# import requests
# from flask import Flask, render_template, request, jsonify, send_file
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse, urljoin

# app = Flask(__name__)

# def text_to_pdf(text, output_filename):
#     c = canvas.Canvas(output_filename, pagesize=letter)
#     width, height = letter

#     # Set up the font and size
#     c.setFont("Helvetica", 12)

#     # Calculate the height of the text and draw it on the canvas
#     text_lines = text.split('\n')
#     y_offset = height - 50
#     for line in text_lines:
#         c.drawString(50, y_offset, line)
#         y_offset -= 20

#     c.save()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/generate-files', methods=['POST'])
# def generate_files():
#     url = request.form['url']
#     try:
#         # Fetch HTML content from the URL
#         response = requests.get(url)
#         if response.status_code == 200:
#             html_content = response.text
            
#             # Extract CSS and JavaScript links from HTML
#             soup = BeautifulSoup(html_content, 'html.parser')
#             css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
#             js_links = [script['src'] for script in soup.find_all('script', src=True)]

#             # Extract external JavaScript files
#             external_js_links = []
#             for script in soup.find_all('script', src=True):
#                 if 'http' in script['src']:  # Check if the src attribute contains 'http' (indicating an external link)
#                     external_js_links.append(script['src'])

#             # Write HTML, CSS, and JavaScript content to files
#             with open('index.html', 'w', encoding='utf-8') as f:
#                 f.write(html_content)
#             for css_link in css_links:
#                 resolved_css_link = urljoin(url, css_link)
#                 css_response = requests.get(resolved_css_link)
#                 if css_response.status_code == 200:
#                     with open(os.path.basename(resolved_css_link), 'w', encoding='utf-8') as f:
#                         f.write(css_response.text)
#             for js_link in js_links + external_js_links:
#                 resolved_js_link = urljoin(url, js_link)
#                 js_response = requests.get(resolved_js_link)
#                 if js_response.status_code == 200:
#                     with open(os.path.basename(resolved_js_link), 'w', encoding='utf-8') as f:
#                         f.write(js_response.text)

#             return jsonify({
#                 'message': 'Files generated successfully',
#                 'html_content': html_content,
#                 'css_links': css_links,
#                 'js_links': js_links
#             })
#         else:
#             return jsonify({'error': 'Failed to fetch URL'})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# @app.route('/download', methods=['POST'])
# def download():
#     data = request.json
#     files_to_download = data.get('files')
#     if not files_to_download:
#         return jsonify({'error': 'No files specified for download'})
    
#     # Generate PDF file containing selected files
#     pdf_filename = 'downloaded_files.pdf'
#     with open(pdf_filename, 'wb') as pdf_file:
#         # Write HTML content to PDF
#         pdf_file.write(data['html_content'].encode('utf-8'))
        
#         # Write CSS files to PDF
#         for css_link in data['css_links']:
#             with open(os.path.basename(css_link), 'rb') as css_file:
#                 pdf_file.write(css_file.read())
        
#         # Write JS files to PDF
#         for js_link in data['js_links']:
#             with open(os.path.basename(js_link), 'rb') as js_file:
#                 pdf_file.write(js_file.read())
    
#     if len(files_to_download) == 1:
#         file_to_send = files_to_download[0]
#         if file_to_send == 'html':
#             return send_file('index.html', as_attachment=True)
#         elif file_to_send == 'pdf':
#             return send_file(pdf_filename, as_attachment=True, mimetype='application/pdf')
#         elif file_to_send in ['css', 'js']:
#             return send_file(os.path.basename(file_to_send), as_attachment=True)
#     else:
#         return send_file(pdf_filename, as_attachment=True, mimetype='application/pdf')

# if __name__ == '__main__':
#     app.run(debug=True)





#############################new chat gpt code (above is working properly)

import os
import requests
from flask import Flask, render_template, request, jsonify, send_file
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

def text_to_pdf(text, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Set up the font and size
    c.setFont("Helvetica", 12)

    # Calculate the height of the text and draw it on the canvas
    text_lines = text.split('\n')
    y_offset = height - 50
    for line in text_lines:
        c.drawString(50, y_offset, line)
        y_offset -= 20

    c.save()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-files', methods=['POST'])
def generate_files():
    url = request.form['url']
    try:
        # Fetch HTML content from the URL
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            
            # Extract CSS and JavaScript links from HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
            js_links = [script['src'] for script in soup.find_all('script', src=True)]

            # Extract external JavaScript files
            external_js_links = []
            for script in soup.find_all('script', src=True):
                if 'http' in script['src']:  # Check if the src attribute contains 'http' (indicating an external link)
                    external_js_links.append(script['src'])

            # Write HTML, CSS, and JavaScript content to files
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            for css_link in css_links:
                resolved_css_link = urljoin(url, css_link)
                css_response = requests.get(resolved_css_link)
                if css_response.status_code == 200:
                    with open(os.path.basename(resolved_css_link), 'w', encoding='utf-8') as f:
                        f.write(css_response.text)
            for js_link in js_links + external_js_links:
                resolved_js_link = urljoin(url, js_link)
                js_response = requests.get(resolved_js_link)
                if js_response.status_code == 200:
                    with open(os.path.basename(resolved_js_link), 'w', encoding='utf-8') as f:
                        f.write(js_response.text)

            return jsonify({
                'message': 'Files generated successfully',
                'html_content': html_content,
                'css_links': css_links,
                'js_links': js_links
            })
        else:
            return jsonify({'error': 'Failed to fetch URL'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    files_to_download = data.get('files')
    if not files_to_download:
        return jsonify({'error': 'No files specified for download'})
    
    # Generate PDF file containing selected files
    pdf_filename = 'downloaded_files.pdf'
    with open(pdf_filename, 'wb') as pdf_file:
        # Write HTML content to PDF
        pdf_file.write(data['html_content'].encode('utf-8'))
        
        # Write CSS files to PDF
        for css_link in data['css_links']:
            with open(os.path.basename(css_link), 'rb') as css_file:
                pdf_file.write(css_file.read())
        
        # Write JS files to PDF
        for js_link in data['js_links']:
            with open(os.path.basename(js_link), 'rb') as js_file:
                pdf_file.write(js_file.read())

        # Iterate through folders to include their contents in the PDF
        folders_to_include = ['C:/Users/harsh/Documents/New Folder', 'C:/Users/harsh/Documents/New Folder/']
        for folder_path in folders_to_include:
            print(f"Processing folder: {folder_path}")
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"Including file: {file_path}")
                    with open(file_path, 'rb') as f:
                        pdf_file.write(f.read())

    return send_file(pdf_filename, as_attachment=True, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)


