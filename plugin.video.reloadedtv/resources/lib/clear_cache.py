import xbmc
import os
import shutil


def wipe_cache():
    xbmc_cache_path = xbmc.translatePath(os.path.join('special://home', 'cache'))
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)       
            if file_count > 0:            
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass

def delete_packages():
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        if file_count > 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

wipe_cache()
delete_packages()