import scrapy
import re

class RestaurantSpider(scrapy.Spider):
    name = "restaurant_spider"
    start_urls = [
        "https://guide.michelin.com/hk/zh_HK/hong-kong-region/hong-kong/restaurants/page/1?sort=distance"
    ]
    current_page_pointer = 1

    def parse(self, response):
        for restaurant in response.css(".card__menu-content.card__menu-content--flex.js-match-height-content"):
            name = restaurant.css("h3.card__menu-content--title.pl-text.pl-big.js-match-height-title a::text").get().strip()
            relative_url = restaurant.css("h3.card__menu-content--title a::attr(href)").get()
            restaurant_url = response.urljoin(relative_url)
            
            award_imgs = restaurant.css("img.michelin-award::attr(src)").getall()

            star_count = "No Award"
            distinction = "No Distinction"
            
            if any("bib-gourmand" in src for src in award_imgs):
                distinction = "必比登"
            elif any("1star" in src for src in award_imgs):
                star_count = sum(1 for src in award_imgs if "1star" in src)
                star_dict = {1:"一", 2:"二", 3:"三"}
                distinction = f"{star_dict[star_count]}星" if star_count > 0 else None
            
            footer_text = restaurant.css(".card__menu-footer--score.pl-text::text").getall()
            
            price_point = None
            cuisine_type = None
            
            for text in footer_text:
                text = text.strip()
                if '$' in text:
                    parts = text.split('·')
                    price_point = parts[0].strip()
                    if len(parts) > 1:
                        cuisine_type = parts[1].strip()

            # Instead of yielding here, request the restaurant page
            yield scrapy.Request(
                url=restaurant_url,
                callback=self.parse_restaurant,
                meta={
                    'restaurant_data': {
                        "餐廳名稱": name,
                        "推介": distinction,
                        "米芝蓮星星": star_count,
                        "價錢": price_point,
                        "菜式": cuisine_type,
                        "Restaurant Url": restaurant_url
                    }
                }
            )

        # Pagination Logic
        arrow_elements = response.css("div.js-restaurant__bottom-pagination li.arrow a")
        for arrow in arrow_elements:
            next_page_url = arrow.attrib.get("href")
            if next_page_url:
                match = re.search(r'/page/(\d+)', next_page_url)
                if match:
                    next_page_value = int(match.group(1))
                    if next_page_value > self.current_page_pointer:
                        self.current_page_pointer = next_page_value
                        full_next_page_url = response.urljoin(next_page_url)
                        yield scrapy.Request(url=full_next_page_url, callback=self.parse)

    def parse_restaurant(self, response):
        # Get the existing restaurant data from meta
        restaurant_data = response.meta['restaurant_data']
        
        # Extract address from the first data-sheet__block--text div
        address = response.css('div.data-sheet__block--text::text').get()

        if address:
            address = address.strip()
        
        # First try to get text from <p> inside div
        description = response.css('div.data-sheet__description p::text').get()
        # If no <p> text found, try getting direct text from div
        if not description:
            description = response.css('div.data-sheet__description::text').get()
        
        if description:
            description = description.strip()
                
        # Add new data to restaurant_data
        restaurant_data.update({
            "地址": address,
            "描述": description
        })
        
        yield restaurant_data

def run_spider():
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess(settings={
        "FEEDS": {
            "restaurants.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 2,
            },
        },
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_EXPORT_INDENT": 2,
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter'
    })
    
    process.crawl(RestaurantSpider)
    process.start()

if __name__ == "__main__":
    run_spider()