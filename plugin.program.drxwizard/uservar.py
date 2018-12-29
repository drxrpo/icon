import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = '[COLOR gold]Durex Wizard[/COLOR]'
EXCLUDES       = [ADDON_ID]
# Text File with build info in it.
BUILDFILE      = 'https://raw.githubusercontent.com/drxbld/tools/master/wizard.xml'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'https://raw.githubusercontent.com/drxbld/tools/master/apk.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = ''
YOUTUBEFILE    = ''
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'https://raw.githubusercontent.com/drxbld/tools/master/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'https://raw.githubusercontent.com/drxbld/images/master/builds.png'
ICONMAINT      = 'https://raw.githubusercontent.com/drxbld/images/master/maint.png'
ICONAPK        = 'https://raw.githubusercontent.com/drxbld/images/master/install.png'
ICONADDONS     = 'https://raw.githubusercontent.com/drxbld/images/master/install.png'
ICONYOUTUBE    = 'https://raw.githubusercontent.com/drxbld/images/master/youtube.png'
ICONSAVE       = 'https://raw.githubusercontent.com/drxbld/images/master/save.png'
ICONTRAKT      = 'https://raw.githubusercontent.com/drxbld/images/master/save.png'
ICONREAL       = 'https://raw.githubusercontent.com/drxbld/images/master/save.png'
ICONLOGIN      = 'https://raw.githubusercontent.com/drxbld/images/master/save.png'
ICONCONTACT    = 'https://raw.githubusercontent.com/drxbld/images/master/contact.png'
ICONSETTINGS   = 'https://raw.githubusercontent.com/drxbld/images/master/set2.png'
ICONBROOM       = 'https://raw.githubusercontent.com/drxbld/images/master/broom.png'
ICONTHUMBS       = 'https://raw.githubusercontent.com/drxbld/images/master/thumb.png'
ICONTRASH       = 'https://raw.githubusercontent.com/drxbld/images/master/trash.png'
ICONPACKAGE       = 'https://raw.githubusercontent.com/drxbld/images/master/package.png'
ICONUPDATE       = 'https://raw.githubusercontent.com/drxbld/images/master/update.png'
ICONFORCE       = 'https://raw.githubusercontent.com/drxbld/images/master/forceupdate.png'
ICONRD       = 'https://raw.githubusercontent.com/drxbld/images/master/realdebrid.png'
ICONTRAKT       = 'https://raw.githubusercontent.com/drxbld/images/master/trakt.png'
ICONSET       = 'https://raw.githubusercontent.com/drxbld/images/master/settings.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '[COLOR red]----------------------------------[/COLOR]'

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'gold'
COLOR2         = 'white'
COLOR3         = 'red'
COLOR3         = 'blue'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR2+']%s[/COLOR] >'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing Durex Build.\r\n[B][COLOR gold]Website:[/COLOR][/B] www.drxbld.com\r\n[COLOR blue][B]Facebook Group:[/COLOR][/B] https://www.facebook.com/groups/drxbld\r\n[COLOR red][B]For Durex TV 2.0 accounts email:[/COLOR][/B] drx.iptv@gmail.com'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://'
CONTACTFANART  = os.path.join(ART, 'ContentPanel.png')
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = 'https://raw.githubusercontent.com/drxbld/tools/master/wizard.xml'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.drxrepopub'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.githubusercontent.com/drxbld/repo/master/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.githubusercontent.com/drxbld/repo/master/repository.drxrepopub/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'https://raw.githubusercontent.com/drxbld/tools/master/news.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = 'Durex Wizard'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = os.path.join(ART, 'fanart.jpg')
#########################################################