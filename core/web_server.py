
from site import abs_paths
from quart import Quart, abort, send_file, request, render_template
import os

app = Quart(__name__, static_folder=os.getcwd()+'/',template_folder=os.getcwd()+'/templates/')




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

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)
    url = abs_path.replace(BASE_DIR+'\\','/',99)
    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return await render_template('image.html',ss_location=f"/file?path={url}")
    
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

@app.route('/file')
async def s_file():
    print(request.args)
    
    args_ = request.args.get('path', None)
    print(args_)
    if args_ is not None:
        return await send_file(os.getcwd()+'/'+args_)
    

