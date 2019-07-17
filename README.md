# AmendmentBackUp
A Python class for file comparison and new file backup.

Author: Yu Sun at University of Sydney

Email: sunyu0410@gmail.com

Website: https://github.com/sunyu0410/AmendmentBackUp

## Motivations
When it comes to backing up a large amoumt of data, it is often preferable to only copy the modified and new files, rather than simply coping the whole directory. The `AmendmentBackUp` (`ABU`) class provides a simple interface to do that. No dependencies are required apart from the Python 3 standard library.

## The design
Say we have two folders, a source folder `dir1` which you have your most recent files and a reference folder `dir2` which holds some of your previous backup. What the `ABU` does is to compare all files in `dir1` with those in `dir2`, and copy the files to a third destination folder `dst`. 

## A quick example
```python
from AmendmentBackUp import *
createDemo()
abu = AmendmentBackUp(dir1=r"demo/dir1",
                      dir2=r"demo/dir2",
                      dst=r"demo/dst")
abu.compare()
abu.backup()
```

## Explanations
Say you have the `dir1` and `dir2` (along with a `dst` to copy the files to) with the following tree structures:

```
        dir1 (source, recently updated)
        |   file1.txt
        |   file2.txt (modified)
        |   file3.txt (new)
        |   
        +---subfolder1
        |       file4.txt
        |       
        +---subfolder2
        |       file5.txt
        |       file6.txt (modified)
        |       
        \---subfolder3 (new)
                anyfile.txt
                
        dir2 (reference, e.g. a previous backup)
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
                
        dst (destination)
        
```

In this case, we want to copy the modified and new file(s) in `dir1`:

```
file2.txt
file3.txt
subfolder2/file6.txt
```

and new folder(s):

```
subfolder3
```

You can initiate an `ABU` object by calling

```python
abu = AmendmentBackUp(dir1=r'path_to/dir1', 
                      dir2=r'path_to/dir2', 
                      dst=r'path_to/dst')
```

By the way, the `createDemo()` will create a demo folder with structures shown above. After initiation, call the following `ABU` methods to proceed:

* `abu.compare()`: Compare files by walking through all files and folders in `dir1` and check the existence of the corresponding counterparts in `dir2`.

    * If negative, it then adds the file or folder to the copy list;

    * If positive, it compares two corresponding files (from `dir1` and `dir2` respectively, shallow comparison using the time stamp and the file size);

        * If two files don't match, it will add the file to the copy list;
        
        * Otherwise, it will continue to the next one.
        
* `abu.backup()`: Copy the files and folders in the copy list.
    
    * Folders will be copied first. If the parent folder has been copied, any child folder will be skipped;
    
    * Files will copied next. If the file falls under any folder copied in the previous step, it will be skipped.

* The metadata of the backup process will be stored in a folder called `_abu` with a time stamp (year-month-day-hour-minute-second) in the `dst` folder. These include

```

    - abu_log.txt      Log file
    - abu_obj.pickle   ABU object of this backup task
    - dir1_tree.txt    Tree structure of dir1 (source)
    - dir2_tree.txt    Tree structure of dir2 (reference)
    - dst_tree.txt     Tree structure of dst (destination)

```

## Results
Here is the tree structure of `dst` after the backup:

```
        dst
        |   file2.txt
        |   file3.txt
        |
        +---subfolder2
        |       file6.txt
        |
        +---subfolder3
        |       anyfile.txt
        |
        \---_abu_20190717101307
                abu_log.txt
                abu_obj.pickle
                dir1_tree.txt
                dir2_tree.txt
                dst_tree.txt
```

If you want to add the files to the previous back `dir2`, you can simply set `dst` to `dir2`.

## Limitations
The `ABU` is best suited when the source folder `dir1` is a natural growth of the reference folder `dir2`. What *natural growth* means is that there should not be too much renaming or move of the subfolders from `dir2` to `dir1`. Otherwise, using a version control system is probably a better option since `ABU` won't track the history of any folder or file.

