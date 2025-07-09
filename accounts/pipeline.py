from django.shortcuts import redirect
from django.contrib.auth import login

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'kakao':
        kakao_account = response.get('kakao_account')
        profile = kakao_account.get('profile')

        user.nickname = profile.get('nickname', '')
        user.region_city = ''  # 기본값
        user.region_district = ''
        user.region_dong = ''
        user.image = None
        user.save()

def redirect_to_location(strategy, details, user=None, *args, **kwargs):
    if user and user.is_authenticated:
        login(strategy.request, user, backend='social_core.backends.kakao.KakaoOAuth2')
        # 이미 동네(region)가 저장돼 있으면 그냥 home으로 리다이렉트
        if user.region_city and user.region_district and user.region_dong:
            return redirect('home')
        else:
            # region 정보가 없으면 location 설정하러 보내기
            return redirect('location')