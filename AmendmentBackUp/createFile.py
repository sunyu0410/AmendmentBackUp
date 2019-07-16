def createFile(filename, content):
    '''Create a file using the given filename and contents)'''
    with open(filename, 'w') as f:
        f.write(content)