import json

from django.utils import timezone


class NewsService:
    def __init__(self, news_json_path, encoding='U8'):
        self.news_json_path = news_json_path
        self.encoding = encoding

    def _read_news(self):
        with open(self.news_json_path, encoding=self.encoding) as f:
            return json.load(f)

    def _filter_news(self, news, query):
        if query:
            return [article for article in news if query.lower() in article['title'].lower()]
        return news

    def _format_dates(self, news):
        for article in news:
            created_dt = timezone.datetime.strptime(article['created'], '%Y-%m-%d %H:%M:%S')
            article['created_date'] = created_dt.strftime('%Y-%m-%d')
        return news

    def get_news(self, query=None):
        news = self._read_news()
        news = self._filter_news(news, query)
        news = self._format_dates(news)
        news.sort(key=lambda x: (x['created_date'], x['created']), reverse=True)
        return news

    def get_single(self, link):
        return next((article for article in self._read_news() if link == article['link']), None)

    def add(self, title, text):
        articles = self._read_news()
        link = max(article['link'] for article in articles) + 1 if articles else 1
        new_article = {
            'created': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'text': text,
            'title': title,
            'link': link,
        }
        articles.append(new_article)

        with open(self.news_json_path, mode='w', encoding=self.encoding) as f:
            json.dump(articles, f)
