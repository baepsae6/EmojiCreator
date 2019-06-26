import requests
import lxml
import lxml.html as html
from urllib.parse import urljoin
import json
from selenium import webdriver 

def get_html(url):
    r = requests.get(url) 
    return r

def click(base_url):
    driver = webdriver.Firefox()
    driver.get(base_url)
    button = driver.find_element_by_xpath('.//div[@class="region-sidebar"]')
    button.click()

def get_city_link(base_url):
    main_html = get_html(base_url)
    tree = html.fromstring(main_html.text)
    items = tree.xpath('.//ul[@id="region-sidebar__dropdown"]//a/@href')
    urls = items
    urls = [urljoin(base_url, url) for url in urls][1:]

    return urls

def get_section_link(main_html):
    tree = html.fromstring(main_html.text)
    items = tree.xpath('.//nav[@class="nav"]//a/@href')
    urls = items
    base_url = 'https://ticketon.kz'
    urls = [urljoin(base_url, url) for url in urls]

    return urls

def get_popular_links(html_str):
    tree = html.fromstring(html_str.text)
    items1 = tree.xpath('.//div[@class="row grid"]//div[@class="list-popular"]//a[@class="list-item__link"]/@href')
    items2 = tree.xpath('.//div[@class="row grid"]//div[@class="block-1 list-block"]//a[@class="list-item__link"]/@href')
    items = items1 + items2
    urls = items
    base_url = 'https://ticketon.kz'
    urls = [urljoin(base_url, url) for url in urls]

    return urls

def parse(tree, xpath):
    els = tree.xpath(xpath)
    if len(els):
        return els[0]
    else:
        return None


def get_page_data(url):
    html_str = get_html(url)
    tree = html.fromstring(html_str.text)
    title = tree.xpath('.//h1')[0].text_content()
    time = parse(tree, './/div[@class="button-buy__wrapper"]//time/@datetime')
    image = parse(tree, './/div[@class="event__information"]//img/@src')
    description = parse(tree, './/div[@class="event__information"]')
    if isinstance(description,lxml.html.HtmlElement):
        description = description.text_content()

    data = {'title': title,
            'time': time,
            'image': image,
            'description': description}

    return data


def write_json(file_name, data):
    with open(file_name + '.json', 'w') as f:
        json.dump(data, f)


def cities_sectons_parser(cities_sections_url):
    base_dict = {}
    
    for section_url in cities_sections_url:
        s_events_list = get_popular_links(get_html(section_url))

        b_dict={}
        for s_event_url in s_events_list:
            b_dict[s_event_url] = get_page_data(s_event_url)

        base_dict[section_url] = b_dict
        print(section_url + ' done')
        
    write_json('base_dict', base_dict)

    return base_dict

def cities_parser(cities_url):
    city_dict = {}
    
    for city in cities_url:
        events_list = get_popular_links(get_html(city))
        
        c_dict = {}
        for event_url in events_list:
            c_dict[event_url] = get_page_data(event_url)
        city_dict[city] = c_dict
        print(city + ' done')
    write_json('city_dict', city_dict)

    return city_dict

def sections_parser(sections_url): 
    section_dict = {}
    
    for section_url in sections_url:
        events_list = get_popular_links(get_html(section_url))
        
        s_dict = {}
        for event_url in events_list:
            s_dict[event_url] = get_page_data(event_url)
            
        section_dict[section_url] = s_dict
        print(section_url + ' done')
    write_json('section_dict', section_dict)
        
    return section_dict

def parser(cities_url, sections_url, cities_sections_url):
    city_dict = cities_parser(cities_url)
    section_dict = sections_parser(sections_url)
    base_dict = cities_sectons_parser(cities_sections_url)
    
    return city_dict, section_dict, base_dict
    

def main():
    # Names must be intuitive! 
    base_url = 'https://ticketon.kz'
    click(base_url)
     
    cities_url = get_city_link( base_url ) 
    sections_url = get_section_link( get_html(base_url) )
    
    cities_sections_url = []
    for i in cities_url:
        for j in sections_url:
            cities_sections_url.append(i + '/' + j.partition('https://ticketon.kz/')[2])
            
    parser(cities_url, sections_url, cities_sections_url)


if __name__ == '__main__':
    main()
