from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ConditionForm
from .models import Condition, InLineDescription


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


class UserProfileListView(ListView):
    model = Condition
    template_name = "records/user_profile_list.html"
    context_object_name = "conditions"

    def get_queryset(self):
        return Condition.objects.filter(patient=self.request.user)
