#  ducker.py
#  Copyright 2016 Marcus Hogue <marcus@hogue.me>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""A module for ZNC (IRC bouncer software)
Purpose: React, auto-shoot, or befriend gonzobot ducks
"""
import znc
import re
import random
import time

class ducker(znc.Module):
    description = "Gonzobot duck autoresponder for ZNC"
    module_types = [znc.CModInfo.NetworkModule]

    def OnLoad(self, args, message):
        responses = [
            'What is that thing?','Is that a duck?',
            'I\'m scared of ducks','Oh, that one looks friendly!',
            'Kill it with fire!','.bef',
            '.bang','.bfe',
            '.bnag','bang',
            'bef','.befriend',
            'I\'m not feeling this one','I need coffee',
            'My cousin was bitten by a duck once','/me runs away',
            '¯\\_(ツ)_/¯','.lenny',
            '\\o/','.flip DUCK!',
            '.ask Is that a duck?','ლ(ಠ益ಠ)ლ',
            '༼ ༎ຶ ෴ ༎ຶ༽','「(°ヘ°)',
            'ᕕ( ᐛ )ᕗ','(╯°□°）╯︵ ┻━┻',
            '༼ つ ◕_◕ ༽つ','(✿◠‿◠)',
            '¯(°_o)/¯','(͡° ͜ʖ ͡°)',
            '(ಠ_ಠ)','(╯_╰)',
            '(─‿‿─)','\,,/(^_^)\,,/',
            '(¬､¬)','(ﾉﾟ0ﾟ)ﾉ',
            '( •_•)O*¯`·.¸.·´¯`°Q(•_• )',
            '^(;,;)^',
        ]
        botname = "gonzobot"
        decoy = 'DECOY DUCK'
        duck_re = re.compile('[o○O0öøóóȯôőŏᴏōο](<|＜)')

    def OnChanMsg(self, nick, channel, message):
        own_host = self.GetNetwork().GetIRCNick().GetHostMask()
        channel = channel.GetName()
        nick = nick.GetNick()
        msg = str(message)
        msg = msg.replace('\u200b', '')
        if nick == botname and duck_re.search(msg) is not None:
            self.duck_react(msg, channel, nick, own_host)
        return znc.CONTINUE

    def duck_react(self, msg, channel, nick, own_host):
        self.PutModule("INCOMING IN {}!".format(channel)
        if self.msg.find(self.decoy) != -1:
            self.PutModule("(I think it's a DECOY)")
            response = 'nice try.'
        else:
            response = random.choice(self.responses)
        delay = random.randint(0,99)/10+1
        time.sleep(delay)
        self.GetNetwork().PutIRC("PRIVMSG {0} :{1}".format(channel, response))
        self.PutModule("Triggered when {0} said {1} on {2}".format(nick, message.s, channel)
        self.PutModule("I waited {1} seconds and said \"{0}\" in response".format(response, delay))
        self.GetNetwork().PutUser(':{own_host} {msg}'.format(own_host=own_host, msg=response))
