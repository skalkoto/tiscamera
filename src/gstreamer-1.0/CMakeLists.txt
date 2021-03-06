
# Copyright 2014 The Imaging Source Europe GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set(PLUGINS
  gsttcamsrc
  gsttcamwhitebalance
  gsttcamautoexposure
  gsttcamautofocus
  gsttcambiteater
  gsttcambin
  )

find_package(GStreamer REQUIRED QUIET)
find_package(GLIB2     REQUIRED QUIET)
find_package(GObject   REQUIRED QUIET)
find_package(GObjectIntrospection REQUIRED QUIET)


include_directories(${GSTREAMER_INCLUDE_DIRS})
include_directories(${GSTREAMER_BASE_INCLUDE_DIRS})
include_directories(${GSTREAMER_VIDEO_INCLUDE_DIRS})
include_directories(${GLIB2_INCLUDE_DIR})
include_directories(${GObject_INCLUDE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/src)
include_directories(${CMAKE_SOURCE_DIR}/src/algorithms/)
include_directories(${CMAKE_SOURCE_DIR}/src/gobject)
include_directories(${CMAKE_SOURCE_DIR}/dependencies/json)

include_directories(${INTROSPECTION_INCLUDE_DIR})

add_library(tcamgstbase SHARED tcamgstbase.cpp tcamgstjson.cpp)
target_link_libraries(tcamgstbase tcam)
target_link_libraries(tcamgstbase tcamprop)
target_link_libraries(tcamgstbase tcam-algorithms)
target_link_libraries(tcamgstbase ${GOBJECT_LIBRARIES})
target_link_libraries(tcamgstbase ${GLIB2_LIBRARIES})
target_link_libraries(tcamgstbase ${GSTREAMER_LIBRARIES})
target_link_libraries(tcamgstbase ${GSTREAMER_BASE_LIBRARIES})
target_link_libraries(tcamgstbase ${GSTREAMER_VIDEO_LIBRARIES})


add_library(gsttcamsrc SHARED gsttcamsrc.cpp gstmetatcamstatistics.cpp)

add_library(gsttcamwhitebalance SHARED gsttcamwhitebalance.cpp)

add_library(gsttcamautoexposure SHARED gsttcamautoexposure.cpp)

add_library(gsttcamautofocus SHARED gsttcamautofocus.cpp)

add_library(gsttcambiteater SHARED gsttcambiteater.cpp)

add_library(gsttcambin SHARED gsttcambin.cpp)

foreach (t IN ITEMS ${PLUGINS})

    target_link_libraries(${t} tcam)
    target_link_libraries(${t} tcamprop)
    target_link_libraries(${t} tcam-algorithms)
    target_link_libraries(${t} tcamgstbase)
    target_link_libraries(${t} ${GOBJECT_LIBRARIES})
    target_link_libraries(${t} ${GLIB2_LIBRARIES})

    target_link_libraries(${t} ${GSTREAMER_LIBRARIES})
    target_link_libraries(${t} ${GSTREAMER_BASE_LIBRARIES})
    target_link_libraries(${t} ${GSTREAMER_VIDEO_LIBRARIES})

endforeach (t)

pkg_check_variable(gstreamer-1.0 pluginsdir)
pkg_check_variable(gstreamer-1.0 includedir)

if (GSTREAMER_1.0_PLUGINSDIR)
  set(TCAM_INSTALL_GST_1_0 ${GSTREAMER_1.0_PLUGINSDIR} CACHE PATH "gstreamer-1.0 module installation path")

else()
  set(TCAM_INSTALL_GST_1_0 "${CMAKE_INSTALL_PREFIX}/lib/gstreamer-1.0" CACHE PATH "gstreamer-1.0 module installation path")
endif()

install(TARGETS tcamgstbase
  LIBRARY
  DESTINATION "${TCAM_INSTALL_LIB}"
  COMPONENT tcam-gstreamer-1)

install(TARGETS ${PLUGINS}
  DESTINATION ${TCAM_INSTALL_GST_1_0}
  COMPONENT tcam-gstreamer-1)

install(FILES gstmetatcamstatistics.h
  DESTINATION "${GSTREAMER_1.0_INCLUDEDIR}"
  COMPONENT tcam-gstreamer-1)
