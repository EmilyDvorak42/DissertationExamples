#
# $Id: CMakeLists.txt 173671 2019-06-03 17:59:13Z acoleman $
#
i3_project(rock_bottom
  PYTHON_DIR python
  )

set (ROCKBOTTOM_DATA_DIR ${CMAKE_CURRENT_SOURCE_DIR}/resources/data)
add_definitions (-DROCKBOTTOM_DATA_DIR="${ROCKBOTTOM_DATA_DIR}")

i3_add_library(rock_bottom
  private/rock_bottom/*.cxx
  private/rock_bottom/interface/*.cxx
  private/rock_bottom/interface/*/*.cxx
  private/rock_bottom/models/*.cxx
  private/rock_bottom/models/*/*.cxx
  private/rock_bottom/functions/*.cxx
  private/rock_bottom/snowservices/*.cxx
  USE_TOOLS boost python gsl
  USE_PROJECTS icetray dataclasses phys-services toprec gulliver tableio photospline recclasses serialization radcube
  )


# Fetch rock_bottom data only if explicitly requested
OPTION(FETCH_ROCKBOTTOM On)
FIND_PACKAGE(Wget)
IF (WGET_FOUND)
  FILE(MAKE_DIRECTORY ${ROCKBOTTOM_DATA_DIR})
  ADD_CUSTOM_TARGET(rock_bottom-fetch
    COMMAND rm -f ${ROCKBOTTOM_DATA_DIR}/${FILE}
    COMMAND ${WGET_EXECUTABLE} ${SOURCE}/${FILE}
    WORKING_DIRECTORY ${ROCKBOTTOM_DATA_DIR}
    COMMENT "Downloading and unpacking Rockbottom data.")
  IF (FETCH_ROCKBOTTOM)
    colormsg(GREEN "+-- Downloading and unpacking Rockbottom data.")
    EXECUTE_PROCESS(COMMAND rm -f ${FILE} WORKING_DIRECTORY ${ROCKBOTTOM_DATA_DIR})
    EXECUTE_PROCESS(COMMAND ${WGET_EXECUTABLE} -q ${SOURCE}/${FILE} WORKING_DIRECTORY ${ROCKBOTTOM_DATA_DIR})
  ENDIF (FETCH_ROCKBOTTOM)
ELSE (WGET_FOUND)
  colormsg(CYAN "+-- WGet not found. Rockbottom data will not be available.")
ENDIF (WGET_FOUND)

i3_test_executable(test
  private/test/*.cxx
  USE_TOOLS boost python gsl
  USE_PROJECTS toprec icetray dataclasses phys-services dataio interfaces lilliput recclasses radcube
)
set_tests_properties(rock_bottom::test PROPERTIES LABELS RUN_LONG)


i3_add_pybindings(rock_bottom
  private/pybindings/module.cxx
  private/pybindings/I3RbLDFService.cxx
  private/pybindings/I3LaputopSignalModel.cxx
  private/pybindings/I3GaussCurveModel.cxx
  private/pybindings/I3FrontScintModel.cxx
  private/pybindings/I3TwoLDFSignalModel.cxx
  private/pybindings/I3RbUtilities.cxx
  private/pybindings/I3ParameterMap.cxx
  private/pybindings/I3ScintSignalModel.cxx

  USE_TOOLS boost python
  USE_PROJECTS icetray dataclasses gulliver lilliput
)
