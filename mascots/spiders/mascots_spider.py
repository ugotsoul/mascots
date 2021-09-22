import scrapy
from mascots.items import MascotsItem


class MascotsSpider(scrapy.Spider):
	name = "mascots"
	allowed_domains = ["yurugp.jp"]

	def start_requests(self):
		# sort=1 local mascot, sort=2 company mascot
		yield scrapy.Request(f'https://www.yurugp.jp/en/ranking/?year={self.year}&sort={self.sort}&page={self.page}')

	def parse(self, response):
		profile_links = response.css('ul.chararank > li > a::attr(href)').getall()
		yield from response.follow_all(profile_links, callback=self.parse_mascot)

		next_page = response.css('div.paging > ul > li:nth-child(2) > a::attr(href)').get()
		
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)
	
	def parse_mascot(self, response):
		chara = response.css('div.chara')
		
		en_name = chara.css('div.charaname span.en::text').get()
		jp_name = chara.css('div.charaname h4::text').get()

		description_raw = chara.css('div.prof::text').getall()
		description = ''.join(description_raw).strip()
		
		image_url_raw = chara.css('div.charaimage img::attr(src)').get()
		image_url = response.urljoin(image_url_raw)

		is_local = self.sort == '1'  # spider arguments from cmdline are parsed as strings

		yield MascotsItem(
			name = en_name or jp_name, # TODO: translate this to english
			rank = chara.css('span.rank > strong::text').get(),
			region = chara.css('div.charaname span.region::text').get(),
			image_url = [image_url],
			description = description, # TODO: translate this to english
			is_local = is_local,
			year = self.year,
		)