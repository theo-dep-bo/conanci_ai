cmake_minimum_required(VERSION 3.15)
project(ai VERSION 1.0 LANGUAGES CXX)

find_package(mathlib CONFIG REQUIRED)

add_library(ai src/ai.cpp)
target_include_directories(ai PUBLIC include)
target_compile_definitions(ai PRIVATE PKG_VERSION="${PROJECT_VERSION}")
target_link_libraries(ai mathlib::mathlib)

set_target_properties(ai PROPERTIES PUBLIC_HEADER "include/ai.h")
install(TARGETS ai)
