from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.urls import reverse_lazy


from .models import Condition, InLineDescription
from .forms import ConditionForm


class ConditionCreateView(CreateView):
    form_class = ConditionForm
    model = Condition
    template_name = "records/condition_create.html"
    # success_url = reverse_lazy("records:condition_detail", args=[str(self.id)])

    def get_context_data(self, **kwargs):
        ConditionFormSet = inlineformset_factory(Condition, InLineDescription, fields=("description",), extra=3, can_delete=False)
        context = super().get_context_data(**kwargs)

        context["descriptions"] = ConditionFormSet()
        return context

    # def post(self, request, *args, **kwargs):
    #
    #     self.ConditionFormSet = inlineformset_factory(Condition, InLineDescription, fields=("description",), extra=3, can_delete=False)
    #     formset = self.ConditionFormSet(self.request.POST, self.request.FILES)
    #     if formset.is_valid():
    #         print(formset.cleaned_data)
    #         formset.save()
    #         return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.patient = self.request.user
        self.ConditionFormSet = inlineformset_factory(Condition, InLineDescription, fields=("description",), extra=3,
                                                      can_delete=False)
        formset = self.ConditionFormSet(self.request.POST, self.request.FILES)
        if formset.is_valid():

            print(formset.cleaned_data)
            formset.save()

        return super().form_valid(form)


class ConditioDetailView(DetailView):
    model = Condition
    template_name = "records/condition_detail.html"


class UserProfileListView(ListView):
    model = Condition
    template_name = "records/user_profile_list.html"
    context_object_name = "conditions"

    def get_queryset(self):
        return Condition.objects.filter(patient=self.request.user)
