
from site import abs_paths
from flask import url_for
from quart import Quart, abort, send_file, request, render_template, redirect
import os
from os.path import exists
from requests import Session
from io import BytesIO
import requests
from urllib.parse import unquote
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Webserver(Quart):
    def __init__(self, import_name: str, bot, static_url_path: Optional[str] = None, static_folder: Optional[str] = "static", static_host: Optional[str] = None, host_matching: bool = False, subdomain_matching: bool = False, template_folder: Optional[str] = "templates", instance_path: Optional[str] = None, instance_relative_config: bool = False, root_path: Optional[str] = None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.static_folder = os.getcwd()+'/'
        self.template_folder = os.getcwd()+'/templates/'
        self.bot = bot

def create_custom_server(bot):
    app = Webserver(__name__, bot)
    flow : InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                        os.getcwd()+'/credentials.json', SCOPES,
                        redirect_uri='http://rekobeep.xyz/wishes')
    
    

    @app.route('/<path:req_path>')
    async def dir_listing(req_path):
        
        print(app.static_folder)
        BASE_DIR = os.getcwd()
        args_ = request.args
        filters = []

        if len(args_) != 0:

            if args_.get('filter', '') != '':

                filters = args_.get('filter').split(',')
            
            else:

                filters = ['files', 'folders']
        
        else:

            filters = ['files', 'folders']

        #add filters to dict

        data = {x : [] for x in filters}
        if req_path.split('/')[0] == 'pixiv':
            LINK = f"https://pixiv.net/ajax/illust/{req_path.split('/')[1]}"
            if not exists(BASE_DIR+f"/assets/pixiv/{req_path.split('/')[1]}.jpg"):   


                session = Session()
                headers = {
                    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                    "referer": "https://pixiv.net/"
                }

                print('provided link', LINK)


                links = session.get(LINK, 
                            headers=headers)
                data = links.json()
                image = data['body']['urls']['original']
                
                
                print('original image link', image)
                with session.get(image, headers=headers, cookies=links.cookies) as u:   

                    with open(BASE_DIR+f"/assets/pixiv/{req_path.split('/')[1]}.jpg", 'wb') as f:
                        f.write(u.content)

            return await send_file(BASE_DIR+f"/assets/pixiv/{req_path.split('/')[1]}.jpg")
        
        if req_path.split('/')[0] == 'paimonmoe_link':
            
            creds = None
           
            url, state = flow.authorization_url()

            app.config['state'] = state

            return redirect(url)

        if req_path.split('/')[0] == 'wishes':
            return await render_template('wish.html')
           
      

            

        if req_path.split('/')[0] == 'danbooru':
            headers = {
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                "referer": "https://danbooru.donmai.us/"
            }
            file = req_path.split('/')[1]
            session = Session()
            gen_link = f"https://cdn.donmai.us/original/"
            gen_link += file[:2]+"/"
            gen_link += file[2:4]+"/"
            gen_link += file
            if not exists(BASE_DIR+f"/assets/danbooru/"+file):
                with session.get(gen_link, headers=headers) as r:            
                    if r.status_code == 200:
                        with open(BASE_DIR+f"/assets/danbooru/"+file, 'wb') as f:
                            f.write(r.content)
            if exists(BASE_DIR+f"/assets/danbooru/"+file):
                return await send_file(BASE_DIR+f"/assets/danbooru/{req_path.split('/')[1]}")
            else:
                return await send_file(BASE_DIR+f"/assets/misc/nothing.png")



        # Joining the base and the requested path
        abs_path = os.path.join(BASE_DIR, req_path)

        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)
        url = abs_path.replace(BASE_DIR+'\\','/',99)
        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            if '?' in abs_path:
                abs_path = abs_path[:abs_path.find('?')]
            return await send_file(abs_path, cache_timeout=0)
        
        # Show directory contents
        listed = os.listdir(abs_path)
        for i in listed:
            if os.path.isfile(os.path.join(abs_path, i)):
                if 'files' in filters:
                    data['files'].append(i)
            else:
                if 'folders' in filters:
                    data['folders'].append(i)

        return data
    return app

SCOPES = ['https://www.googleapis.com/auth/drive.appdata']
def wishes_data():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow : InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                os.getcwd()+'/credentials.json', SCOPES)
            return flow.authorization_url()[0]
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        print(creds)
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, spaces='appDataFolder', q="name = 'save.json'").execute()
        items = results.get('files', [])
        return items
      

    return {'data': []}