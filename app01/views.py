from django.shortcuts import render,redirect
# Create your views here.
from app01 import models
from django.http import HttpResponse

def book_list(request):
    ret = models.Book_list.objects.all()
    return render(request,'book_list.html',{'book_lists':ret})

def add_book(request):
    if request.method == "POST":
        print('add')
        new_book_name = request.POST['book_name']
        new_book_description = request.POST['book_description']
        new_book_country = request.POST['book_country']
        models.Book_list.objects.create(book_name=new_book_name, book_country=new_book_country,
                                     book_description=new_book_description)
        return redirect('/book_list/')
    return render(request, 'add_book.html')

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
    print('edit')
    edit_book_id=request.GET.get('id',None)
    print(edit_book_id)
    if edit_book_id:
        book_obj=models.Book_list.objects.get(book_id=edit_book_id)
        print(edit_book_id)
        return render(request,'edit_book.html',{'book_obj':book_obj})