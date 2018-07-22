# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.


import octoprint.plugin
import requests
import os

from twilio.rest import Client

class IPNotifPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.StartupPlugin):

        def on_after_startup(self):
        	IPAddress = os.popen("hostname -I").read()
        	jsonData = {"type": "note", "title": "Octopi\'s IP Address", "body": "Your Octopi\'s IP Address is {}".format(IPAddress)}
        	headers = {"Access-Token": self._settings.get(["key"])}
        	url = "https://api.pushbullet.com/v2/pushes"
        	r = requests.post(url, data=jsonData, headers=headers)

		#Twilio Text Notification
		client = Client('ACfe93b66865eb27816e7548b9808029b5', '38e4e572502ac4a13690173bbd008b2d')
		message = client.messages.create(from_='+14243735073', to='+15624122360', body='Your Octopi\'s IP Address is {}'.format(IPAddress))

    	def get_settings_defaults(self):
        	return dict(key="YOUR PUSHBULLET API KEY")

    	def get_template_vars(self):
        	return dict(key=self._settings.get(["key"]))

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/IPNotif.js"],
			css=["css/IPNotif.css"],
			less=["less/IPNotif.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			IPNotif=dict(
				displayName="IPNotif Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="ankushvangari",
				repo="OctoPrint-IPNotif",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/ankushvangari/OctoPrint-IPNotif/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "OctoPrint IP Notification"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = IPNotifPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

