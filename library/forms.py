from django import forms
from library.models import Review, Book
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.forms import AuthenticationForm

BAD_WORDS = ["malo", "mugroso", "estupido", "wey", "todo wey", "gonorrea"]

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu usuario'
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña'
        })
    )


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
    
    would_recommend = forms.BooleanField(
        label="¿Recomendarías este libro?", required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }))
    
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
        
    def save(self, commit=True):
        review = super().save(commit=False)
        # agregar lógica antes de que se guarde
        # ! ojo ! esto unicamente va al formulario no al admin
        if commit:
            review.save()
            
        return review
    
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'author', 'publication_date', 'pages', 
                  'isbn', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={
                'value': 'Libro de prueba',
                'placeholder': 'Escribe tu titulo aqui...',
                'class': 'form-control'
            }),
            'cover': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control',
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'publication_date': forms.DateInput(attrs={
                'value': '2004-07-01',
                'type': 'date',
                'class': 'form-control'
            }),
            'pages': forms.NumberInput(attrs={
                'value': '100',
                'class': 'form-control'
            }),
            'isbn': forms.TextInput(attrs={
                'value': 'A1B2C3D4F5',
                'class': 'form-control'
            }),
            'genres': forms.SelectMultiple(attrs={                
                'class': 'form-control'
            }),
        }
        
    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        
        if cover and isinstance(cover, UploadedFile):
            if cover.size > 1 * 1024 * 1024:
                raise forms.ValidationError(
                    "El archivo no debe superar los 1MB"
                )

            if cover.content_type not in [
                'image/jpeg',
                'image/png',
                'image/gif'
            ]:
                raise forms.ValidationError(
                    "El archivo solo acepta imágenes .jpeg, .png o .gif"
                )

        return cover