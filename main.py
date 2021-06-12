from selenium import webdriver
from pathlib import Path
import fake_useragent
import pandas

#путь к папке скрипта
#path to script dir
current_dir = Path(__file__).resolve().parent

#fake user agent
fake_user = fake_useragent.UserAgent().random

####создаю настройки/create settings
option = webdriver.FirefoxOptions()
#скрываем что заходим через бота
#hide that we go through the bot
option.set_preference('dom.webdriver.enabled', False)
#выключаю уведомления/turn off notifications
option.set_preference('dom.webnotifications.enabled', False)
#выключаю звук/turn off volume
option.set_preference('media.volume_scale', '0.0')
#меняю useragent/change useragent
option.set_preference('general.useragent.override', fake_user)

#показывать окно или нет
#show window or no
option.headless = False

browser = webdriver.Firefox(options=option)

# db = [
#	{'date':str(date), 'name':namepost, 'url':urlpost, 'text':textpost, 'tags':tag},
#	{'date':str(date), 'name':namepost, 'url':urlpost, 'text':textpost, 'tags':tag},]
db = []

def pars_page(url):
	tag = []
	date = ''

	#беру из ссылки(url) дату
	#take from url date
	#https://zadolba.li/20090908
	#['https:','','','zadolba.li','20090908']
	date = url.split('/')[-1]

	#заходит на сайт url
	#enter to site from url
	browser.get(url)

	#нахожу все посты на странице
	#finds all posts on page
	posts = browser.find_elements_by_class_name("story")
	for post in posts:
		#нахожу название поста
		#find name post
		title = post.find_element_by_tag_name('h2').text

		#нохожу тект самого поста
		#find the text of the post
		textpost = post.find_element_by_class_name("text").text

		idpost = post.find_element_by_class_name("id").text
		#вставляю id в ссылку поста 
		#insert id in post link 
		urlpost = f'https://zadolba.li/story/{idfinder}'
		
		try:
			#векта с тегами/tree of the tags
			tagblockpost = post.find_element_by_class_name("tags")	

			#нахожу все теги из ветки/find all tags from tree
			tagspost = tagblockpost.find_elements_by_tag_name("li")

			for tagpost in tagspost:
				#добавляю каждый тег/add every tag
				tag.append(tagpost.text)
		except Exception:
			#если тегов нету, то в db отправится эта надпись
			#if there are no tags, then this inscription will be sent to db 
			tag.append('Тегов нет./No tags')
		#добавляю полученую информацию в db/add the received information to db
		db.append({'date':str(date), 'name':title, 'url':urlpost, 'text':textpost, 'tags':tag})
		#обнуляю массив tag
		#zeroing array tag
		tag = []
	
# https://zadolba.li/20090908
# самая старая на этом сайте\
# most old page on this site/
pars_page('https://zadolba.li/20090908')
print('Парсинг начался./ Parsing begin.')

#while True:
for i in range(1, 100):
	try:
		#нахожу кнопку "следующая страница"
		#find button "next page"
		nextbtn = browser.find_element_by_class_name("next")

		#беру там ссылку на следующую страницу
		#take from button url to next page
		urlnextpage = nextbtn.find_element_by_tag_name('a').get_attribute("href")

		pars_page(urlnextpage)
		print(f'Страниц пройдено:{i}./Pages complete:{i}.')
	except Exception:
		print('Больше страниц нету./No more pages.')
		#break

datedb = []
namedb = []
urldb = []
textdb = []
tagdb = []
for post in db:
	datedb.append(post['date'])
	namedb.append(post['name'])
	urldb.append(post['url'])
	textdb.append(post['text'])
	tagdb.append(post['tags'])

#создаю словарь info для удобства
#creating info dictionary for convenience 
info = {
	'date': datedb,
	'name': namedb,
	'url': urldb,
	'text': textdb,
	'tags': tagdb,
}

#удаляю все ненужную информацию из памяти
#delete all unnecessary information from memory
del datedb, namedb, urldb, textdb, tagdb

#create DataFrame
df = pandas.DataFrame(info)

#создаю .xlsx файл из dataframe
#create .xlsx file from dataframe
df.to_excel(f'{current_dir}\\result.xlsx')