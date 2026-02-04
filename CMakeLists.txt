cmake_minimum_required(VERSION 3.16)

set(PROJECT_NAME blog-roll)

# ---- Python venv ----
set(VENV_DIR ${CMAKE_SOURCE_DIR}/blog-roll)
set(VENV_PYTHON ${VENV_DIR}/bin/python)

# ---- Blogroll generation + git automation ----
add_custom_command(
    OUTPUT _layout/blogroll.html

    # 1. Run blogroll generator with venv Python
    COMMAND ${VENV_PYTHON} build_blogroll.py

    # 2. Commit ONLY the two existing files
    COMMAND git add build_blogroll.py _data/websites.txt

    # 3. Commit & push only if there are changes
    COMMAND git diff --cached --quiet
           || (git commit -m "Update Links page" && git push)

    DEPENDS
        build_blogroll.py
        _data/websites.txt

    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Build Links page + auto git commit & push"
)

# ---- Default build target ----
add_custom_target(${PROJECT_NAME} ALL
    DEPENDS _layout/blogroll.html
)
