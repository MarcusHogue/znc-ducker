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
#  Work in progress using Thor77's SlapAnswer as the starting point

"""A module for ZNC (IRC bouncer software)
Purpose: auto-shoot (or befriend) gonzobot ducks
"""
import random
import json
import znc
import re


class ducker(znc.Module):
    description = 'Do things to ducks automatically'
    module_types = [znc.CModInfo.NetworkModule]

    def OnLoad(self, args, message):
        self.default_answers = [
            '.bef','.bang','.befriend','.bnag','.bfe',
        ]
        if 'answers' in self.nv:
            self.ANSWERS = json.loads(self.nv['answers'])
        else:
            self.ANSWERS = self.default_answers
            self.save_answers()
        return True

    def OnModCommand(self, cmd):
        split = cmd.split()
        command = str(split[0]).lower()
        args = [a.lower() for a in split[1:]]
        if command == 'help':
            self.command_help()
        elif command == 'list':
            self.command_list()

    def save_answers(self):
        self.nv['answers'] = json.dumps(self.ANSWERS)

    def command_help(self):
        self.PutModule('list | get a list with msgs')
        return True

    def command_list(self):
        for index, value in enumerate(self.ANSWERS):
            self.PutModule('{} | {}'.format(index, value))
        return True

    def OnChanAction(self, invoker, channel, message):
        own_nick = self.GetNetwork().GetIRCNick().GetNick()
        own_host = self.GetNetwork().GetIRCNick().GetHostMask()
        nick = invoker.GetNick()
        channel = channel.GetName()
        duckregex = '\\_o<|\\_O<|\\_0<|\\_\u00f6<|\\_\u00f8<|\\_\u00f3<'
        msg = str(message)
        if re.match(duckregex, msg) is not None:
            self.get_duck(channel, own_host)
        return znc.CONTINUE

    def get_duck(self, channel, own_host):
        msg = random.choice(self.ANSWERS)
        msg = 'PRIVMSG {channel} :{msg}'.format(channel=channel, msg=msg)
        self.GetNetwork().PutIRC(msg)
        self.GetNetwork().PutUser(':{own_host} {msg}'.format(own_host=own_host, msg=msg))
