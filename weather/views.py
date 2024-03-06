from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def get_html_content(city):
    import requests
    city = city.replace(' ','+')
    USER_AGENT = "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+in+{city}').text
    return html_content

def HOME(request):
    weather = None
    if 'city' in request.GET:
        # Fetch weather data
        city = request.GET['city']
        html_content = get_html_content(city)
        from bs4 import BeautifulSoup
        weather = dict()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        region_element = soup.find('span', attrs={'class': 'BBwThe'})
        dayhour_element = soup.find('div', attrs={'id': 'wob_dts'})
        status_element = soup.find('span', attrs={'id': 'wob_dc'})
        temp_element = soup.find('span', attrs={'id': 'wob_tm'})
        humidity_element = soup.find('span', attrs={'id': 'wob_hm'})
        wind_element = soup.find('span', attrs={'id': 'wob_ws'})


        
        # Check if elements are found before accessing their text content
        if region_element:
            weather['region'] = region_element.text
        if dayhour_element:
            weather['dayhour'] = dayhour_element.text
        if status_element:
            weather['status'] = status_element.text
        if temp_element:
            weather['temp'] = temp_element.text
        if humidity_element:
            weather['humidity'] = humidity_element.text
        if wind_element:
            weather['wind'] = wind_element.text

    return render(request, 'home.html', {'weather': weather})
