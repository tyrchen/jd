from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from jd.items import Employee
from scrapy.selector import HtmlXPathSelector


class DirectorySpider(CrawlSpider):
    name = 'directory'
    allowed_domains = ['core.juniper.net']
    start_urls = [
        "http://core.juniper.net/directory/detail.asp?uid=jk",
    ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(SgmlLinkExtractor(
            allow=('OrgChart\.asp', ),
            deny=('nawaf', )),
        ),

        # Extract links matching 'item['php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(
            allow=('detail\.asp', 'Detail\.asp'),
            deny=('nawaf',)),
            callback='parse_item'
        ),
    )

    def get_text(self, hxs, xpath):
        try:
            return hxs.select('%s/text()' % xpath).extract()[0].strip()
        except:
            return ''

    def get_image(self, hxs, xpath):
        try:
            return hxs.select('%s/@src' % xpath).extract()[0].strip()
        except:
            return ''

    def get_address(self, hxs):
        addr = self.get_text(hxs, '/html/body/table[2]/tbody/tr[14]/td[2]')
        city = self.get_text(hxs, '/html/body/table[2]/tbody/tr[15]/td[2]')
        state = self.get_text(hxs, '/html/body/table[2]/tbody/tr[16]/td[2]')
        zipcode = self.get_text(hxs, '/html/body/table[2]/tbody/tr[17]/td[2]')
        country = self.get_text(hxs, '/html/body/table[2]/tbody/tr[18]/td[2]')

        return ' '.join([addr, city, state, zipcode, country])

    def parse_item(self, response):
        print('Crawling %s' % response.url)

        hxs = HtmlXPathSelector(response)
        item = Employee()
        item['uid'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[4]/td[2]')
        item['email'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[5]/td[2]/a')
        item['cube'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[6]/td[2]')
        item['manager'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[9]/td[2]/a')
        item['department'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[10]/td[2]/a')
        item['address'] = self.get_address(hxs)
        item['preferred_name'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[4]/td[3]/table/tr/td/table/tr[1]/td[2]')
        item['phone'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[4]/td[3]/table/tr/td/table/tr[2]/td[2]')
        item['extension'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[4]/td[3]/table/tr/td/table/tr[3]/td[2]')
        item['mobile'] = self.get_text(hxs, '/html/body/table[2]/tbody/tr[4]/td[3]/table/tr/td/table/tr[5]/td[2]')
        item['photo_url'] = self.get_image(hxs, '/html/body/table[2]/tbody/tr[4]/td[3]/table/tr/td/span/img')
        return item
