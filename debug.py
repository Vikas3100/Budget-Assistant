import sys
import traceback

try:
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
