import os
import rospy
import rospkg
import rosservice

import rsv_balance_msgs.srv

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QWidget


class BalanceModeWidget(Plugin):
    def __init__(self, context):
        super(BalanceModeWidget, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('BalanceMode')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                            dest="quiet",
                            help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rsv_balance_rqt'), 'resource', 'BalanceModeWidget.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('BalanceModeWidgetUI')
        # Numerated windowTitle
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)

        self._widget.set_park.clicked[bool].connect(self.on_set_park_button)
        self._widget.set_tractor.clicked[bool].connect(self.on_set_tractor_button)
        self._widget.set_balance.clicked[bool].connect(self.on_set_balance_button)

        self._widget.topic_line_edit.textChanged.connect(self.on_topic_changed)

        # Set mode client
        self.set_mode_srv = None
        self.on_topic_changed()

    def shutdown_plugin(self):
        pass

    def save_settings(self, plugin_settings, instance_settings):
        instance_settings.set_value('topic', self._widget.topic_line_edit.text())

    def restore_settings(self, plugin_settings, instance_settings):
        value = instance_settings.value('topic', "/set_mode")
        self._widget.topic_line_edit.setText(value)

    def on_set_park_button(self):
        try:
            self.set_mode_srv(rsv_balance_msgs.srv.SetModeRequest.PARK)
        except rospy.ServiceException, e:
            rospy.logwarn("Service call failed: %s" % e)

    def on_set_tractor_button(self):
        try:
            self.set_mode_srv(rsv_balance_msgs.srv.SetModeRequest.TRACTOR)
        except rospy.ServiceException, e:
            rospy.logwarn("Service call failed: %s" % e)

    def on_set_balance_button(self):
        try:
            self.set_mode_srv(rsv_balance_msgs.srv.SetModeRequest.BALANCE)
        except rospy.ServiceException, e:
            rospy.logwarn("Service call failed: %s" % e)

    def on_topic_changed(self):
        # self._widget.set_park.setEnabled(False)
        # self._widget.set_tractor.setEnabled(False)
        # self._widget.set_balance.setEnabled(False)

        topic = self._widget.topic_line_edit.text()

        if self.set_mode_srv is not None:
            self.set_mode_srv.close()
            self.set_mode_srv = None

        if not topic == "":
            # try:
                # rospy.wait_for_service('/set_mode', 2)
                # self._widget.set_park.setEnabled(True)
                # self._widget.set_tractor.setEnabled(True)
                # self._widget.set_balance.setEnabled(True)
            # except rospy.ROSException, e:
                # rospy.logwarn("Changing topic exception: %s" % e)

            self.set_mode_srv = rospy.ServiceProxy(topic, rsv_balance_msgs.srv.SetMode)
