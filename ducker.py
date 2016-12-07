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

class ducker(znc.Module):
    description = "Example python3 module for ZNC"

    def OnChanMsg(self, nick, channel, message):
        self.responses = [
            'What is that thing?','Is that a duck?','I\'m scared of ducks','Oh, that one looks friendly!','Kill it with fire!','.bef','.bang',
        ]
        own_host = self.GetNetwork().GetIRCNick().GetHostMask()
        duckregex = '[oO0öøóóȯôőŏᴏōο](<|>|＜)'
        msg = str(message)
        if re.search(duckregex, msg) is not None:
             response = random.choice(self.responses)
             self.GetNetwork().PutIRC("PRIVMSG {0} :{1}".format(channel.GetName(), response))
             self.GetNetwork().PutUser(':{own_host} {msg}'.format(own_host=own_host, msg=msg))
             self.PutModule("Hey, {0} said {1} on {2}".format(nick.GetNick(), message.s, channel.GetName()))
             self.PutModule("I said \"{0}\" in response".format(response))
        return znc.CONTINUE
