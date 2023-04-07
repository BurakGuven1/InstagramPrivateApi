from instagram_private_api import (
    Client, 
    ClientCompatPatch, 
    ClientError, 
    ClientLoginRequiredError
)
import time
from urllib.request import urlretrieve

# your info
username = 'IGUSERNAME'
password = 'IGPASSWORD'


api = Client(username, password)
api.login()

#get this persons info
result = api.username_info('IGUSERNAME') 
user_id = result['user']['pk']


from urllib.request import urlretrieve


next_max_id = None
while True:
    try:
        user_feed = api.user_feed(user_id, max_id=next_max_id)
        items = user_feed.get('items', [])
        
        if not items:
            break
            
        for post in items:
            print(post.get('caption', 'No caption'))
            images = post.get('carousel_media', [])
            if not images:
                images = [post.get('image_versions2', {}).get('candidates', [{}])[0]]

            for i, image in enumerate(images):
                image_versions = image.get('image_versions2', {})
                candidates = image_versions.get('candidates', [])

                for candidate in candidates:
                    image_url = candidate.get('url')
                    if image_url:
                        print(image_url)

                        # Görselin indirilmesi
                        filename = 'post_{}_{}.jpg'.format(post['id'], i)
                        urlretrieve(image_url, filename)

        next_max_id = user_feed.get('next_max_id')
        if not next_max_id:
            break
        
    except (ClientError, ClientLoginRequiredError) as e:
        print(e)
        break
