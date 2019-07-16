AmendmentBackUp
===============

A Python class for file comparison and new file backup.

Author: Yu Sun at University of Sydney

Email: sunyu0410@gmail.com

Website: https://github.com/sunyu0410/AmendmentBackUp

Motivation
----------

When it comes to backing up a large amout of data, it is often
preferable to only copy the modified and unique files, rather than
simply coping the whole directory. The ``AmendmentBackUp`` (``ABU``)
class provides a simple interface to do that. No dependencies are
required apart from the Python 3 standard library.

Design
------

Say we have two folders, a source folder ``dir1`` which you have your
most recent files and a reference folder ``dir2`` which holds some of
your previous backup. What the ``ABU`` does is to compare all files in
``dir1`` with those in ``dir2``, and copy the files to a third
destination folder ``dst``. If you simply want to add the files to the
original back, you can set ``dst`` to ``dir2``.

A quick example
---------------

::

    createDemo()
    abu = AmendmentBackUp(dir1=r"demo/dir1",
                          dir2=r"demo/dir2",
                          dst=r"demo/dst")
    abu.compare()
    abu.backup()

Explanation
-----------

Say you have the ``dir1`` and ``dir2`` with the following tree
structures:

::

            dir1 (source, recently updated)
            |   file1.txt
            |   file2.txt (modified)
            |   file3.txt (unique)
            |   
            +---subfolder1
            |       file4.txt
            |       
            +---subfolder2
            |       file5.txt
            |       file6.txt (modified)
            |       
            \---subfolder3 (unique)
                    anyfile.txt
                    
            dir2 (reference, previous backup)
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

You can inititate an ``ABU`` object by calling

::

    abu = AmendmentBackUp(r'demo/dir1', r'demo/dir2', r'demo/dst')

By the way, the ``createDemo()`` will create the demo file structures
shown above.

After initiation, what ``ABU`` will do:

-  Comparison (``abu.compare()``) by walking through all files and
   folders in ``dir1`` and check the existence of the corresponding
   counter in ``dir2``.

   -  If no, then add to the copy list. For folders, this will be the
      entire folder.

   -  If yes, compare the two folders (shallow comparison using the time
      stamp and the file size) for files;

      -  If the comparison returns False, add to the copy list;

      -  Otherwise, continue to the next one.

-  Copy (``abu.backup()``) the files and folders in the copy list.

   -  Folders will be copied first. If the parent folder has been
      copied, any child folder will be skipped;

   -  Files will copied next. If the file falls under any folder from
      the previous step, it will be skipped.

-  The meta data of the backup process will be store in a folder called
   ``_abu`` with a time stamp (year-month-day-hour-minute-second) in the
   ``dst`` folder.

Limitation
----------

The ``ABU`` is best suited when the source folder ``dir1`` is a
natural growth of the reference folder ``dir2``. What *natural
growth* means is that there should not be too much renaming or move of the
subfolders from ``dir2`` to ``dir1``. If that's the case, using a
version control system is probably a better option.
