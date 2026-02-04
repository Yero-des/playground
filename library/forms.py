from django import forms
from library.models import Review

BAD_WORDS = ["malo", "mugroso", "estupido", "wey", "todo wey", "gonorrea"]

class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Califica del 1 al 5',
            'class': 'form-control'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tu reseña aquí...',
            'class': 'form-control',
            'rows': 4
        })
    )
 
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']    
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Califica del 1 al 5',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Escribe tu reseña aquí...',
                'class': 'form-control',
                'rows': 3
            })
        }
        
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        
        if rating < 1 or rating > 5:
            raise forms.ValidationError("La calificación debe estar enter 1 y 5")        
        
        return rating

    def clean_text(self):
        text = self.cleaned_data['text']
        
        for word in BAD_WORDS:
            if word in text.lower():
                raise forms.ValidationError(f"Se detecto la palabra \"{word}\", esta palabra no esta aceptada en la pagina")
            
        return text
    
    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text') or ''
        
        if rating == 1 and len(text) < 10:
            raise forms.ValidationError("Si la calificación es de 1 estrella por favor explica mejor tu reseña")
    
        
        