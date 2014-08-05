# Scrapy settings for jd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'jd'

SPIDER_MODULES = ['jd.spiders']
NEWSPIDER_MODULE = 'jd.spiders'

ITEM_PIPELINES = [
    'jd.pipelines.MongoPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Bot'
