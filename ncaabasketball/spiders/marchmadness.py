import scrapy
from datetime import datetime, timedelta

'''
Uses Scrapy library to scrape the 2021 scoreboard of marchmadness from March 18th to April 6th.
Can easily be adapted for other NCAA scoreboards just by changing the 'start_urls' and 'date'
Can be run with 'scrapy crawl 'your_project_name' -O marchmadness2021.json' on the terminal to create a json
file with the keys below.
'''

class MarchMadness(scrapy.Spider):
    date = datetime(2021, 3, 18) # Beginning of March Madness
    stop_condition = 18 # Goes on for 18 days
    name = 'marchmadness' # Project unique name for the Spyder
    start_urls = [f"https://www.ncaa.com/scoreboard/basketball-men/d1/{date.strftime('%Y/%m/%d')}"] # 'year/month/day'

    def parse(self, response):
        games = response.css('div.gamePod-type-game')

        for game in games:
            game_name = game.css('span.game-round')
            if game is not None and len(game_name) != 0 : # if either of this is true, ignore
                yield {
                    'game_date': self.date.strftime('%m/%d/%Y'), # 'month/day/year'
                    'game_name': game_name.css('::text').get(),
                    'game_status': game.css('div.gamePod-status::text').get(),
                    'game_video': game.css('a.gamePod-link::attr(href)').get(),
                    'winner_name': game.css('li.winner .gamePod-game-team-name::text').get(), # 'li.winner' is the winning team
                    'second_name': game.css('li:not(winner) .gamePod-game-team-name::text').get(), #'li:not(winner)' is the losing team
                    'winner_rank': game.css('li.winner .gamePod-game-team-rank::text').get(),
                    'second_rank':  game.css('li:not(winner) .gamePod-game-team-rank::text').get(),
                    'winner_score': game.css('li.winner .gamePod-game-team-score::text').get(),
                    'second_score': game.css('li:not(winner) .gamePod-game-team-score::text').get(),
                    'winner_logo': game.css('li.winner .gamePod-game-team-logo::attr(src)').get(),
                    'second_logo': game.css('li:not(winner) .gamePod-game-team-logo::attr(src)').get()
                }
        if self.stop_condition>0:
            self.date += timedelta(days=1) # add day to date obj
            url= f"https://www.ncaa.com/scoreboard/basketball-men/d1/{self.date.strftime('%Y/%m/%d')}"
            self.stop_condition-=1
            yield scrapy.Request(url=url, callback=self.parse) # Follow the link again
