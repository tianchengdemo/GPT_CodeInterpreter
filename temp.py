from PIL import Image

img = Image.open('/tmp/1.png')
new_img = img.resize((640, 640))
new_img.save('/tmp/resized.png')
print({'type': 'image', 'path': '/tmp/resized.png', 'status':'true'})