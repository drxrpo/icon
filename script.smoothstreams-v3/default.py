import sys,os

if __name__ == '__main__':
    arg = None
    if len(sys.argv) > 1: arg = sys.argv[1] or False

    if arg == 'REFRESH_SCHEDULE':
        from lib import smoothstreams
        from lib import util
        fetch = {   'guide':'feed-new-latest.zip',
                    'guide_json':'feed-new.json',
                    'full_guide':'feed-new-full-latest.zip',
                    'full_guide_json':'feed-new-full.json'}
        LIST = util.getSetting('mode')
        if util.getSetting('full_guide_switch') == 'false' or LIST == "List":
            smoothstreams.Schedule.sscachejson(fetch['guide'],fetch['guide_json'],age=3600)
        else:
            smoothstreams.Schedule.sscachejson(fetch['full_guide'],fetch['full_guide_json'],age=3600)
        #smoothstreams.Schedule.sscachejson(force=True)
    elif arg == 'ABOUT':
        from lib import util
        util.about()
    elif arg == 'DOWNLOAD_CALLBACK':
        from lib.smoothstreams import player
        player.downloadCallback(sys.argv[2])
    elif arg == 'REFRESH_HASH':
        from lib import util
        hashFile = os.path.join(util.PROFILE,'hash')
        if os.path.exists(hashFile):
            os.remove(hashFile)
        from lib.smoothstreams import player
        player.ChannelPlayer().login()
        try:
            hash = util.getSetting('SHash_0')
        except:
            hash = util.getSetting('SHash_1')
        with open(hashFile,'w') as f:

            f.write(str(hash))
    else:
        from ssmain import main
        main()