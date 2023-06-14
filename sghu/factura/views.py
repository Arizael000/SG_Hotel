from django.shortcuts import render
from .models import Factura
from administration.models import Room
from django.views.generic import DeleteView, ListView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from .utils import render_to_pdf
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
# Create your views here.


class manageFactura(LoginRequiredMixin,ListView):
    model = Factura
    template_name = 'manageFactura.html'
    success_url = reverse_lazy('manageFactura')
    queryset = Factura.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users']=User.objects.all()
        context['rooms'] = Room.objects.all()
        return context
        
class ListaFact_toPDF(LoginRequiredMixin,ListView):
    template_name = 'lista.html'
    model = Factura
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['rooms'] = Room.objects.all()
        return context
    
    def render_to_pdfA(self, template_src, context_dict):
        template = get_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
        pdf = render_to_pdf(template_src, context_dict)
        if not pdf.err:
            return pdf
        return None

    def get(self, request, *args, **kwargs):
        facturas = self.get_queryset()
        context = {
            'facturas': facturas,
            'users': User.objects.all(),
            'rooms': Room.objects.all(),

        }
        pdf = render_to_pdf('lista.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="facturas.pdf"'
        return response


class manageFacturaUpdateView(LoginRequiredMixin,View):
    
    def post(self, request, pk):
        if request.user.is_staff:
         factura = get_object_or_404(Factura, pk=pk)
         factura.pagada = True
         factura.save()
         return redirect(reverse_lazy('manageFactura'))
        else:
         factura = get_object_or_404(Factura, pk=pk)
         factura.pagada = True
         factura.save()
         return redirect(reverse_lazy('userFactura'))

class userFactura(LoginRequiredMixin,ListView):
    model = Factura
    template_name = 'userFactura.html'
    success_url = reverse_lazy('userFactura')
    queryset = Factura.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        return context
    
class userPagando(LoginRequiredMixin,View):
    template_name='userPagando.html'
    success_url= reverse_lazy('userPagando')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            perfil = self.request.user.perfil
            if not perfil.ci or not perfil.phone:
                return redirect('CompletarPerfil')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
         return redirect('core:login')
    
    def post(self, request, pk):
         factura = get_object_or_404(Factura, pk=pk)
         factura.pagada = True
         factura.save()
         return render(request, 'userPagando.html')
        