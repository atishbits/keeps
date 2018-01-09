from PIL import Image, ImageFile
from sys import exit, stderr
from os.path import getsize, isfile, isdir, join
from os import remove, rename, walk, stat
from stat import S_IWRITE
from shutil import move
from abc import ABCMeta, abstractmethod
 
class ProcessBase:
    """Abstract base class for file processors."""
    __metaclass__ = ABCMeta
 
    def __init__(self):
        self.extensions = []
        self.backupextension = 'compressimages-backup'
 
    @abstractmethod
    def processfile(self, filename):
        """Abstract method which carries out the process on the specified file.
        Returns True if successful, False otherwise."""
        pass
 
    def processdir(self, path):
        """Recursively processes files in the specified directory matching
        the self.extensions list (case-insensitively)."""
 
        filecount = 0 # Number of files successfully updated
 
        for root, dirs, files in walk(path):
            for file in files:
                # Check file extensions against allowed list
                lowercasefile = file.lower()
                matches = False
                for ext in self.extensions:
                    if lowercasefile.endswith('.' + ext):
                        matches = True
                        break
                if matches:
                    # File has eligible extension, so process
                    fullpath = join(root, file)
                    if self.processfile(fullpath):
                        filecount = filecount + 1
        return filecount
 
class CompressImage(ProcessBase):
    """Processor which attempts to reduce image file size."""
    def __init__(self):
        ProcessBase.__init__(self)
        self.extensions = ['jpg', 'jpeg', 'png']
 
    def processfile(self, filename):
        """Renames the specified image to a backup path,
        and writes out the image again with optimal settings."""
        try:
            # Skip read-only files
            if (not stat(filename)[0] & S_IWRITE):
                print 'Ignoring read-only file "' + filename + '".'
                return False
            
            # Create a backup
            backupname = filename + '.' + self.backupextension
 
            if isfile(backupname):
                print 'Ignoring file "' + filename + '" for which existing backup file is present.'
                return False
 
            rename(filename, backupname)
        except Exception as e:
            stderr.write('Skipping file "' + filename + '" for which backup cannot be made: ' + str(e) + '\n')
            return False
 
        ok = False
 
        try:
            # Open the image
            with open(backupname, 'rb') as file:
                img = Image.open(file)
 
                # Check that it's a supported format
                format = str(img.format)
                if format != 'PNG' and format != 'JPEG':
                    print 'Ignoring file "' + filename + '" with unsupported format ' + format
                    return False
 
                # This line avoids problems that can arise saving larger JPEG files with PIL
                ImageFile.MAXBLOCK = img.size[0] * img.size[1]
                
                # The 'quality' option is ignored for PNG files
                img.save(filename, quality=20, optimize=True)
 
            # Check that we've actually made it smaller
            origsize = getsize(backupname)
            newsize = getsize(filename)
 
            if newsize >= origsize:
                print 'Cannot further compress "' + filename + '".'
                return False
 
            # Successful compression
            ok = True
        except Exception as e:
            stderr.write('Failure whilst processing "' + filename + '": ' + str(e) + '\n')
        finally:
            if not ok:
                try:
                    move(backupname, filename)
                except Exception as e:
                    stderr.write('ERROR: could not restore backup file for "' + filename + '": ' + str(e) + '\n')
            else:
			    remove(backupname)
        return ok
 
if __name__ == "__main__":
    # Argument parsing
    modecompress = 'compress'
    path = raw_input("Please provide complete path to Directory containing images that you wish to compress, ex: C:\Documents\Pictures : \n")
	#moderestorebackup = 'restorebackup'
    #modedeletebackup = 'deletebackup'
    processor = CompressImage()
 
    # Run according to whether path is a file or a directory
    if isfile(path):
        processor.processfile(path)
    elif isdir(path):
        filecount = processor.processdir(path)
        print '\nSuccessfully updated file count: ' + str(filecount)
    else:
		stderr.write('Invalid path "' + path + '"\n')
    test = raw_input("Press any key to exit the program")
