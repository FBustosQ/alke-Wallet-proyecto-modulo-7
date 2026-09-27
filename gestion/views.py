from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ClienteForm

from .models import Cliente, Cuenta, Transaccion



class AccesoPersonalMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ClienteListView(AccesoPersonalMixin, ListView):
    model = Cliente
    template_name = "gestion/lista_clientes.html"
    context_object_name = "clientes"

    def get_queryset(self):
        clientes = Cliente.objects.annotate(
            total_movimientos = Count("cuenta__transacciones")).order_by("nombre")

        buscar = self.request.GET.get("buscar", "").strip()

        if buscar:
            clientes = clientes.filter(
                Q(nombre__icontains=buscar) | Q(email__icontains=buscar)
                )
        return clientes

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["buscar"] = self.request.GET.get("buscar", "")

        return contexto

class ClienteDetailView(AccesoPersonalMixin, DetailView):
    model = Cliente
    template_name = "gestion/detalle_cliente.html"
    context_object_name = "cliente"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        cuenta = Cuenta.objects.filter(cliente=self.object).first()

        contexto["cuenta"] = cuenta
        contexto["movimientos"] = (
            cuenta.transacciones.all()
            if cuenta 
            else []
        )

        return contexto


    
class ClienteCreateView(AccesoPersonalMixin, CreateView):
    model = Cliente

    form_class = ClienteForm
    template_name = "gestion/form_cliente.html"

    success_url = reverse_lazy("lista_clientes")

    extra_context = {
        "titulo": "Crear cliente"
    }

    def form_valid(self, form):
        respuesta = super().form_valid(form)

        messages.success(
            self.request, "Cliente creado exitosamente"
        )
        return respuesta

    

class ClienteUpdateView(AccesoPersonalMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestion/form_cliente.html"
    success_url = reverse_lazy("lista_clientes")

    extra_context = {
        "titulo" : "Actualizar cliente"
    }

    def form_valid(self, form):
        respuesta = super().form_valid(form)

        messages.success(
            self.request, "Cliente actualizado exitosamente"
        )

        return respuesta

class ClienteDeleteView(AccesoPersonalMixin, DeleteView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestion/confirmar_eliminacion.html"
    success_url = reverse_lazy("lista_clientes")

    def form_valid(self, form):
        try: 
            respuesta = super().form_valid(form)

        except ProtectedError:
            messages.error(self.request, "No se puede eliminar el cliente (tiene una cuenta asociada)")

            return redirect("detalle_cliente", pk=self.object.pk)
        messages.success(self.request, "Cliente eliminado exitosamente")

        return respuesta



    