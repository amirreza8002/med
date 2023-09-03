from django.forms import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ConditionForm
from .models import Condition, InLineDescription, Medicine


class ConditionCreateView(CreateView):
    form_class = ConditionForm
    model = Condition
    template_name = "records/condition_create.html"

    def get_context_data(self, **kwargs):
        ConditionFormSet = inlineformset_factory(
            Condition, InLineDescription, fields=("description",), extra=3
        )
        context = super().get_context_data(**kwargs)

        context["descriptions"] = ConditionFormSet()
        return context

    def form_valid(self, form):
        form.instance.patient = self.request.user
        form.save()

        self.ConditionFormSet = inlineformset_factory(
            Condition, InLineDescription, fields=("description",), extra=3
        )
        formset = self.ConditionFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )
        formset.save()

        return HttpResponseRedirect(self.get_success_url())


class ConditionDeleteView(DeleteView):
    model = Condition
    template_name = "records/condition_delete.html"
    success_url = reverse_lazy("patient_profile")


class ConditionUpdateView(UpdateView):
    model = Condition
    fields = ("condition", "severity", "medicines")
    template_name = "records/condition_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        ConditionFormSet = inlineformset_factory(
            Condition, InLineDescription, fields=("description",), extra=0
        )
        context["descriptions"] = ConditionFormSet(instance=form.instance)
        return context

    def form_valid(self, form):
        form.save()

        self.ConditionFormSet = inlineformset_factory(
            Condition, InLineDescription, fields=("description",), extra=0
        )
        formset = self.ConditionFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )
        formset.save()
        return HttpResponseRedirect(self.get_success_url())


class ConditioDetailView(DetailView):
    model = Condition
    template_name = "records/condition_detail.html"


# class MedicineDelete(DeleteView):
#     model = Condition
#     template_name = "records/medicine_delete.html"
#     success_url = reverse_lazy("patient_profile")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         slug_field = self.get_slug_field()
#         context["med"] = Condition.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).filter(medicines__medicine=slug_field).values_list("medicines", flat=True)
#         return context
#
#     def get_queryset(self):
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         slug = self.kwargs.get("medicines")
#
#
#         print(Condition.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).filter(
#             medicines__medicine=slug))
#         return Condition.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).filter(medicines__medicine=slug).values_list("medicines", flat=True).values("medicines")

# def form_valid(self, form):
#     pk = self.kwargs.get(self.pk_url_kwarg)
#     import psycopg
#     with psycopg.connect("dbname=med user=postgres password=ar138050") as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 SELECT * FROM public.records_condition_medicines WHERE condition_id = %s and medicine_id = %s
#             """, (pk, ))


class MedicineDelete(DeleteView):
    model = Medicine
    template_name = "records/medicine_delete.html"
    success_url = reverse_lazy("patient_profile")

    def form_valid(self, form):
        con_pk = self.kwargs.get("con_pk")
        slug = self.kwargs.get("medicine")
        print(
            Medicine.objects.filter(medicine=slug)
            .filter(conditions__id=con_pk)
            .values()
        )
        med_pk = (
            Medicine.objects.filter(medicine=slug)
            .filter(conditions__id=con_pk)
            .values()[0]["id"]
        )

        self.delete_func(con_pk, med_pk)

        return HttpResponseRedirect(self.success_url)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get("medicine")

        if slug is not None:
            queryset = queryset.filter(**{"medicine": slug})

        if slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def delete_func(self, con_pk, med_pk):
        from django.db import connection

        with connection.cursor() as cur:  # ("dbname=med user=postgres password=ar138050") as conn:
            cur.execute(
                "DELETE "
                "FROM public.records_condition_medicines "
                "WHERE condition_id=%s AND medicine_id=%s",
                (con_pk, med_pk),
            )
        return True


class UserProfileListView(ListView):
    model = Condition
    template_name = "records/user_profile_list.html"
    context_object_name = "conditions"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["patient"] = self.request.user

        return context

    def get_queryset(self):
        return Condition.objects.filter(patient=self.request.user)
