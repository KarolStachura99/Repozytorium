import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class OlxSpider(CrawlSpider):
    name = 'olx_spider'
    allowed_domains = ['olx.pl']
    start_urls = ['https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/krakow/?search%5Bprivate_business%5D=private']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5, # Opóźnienie 0.5 sekundy między zapytaniami
    }
    
    max_items = 300  # Maksymalna liczba ofert do pobrania
    item_count = 0   # Licznik pobranych ofert


    def parse_item(self, response):
        if self.item_count >= self.max_items:
            self.crawler.engine.close_spider(self, f"Zakończono scrapowanie: pobrano {self.max_items} mieszkań z 7 parametrami.")
            return
        
        self.item_count += 1
        
        if "olx.pl" in response.url:
            yield {
                'Nazwa': response.xpath('//h4[@class="css-yde3oc"]/text()').get(),
                'Cena': response.xpath('//h3[@class="css-fqcbii"]/text()').get(),
                'Cena_za_m2': response.xpath('//p[@class="css-1wgiva2"][contains(text(), "Cena za m²:")]/text()').get(default='').replace("Cena za m²:", "").strip(),
                'Powierzchnia': response.xpath('//p[contains(@class, "css-1wgiva2")][contains(., "Powierzchnia")]/text()').get(default='').replace("Powierzchnia:", "").strip(),
                'Liczba_pokoi': response.xpath('//p[@class="css-1wgiva2"][contains(text(), "Liczba pokoi:")]/text()').get(default='').replace("Liczba pokoi:", "").strip(),
                'Rodzaj_zabudowy': response.xpath('//p[@class="css-1wgiva2"][contains(text(), "Rodzaj zabudowy:")]/text()').get(default='').replace("Rodzaj zabudowy:", "").strip(),
                'Rynek': response.xpath('//p[@class="css-1wgiva2"][contains(text(), "Rynek:")]/text()').get(default='').replace("Rynek:", "").strip(),
                'Opis': ' '.join(response.xpath('//div[@data-cy="ad_description"]//text()[not(ancestor::style)]').getall()).replace('\n', ' ').replace('\t', ' ').strip(),
                'url': response.url,
            }

        elif "otodom.pl" in response.url:
            yield {
                'Nazwa': response.xpath('//h1[@data-cy="adPageAdTitle"]/text()').get(),
                'Cena': response.xpath('//strong[@aria-label="Cena"]/text()').get(),
                'Cena_za_m2': response.xpath('//div[@class="css-z3xj2a e1k1vyr25"]/text()').get(),
                'Powierzchnia': response.xpath('//div[@class="css-1ftqasz"][contains(text(), "m²")]/text()').get(),
                'Liczba_pokoi': response.xpath('//div[@class="css-1ftqasz"][contains(text(), "pokoje")]/text()').get(),
                'Rodzaj_zabudowy': response.xpath('//p[contains(text(), "Rodzaj zabudowy")]/following-sibling::p[1]]/text()').get(),
                'Rynek': response.xpath('//p[contains(text(), "Rynek")]/following-sibling::p/text()').get(),
                'Opis': ' '.join(response.xpath('//div[@data-cy="adPageAdDescription"]//text()').getall()).replace('\n', ' ').replace('\t', ' ').strip(),
                'url': response.url,
            }
