from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
import json

USER = '1VxHpbTkJX'
PASS = 'MBy22z@ckD@%'
SOCS = ['general', 'science_&_technology', 'gaming', 'politics', 'arts_&_entertainment',
        'health_&_lifestyle', 'empeopled_meta_discussion', 'hearthstone']

COMMENTS = []

DATA = []

def init_driver():

    driver = webdriver.Chrome('./chromedriver')
    driver.wait = WebDriverWait(driver, 5)
    driver.implicitly_wait(0.1)  # seconds
    return driver

def recurse_comments(com_obj, target, soc):
    id = com_obj.get_attribute('id')
    author = com_obj.find_element_by_css_selector('span.author a').text.split('\n')[0]
    try:
        comment_text = com_obj.find_element_by_css_selector('div.expander-content > div.contextualinfo + div > div.comment-content span p').text
    except:
        comment_text = ''

    print(comment_text)

    children = com_obj.find_elements_by_css_selector('#comment_children'+id.split('_')[-1]+' > div.comment')
    [recurse_comments(c, author, soc) for c in children]

    COMMENTS.append({
        'source': author,
        'target': target,
        'text': comment_text
    })

    return

def unfold_comments(container):

    coms = container.find_element_by_css_selector('div.comments')

    numcoms = 0
    more = True
    while (more):
        print(numcoms)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        commenters = coms.find_elements_by_css_selector('span.author a')
        if len(commenters) > numcoms:
            more = True
            numcoms = len(commenters)
        else:
            more = False


def lookup(driver, query):

    for so in SOCS:

        driver.get('https://empeopled.com/t/'+so)
        time.sleep(2)
        new_btn = driver.find_element_by_css_selector('a[data-val="2"]')
        new_btn.click()
        time.sleep(1)

        post_objs = []
        while len(post_objs) < 200:
            post_objs = driver.find_elements_by_css_selector('div.post')
            print(len(post_objs))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        links = [post.find_element_by_css_selector('a.post-link').get_attribute('href') for post in post_objs]
        print(links)

        for l in links:
            driver.get(l)
            time.sleep(1)

            cont = driver.find_element_by_css_selector('div.container')

            soc = cont.find_element_by_css_selector('a.society-name').text
            post_author = cont.find_element_by_css_selector('p.contextualinfo a').text.split('\n')[0]

            com_count = driver.find_element_by_css_selector('a.post-link b.comments-count').text
            print(com_count)
            com_count = int(com_count) if com_count.isdigit() else 0

            unfold_comments(cont)
            first_level_comments = cont.find_elements_by_css_selector('div.comments > div > div.comment')
            [recurse_comments(c, post_author, soc) for c in first_level_comments]

            titles = driver.find_elements_by_css_selector('.post-title')
            [print(t.text) for t in titles]

            post = {
                'title': titles[1].text,
                'author':{
                    'author': post_author,
                    'level': int(cont.find_element_by_css_selector('span.user-level strong').text)
                },
                'soc': soc,
                'date': int(cont.find_element_by_css_selector('span[data-since-date]').get_attribute('data-since-date')),
                'votes': int(cont.find_element_by_css_selector('span.vote-sum').text),
                'comments': com_count,
                'content': cont.find_element_by_css_selector('div.full-body.richtext').text
            }

            print(json.dumps(post, indent=2))

            DATA.append(post)

    with open('emd.json', 'w+') as fp:
        json.dump(DATA, fp, indent=2)

    with open('edges.json', 'w+') as fp:
        json.dump(COMMENTS, fp, indent=2)



if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    time.sleep(5)
    driver.quit()
