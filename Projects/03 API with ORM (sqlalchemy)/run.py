"""
Running this python module is equivalent to enter the following command in terminal:
uvicorn sql_app.main:app --reload
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("sql_app.main:app", reload=True)
