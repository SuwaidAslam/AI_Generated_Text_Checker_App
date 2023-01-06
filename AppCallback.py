from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import logging
from Pages import home
import dash
import base64
import io
import docx2txt
import PyPDF2
import os



# -----------------------------------
home_page_path = '/'

def parse_contents(content, filename):
    
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if '.docx' in filename:
                text = docx2txt.process(io.BytesIO(decoded))
        if '.txt' in filename:
                text = decoded.decode()
        if '.pdf' in filename:
            reader = PyPDF2.PdfReader(io.BytesIO(decoded))
            # get the number of pages in pdf file
            num_of_pages = len(reader.pages)
            text = ''
            for n_page in range(num_of_pages):
                # extract the text of the page
                text = text + reader.pages[n_page].extract_text()
    except Exception as e:
        print(e)
        raise PreventUpdate

    return text


class AppCallback:
    def __init__(self, app):
        self.app = app
        logging.set_verbosity_error()
        absolute_path = os.path.dirname(__file__)
        relative_path = "./roberta-base-openai-detector/"
        full_path = os.path.join(absolute_path, relative_path)
        tokenizer = AutoTokenizer.from_pretrained(full_path, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(full_path, local_files_only=True)
        self.classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

        self.app.callback([
            Output("real_prog", "value"), 
            Output("real_prog", "label"),
            Output("fake_prog", "value"),
            Output("fake_prog", "label"),
            Output('loading', 'children'),
        ],
        Input('text', 'value')
        )(self.classifyText)
        
        # Main callback to decide which page to render
        self.app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
        )(self.display_page)

    
        app.callback(
                [Output('text', 'value')],
                [Input('upload_file', 'contents'),
                Input('upload_file', "filename")],
            )(self.import_data)

    def import_data(self, contents, filename):
        if contents:
            text = parse_contents(contents, filename)
            return [text]
        else:
            raise PreventUpdate

    def display_page(self, pathname):
        if pathname == home_page_path:
            return home.layout
        else:
            return dash.no_update
    
    def classifyText(self, text):
        if text != None and text != "":
            res = self.classifier(text, truncation=True, max_length=510)
            label = res[0]['label']
            score = res[0]['score']

            if label == 'Real':
                real_score = score*100
                fake_score = 100-real_score
                real_score_lable = f"{real_score:.0f}%"
                if int(fake_score) < 10:
                    fake_score_lable = ""
                else:
                    fake_score_lable =f"{fake_score:.0f}%"
            else:
                fake_score = score*100
                real_score = 100-fake_score
                fake_score_lable = f"{fake_score:.0f}%"
                if int(real_score) < 10:
                    real_score_lable = ""
                else:
                    real_score_lable =f"{real_score:.0f}%"


            return [real_score, real_score_lable, fake_score, fake_score_lable, '']
        else:
            return [50, "", 50, "", '']
