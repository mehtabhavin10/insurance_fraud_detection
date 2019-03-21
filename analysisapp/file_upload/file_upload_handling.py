
def handle_upload_file(f):
    with open('uploaded.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)