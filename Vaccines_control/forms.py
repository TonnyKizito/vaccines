
from django import forms

from django.contrib.auth.models import User
from . import models
from . models import Stock ,StockHistory,Issue


#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for district admin signup

class DistrictAdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class distForm(forms.ModelForm):
    class Meta:
        model=models.Vaccinator
##        model=models.Doctor
        fields=['district']









class StockCreateForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['district','health_facility', 'vaccine_name', 'vial_size','manufacturer','quantity', 'From','Batch_No','exp_date', 'receive_by',]


   def clean_health_facility(self):
      health_facility = self.cleaned_data.get('health_facility')
      if not health_facility:
         raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
         if instance.health_facility == health_facility:
            pass
##            raise forms.ValidationError(category + 'is already created')
      return health_facility

   def clean_vaccine_name(self):
      vaccine_name = self.cleaned_data.get('vaccine_name')
      health_facility = self.cleaned_data.get('health_facility')
      if not vaccine_name:
         raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
         pass
         # if instance.vaccine_name == vaccine_name and instance.health_facility == health_facility:
         #    raise forms.ValidationError(vaccine_name + ' is already created')
         
      return vaccine_name




      #===============================================================================================


class StockIssueCreateForm(forms.ModelForm):
   class Meta:
     model = Issue
     fields = ['district','health_facility', 'vaccine_name','issue_quantity','issue_by','issue_to','doses_given_to_other_facilities','number_vaccinated']


   def clean_health_facility(self):
      health_facility = self.cleaned_data.get('health_facility')
      if not health_facility:
         raise forms.ValidationError('This field is required')
      for instance in Issue.objects.all():
         if instance.health_facility == health_facility:
            pass
##            raise forms.ValidationError(category + 'is already created')
      return health_facility

   def clean_vaccine_name(self):
      vaccine_name = self.cleaned_data.get('vaccine_name')
      health_facility = self.cleaned_data.get('health_facility')
      if not vaccine_name:
         raise forms.ValidationError('This field is required')
      for instance in Issue.objects.all():
         pass
         # if instance.vaccine_name == vaccine_name and instance.health_facility == health_facility:
         #    raise forms.ValidationError(vaccine_name + ' is already created')
         
      return vaccine_name




      #===================================================================================================


# =========================================try stockcreationForm=================================

class StockCreateForm1(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['district','health_facility', 'vaccine_name', 'vial_size','manufacturer','quantity', 'From','Batch_No','exp_date', 'receive_by',]


   def clean_category(self):
      health_facility = self.cleaned_data.get('category')
      if not health_facility:
         raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
         if instance.health_facility == health_facility:
            pass
##            raise forms.ValidationError(category + 'is already created')
      return health_facility

   def clean_vaccine_name(self):
      vaccine_name = self.cleaned_data.get('vaccine_name')
      health_facility = self.cleaned_data.get('health_facility')
      if not vaccine_name:
         raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
         pass
         # if instance.vaccine_name == vaccine_name and instance.health_facility==health_facility:
         #    raise forms.ValidationError(vaccine_name + ' is already created')
         
      return vaccine_name




# ===========================================================

class StockCreateForm2(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['district','health_facility', 'vaccine_name', 'vial_size','manufacturer','quantity', 'From','Batch_No','exp_date',]


   def clean_category(self):
      health_facility = self.cleaned_data.get('category')
      if not health_facility:
         raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
         if instance.health_facility == health_facility:
            pass
##            raise forms.ValidationError(category + 'is already created')
      return health_facility

   def clean_vaccine_name(self):
      vaccine_name = self.cleaned_data.get('vaccine_name')
      health_facility = self.cleaned_data.get('health_facility')
      if not vaccine_namee:
         raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
         if instance.vaccine_name == vaccine_name and instance.health_facility==health_facility:
            raise forms.ValidationError(vaccine_name + ' is already created')
         
      return vaccine_name





# ============================================================
   
   



# ==============================================================================================



# class StockHistorySearchForm(forms.ModelForm):
#    export_to_CSV = forms.BooleanField(required=False)
#    start_date = forms.DateTimeField(required=False)
#    end_date = forms.DateTimeField(required=False)

# ##   start_date = forms.DateField(required=False)
# ##   end_date = forms.DateField(required=False)
#    class Meta:
#       model = StockHistory
#       fields = ['health_facility', 'vaccine_name', 'start_date', 'end_date']
  



class VaccUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class vaccForm(forms.ModelForm):
    class Meta:
        model=models.Vaccinator
##        model=models.Doctor
        fields=['Full_Name','mobile','district','status']



class DistrictUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class districtForm(forms.ModelForm):
    class Meta:
        model=models.DCCT
##        model=models.Doctor
        fields=['Full_Name','mobile','status']



# for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

# item_name, category
class StockSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Stock
     fields = ['health_facility', 'vaccine_name']

class StockSearchForm1(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Stock
     fields = ['health_facility', 'vaccine_name']


class StockSearchForm2(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Stock
     fields = ['health_facility', 'vaccine_name']
 
 
 


class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']


class IssueFormx(forms.ModelForm):
	class Meta:
		model = Issue
		fields = ['issue_quantity', 'issue_to']




class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['district','health_facility', 'vaccine_name', 'vial_size','manufacturer','quantity', 'From','Batch_No','exp_date', 'receive_by',]



class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_by']



class StockHistorySearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   start_date = forms.DateTimeField(required=False)
   end_date = forms.DateTimeField(required=False)

##   start_date = forms.DateField(required=False)
##   end_date = forms.DateField(required=False)
   class Meta:
      model = Stock
      fields = ['health_facility', 'vaccine_name', 'start_date', 'end_date']



class StockSearchForm(forms.ModelForm):
   export_to_CSV = forms.BooleanField(required=False)
   class Meta:
     model = Stock
     fields = ['health_facility', 'vaccine_name']
      







