from django.db import models
from django.contrib.auth.models import User

# Create your models here.


category_choiceX = (
		('Tablets', 'Injection','Syrup'),
##		('IT Equipment', 'IT Equipment'),
##		('Phone', 'Phone'),
	)

class Health_Facility(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	def __str__(self):
		return self.name




vaccines_cat = (
		('BCG','BCG'),('DPT-HepB-Hib','DPT-HepB-Hib'),('OPV','OPV'),('IPV','IPV'),
        ('Rotavirus vaccine','Rotavirus vaccine'),
        ('Yellow Fever','Yellow Fever'),
        ('Measles Rubella','Measles Rubella'),('PCV','PCV'),('HPV','HPV'),('Tetanus Toxiod diptheria(Td)','Tetanus Toxiod diptheria(Td)'),('0.05mls','0.05mls'),('0.5mls','0.5mls'),('2mls','2mls'),
        
        ('5mls','5mls'),('0.1mls','0.1mls'),('Mabendazole','Mabendazole'),('Vitamin A 200,000iu','Vitamin A 200,000iu'),
        ('Vitamin A 100,000iu','Vitamin A 100,000iu'),('Albendazole','Albendazole'),

        )


class Stock(models.Model):
        health_facility = models.ForeignKey(Health_Facility, on_delete=models.CASCADE,blank=True)
        health_facility = models.CharField(max_length=50, blank=True, null=True,)
        district= models.CharField(max_length=50,null=True,)
        Date=models.DateField(auto_now=True)
        vaccine_name = models.CharField(max_length=50, blank=True, null=True,choices=vaccines_cat)
        # vaccine_name = models.CharField(max_length=50, blank=True, null=True)
        quantity = models.IntegerField(default='0', blank=True, null=True)
        vial_size = models.CharField(max_length=50, blank=True, null=True)
        receive_quantity = models.IntegerField(default='0', blank=True, null=True)
        receive_by = models.CharField(max_length=50, blank=True, null=True)
        issue_quantity = models.IntegerField(default='0', blank=True, null=True)
        issue_by = models.CharField(max_length=50, blank=True, null=True)
        exp_date = models.CharField(max_length=50, blank=True, null=True)
        people_vaccinated = models.CharField(max_length=50, blank=True, null=True)
        issue_to = models.CharField(max_length=50, blank=True, null=True)
        phone_number = models.CharField(max_length=50, blank=True, null=True)
        dosed_given_out = models.IntegerField(default='0', blank=True, null=True)
        manufacturer = models.CharField(max_length=50, blank=True, null=True)
        From = models.CharField(max_length=50, blank=True, null=True,)
        created_by = models.CharField(max_length=50, blank=True, null=True)
        reorder_level = models.IntegerField(default='0', blank=True, null=True)
        Batch_No = models.CharField(max_length=50, blank=True, null=True,)
        last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
        timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
        
        ##date = models.DateTimeField(auto_now_add=False, auto_now=False)
        ##export_to_CSV = models.BooleanField(default=False)
        def __str__(self):
                return str(self.vaccine_name) +' - '+ str(self.health_facility)
                


# ========================================

class StockHistory(models.Model):
        health_facility = models.ForeignKey(Health_Facility, on_delete=models.CASCADE,blank=True)
        health_facility = models.CharField(max_length=50, blank=True, null=True,)
        district= models.CharField(max_length=50,null=True,)
#       category = models.CharField(max_length=50, blank=True, null=True,choices=category_choice)
        vaccine_name = models.CharField(max_length=50, blank=True, null=True)
        quantity = models.IntegerField(default='0', blank=True, null=True)
        vial_size = models.CharField(max_length=50, blank=True, null=True)
        receive_quantity = models.IntegerField(default='0', blank=True, null=True)
        receive_by = models.CharField(max_length=50, blank=True, null=True)
        issue_quantity = models.IntegerField(default='0', blank=True, null=True)
        issue_by = models.CharField(max_length=50, blank=True, null=True)
        exp_date = models.CharField(max_length=50, blank=True, null=True)
        people_vaccinated = models.CharField(max_length=50, blank=True, null=True)
        issue_to = models.CharField(max_length=50, blank=True, null=True)
        phone_number = models.CharField(max_length=50, blank=True, null=True)
        dosed_given_out = models.IntegerField(default='0', blank=True, null=True)
        manufacturer = models.CharField(max_length=50, blank=True, null=True)
        From = models.CharField(max_length=50, blank=True, null=True,)
        created_by = models.CharField(max_length=50, blank=True, null=True)
        reorder_level = models.IntegerField(default='0', blank=True, null=True)
        Batch_No = models.CharField(max_length=50, blank=True, null=True,)
        last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
        timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

        
        ##date = models.DateTimeField(auto_now_add=False, auto_now=False)
        ##export_to_CSV = models.BooleanField(default=False)
        # def __str__(self):
        #         return str(self.vaccine_name) +' - '+ str(self.health_facility)




#==============================================================



class Vaccinator(models.Model):
        user=models.OneToOneField(User,on_delete=models.CASCADE) 
        Full_Name=models.CharField(max_length=40,null=True)
        # profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
        address = models.CharField(max_length=40)
        mobile = models.CharField(max_length=20,null=True)
        health_facility= models.CharField(max_length=50,null=True,)
        district= models.CharField(max_length=50,null=True,)
        # ==================================================
        status=models.BooleanField(default=False)
#        category = models.CharField(max_length=50, blank=True, null=True,choices=category_choice)
        
        @property
        def get_name(self):
            return self.user.first_name+" "+self.user.last_name
        @property
        def get_id(self):
            return self.user.id
        def __str__(self):
            return (self.user.first_name)




# |==============================DISTRICT ADDMINE================================

class DCCT(models.Model):
        user=models.OneToOneField(User,on_delete=models.CASCADE) 
        Full_Name=models.CharField(max_length=40,null=True)
        # profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
        address = models.CharField(max_length=40)
        mobile = models.CharField(max_length=20,null=True)
        district= models.CharField(max_length=50,null=True,)
        # ==================================================
        status=models.BooleanField(default=False)
#        category = models.CharField(max_length=50, blank=True, null=True,choices=category_choice)
        
        @property
        def get_name(self):
            return self.user.first_name+" "+self.user.last_name
        @property
        def get_id(self):
            return self.user.id
        def __str__(self):
            return (self.user.first_name)



# ==================================================================================








class Pharmacy_Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    pharmacistId=models.PositiveIntegerField(null=True)
    patient_Name=models.CharField(max_length=40,null=True)
    Pharmacist=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.patient_Name
    @property
    def get_id(self):
        return self.patient_Name.id
    def __str__(self):
        return self.patient_Name



category_choice1 = (
		('0-28 days','0-28 days'),('29 days -4Yrs','29 days -4Yrs'),
                   ('5-9Yrs','5-9Yrs'),('10-19Yrs','10-19Yrs'),('20Yrs & Above','20Yrs & Above')

)




category_choice2 = (
		('Male','Male'),('Female','Female'),
)



category_choice3 = (
		('New attendance','New attendance'),('Re-attendace','Re-attendace')
)






class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
##    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    classification = models.CharField(max_length=100, null=True,choices=category_choice3)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)

    assignedLabTechnicianId = models.PositiveIntegerField(null=True)
    Sex = models.CharField(max_length=10, null=True,choices=category_choice2)
    Age_Category = models.CharField(max_length=100,choices=category_choice1,null=True)
    Age = models.PositiveIntegerField(null=True)
    Date=models.DateField(auto_now=True)
    HealthUnitName = models.CharField(max_length=100,null=False)
    Ref_in_No = models.CharField(max_length=10,null=False)
    Ref_out_No = models.CharField(max_length=10,null=False)
    assignedCashierId = models.PositiveIntegerField(null=True)
    

    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"






class Issue(models.Model):
        health_facility = models.ForeignKey(Health_Facility, on_delete=models.CASCADE,blank=True)
        health_facility = models.CharField(max_length=50, blank=True, null=True,)
        district= models.CharField(max_length=50,null=True,)
        Date=models.DateField(auto_now=True)
        vaccine_name = models.CharField(max_length=50, blank=True, null=True,choices=vaccines_cat)
       
        issue_quantity = models.IntegerField(default='0', blank=True, null=True)
        # issue_quantity = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True)
        issue_by = models.CharField(max_length=50, blank=True, null=True)
        issue_to = models.CharField(max_length=50, blank=True, null=True)
        doses_given_to_other_facilities = models.IntegerField(default='0', blank=True, null=True)
        number_vaccinated = models.IntegerField(default='0', blank=True, null=True)
        
        last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
        timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
        
        ##date = models.DateTimeField(auto_now_add=False, auto_now=False)
        ##export_to_CSV = models.BooleanField(default=False)
        def __str__(self):
                return str(self.vaccine_name) +' - '+ str(self.health_facility)
                
