import os
import filecmp
import shutil
import time
import pickle
from AmendmentBackUp.createDemo import createDemo

class AmendmentBackUp(object):

    def __init__(self, dir1, dir2, dst):
        '''__init__() function of class AmendmentBackUp'''
        self.dir1 = dir1
        self.dir2 = dir2
        self.dst = dst
        self.fileToCopy = []
        self.folderToCopy = []
        self.folderCopied = []
        self.folderCopyFlag = False
        self.walk = os.walk(self.dir1)
        self.log = []
        self.abu_folder = os.path.join(self.dst,
                          '_abu_'+time.strftime('%Y%m%d%H%M%S'))

    def log_msg(self, msg, verbose=False):
        self.log.append(msg)
        if verbose:
            print(msg)
            print()
        
    def compare(self):
        '''Recursively compare the two directories: dir1 and dir2'''
        self.log_msg(' Comparison started '.center(80, '#'), True)
        
        for (path, folders, files) in self.walk:
            # Get the relative path to construct the dir2 counterpart
            path_rel = os.path.relpath(path, start=self.dir1)
            self.log_msg(path_rel, True)
            # Compare files
            filelist1 = [os.path.join(path, i) for i in files]
            filelist2 = [os.path.join(self.dir2, path_rel, i) for i in files]
            for i in range(len(files)):
                if not os.path.exists(filelist2[i]):
                    item = (self.dir1, path_rel, files[i]), 'Not exists'
                    self.fileToCopy.append(item)
                else:
                    same = filecmp.cmp(filelist1[i], filelist2[i])
                    if not same:
                        item = (self.dir1, path_rel, files[i]), 'Not identical'
                        self.fileToCopy.append(item)

            # Compare folders
            folderlist2 = [os.path.join(self.dir2, path_rel, i) for i in folders]
            for i in range(len(folders)):
                if not os.path.exists(folderlist2[i]):
                    item = (self.dir1, path_rel, folders[i]), 'Not exists'
                    self.folderToCopy.append(item)
        self.log_msg(' Comparison finished '.center(80, '#'), True)

    def __isSubdir(self, subDir, parDir):
        '''Determine whether subDir is a (nested) subdirectory of parDir'''
        # Using realpath will make sure no trailing '\\'
        subDir_split = os.path.realpath(subDir).split(os.path.sep)
        parDir_split = os.path.realpath(parDir).split(os.path.sep)
        cmp = [parDir_split == subDir_split[:i] for i in range(len(subDir_split)+1)]
        if sum(cmp)==1:
            return True
        else:
            return False
    
    def __containSubdir(self, subDir, dir_list):
        '''Determine whether subDir is a (nested) subdirectory of a list of directories (dir_list)'''
        dir_list = [os.path.realpath(i) for i in dir_list]
        isSubdir = any([self.__isSubdir(subDir, i) for i in dir_list])
        return isSubdir
    
    def __copyFolders(self):
        '''Copy the relevant folders from dir1 to dst'''
        self.log_msg(' Copy folders stated'.center(80, '#'), True)
        for (d, path_rel, folder), label in self.folderToCopy:
            oriFolder = os.path.join(d, path_rel, folder)
            dstFolder = os.path.join(self.dst, path_rel, folder)
            oriFolder = os.path.realpath(oriFolder)
            dstFolder = os.path.realpath(dstFolder)

            # Check if the parent folder has been copied
            # If so, don't need to copy again
            included = self.__containSubdir(dstFolder, self.folderCopied)
            if not included:
                shutil.copytree(oriFolder, dstFolder)
                self.folderCopied.append(dstFolder)
                self.log_msg(time.strftime('%d/%m/%Y %H:%M:%S') +
                             ' [%s] copied to [%s]' % (oriFolder, dstFolder))
        self.log_msg(' Copy folders finished '.center(80, '#'), True)
        self.folderCopyFlag = True

    def __copyFiles(self):
        '''Copy the relevant files from dir1 to dst. Folders must be copied first.'''
        assert self.folderCopyFlag
        self.log_msg(' Copy files stared'.center(80, '#'), True)
        for (d, path_rel, f), label in self.fileToCopy:
            oriPath = os.path.join(d, path_rel, f)
            dstPath = os.path.join(self.dst, path_rel, f)
            oriPath = os.path.realpath(oriPath)
            dstPath = os.path.realpath(dstPath)

            folder, filename = os.path.split(dstPath)

            if not self.__containSubdir(folder, self.folderCopied):
                if not os.path.exists(folder):
                    os.makedirs(folder)
                shutil.copy(oriPath, dstPath)
                self.log_msg(time.strftime('%d/%m/%Y %H:%M:%S') +
                             '[%s] copied to [%s]' % (oriPath, dstPath))
        self.log_msg(' Copy folders finished '.center(80, '#'), True)

    def saveTree(self, path, filename):
        '''Save the tree stucture of the directory indicated by path in the _abu folder.'''
        tree_path = os.path.join(self.abu_folder, filename)
        os.system('tree /F /A "%s" > "%s"' % (path, tree_path))

    def backup(self):
        '''Copy the relevant folders and files from dir1 to dst.'''
        self.__copyFolders()
        self.__copyFiles()
        
        os.makedirs(self.abu_folder)

        # Save log
        log_path = os.path.join(self.abu_folder, 'abu_log.txt')
        with open(log_path, 'w') as f:
            contents = [i+'\n' for i in self.log]
            f.writelines(contents)

        msg = '''
        ############################################################
        ABU ran successfully. 
        Meta data saved to _abu_{timestamp}, including:
           - abu_log.txt      Log file
           - abu_obj.pickle   ABU object of this backup
           - dir1_tree.txt    Tree structure of dir1 (source)
           - dir2_tree.txt    Tree structure of dir2 (reference)
           - dst_tree.txt     Tree structure of dst (files copied)
        ############################################################
        '''
        self.log_msg(msg, True)

        # Save tree
        self.saveTree(self.dir1, 'dir1_tree.txt')
        self.saveTree(self.dir2, 'dir2_tree.txt')
        self.saveTree(self.dst, 'dst_tree.txt')

        # Save the ABU object
        abu_path = os.path.join(self.abu_folder, 'abu_obj.pickle')
        with open(abu_path, 'wb') as f:
            # Pickle can't store generators, so change self.walk to None,
            #  since it's already exhausted
            self.walk = None 
            pickle.dump(self, f)

if __name__ == '__main__':
    createDemo()
    abu = AmendmentBackUp(dir1=r"demo/dir1",
                          dir2=r"demo/dir2",
                          dst=r"demo/dst")
    abu.compare()
    abu.backup()
    
