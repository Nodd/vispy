# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
"""
Support for iPython 3.x to allow VisPy's event loop to be run alongside
an interactive or notebook, without using threads.  This code relies on
inputhooks built-in to the Python interpreter.
"""

import time
from timeit import default_timer as clock
from IPython.lib.inputhook import inputhook_manager, InputHookBase, stdin_ready

import vispy.app


def enable(app=None):
    """Activate the iPython hook for VisPy.  If the app is not specified, the
    default is used.
    """
    inputhook_manager.enable_gui('vispy', app)


@inputhook_manager.register('vispy')
class VisPyInputHook(InputHookBase):
    """Implementation of an iPython 3.x InputHook for VisPy.  This is registered
    with the manager, so once imported can be used from the notebook with
        >> %enable_gui vispy
    """

    def enable(self, app=None):
        """Enable event loop integration with vispy.
        Parameters
        ----------
        app :
           The vispy application that's being used.  If None, then the
           default application is retrieved.
        Notes
        -----
        This methods sets the ``PyOS_InputHook`` for vispy, which allows
        vispy to integrate with terminal based applications like
        IPython.
        """

        self.app = app or vispy.app.use_app()
        self.manager.set_inputhook(self._vispy_inputhook)
        return app

    def _vispy_inputhook(self):
        try:
            t = clock()
            while not stdin_ready():
                self.app.process_events()

                used_time = clock() - t
                if used_time > 10.0:
                    time.sleep(1.0)
                elif used_time > 0.1:
                    time.sleep(0.05)
                else:
                    time.sleep(0.001)
        except KeyboardInterrupt:
            pass
        return 0
