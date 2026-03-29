cmake_minimum_required(VERSION 3.16)

# Define the project name and language
project(blog-roll LANGUAGES NONE)

# ---- Python venv ----
set(VENV_DIR ${CMAKE_SOURCE_DIR}/.venv)
set(VENV_PYTHON ${VENV_DIR}/bin/python)

# ---- Blogroll generation + git automation ----
add_custom_command(
    OUTPUT _layouts/blogroll.html

    # 1. Run blogroll generator with venv Python
    COMMAND ${VENV_PYTHON} build_blogroll.py

    # 2. Commit ONLY the two existing files
    COMMAND git add build_blogroll.py _data/websites.txt _layouts/blogroll.html

    # 3. Commit & push only if there are changes
    COMMAND git diff --cached --quiet
           || (git commit -m "Update Links page" && git push)

    DEPENDS
        _layouts/blogroll.html
        build_blogroll.py
        _data/websites.txt

    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Build Links page + auto git commit & push"
)

# ---- Default build target ----
add_custom_target(${PROJECT_NAME} ALL
    DEPENDS _layouts/blogroll.html
)
