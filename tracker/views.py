from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from .models import Item
from .forms import AddNewItemForm
from urllib import request
from bs4 import BeautifulSoup

def tracker_view(request):
	items=Item.objects.order_by('-id')
	form=AddNewItemForm(request.POST)
	if request.method=='POST':
		if form.is_valid():
			url=form.cleaned_data.get('url')
			requested_price=form.cleaned_data.get('requested_price')
			#crawling the data
			crawled_data=crawl_data(url)
			Item.objects.create(url=url,title=crawled_data['title'],requested_price=requested_price,last_price=crawled_data['last_price'],discount_price='No discount yet',)
			return HttpResponseRedirect('')
		else:
			form=AddNewItemForm()
	context={'items':items,'form':form,}
	return render(request,'tracker.html',context)			

def crawl_data(url):
	req=Request(url,headers={'User-Agent':'Mozilla/5.0'}) #user agent removes 403 error
	html=urlopen(req).read()
	bs=BeautifulSoup(html,'html.parser')
	title=bs.find('h1',id="itemTitle").get_text().replace("Details about","")
	price=bs.find('span',id="prcIsum").get_text()
	clean_price=float(price.strip().replace("US","").replace("$",""))
	return { 'title':title,'last_price':clean_price}
