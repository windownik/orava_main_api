import aiohttp
import requests


async def user_fb_check_auth(access_token: str, user_id: int, email: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://graph.facebook.com/{user_id}?fields=id,name,email&access_token={access_token}', ssl=False) as resp:
            answer = await resp.json()
            if resp.status != 200:
                return False

            if answer['email'] == email:
                return True

            return False


def user_google_check_auth(access_token: str, email: str,) -> bool:

    # access = 'ya29.a0Ael9sCMrg_wvDlccqnOmarO3K-T5dq-efKph2jGh5d3XMGdysGjJVgQuByXFnu2NSUFwAztBhbam5QEZ5TKWGCvv1FJYzcL5Ea93_jDJMjpS6HgqnfPoSs_2SUMRcmNZKm7QWXXKrJ3NgtlXYw8nToHnD7t_aCgYKAboSARMSFQF4udJh8DTfDwjxqzVhIalyEic17A0163'
    resp = requests.get(url=f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}')
    print(resp.status_code)
    try:
        print(resp.json())
    except:
        pass
    if resp.status_code == 200:
        if resp.json()['email'] == email:
            return True
    return False
