# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client

def send_pushbullet_notification(self):
                IPAddress = os.popen("hostname -I").read()
                jsonData = {'type': 'note', 'title': 'Octopi\'s IP Address', 'body': 'Your Octopi\'s IP Address is {}'.format(IPAddress)}
		headers = {'Access-Token': self._settings.get(['pushbulletKey'])}
                url = "https://api.pushbullet.com/v2/pushes"
                r = requests.post(url, data=jsonData, headers=headers)

def send_email_notification(self):
                IPAddress = os.popen("hostname -I").read()
                fromEmail = self._settings.get(['emailUsername'])
                fromPassword = self._settings.get(["emailPassword"])
                msg = MIMEMultipart()
                message = 'Your Octopi\'s IP Address is {}'.format(IPAddress)
                msg['From']=fromEmail
                msg['To']=self._settings.get(['toEmailUsername'])
                msg['Subject']='OctoPi\'s IP Address'
                msg.attach(MIMEText(message, 'plain'))
                s = smtplib.SMTP_SSL('smtp.gmail.com')
                s.login(fromEmail, fromPassword)
                s.sendmail(fromEmail, self._settings.get(['toEmailUsernam']), msg.as_string())
                s.quit()

def send_text_notification(self):
		IPAddress = os.popen("hostname -I").read()
		client = Client(self._settings.get(["twilioSID"]), self._settings.get(["twilioKey"]))
		message = client.messages.create(from_='+1{}'.format(self._settings.get(["twilioNumber"])),
                                                to='+1{}'.format(self._settings.get(["ToNumber"])),
                                                body='Your Octopi\'s IP Address is {}'.format(IPAddress))

class IPNotifPlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.StartupPlugin):

	def on_after_startup(self):
		send_pushbullet_notification(self)
		send_text_notification(self)
		send_email_notification(self)

	def get_settings_defaults(self):
        	return [
			dict(pushbulletKey="YOUR PUSHBULLET API KEY"),
			dict(twilioSID="YOUR TWILIO SID"),
			dict(twilioKey="YOUR TWILIO API KEY"),
			dict(twilioNumber="YOUR TWILIO NUMBER"),
			dict(ToNumber="YOUR RECEIVING NUMBER").
			dict(emailUsername="YOUR FROM EMAIL USERNAME"),
			dict(emailPassword="YOUR FROM EMAIL PASSWORD"),
			dict(toEmailUsername='YOUR RECEIVER EMAIL ADDRESS')
		]

	def get_template_vars(self):
        	return [
			dict(key=self._settings.get(["pushbulletKey"])),
			dict(key=self._settings.get(["twilioSID"])),
			dict(key=self._settings.get(["twilioKey"])),
			dict(key=self._settings.get(["twilioNumber"])),
			dict(key=self._settings.get(["ToNumber"])),
			dict(key=self._settings.get(["emailUsername"])),
			dict(key=self._settings.get(["emailPassword"])),
			dict(key=self._settings.get(['toEmailUsername']))
		]
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

