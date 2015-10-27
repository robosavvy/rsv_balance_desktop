cmake_minimum_required(VERSION 2.8.3)
project(rsv_balance_rqt)

find_package(catkin REQUIRED COMPONENTS
  roslint
  rospy
  rqt_gui
  rqt_gui_py 
  rsv_balance_msgs
)

catkin_package(
  CATKIN_DEPENDS rsv_balance_msgs
)
catkin_python_setup()

roslint_python()

install(FILES plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY resource
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
