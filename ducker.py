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
#
#  duck regex match : \\_o<|\\_O<|\\_0<|\\_\u00f6<|\\_\u00f8<|\\_\u00f3<

"""A module for ZNC (IRC bouncer software)
Purpose: React, auto-shoot, or befriend gonzobot ducks
"""
# ducker.py

import znc
import re
import random
import time

class ducker(znc.Module):
    description = "Gonzobot duck autoresponder for ZNC"
    module_types = [znc.CModInfo.NetworkModule]

    def OnChanMsg(self, nick, channel, message):
        self.responses = [
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
        own_host = self.GetNetwork().GetIRCNick().GetHostMask()
        duck_re = re.compile('[o○O0öøóóȯôőŏᴏōο](<|＜)')
        decoy = 'DECOY DUCK'
        msg = str(message)
        msg = msg.replace('\u200b', '')
        if nick.GetNick() == botname and duck_re.search(msg) is not None:
             self.PutModule("INCOMING IN {}!".format(channel.GetName()))
             if msg.find(decoy) != -1:
                self.PutModule("(I think it's a DECOY)")
                response = 'nice try.'
             else:
                response = random.choice(self.responses)
             delay = random.randint(0,99)/10+1
             time.sleep(delay)
             self.GetNetwork().PutIRC("PRIVMSG {0} :{1}".format(channel.GetName(), response))
             self.PutModule("Triggered when {0} said {1} on {2}".format(nick.GetNick(), message.s, channel.GetName()))
             self.PutModule("I waited {1} seconds and said \"{0}\" in response".format(response, delay))
             self.GetNetwork().PutUser(':{own_host} {msg}'.format(own_host=own_host, msg=response))
        return znc.CONTINUE
