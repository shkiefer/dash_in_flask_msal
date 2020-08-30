import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.exceptions import PreventUpdate
from dash_table.Format import Format, Scheme, Sign, Symbol

from app import db
from app.dashapps.models import User_Image

from base64 import b64encode, b64decode, decodebytes
from io import BytesIO
from PIL import Image
import re
from werkzeug.utils import secure_filename
import uuid
import os
from pathlib import Path

APP_ID = 'user_image_upload'
URL_BASE = '/dash/user_image_upload/'
MIN_HEIGHT = 2000

def add_dash(server):

    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
    ]

    app = dash.Dash(
        server=server,
        url_base_pathname=URL_BASE,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )

    app.layout = dbc.Container([
        html.H1('Add / Modify User Image Database'),
        html.H3('Select Row to Edit Existing'),
        dbc.Button('Refresh List', id=f'{APP_ID}_database_refresh_button'),
        dash_table.DataTable(
            id=f'{APP_ID}_database_dt',
            columns=[
                {'name': c, "id": c, 'type': 'text'} for c in ['name', 'creator', 'id', 'img_web_url']
            ],
            data=[{}],
            editable=False,
            row_deletable=False,
            row_selectable='single',
            page_action='none',
            style_table={'maxHeight': '400px', 'overflowY': 'auto'},
            css=[{'selector': '.row', 'rule': 'margin: 0'}]
        ),
        html.Br(),
        html.H3("Upload to Add New Image"),
        dcc.Upload(
            id=f'{APP_ID}_upload',
            children=[
                dbc.Button('Drag and Drop or click to browse')
            ]
        ),
        dbc.Row([
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label('Image Name'),
                    dbc.Input(id=f'{APP_ID}_name_input'),
                ]),
            ),
            dbc.Col(
                dbc.FormGroup([
                    dbc.Label('Creator Name'),
                    dbc.Input(id=f'{APP_ID}_creator_input'),
                ]),
            )
        ]),
        dbc.FormGroup([
            dbc.Label('Web URL'),
            dbc.Input(id=f'{APP_ID}_web_url_input'),
        ]),
        dbc.Card([
            dbc.CardImg(id=f'{APP_ID}_card_Img', src='', top=True, style={'width': '18rem'}),
            dbc.CardBody([
                html.H4('', id=f'{APP_ID}_card_name_H4'),
                html.P('', id=f'{APP_ID}_card_creator_P'),
                dbc.ButtonGroup([
                    dbc.Button('Enlarge', id=f'{APP_ID}_card_enlarge_button', color='secondary'),
                    dbc.Button('Submit to Database', id=f'{APP_ID}_card_submit_button', color='primary', disabled=True),
                ]),
                dbc.CardFooter(
                    dbc.CardLink('Web Link', id=f'{APP_ID}_card_web_link', href='', external_link=True, target="_blank")
                )

            ])
        ],
            style={'max-width': '18rem'}
        ),
        html.Div(id=f'{APP_ID}_upload_feedback_div'),

    ])

    @app.callback(
        Output(f'{APP_ID}_card_Img', 'src'),
        [
            Input(f'{APP_ID}_upload', 'contents'),
            Input(f'{APP_ID}_database_dt', "derived_virtual_selected_rows"),
        ],
        [State(f'{APP_ID}_database_dt', "data")]
    )
    def user_image_upload_img(contents, derived_virtual_selected_rows, data):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate

        if ctx.triggered[0]['prop_id'].split('.')[0] == f'{APP_ID}_upload' and contents is not None:
            im_file2 = make_thumb(contents)
            im_b64 = b64encode(im_file2.read()).decode('utf-8')
            return f'data:image/jpg;base64, {im_b64}'

        elif ctx.triggered[0]['prop_id'].split('.')[0] == f'{APP_ID}_database_dt':
            if derived_virtual_selected_rows is not None and len(derived_virtual_selected_rows) > 0:
                ui_id = data[derived_virtual_selected_rows[0]]['id']
                uimg = User_Image.query.filter_by(id=ui_id).first()
                return f"data:image/jpg;base64, {b64encode(uimg.thumb).decode('utf-8')}"
        else:
            return None


    @app.callback(
        Output(f'{APP_ID}_card_name_H4', 'children'),
        [
            Input(f'{APP_ID}_name_input', 'value')
        ]
    )
    def user_image_upload_name(name):
        return name


    @app.callback(
        Output(f'{APP_ID}_card_creator_P', 'children'),
        [
            Input(f'{APP_ID}_creator_input', 'value')
        ]
    )
    def user_image_upload_creator(creator):
        return creator


    @app.callback(
        Output(f'{APP_ID}_card_web_link', 'href'),
        [
            Input(f'{APP_ID}_web_url_input', 'value')
        ]
    )
    def user_image_upload_web_url(web_link):
        return web_link


    @app.callback(
        Output(f'{APP_ID}_card_submit_button', 'disabled'),
        [
            Input(f'{APP_ID}_name_input', 'value'),
            Input(f'{APP_ID}_creator_input', 'value'),
            Input(f'{APP_ID}_web_url_input', 'value'),
            Input(f'{APP_ID}_upload', 'contents'),
            Input(f'{APP_ID}_database_dt', "derived_virtual_selected_rows"),
            Input(f'{APP_ID}_card_Img', 'src')
        ],
    )
    def user_image_upload_submit_enable(name, creator, web_url, contents, derived_virtual_selected_rows, img_src):
        if any([v is None or v == '' for v in [name, creator, web_url, img_src]]):
            return True
        else:
            return False


    @app.callback(
        Output(f'{APP_ID}_upload_feedback_div', 'children'),
        [
            Input(f'{APP_ID}_card_submit_button', 'n_clicks'),
            Input(f'{APP_ID}_name_input', 'value'),
            Input(f'{APP_ID}_creator_input', 'value'),
            Input(f'{APP_ID}_web_url_input', 'value'),
            Input(f'{APP_ID}_card_Img', 'src')
        ],
        [
            State(f'{APP_ID}_upload', 'contents'),
            State(f'{APP_ID}_upload', 'filename'),
            State(f'{APP_ID}_database_dt', "derived_virtual_selected_rows"),
            State(f'{APP_ID}_database_dt', "data")
        ]
    )
    def user_image_upload_save(n_clicks, name, creator, web_url, img_src, contents, filename, derived_virtual_selected_rows, data):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate

        if ctx.triggered[0]['prop_id'].split('.')[0] in [f'{APP_ID}_name_input', f'{APP_ID}_creator_input', f'{APP_ID}_web_url_input', f'{APP_ID}_card_Img']:
            if any([v is None or v == '' for v in [name, creator, web_url, img_src]]):
                return dbc.Alert([html.H3('Incomplete'), html.P('fill all forms and load image before submitting')], color='danger')
            else:
                return dbc.Alert([html.H3('Ready to Submit'), html.P('going once...')], color='primary')
        else:
            im_filename = ''
            try:
                # if selected remove existing before submitting
                if len(derived_virtual_selected_rows) > 0:
                    ui_id = data[derived_virtual_selected_rows[0]]['id']
                    uimg = User_Image.query.filter_by(id=ui_id).first()
                    uimg.name = name
                    uimg.creator = creator
                    uimg.img_web_url = web_url
                    db.session.commit()
                    db.session.close()
                else:
                    img_file = make_img_file(contents)
                    im_filename = uuid.uuid4().hex + '.' + filename.split('.')[-1]
                    with open(os.path.join(server.config['IMG_FILE_DIR'], secure_filename(im_filename)), 'wb') as f:
                        f.write(img_file.getbuffer())

                    thumb_file = make_thumb(contents)
                    user_img = User_Image(
                        name=name,
                        creator=creator,
                        img_web_url=web_url,
                        img_dir_url=secure_filename(im_filename),
                        thumb=thumb_file.read()
                    )
                    db.session.add(user_img)
                    db.session.commit()
                    db.session.close()
            except Exception as e:
                pf = Path(server.config['IMG_FILE_DIR']) / secure_filename(im_filename)
                if pf.is_file():
                    pf.unlink()
                return dbc.Alert([html.H3('Add Failed!'), str(e)], color='danger')

            return dbc.Alert([html.H3('File Added to Database!'), html.P('claps and cheers all around!')], color='success')


    @app.callback(
        [
            Output(f'{APP_ID}_name_input', 'value'),
            Output(f'{APP_ID}_creator_input', 'value'),
            Output(f'{APP_ID}_web_url_input', 'value'),
        ],
        [Input(f'{APP_ID}_database_dt', "derived_virtual_selected_rows")],
        [State(f'{APP_ID}_database_dt', "data")]
    )
    def user_image_edit_select(derived_virtual_selected_rows, data):
        if derived_virtual_selected_rows is None or len(derived_virtual_selected_rows) == 0:
            raise PreventUpdate
        name = data[derived_virtual_selected_rows[0]]['name']
        creator = data[derived_virtual_selected_rows[0]]['creator']
        img_web_url = data[derived_virtual_selected_rows[0]]['img_web_url']
        return [name, creator, img_web_url]


    @app.callback(
        [
            Output(f'{APP_ID}_database_dt', 'data'),
            Output(f'{APP_ID}_database_dt', 'selected_rows'),
         ],
        [
            Input(f'{APP_ID}_database_refresh_button', 'n_clicks')
        ]
    )
    def user_image_edit_refresh(n_clicks):
        user_imgs = db.session.query(User_Image).all()
        data = []
        for ui in user_imgs:
            data.append({'name': ui.name, 'creator': ui.creator, 'id': ui.id, 'img_web_url': ui.img_web_url})
        return data, []

    return server


def make_img_file(contents):
    im_data_tag = contents.split(',')[1]
    im_data = re.sub('^data:image/.+;base64,', '', im_data_tag)
    im_file = BytesIO(b64decode(im_data))
    return im_file


def make_thumb(contents):

    im_file = make_img_file(contents)
    img = Image.open(im_file)
    width, height = img.size
    new_w = 200
    new_h = int(height / width * new_w)
    img2 = img.resize((new_w, new_h))

    im_file2 = BytesIO()
    img2.save(im_file2, format="JPEG")
    im_file2.seek(0)
    return im_file2


if __name__ == '__main__':
    from flask import Flask, render_template
    from flask_bootstrap import Bootstrap
    from config import Config

    bootstrap = Bootstrap()
    Config.TESTING = True
    app = Flask(__name__)
    # configuration
    app.config.from_object(Config)

    # register extensions
    db.init_app(app)
    bootstrap.init_app(app)

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    # inject Dash
    app = add_dash(app)

    @app.route(URL_BASE+'debug')
    def dash_app():
        return render_template('dashapps/dash_app_debug.html', dash_url=URL_BASE,
                               min_height=MIN_HEIGHT)

    app_port = 5002
    print(f'http://localhost:{app_port}{URL_BASE}debug')
    app.run(debug=True, port=app_port)
