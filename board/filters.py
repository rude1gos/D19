import django_filters
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from django import forms

class PostFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title',
                                      label='В названии:',
                                      lookup_expr='icontains',)
    author = django_filters.CharFilter(field_name='author__user__username',
                                      label='По автору:',
                                      lookup_expr='icontains',)
    date = django_filters.DateFilter(field_name='date',
                                     label='С даты:',
                                     widget=forms.DateInput(attrs={'type': 'date'}),
                                     lookup_expr='icontains',)
