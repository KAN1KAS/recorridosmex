from django import forms
from tours.models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
    #         tour = models.ForeignKey(Tours, on_delete=models.CASCADE)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # lugares_reservados = models.IntegerField()
    # precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    # fecha_reserva = models.DateTimeField(auto_now_add=True)
        fields = ['lugares_reservados','precio_pagado']
        widgets = {
            'lugares_reservados': forms.NumberInput(attrs={'min': '1'}),
            'precio_pagado': forms.NumberInput(attrs={'step': '0.01'}),
        }

