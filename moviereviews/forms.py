from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    """
    Apžvalgos formos klasė.

    Ši forma naudojama apžvalgoms kurti. Ji leidžia vartotojui įvesti pavadinimą, turinį ir įvertinimą.

    Meta klasė nurodo, kad forma yra susieta su Review modeliu ir apima šiuos laukus:
    - title: Apžvalgos pavadinimas.
    - content: Apžvalgos turinys.
    - rating: Apžvalgos įvertinimas.

    Metodai:
    - class Meta: Nurodo susiejimą su `Review` modeliu ir pasirinktus laukus.
    """
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']


class CommentForm(forms.ModelForm):
    """
    Komentaro formos klasė.

    Ši forma naudojama komentarams rašyti. Ji leidžia vartotojui įvesti tik komentarą (turinį).

    Meta klasė nurodo, kad forma yra susieta su `Comment` modeliu ir apima šį lauką:
    - content: Komentaro turinys.

    Metodai:
    - class Meta: Nurodo susiejimą su `Comment` modeliu ir pasirinktą lauką.
    """
    class Meta:
        model = Comment
        fields = ['content']
