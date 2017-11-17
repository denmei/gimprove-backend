from django import forms
from .models import ExerciseUnit


class AddExerciseUnitForm(forms.ModelForm):

    class Meta:
        model = ExerciseUnit
        fields = '__all__'