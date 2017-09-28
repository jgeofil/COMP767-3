import scrapy
import string

class WhoDatesWhoSpider(scrapy.Spider):
    name = "who_dates_who"

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        'LOG_LEVEL': 'INFO'
    }

    base_url = 'http://www.whosdatedwho.com'
    start_urls = ['http://www.whosdatedwho.com/popular?letter='+ c for c in ['o','p','q','r','s','t','u','v','w','x','y','z']]

    recalls = []

    def parse(self, response):
        person_links = response.css('li.ff-grid-box a ::attr(href)').extract()

        next_page = response.css('a.ff-inext ::attr(href)').extract()[0]

        if len(person_links) > 0:
            yield scrapy.Request(self.base_url + next_page)

        for link in person_links:
            yield scrapy.Request(link, callback=self.parse_person)


    def parse_person(self, response):

        try:
            container = response.css('div.ff-cont-main')[0]
            ages = response.css('div.small.age div.fact ::text').extract()

            table = container.css('h4.ff-auto-details + table tr')
            dating = container.css('div#ff-dating-history-grid div.ff-grid-box')

            dates = []

            for date in dating:
                date_obj = dict()
                date_obj['id'] = date.css('::attr(id)').extract()[0].replace('dating-','')
                date_obj['up'] = int(date.css('i.icon-thumbs-up + v ::text').extract()[0])
                date_obj['down'] = int(date.css('i.icon-thumbs-down + v ::text').extract()[0])
                dates.append(date_obj)

            obj = {'dates': dates, 'id': response.url.split('/')[-1]}

            for tr in table:
                td = tr.css('td ::text').extract()
                obj[td[0]] = td[1].strip('\t\n')

            yield obj

        except IndexError:
            if response.url in WhoDatesWhoSpider.recalls:
               raise RuntimeError
            else:
                WhoDatesWhoSpider.recalls.append(response.url)
                yield scrapy.Request(response.url, callback=self.parse_person)

