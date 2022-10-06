import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://yoderandfrey.com/en/equipment-search/1/?searchTerm={}'

class FreySpider(scrapy.Spider):
    name = 'frey'
    headers= {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
    def start_requests(self):        
        for index in df:            
            yield scrapy.Request(base_url.format(index), headers = self.headers,meta={"pyppeteer": True},cb_kwargs={'index':index})

    def parse(self, response, index):
        """Pagination"""
        total_pages = response.xpath("//ul[@class='pagination ng-scope']/li[last()-1]/a/text()").get()
        # print(total_pages)
        current_page = response.xpath("//li[@class='ng-scope current']/span/text()").get()
        # print(current_page)
        url = response.url      
       
        if total_pages and current_page:            
            if int(current_page) ==1:                
                for i in range(2, int(total_pages)+1):                   
                    min = str(i-1)
                    max = str(i)
                    url = url.replace(min,max)                                
                    yield response.follow(url, cb_kwargs={'index':index},headers = self.headers)
                   
        products = response.css(".equipment-item")
        images = response.xpath("//*[@class='equipment-item-image']/a/img/@ng-src").getall()
        counter = 0
        for item in products:
            print("........................................................................................")
            link = 'https://yoderandfrey.com'+item.css(".equipment-item-image a::attr(href)").get() 
            print(link)  
            image = images[counter]
            counter = counter+1
            print(image)
            name = item.css(".equipment-item-text h2 a::text").get().strip()
            print(name)
            location = item.xpath("//div[@class='equipment-item-footer']/p[@class='ng-binding']/text()").get()
            print(location)
            date = item.xpath("//div[@class='equipment-item-footer']/p[@class='ng-binding']/span/text()").get()
            print(date)
            description = item.css(".equipment-item-text p::text").get()
            print(description)
            auctioner = "Selling in Yoder & Frey"
            print(auctioner)
            lot = link.split('=')
            lot_id = lot[1]
            print(lot_id) 
            print(index)               
       
            yield{
                'product_url' : link,
                'item_type' : index,
                'image_link' : image,
                'product_name': name,
                'auction_date' : date,
                'location' : location,            
                'lot_id' : lot_id,
                'auctioner' : auctioner,
                'website' : "yoderandfrey",
                'description' : description
            }
        


   