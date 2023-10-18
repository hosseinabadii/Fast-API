"""
Running this python module is equivalent to enter the following command in terminal:
uvicorn main:app --reload
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
