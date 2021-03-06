# Instabd

Instabd is a Python library client for Instagram Basic Display API

## Starting

To start you need:

- A Facebook developers account.
- A app with permissions to Instagram Basic Display API.

For more instructions, please, read the [docs](https://developers.facebook.com/docs/instagram-basic-display-api/) from facebook.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install instabd.

```bash
pip install instabd
```

## Usage

```python
from instabd import InstabdClient

# create your client
client = InstabdClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="your_redirect_uri",
)

# generate authorize url
client.authorize()
>>> 'https://api.instagram.com/oauth/authorize?client_id=your_client_id&redirect_uri=your_redirect_uri&scope=user_profile,user_media&response_type=code'
```

This is the url that will authenticate the instagram user account.

### Receiving the code

On your `redirect_uri` you will receive an code that will be sent by the instagram.

With this code you can authenticate your user_client.

For example in a `flask` app.

```python
code = request.args.get("code")
user_client = client.to_user_client_from_code(code)
```

This way you can get the authorization for your user_client.

If you need the **_long lived token_** you can do this:

```python
code = requests.args.get("code")
user_client = client.to_user_client_from_code(code, long=True)
```

### Refresh token

You can refresh a token in two ways

#### 1 - From access token

You will receive a new Authentication schema.

```python
client.refresh("access_token")
>>> Authentication(access_token='new_access_token', expires_at=datetime.datetime(2022, 4, 26, 11, 27, 0, 221694))
```

#### 2 - From user client

```python
client.refresh_for(user_client)
user_client.authentication
>>> Authentication(access_token='new_access_token', expires_at=datetime.datetime(2022, 4, 26, 11, 27, 0, 188948))
```

## User client

Now with this user client you can get his data.

```python
user_client.user
>>> User(id="user_id", username="username", account_type="account_type", media_count=10)
```

### Getting medias

When you get the medias, the user client get all the children if the media is a `carousel album`.

Getting the medias now it's easy, just do:

```python
user_client.medias()
>>> [Media(id='id', caption=None, media_type='IMAGE', media_url='media_url', permalink='permalink', thumbnail_url=None, timestamp='2022-02-03T13:26:29+0000', username='username', children=[])]
```

#### Limiting medias

You can limit the medias, just pass the `limit` param.

The default is: 10

```python
user_client.medias(limit=100)
>>> [Media(id='id', caption=None, media_type='IMAGE', media_url='media_url', permalink='permalink', thumbnail_url=None, timestamp='2022-02-03T13:26:29+0000', username='username', children=[])]
```

##### :warning: Atention

> The limit sometimes can be smaller than you put.
> It's because the user can have no medias on your Instagram account or have less medias.

#### Grabbing all medias

You can grab all medias from your user client

```python
user_client.medias(grab_all=True)
>>> [Media(id='id', caption=None, media_type='IMAGE', media_url='media_url', permalink='permalink', thumbnail_url=None, timestamp='2022-02-03T13:26:29+0000', username='username', children=[])]
```

#### Getting by time

And the last example is when you need get the medias between some time.
In this case you can use the `since`and `until` params.

For example

```python
from datetime import datetime, timedelta

now = datetime.now()
seven_hours_ago = now - timedelta(hours=7)

since = int(seven_hours_ago.timestamp())
until = int(now.timestamp())

user_client.medias(since=since, until=until)
>>> [Media(id='id', caption=None, media_type='IMAGE', media_url='media_url', permalink='permalink', thumbnail_url=None, timestamp='2022-02-03T13:26:29+0000', username='username', children=[])]
```

:information_source: Here we have this conversion because facebook's tell us to pass a unix timestamp without the dots.

#### Create a user client from access token

If you need you can create a user client from your access token from db

```python
>>> from instabd import UserClient
>>> user_client = UserClient.from_access_token("access_token_from_db")
```

## Todo

- [x] Get medias with pagination
- [x] Get user medias with since and util params
- [x] Implement error codes
- [x] Create hook to handle error codes
- [x] Add account type on user
- [x] Add media count on user
- [ ] Add limitations section
- [x] Update readme to show medias cases
- [x] Get all media from user
