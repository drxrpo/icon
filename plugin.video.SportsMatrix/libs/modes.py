import koding

def Mode(mode):
	koding.dolog('Mode= '+str(mode))
	if mode>=100 and mode <200:
		from libs import tools
		tools.Modes(mode)
