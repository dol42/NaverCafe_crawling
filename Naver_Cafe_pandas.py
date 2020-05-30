import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd

#변수 기본값 지정

dir_driver = "C:/Users/HMH/Desktop/20200530/chromedriver"

url = 'https://nid.naver.com/nidlogin.login'
id = ""
pw = ""

driver = webdriver.Chrome(dir_driver)
driver.get(url)
driver.implicitly_wait(2) #기본적으로는 웹 자원이 모두 로드되는걸 기다리지만 혹시 모르니 직접 지정해줌.

# execute_script 함수 사용하여 자바스크립트로 id,pw 넘겨주기
driver.execute_script("document.getElementsByName('id')[0].value=\'"+id+"\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+pw+"\'")

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(1)

# 로그인 정보 저장안함 클릭하기
login_btn = driver.find_element_by_id('new.dontsave')
login_btn.click()
time.sleep(1)

# 내가 검색하려는 카페 주소 입력하기
baseurl = 'https://cafe.naver.com/joonggonara/'
driver.get(baseurl)

# &search.menuid = : 게시판 번호
# &search.page = : 데이터 수집 할 페이지 번호 
# &userDisplay = 50 : 한 페이지에 보여질 게시글 수

clubid = 10050146
menuid = 338
pageNum = 1
userDisplay = 50

driver.get(baseurl + 'ArticleList.nhn?search.clubid=' + str(clubid) + '&search.menuid=' + str(menuid) +'&search.page='+ str(pageNum) +'&userDisplay=' + str(userDisplay))
driver.switch_to.frame('cafe_main') #iframe으로 접근

soup = bs(driver.page_source ,'html.parser')
soup = soup.find_all(class_ = 'article-board m-tcol-c')[1]# 네이버 카페 구조 확인후 게시글 내용만 가저오기
#datas = soup.find_all('td', class_ = 'td_article')

datas = soup.find_all(class_ = 'td_article')
for data in datas:

    article_title = data.find(class_ = 'article')
    link = article_title.get('href')
    article_title = article_title.get_text().strip()
    #print(article_title)
    #print(baseurl + link)
    
    pandasData = {"title":[article_title], "link":[baseurl + link]}
    db=pd.DataFrame(pandasData, columns=('title','link'))
    db.to_csv('DB.csv', mode='a+',index=False,header=False, encoding = "euc-kr")
    
    
print('종료')
driver.close()
