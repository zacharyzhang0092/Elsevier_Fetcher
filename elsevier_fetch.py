from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()





class ElsevierFetcher:
    def __init__(self, journal):
        self.subject = journal
        self.base_url = 'https://www.sciencedirect.com'


    def fetch_journal(self):
        url_journal = "https://www.sciencedirect.com/journal/"+self.subject+"/issues"
       
        r_journal = session.get(url_journal)
        issues = r_journal.html.find('span.accordion-title')
        issues_list = []
        for issue in issues:
            issue_name = issue.text
            issues_list.append(issue_name)
        #issues_list_df = pd.DataFrame(issues_list).iloc[3:]
        imglist = []
        for img in r_journal.html.find('img'):
            imglist.append(img.attrs['src'])
        img = imglist[2]

        return issues_list, img

    def fetch_articles(self,Volume_choose):        
        url = "https://www.sciencedirect.com/journal/"+ self.subject +"/vol/"+ Volume_choose +"/suppl/C"
        r = session.get(url)

        info_list = []
        articles = r.html.find('a.anchor.article-content-title.u-margin-xs-top.u-margin-s-bottom.anchor-default')
        for article in articles:
            
            #文章链接
            link = self.base_url + article.attrs.get('href')
            article_url = link
            article_r = session.get(article_url)
            
            #文章名
            article_name = article_r.html.find('span.title-text')[0].text

            #文章摘要
            abstract = article_r.html.find('div.abstract.author')
            if abstract:
                abstract = abstract[0].text.strip('Abstract')
            else:
                abstract = ''
            
            #文章亮点
            highlights = article_r.html.find('div.abstract.author-highlights')
            if highlights:
                highlights_list = [highlight.text for highlight in highlights]
                highlights_str = '\n'.join(highlights_list)
            else:
                highlights_str = ''
            
            #文章关键词
            keywords = article_r.html.find('div.keyword')
            if keywords:
                keywords_list = [keyword.text for keyword in keywords]
                keywords_str = '\n'.join(keywords_list)
            else:
                keywords_str = ''

            list = [article_name, keywords_str, highlights_str, abstract, link]
            info_list.append(list)

        info_df = pd.DataFrame(info_list)
        info_df.columns = ['标题', '关键词', '亮点', '摘要', '链接']
         
        ###如果存在page2
        page2 = r.html.find('div.pagination.text-s.u-margin-l-top')
        
        if page2:
            page2_url = url + '?page=2'
            page2_r = session.get(page2_url)
            articles2 = page2_r.html.find('a.anchor.article-content-title.u-margin-xs-top.u-margin-s-bottom.anchor-default')
            
            for article2 in articles2:
        
                #文章链接
                link2 = self.base_url + article2.find('a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default')['href']
                article_url2 = link2
                article_r2 = session.get(article_url2)

                #文章名
                article_name2 = article_r2.html.find('span.title-text')[0].text

                #文章摘要
                abstract2 = article_r2.html.find('div.abstract.author')
                if abstract2:
                    abstract2 = abstract2[0].text.strip('Abstract')
                else:
                    abstract2 = ''
                
                #文章亮点
                highlights2 = article_r2.html.find('li.react-xocs-list-item')
                if highlights2:
                    highlights_list2 = [highlight.text for highlight in highlights2]
                    highlights_str2 = '\n'.join(highlights_list2)
                else:
                    highlights_str2 = ''

                #文章关键词
                keywords2 = article_r2.html.find('div.keyword')
                if keywords2:
                    keywords_list2 = [keyword.text for keyword in keywords2]
                    keywords_str2 = '\n'.join(keywords_list2)
                else:
                    keywords_str2 = ''

                
                list2 = [article_name2, keywords_str2, highlights_str2, abstract2, link2]
                info_list.append(list2)

            info_df = pd.DataFrame(info_list)
            info_df.columns = ['标题', '关键词', '亮点', '摘要', '链接']
            
            
        else:
            info_df=info_df
            

        return info_df


