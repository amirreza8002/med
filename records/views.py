from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from django.forms import inlineformset_factory
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ConditionForm, MedicineForm, ConditionInfoForm
from .models import Condition, ConditionInfo, InLineDescription, Medicine


def condition_create_view(request):
    form_class = ConditionForm
    sec_form_class = MedicineForm
    template_name = "records/condition_create.html"
    context = {}

    condition_form_set = inlineformset_factory(
        Condition, InLineDescription, fields=("description",), extra=3, can_delete=False
    )
    if request.method == "GET":
        context["descriptions"] = condition_form_set()
        context["form"] = form_class
        context["sec_form"] = sec_form_class
        return render(request, template_name, context)

    if request.method == "POST":
        form = ConditionForm(request.POST)
        sec_form = MedicineForm(request.POST)
        formset = condition_form_set(
            request.POST, request.FILES, instance=form.instance
        )
        if form.is_valid():
            form.instance.patient = request.user
            form.save()

        # operations for the medicine table
        if sec_form.is_valid():
            condition = Condition.objects.get(pk=form.instance.id)

            with connection.cursor() as cur:
                # check if medicine already exists in the database (many to many)
                cur.execute(
                    "SELECT id FROM records_medicine WHERE LOWER(medicine) = LOWER(%s)",
                    (sec_form.cleaned_data["medicine"],),
                )
                medicine_id = cur.fetchone()
                if medicine_id:
                    # if medicine already exists just create one row in the middle table
                    cur.execute(
                        "INSERT INTO records_condition_medicine(condition_id, medicine_id) VALUES (%s, %s)",
                        (condition.id, medicine_id[0]),
                    )
                else:
                    # if medicine is new, create a new one
                    cur.execute(
                        "INSERT INTO records_medicine(medicine) VALUES (%s)",
                        (sec_form.cleaned_data["medicine"],),
                    )
                    cur.execute(
                        "SELECT id FROM records_medicine WHERE medicine = %s",
                        (sec_form.cleaned_data["medicine"],),
                    )
                    medicine_id = cur.fetchone()
                    cur.execute(
                        "INSERT INTO records_condition_medicine(condition_id, medicine_id) VALUES (%s, %s)",
                        (condition.id, medicine_id[0]),
                    )

        # save the inline formset data
        if formset.is_valid():
            formset.save()

        return HttpResponseRedirect(Condition.get_absolute_url(form.instance))


"""
class ConditionCreateView(LoginRequiredMixin, CreateView):
    model = Condition
    form_class = ConditionForm
    template_name = "records/condition_create.html"

    def __init__(self) -> None:
        super().__init__()
        self.ConditionFormSet = inlineformset_factory(
            Condition,
            InLineDescription,
            fields=("description",),
            extra=3,
            can_delete=False,
        )
        self.get_form()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["descriptions"] = self.ConditionFormSet()
        return context

    def form_valid(self, form):
        form.instance.patient = self.request.user
        self.object = form.save()

        formset = self.ConditionFormSet(
            self.request.POST, self.request.FILES, instance=form.instance
        )
        formset.save()

        return HttpResponseRedirect(self.get_success_url())
"""


class ConditionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Condition
    template_name = "records/condition_delete.html"
    success_url = reverse_lazy("patient_records")

    def test_func(self):
        obj = self.get_object()
        return obj.patient == self.request.user


class ConditionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Condition
    fields = ("conditions", "severity", "medicine", "MRI")
    template_name = "records/condition_update.html"

    def test_func(self):
        obj = self.get_object()
        return obj.patient == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        ConditionFormSet = inlineformset_factory(
            Condition, InLineDescription, fields=("description",), extra=1
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


class ConditionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Condition
    template_name = "records/condition_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.patient == self.request.user


class MedicineDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medicine
    template_name = "records/medicine_delete.html"
    success_url = reverse_lazy("patient_records")

    def form_valid(self, form):
        con_pk = self.kwargs.get("con_pk")
        slug = self.kwargs.get("medicine")

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
        with connection.cursor() as cur:
            cur.execute(
                "DELETE "
                "FROM public.records_condition_medicines "
                "WHERE condition_id=%s AND medicine_id=%s",
                (con_pk, med_pk),
            )
        return True

    def test_func(self):
        obj = self.get_object()
        return obj.patient == self.request.user


class UserRecordListView(LoginRequiredMixin, ListView):
    model = Condition
    template_name = "records/user_record_list.html"
    context_object_name = "conditions"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["patient"] = self.request.user

        return context

    def get_queryset(self):
        return Condition.objects.filter(patient=self.request.user)


class AllConditionListView(ListView):
    model = ConditionInfo
    template_name = "all-conditions/all_condition_list.html"

    def get_queryset(self):
        return ConditionInfo.objects.all()


class ConditionInfoDetail(DetailView):
    model = ConditionInfo
    template_name = "all-conditions/condition_info.html"


class MedicineCreateForm(CreateView):
    model = Medicine
    form_class = MedicineForm
    success_url = reverse_lazy("home")


class ConditionInfoCreateForm(CreateView):
    model = ConditionInfo
    form_class = ConditionInfoForm
