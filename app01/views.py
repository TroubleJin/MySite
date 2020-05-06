from django.shortcuts import render,redirect
# Create your views here.
from app01 import models
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
import os

def book_list(request):
    ret = models.Book_list.objects.all()
    return render(request,'book_list.html',{'book_lists':ret})

def add_book(request):
    if request.method == "POST":
        print('add')
        new_book_name = request.POST['book_name']
        new_book_description = request.POST['book_description']
        new_book_country = request.POST['book_country']
        publisher_id = request.POST.get('publisher')
        # pub_obj=models.publisher_list.objects.get(publisher_id=publisher_id)
        models.Book_list.objects.create(book_name=new_book_name, book_country=new_book_country,
                                     book_description=new_book_description,book_publish_id=publisher_id)
        return redirect('/book_list/')
    all_pub_obj=models.publisher_list.objects.all()
    return render(request, 'add_book.html',{"all_pub_obj":all_pub_obj})

def remove_book(request):
    print('delete')
    print(request.GET)
    del_book_id=request.GET.get('id',None)
    if  del_book_id:
        models.Book_list.objects.get(book_id=del_book_id).delete()
    else:
        print('没有找到删除的id')
    return redirect('/book_list/')

def edit_book(request):
    if request.method == 'POST':
        edit_book_id=request.POST.get('book_id')
        print(request.POST)
        book_obj = models.Book_list.objects.get(book_id=edit_book_id)
        book_obj.book_name=request.POST.get('book_name')
        book_obj.book_description=request.POST.get('book_description')
        book_obj.book_country=request.POST.get('book_country')
        book_obj.book_publish_id = request.POST.get('publisher')
        book_obj.save()
        return redirect('/book_list/')
    edit_book_id=request.GET.get('id',None)
    all_publisher_obj = models.publisher_list.objects.all()
    if edit_book_id:
        book_obj=models.Book_list.objects.get(book_id=edit_book_id)
        print(edit_book_id)
        return render(request,'edit_book.html',{'book_obj':book_obj,'all_publisher_obj':all_publisher_obj})
    else:
        return HttpResponse('ERROR edit_book_id')

def publisher_list(request):
    all_publisher_obj=models.publisher_list.objects.all()
    return render(request,'publisher_list.html',{"publisher_list":all_publisher_obj})

# def add_publisher(request):
#     if request.method == "POST":
#         publisher_name=request.POST.get("publisher_name")
#         models.publisher_list.objects.create(publisher_name=publisher_name)
#         return redirect('/publisher_list/')
#     return render(request,'add_publisher.html')

class AddPublisher(View):
    def get(self,request):
        print(request.path_info)
        return render(request, 'add_publisher.html')
    def post(self,request):
        print(request.body)
        if request.method == "POST":
            publisher_name = request.POST.get("publisher_name")
            models.publisher_list.objects.create(publisher_name=publisher_name)
            return redirect('/publisher_list/')

def remove_publisher(request,publisher_id):
    print(type(publisher_id),publisher_id)
    models.publisher_list.objects.get(publisher_id=publisher_id).delete()
    return redirect('/publisher_list/')

def edit_publisher(request):
    if request.method == "POST":
        publisher_id = request.POST.get('publisher_id')
        publisher_name = request.POST.get('publisher_name')
        publisher_obj = models.publisher_list.objects.get(publisher_id=publisher_id)
        publisher_obj.publisher_name = publisher_name
        publisher_obj.save()
        return redirect('/publisher_list/')
    else:
        publisher_id=request.GET.get('id',None)
        num=request.GET.get('num',None)
        publisher_obj=models.publisher_list.objects.get(publisher_id=publisher_id)
        return render(request,'edit_publisher.html',{'publisher_obj':publisher_obj,'num':num})

def author_list(request):
    all_author_obj = models.Author.objects.all()
    # author_obj_1 = all_author_obj[0]
    #author_ojb.book是什么,是把作者对应数据库里面book_list表中的两条记录给你
    # print(author_obj_1.book.all()[0].book_publish_id)
    # for author_obj in author_obj_1.book.all():
    #     print(author_obj.book_name)
    return render(request,'author_list.html',{'all_author_obj':all_author_obj})


def add_author(request):
    if request.method == 'POST':
        new_author_name = request.POST.get('author')
        books = request.POST.getlist('books')
        print(new_author_name,books)
        author_obj=models.Author.objects.create(name=new_author_name)
        author_obj.book.set(books)
        return  redirect('/author_list/')
    all_book_obj = models.Book_list.objects.all()
    return render(request,'add_author.html',{'all_book_obj':all_book_obj})

def remove_author(request):
    del_id=request.GET.get('id')
    models.Author.objects.get(id=del_id).delete()
    return redirect('/author_list/')

def edit_author(request):
    if request.method == 'POST':
        author_id = request.POST.get('author_id')
        author_name = request.POST.get('author')
        books = request.POST.getlist('books')
        print(author_id,author_name,books)
        author_obj = models.Author.objects.get(id=author_id)
        author_obj.name = author_name
        author_obj.book.set(books)
        author_obj.save()
        return redirect('/author_list/')
    edit_id = request.GET.get('id')
    author_obj = models.Author.objects.get(id=edit_id)
    all_book_obj = models.Book_list.objects.all()
    return render(request,'edit_author.html',{'author_obj':author_obj,'all_book_obj':all_book_obj})


def upload(request):
    if request.method == 'POST':
        filename = request.FILES["upload_file"].name
        with open(filename,'wb') as f:
            for chunk in request.FILES["upload_file"].chunks():
                f.write(chunk)
        return HttpResponse('上传ok')
    else:
        return  render(request,'upload.html')
def download(request):
    if request.method == 'POST':
        download_path=request.POST.get('download_path')
        hostname=request.POST.get('hostname')
        env=request.POST.get('env')
        os.chdir('/data/devops/ansible/deployments')
        cmd_ansible = "ansible -i ../inventories/%s/internal_hosts %s -m fetch -a 'src=%s  dest=/data/'"%(env,hostname,download_path)
        return HttpResponse(cmd_ansible)
    return render(request,'download.html')

def json_test(request):
    return render(request,'json_test.html')

def index(request):
    redirect_url = reverse('json_test')
    return redirect(redirect_url)

def transfer(request):
    if request.method == 'POST':
        return HttpResponse('转账成功')
    return render(request,'transfer.html')