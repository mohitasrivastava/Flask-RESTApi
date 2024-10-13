# __all__=["user_controller", "product_controller"]  # This will import List 
#INThis one we don't have to add each and every file
import os
import glob

__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py" )]

# for f in glob.glob(os.path.dirname(__file__) + "/*.py" ):
#     __all__.append(os.path.basename(f)[:-3])

#This init file will treat as python package not as a file