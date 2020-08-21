from django.shortcuts import render
from .models import Product
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from pdapp.models import *
from django.db.models import Avg
# Create your views here.

# 메인 페이지
def index(request): #랭킹불러옴
    stars=Star.objects.all()
    rank_all = stars.values('pdname').annotate(avg_stars=Avg('star')).order_by('-avg_stars')
    #pdname 별로 star의 평균값을 avg_stars에 넣고,내림차순정렬
    product=Product.objects.all()
    first = rank_all.first() #1등을 따로 뺌(dic형으로 형변환이 됨 이거는 쿼리셋아님 )
    k= first['pdname']
    prod_first = Product.objects.get(id = int(k))
    return render(request,'index.html', {'rank_all' : rank_all , 'product' : product, 'prod_first' : prod_first })

# 상품 페이지
def item_body(request):
    body=Product.objects.filter(pdtype=1) #id1이 바디
    body2=Star.objects.filter(pdtype_id=1)
    body_star = body2.values('pdname').annotate(avg_stars=Avg('star'))

    return render(request,'item_body.html', {'body_star':body_star,'body':body})


def item_lens(request):
    lens=Product.objects.filter(pdtype=2) #id2는 렌즈
    lens2=Star.objects.filter(pdtype_id=2)
    lens_star = lens2.values('pdname').annotate(avg_stars=Avg('star'))

    return render(request,'item_lens.html', {'lens_star':lens_star,'lens':lens})

# 랭킹 페이지
def rank(request):
    stars=Star.objects.all()
    body=Product.objects.filter(pdtype=1) #id1이 바디
    lens=Product.objects.filter(pdtype=2) #id2가 렌즈

    body_star=Star.objects.filter(pdtype_id=1)
    lens_star=Star.objects.filter(pdtype_id=2)

    result_body = body_star.values('pdname').annotate(avg_stars=Avg('star')).order_by('-avg_stars')
    result_lens = lens_star.values('pdname').annotate(avg_stars=Avg('star')).order_by('-avg_stars')
    #pdname 별로 star의 평균값을 avg_stars에 넣고,내림차순정렬

    return render(request,'rank.html', {'result_body':result_body,'result_lens':result_lens,'body':body,'lens':lens})



def item(request):
    return render(request, 'item.html')


def album(request):
    albums=reversed(Album.objects.all()) 
    return render(request, 'album.html',{'albums':albums})

def create_album(request):
    bodypd=Product.objects.filter(pdtype_id=1)
    lenspd=Product.objects.filter(pdtype_id=2)

    if 'img' in request.FILES:
        body=Product.objects.get(pdname=request.POST['bodypd'])
        lens=Product.objects.get(pdname=request.POST['lenspd'])
        album = Album()
        album.user = request.user
        album.bodypd= body
        album.lenspd= lens
        album.pic = request.FILES['img']
        album.save()
        return render(request,'create_album.html',{'done' :'donedone'})
    return render(request,'create_album.html',{'bodypd' : bodypd ,'lenspd' : lenspd })

# 사진 삭제 함수
def delete_album(request):
    album_id = request.GET['album_id'] # 삭제 버튼을 눌렀을 때 album_id 를 받아옴
    album = Album.objects.get(id=album_id) # models 의 Album 중 id 가 같은 것을 가져옴
    album.delete() # 삭제
    return redirect('album')

def search(request):
    album = Album.objects.all()
    search = request.GET['search_name'] 

    albums_body = album.filter(bodypd__pdname__icontains=search)
    albums_lens = album.filter(lenspd__pdname__icontains=search)
    # albums = album.filter(brandpd__icontains=search_brand)

    if albums_body:
        albums = album.filter(bodypd__filmb__icontains=search_body)
        return render(request, 'search_list.html', {'albums':albums})

    elif albums_lens:
        albums = album.filter(lenspd__lname__icontains=search_lens)
        return render(request, 'search_list.html', {'albums':albums})

    # elif albums_brand:
    #     albums = album.filter(brandpd__icontains=search_brand)
    #     return render(request, 'search_list.html', {'albums':albums})
    
    else:
        return redirect('album')

def album_detail(request,pk):
    album = Album.objects.filter(pk=pk)
    return render(request,'album_detail.html',{'album' : album })

#이 위까지 수정한 모델로 했음 0818 16:54


def item_detail(request,pk):
    item = Product.objects.filter(pk=pk) #class에서 product pk로 불러옴
    review = Review.objects.filter(product_id=pk)
    return render(request, 'item_detail.html', {'item' : item ,'review':review})

def create_review(request):
    #가져온거지금 user , pdname , comment,star
    if request.method=='POST':
        product=Product.objects.get(pdname=request.POST['pdname'])
        review=Review()
        review.user = request.user
        review.product = product
        review.content = request.POST['content']
        review.save()  #리뷰생성

        star=Star()
        star.pdname=product
        star.star=int(request.POST['star'])
        star.save() #별점생성
        if product.pdtype_id==1:
            return redirect('item_body')
        else:
            return redirect('item_lens')

def buy(request, pk):
    buys = Buy.objects.filter(pk=pk)
    if request.method == 'POST':
        item = Product.objects.filter(pk=pk)
        countbuy=request.POST['countbuy']
        dcheck=request.POST['dcheck']
        pay=request.POST['pay']
        pdsale=request.POST['pdsale']
        buy=Buy()
        buy.user=request.user
        buy.countbuy=countbuy
        buy.dcheck=dcheck #배송중 배송완료
        buy.pay=pay #카드결제 무통장입금
        buy.product=item
        item.pdsale += user.countbuy #상품 판매량에 중간변수 만큼 더해줌 즉, 구매완료된 상품수
        buy.save()
        item.pdsale += countbuy
        item.save()
        #else : #구매하지않으면
    return render(request, 'buy.html',{
    'buys':buys
    })





        #전체취소하면 내려가는 함수
def not_buy(request, pk):
    if request.method == 'POST':

        item = Product.objects.filter(pk=pk)
        countbuy=request.POST['countbuy']
        dcheck=request.POST['dcheck']
        pay=request.POST['pay']
        pdsale=request.POST['pdsale']

        buy=Buy()
        buy.user=request.user
        buy.countbuy=countbuy
        buy.dcheck=dcheck #배송중 배송완료
        buy.pay=pay #카드결제 무통장입금
        buy.product=item
        item.pdsale -= user.countbuy #상품 판매량에 중간변수 만큼 더해줌 즉, 구매완료된 상품수
        buy.save()

        item.pdsale -= countbuy
        item.save()
        
        #else : #구매하지않으면
        return render(request, 'not_buy.html')
    return render(request, 'not_buy.html')


def buy_check(request, pk):
    buys = Buy.objects.filter(pk=pk)
    return render(request, 'buy_check.html',{
    'buys':buys
    })





        #전체취소하면 내려가는 함수
def not_buy(request, pk):
    if request.method == 'POST':

        item = Product.objects.filter(pk=pk)
        countbuy=request.POST['countbuy']
        dcheck=request.POST['dcheck']
        pay=request.POST['pay']
        pdsale=request.POST['pdsale']

        buy=Buy()
        buy.user=request.user
        buy.countbuy=countbuy
        buy.dcheck=dcheck #배송중 배송완료
        buy.pay=pay #카드결제 무통장입금
        buy.product=item
        item.pdsale -= user.countbuy #상품 판매량에 중간변수 만큼 더해줌 즉, 구매완료된 상품수
        buy.save()

        item.pdsale -= countbuy
        item.save()
        
        #else : #구매하지않으면
        return render(request, 'not_buy.html')
    return render(request, 'not_buy.html')


# def buy_check(request, pk):
#     buys = Buy.objects.filter(pk=pk)
#     if request.method == 'POST':
#         item = Product.objects.filter(pk=pk)
#         countbuy=request.POST['countbuy']


#         pay=request.POST['pay']
        
#         buy=Buy()
#         buy.user=request.user

#         buy.countbuy=int(countbuy)
#         buy.dcheck="결제완료" #배송중 배송완료
#         buy.pay=pay #카드결제 무통장입금
#         buy.product=item

#         item.pdsale += user.countbuy #상품 판매량에 중간변수 만큼 더해줌 즉, 구매완료된 상품수
#         buy.save()
#         item.pdsale += countbuy
#         item.save()
#         #else : #구매하지않으면
#     return render(request, 'buy_check.html',{
#     'buys':buys
#     })

