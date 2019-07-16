import os
import shutil
from AmendmentBackUp.createFile import createFile

def createDemo():
    '''Create the folders / files for a demonstration.
    dir1
    |   file1.txt
    |   file2.txt (different)
    |   file3.txt (unique)
    |   
    +---subfolder1
    |       file4.txt
    |       
    +---subfolder2
    |       file5.txt
    |       file6.txt (different)
    |       
    \---subfolder3 (unique)
            anyfile.txt
            
    dir2
    |   file1.txt
    |   file2.txt
    |   file7.txt
    |   
    +---subfolder1
    |       file4.txt
    |       
    \---subfolder2
            file5.txt
            file6.txt

    All different / unique files and unique subfolders will be copied.
    '''
    choice = input('This will create a folder called demo. Proceed? [Y/N]: ')
    exist = os.path.exists('demo')
    if exist:
        print('Folder demo alreay exist. Task terminated.')
    elif choice.strip().lower() in ['y', 'yes']:
        folders_to_create = [r'demo/dir1',
                             r'demo/dir2',
                             r'demo/dst',
                             r'demo/dir1/subfolder1',
                             r'demo/dir1/subfolder2',
                             r'demo/dir1/subfolder3',
                             r'demo/dir2/subfolder1',
                             r'demo/dir2/subfolder2']
        files_to_create = [(r'demo/dir1/file1.txt', 'File 1'),
                           (r'demo/dir1/file2.txt', 'File 2'),
                           (r'demo/dir1/file3.txt', 'File 3'),
                           (r'demo/dir1/subfolder1/file4.txt', 'File 4'),
                           (r'demo/dir1/subfolder2/file5.txt', 'File 5'),
                           (r'demo/dir1/subfolder2/file6.txt', 'File 6'),
                           (r'demo/dir1/subfolder3/anyfile.txt', 'Any file'),
                           (r'demo/dir2/subfolder2/file6.txt', 'Another file 6'),
                           (r'demo/dir2/file2.txt', 'Another file 2'),
                           (r'demo/dir2/file7.txt', 'File 7')]
        files_to_move = [(r'demo/dir1/subfolder1/file4.txt',
                          r'demo/dir2/subfolder1/file4.txt'),
                         (r'demo/dir1/subfolder2/file5.txt',
                          r'demo/dir2/subfolder2/file5.txt'),
                         (r'demo/dir1/file1.txt',
                          r'demo/dir2/file1.txt')]

        [os.makedirs(i) for i in folders_to_create]
        [createFile(i, j) for (i, j) in files_to_create]
        [shutil.copy(i, j) for (i, j) in files_to_move]
        print('Demo created.')