import django_filters
from django_filters import CharFilter

from django import forms

from .models import *

class PostFilter(django_filters.FilterSet):
	jobtitle = CharFilter(field_name='jobtitle', lookup_expr="icontains", label='jobtitle')
	#tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
		#widget=forms.CheckboxSelectMultiple
  # )
	class Meta:
		model = Post
		fields = ['jobtitle']