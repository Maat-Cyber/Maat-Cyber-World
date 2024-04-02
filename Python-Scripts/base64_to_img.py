# importing pybase64 module  
# might need to install it with: pip install pybase64
import pybase64 
  
# Get the base64 encoded data  
print("insert the name of the file with the base64 encoded data, the image will be saved in the CWD as image.png")  
filename = input()
try:
    with open(filename, 'r') as file:
        encoded_data = file.read()
except:
    print('File cannot be opened:', filename)  
    exit()  
  
# decode base64 string data  
decoded_data = pybase64.b64decode((encoded_data))  
  
# create the image file  
img_file = open('image.png', 'wb')  # change the img extension if you prefer another one
img_file.write(decoded_data)  
img_file.close()
