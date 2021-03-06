#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# module_notifier.py - WIDS/WIPS framework notifier engine module
# Copyright (C)  2009 Peter Krebs, Herbert Haas
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see http://www.gnu.org/licenses/gpl-2.0.html

"""Notifier module

Receives alarm and other messages and relays it to different output templates.

"""

# Imports
#
# Custom modules
from fw_modules.module_exceptions import *
import fw_modules.module_template

# Standard modules


# Third-party modules


class NotifierClass(fw_modules.module_template.ModuleClass):
    """NotifierClass
    
    Relays incoming messages to output templates.
    
    """
    
    def __init__(self, controller_reference, parameter_dictionary, module_logger):
        """Constructor
        
        """
        
        fw_modules.module_template.ModuleClass.__init__(self, controller=controller_reference, param_dict=parameter_dictionary, logger=module_logger)

    def after_run(self):
        """after_run()
        
        Calls termination method of all templates.
        
        """
        
        self.shutdown_templates()

    def before_run(self):
        """
        
        Loads all requested output templates.
        
        """
        
        # Load output templates.
        try:
            self.load_templates()
        except FwTemplateSetupError as err:
            self.module_logger.error(err.errmsg)
            return False
        else:
            return True
        
    def process(self, input):
        """input()
        
        Input interface.
        Decodes received data.
        
        """
        
        self.module_logger.debug("Raw input: " + str(input))
        # Decode and check received data.
        try:
           msg_dict = dict(item.split('_', 1) for item in input.split('|'))
        except ValueError as err:
                self.module_logger.warning("Message information not valid; details " + err.__str__())
        else:
            # Relay message data to output templates.
            print msg_dict
            for template_identifier, template_info in self.template_status_dict.items():
                self.module_logger.info("Sending message data to template " + str(template_identifier))
                try:
                    template_info['template_reference'].template_input(msg_dict)
                except AttributeError as err:
                    self.module_logger.error("Template reference for template " + str(template_identifier) + " invalid; details: " + err.__str__())
        
def main(controller_reference, parameter_dictionary, module_logger):
    notifier_class = NotifierClass(controller_reference, parameter_dictionary, module_logger)
    return notifier_class
        
if __name__ == "__main__":
    print "Warning: This module is not intended to be executed directly. Only do this for test purposes."