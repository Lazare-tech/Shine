from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'shine/body/index.html')
#............................................................................................
def contact(request):
    return render(request,'shine/body/contact.html')
#............................................................................................
def faq(request):
    return render(request,'shine/body/faq.html')    
#............................................................................................
def about(request):
    return render(request,'shine/body/about.html')    
#............................................................................................
def devis(request):
    return render(request,'shine/body/devis.html')
#............................................................................................
def mentorat(request):
    return render(request,'shine/body/mentorat.html')    
#............................................................................................
def infos_bourses(request):
    return render(request,'shine/body/infos_bourse.html')    
#............................................................................................