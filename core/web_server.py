from aiohttp import request
from flask import Flask, abort, send_file, request
import os
app = Flask(__name__)


@app.route('/<path:req_path>')
async def dir_listing(req_path):
    

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

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    
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

