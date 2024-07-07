import bs4
import lxml
import requests
web_link = input("What Wikipedia article's images would you like to scrape?")
image_dir = input ("What directory would you like to save your images?")
image_name = input ("What would you like to name your images?")
req = requests.get(web_link)
wiki_soup = bs4.BeautifulSoup(req.text,'lxml')
n = 1
print('Scraping...')
for img in wiki_soup.select('.mw-file-description img'):
    img_link = img['src']
    img_link = requests.get('https:'+img_link)
    image = open(image_dir+'\\'+image_name+'_{}.jpg'.format(n),'wb')
    image.write(img_link.content)
    image.close()
    n+=1
print('Done!')