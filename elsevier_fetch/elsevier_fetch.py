
import requests
from bs4 import BeautifulSoup
import pandas as pd




class ElsevierFetcher:
    def __init__(self, journal):
        self.subject = journal
        self.base_url = 'https://www.sciencedirect.com'


    def fetch_journal(self):
        url_journal = "https://www.sciencedirect.com/journal/"+self.subject+"/issues"
        headers = {
                'user-agent': '(Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'    
            }
        r_journal = requests.get(url_journal, headers=headers)
        soup_journal = BeautifulSoup(r_journal.text, 'html.parser')
        issues = soup_journal.find_all('li', class_='accordion-panel')
        issues_list = []
        for issue in issues:
            issue_name = issue.find('span', class_='accordion-title').text
            issues_list.append(issue_name)
        #issues_list_df = pd.DataFrame(issues_list).iloc[3:]
        img = soup_journal.find('a', class_='anchor js-cover-image-link anchor-default').find('img')['src']

        return issues_list, img

    def fetch_articles(self,Volume_choose):        
        url = "https://www.sciencedirect.com/journal/"+ self.subject +"/vol/"+ Volume_choose +"/suppl/C"
        headers = {
                'user-agent': '(Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'    
            }
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        Volume = soup.find('div', class_='col-md-16 u-padding-l-right-from-md u-margin-l-bottom').find('h2').text
        Date = soup.find('div', class_='col-md-16 u-padding-l-right-from-md u-margin-l-bottom').find('h3').text


        info_list = []
        articles = soup.find_all('li', class_='js-article-list-item article-item u-padding-xs-top u-margin-l-bottom')
        for article in articles:
            #文章名
            en_title = article.find('span', class_='js-article-title').text
            #文章链接
            link = self.base_url + article.find('a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default')['href']
            article_url = link
            article_r = requests.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_r.text, 'html.parser')
            #文章摘要
            #abstract = article_soup.findAll('div', class_='abstract author')[0].text.strip('Abstract')
            abstract = article_soup.findAll('div', class_='abstract author')
            if abstract:
                abstract = abstract[0].text.strip('Abstract')
            else:
                abstract = ''
            #文章亮点
            #highlights = article_soup.findAll('div', class_='abstract author-highlights')[0].text.strip('Highlights')
            highlights = article_soup.findAll('div', class_='abstract author-highlights')
            if highlights:
                highlights = highlights[0].findAll('li', class_='react-xocs-list-item')
                highlights_list = [highlight.text for highlight in highlights]
                highlights_str = '\n'.join(highlights_list)
            else:
                highlights_str = ''
            #文章关键词
            #keywords_div = article_soup.findAll('div', class_="keywords-section")[0].findAll('div', class_='keyword')
            #keywords_list = [keyword.text for keyword in keywords_div]
            keywords_div = article_soup.findAll('div', class_="keywords-section")
            if keywords_div:
                keywords_div = keywords_div[0].findAll('div', class_='keyword')
                keywords_list = [keyword.text for keyword in keywords_div]
                keywords_str = '\n'.join(keywords_list)
                
            else:
                keywords_str = ''
            
            list = [en_title, keywords_str, highlights_str, abstract, link]
            info_list.append(list)

        info_df = pd.DataFrame(info_list)
        info_df.columns = ['标题', '关键词', '亮点', '摘要', '链接']
        
        
        #info_df.to_csv(f'D:\my_python\Science_Direct\{self.subject}_{Volume}_{Date}.csv',encoding='utf-8-sig') 
        #info_df.to_html(f'D:\my_python\Science_Direct\{self.subject}_{Volume}_{Date}.html', encoding='utf-8-sig')
        
        
        #如果存在page2
        page2 = soup.find('div', class_='pagination text-s u-margin-l-top')
        info_df2 = None
        if page2:
            page2_url = url + '?page=2'
            page2_r = requests.get(page2_url, headers=headers)
            page2_soup = BeautifulSoup(page2_r.text, 'html.parser')
            articles2 = page2_soup.find_all('li', class_='js-article-list-item article-item u-padding-xs-top u-margin-l-bottom')
            info_list2 = []
            for article2 in articles2:
                #文章名
                en_title2 = article2.find('span', class_='js-article-title').text
                #文章链接
                link2 = self.base_url + article2.find('a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default')['href']
                article_url2 = link2
                article_r2 = requests.get(article_url2, headers=headers)
                article_soup2 = BeautifulSoup(article_r2.text, 'html.parser')
                #文章摘要
                #abstract = article_soup.findAll('div', class_='abstract author')[0].text.strip('Abstract')
                abstract2 = article_soup2.findAll('div', class_='abstract author')
                if abstract2:
                    abstract2 = abstract2[0].text.strip('Abstract')
                else:
                    abstract2 = ''
                #文章亮点
                #highlights = article_soup.findAll('div', class_='abstract author-highlights')[0].text.strip('Highlights')
                highlights2 = article_soup2.findAll('div', class_='abstract author-highlights')
                if highlights2:
                    highlights2 = highlights2[0].findAll('li', class_='react-xocs-list-item')
                    highlights_list2 = [highlight2.text for highlight2 in highlights2]
                    highlights_str2 = '\n'.join(highlights_list2)
                else:
                    highlights_str2 = ''
                #文章关键词
                #keywords_div = article_soup.findAll('div', class_="keywords-section")[0].findAll('div', class_='keyword')
                #keywords_list = [keyword.text for keyword in keywords_div]
                keywords_div2 = article_soup2.findAll('div', class_="keywords-section")
                if keywords_div2:
                    keywords_div2 = keywords_div2[0].findAll('div', class_='keyword')
                    keywords_list2 = [keyword2.text for keyword2 in keywords_div2]
                    keywords_str2 = ''
                    for keyword2 in keywords_list2:
                        keywords_str2 = keywords_str2 + keyword2 + '\n'
                else:
                    keywords_str2 = ''
                
                list2 = [en_title2, keywords_str2, highlights_str2, abstract2, link2]
                info_list2.append(list2)
            info_df2 = pd.DataFrame(info_list2)
            info_df2.columns = ['标题', '关键词', '亮点', '摘要', '链接']
            
        else:
            info_df2 = []
            

        return info_df, info_df2


'''
if __name__ == '__main__':
    journal = input('请输入要爬取的期刊名称：')
    journal_fetcher = ElsevierFetcher(journal)
    issues_list = journal_fetcher.fetch_journal()
    print(issues_list)

    Volume_choose = input('请输入要爬取的卷数：')
    DF = journal_fetcher.fetch_articles(Volume_choose)
    print(DF)
'''

