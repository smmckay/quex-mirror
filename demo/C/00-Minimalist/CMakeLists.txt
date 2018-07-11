cmake_minimum_required (VERSION 2.6)
project (Minimalist)

include_directories("${CMAKE_CURRENT_BINARY_DIR}")

add_executable(lexer lexer.c tiny/tiny.c)
add_custom_command (
    OUTPUT  ${CMAKE_CURRENT_BINARY_DIR}/tiny/tiny.c
    COMMAND quex -i tiny.qx -o tiny --language C
    DEPENDS tiny.qx
)
