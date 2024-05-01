cmake_minimum_required(VERSION 3.8)
project(pubsub)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(rd_Ros src/rd_Ros.cpp)
target_include_directories(rd_Ros PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(rd_Ros PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(rd_Ros rclcpp std_msgs)

add_executable(rd_Nano src/rd_Nano_Ros.cpp)
target_include_directories(rd_Nano PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(rd_Nano PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(rd_Nano rclcpp std_msgs)

add_executable(sub src/Sub.cpp)
target_include_directories(sub PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(sub PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(sub rclcpp std_msgs)

install(TARGETS rd_Ros
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS sub
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS rd_Nano
  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
