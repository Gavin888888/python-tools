import base64

base64urls = []
for i in range(1,25):

    image_path = '/Users/leili/Desktop/0.jpg'
    if i < 10:
        image_path = '/Users/leili/Desktop/test/refresh_header_0'+str(i)+'~iphone@2x.png'
    else:
        image_path = '/Users/leili/Desktop/test/refresh_header_'+str(i)+'~iphone@2x.png'

    with open(image_path, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
        toBase64Url = 'data:image/jpeg;base64,' + image_base64
        base64urls.append(toBase64Url)

print(base64urls)
