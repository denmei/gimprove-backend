from django import forms
from .models import ExerciseUnit, TrainUnit


class AddExerciseUnitForm(forms.ModelForm):
    """Formular zum Hinzufuegen einer Uebung zu einer Trainingseinheit. Die Trainingseinheit wird automatisch
    eingetragen und ist fuer den User nicht sichtbar."""

    class Meta:
        model = ExerciseUnit
        context_object_name = 'training_unit'
        fields = '__all__'
        widgets = {'train_unit': forms.HiddenInput(), 'id': forms.HiddenInput}


class AddTrainUnitForm(forms.ModelForm):

    class Meta:
        model = TrainUnit
        fields = '__all__'
        widgets = {'id': forms.HiddenInput, 'user': forms.HiddenInput, 'exercise_units': forms.HiddenInput,
                   'start_time_date': forms.HiddenInput, 'end_time_date': forms.HiddenInput}


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=False, label="Name")
    contact_email = forms.EmailField(required=True, label="Email")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label='Nachricht'
    )
