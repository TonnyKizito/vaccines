from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from . import forms,models
import csv


##from . models import *
# from . forms import StockCreateForm
from . forms import StockSearchForm,StockCreateForm,StockHistorySearchForm,StockSearchForm1,StockCreateForm1,StockSearchForm2,StockCreateForm2,IssueForm,ReceiveForm,StockUpdateForm


from . models import Stock,StockHistory
 

from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from datetime import date


# Create your views here.




def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vaccine/index.html')
	



# for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vaccine/adminclick.html')
	
	
def store_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vaccine/storeclick.html')


def district_adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vaccine/district_adminclick.html')


def aboutus_view(request):
    return render(request,'vaccine/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'vaccine/contactussuccess.html')
    return render(request, 'vaccine/contactus.html', {'form':sub})



def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'vaccine/adminsignup.html',{'form':form})






#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

   



def is_vaccinator(user):
    return user.groups.filter(name='VACCINATOR').exists()


def is_district_admin(user):
    return user.groups.filter(name='DISTRICT_ADMIN').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')

    elif is_district_admin(request.user):
        accountapproval=models.DCCT.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
             return redirect('district-admin-dashboard')
        else:
            return render(request,'vaccine/district_wait_for_approval.html')




    elif is_vaccinator(request.user):
        accountapproval=models.Vaccinator.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('vaccinator-dashboard')
        else:
            return render(request,'vaccine/vaccinator_wait_for_approval.html')



#=========================================================================================
@login_required(login_url='vaccinatorlogin')
@user_passes_test(is_vaccinator)
def vaccinator_dashboard_view(request):
    #for three cards
##    patientcount=models.Patient.objects.all().filter(status=True,assignedPharmacistId=request.user.id).count()
    appointmentcount=models.Pharmacy_Appointment.objects.all().filter(status=True,pharmacistId=request.user.id).count()
##    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Pharmacy_Appointment.objects.all().filter(status=True,pharmacistId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
##    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
##    'patientdischarged':patientdischarged,
    'appointments':appointments,
##    'pharmacist':models.Pharmacy_Appointment.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'vaccine/facility_dashboard.html',context=mydict)




#======================================================

def vaccinator_signup_view(request):
    userForm=forms.VaccUserForm()
    PharmacyForm=forms.vaccForm()
    mydict={'userForm':userForm,'PharmacyForm':PharmacyForm}
    if request.method=='POST':
        userForm=forms.VaccUserForm(request.POST)
        vaccForm=forms.vaccForm(request.POST,request.FILES)
        if userForm.is_valid() and vaccForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            PH=vaccForm.save(commit=False)
            PH.user=user
            PH=PH.save()
            my_PH_group = Group.objects.get_or_create(name='VACCINATOR')
            my_PH_group[0].user_set.add(user)
        return HttpResponseRedirect('pharmacylogin')
    return render(request,'vaccine/vaccinatorsignup.html',context=mydict)



def district_signup_view(request):
    userForm=forms.DistrictUserForm()
    PharmacyForm=forms.districtForm()
    mydict={'userForm':userForm,'PharmacyForm':PharmacyForm}
    if request.method=='POST':
        userForm=forms.DistrictUserForm(request.POST)
        vaccForm=forms.districtForm(request.POST,request.FILES)
        if userForm.is_valid() and vaccForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            PH=vaccForm.save(commit=False)
            PH.user=user
            PH=PH.save()
            my_PH_group = Group.objects.get_or_create(name='DISTRICT_ADMIN')
            my_PH_group[0].user_set.add(user)
        return HttpResponseRedirect('districtlogin')
    return render(request,'vaccine/districtsignup.html',context=mydict)







@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_pharmacy_appointment_view(request):
    return render(request,'vaccine/admin_pharmacy_appointment.html')





# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_vaccinator_view(request):
    return render(request,'vaccine/admin_national_facility.html')


@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def district_admin_vaccinator_view(request):
    return render(request,'vaccine/district_admin_district_facility.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    # confirmDistrict=models.DistrictAdmin.objects.all().filter(user_id=request.user.id, district='KAMPALA')
    doctors=models.Vaccinator.objects.all().order_by('-id').filter(status=False)
    # appro=zip(confirmDistrict,doctors)
    # mydict={'all_approval':appro}

    return render(request,'vaccine/admin_approve_doctor.html',{'doctors':doctors})
    # return render(request,'vaccine/admin_approve_doctor.html',{'all_approval':appro})



@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def district_admin_approve_doctor_view(request):
    #those whose approval are needed
    # confirmDistrict=models.DistrictAdmin.objects.all().filter(user_id=request.user.id, district='KAMPALA')
    doctors=models.Vaccinator.objects.all().order_by('-id').filter(status=False, district=request.user.username)
    # appro=zip(confirmDistrict,doctors)
    # mydict={'all_approval':appro}

    return render(request,'vaccine/district_admin_approve_vaccinator.html',{'doctors':doctors})
    # return render(request,'vaccine/admin_approve_doctor.html',{'all_approval':appro})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-vaccinator'))



@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def approve_vaccinator_by_district_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('district-admin-approve-vaccinator'))






@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def reject_vaccinator_by_district_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('district-admin-approve-vaccinator')





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Vaccinator.objects.all().order_by('-id').filter(status=True)
    return render(request,'vaccine/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def district_admin_view_vaccinator_view(request):
    doctors=models.Vaccinator.objects.all().order_by('-id').filter(status=True, district= request.user.username)
    return render(request,'vaccine/district_admin_view_vaccinator.html',{'doctors':doctors})




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_view_district_view(request):
#     doctors=models.DCCT.objects.all().order_by('-id').filter(status=True)
#     return render(request,'vaccine/admin_view_doctor.html',{'doctors':doctors})




# ==========================NATIONAL ADMIN APPROVE DISTRICT ADMIN



# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_national_district_view(request):
    return render(request,'vaccine/admin_national_district.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_district_view(request):
    #those whose approval are needed
    # confirmDistrict=models.DistrictAdmin.objects.all().filter(user_id=request.user.id, district='KAMPALA')
    district_admin=models.DCCT.objects.all().order_by('-id').filter(status=False)
    # appro=zip(confirmDistrict,doctors)
    # mydict={'all_approval':appro}

    return render(request,'vaccine/admin_approve_district.html',{'district_admin':district_admin})
    # return render(request,'vaccine/admin_approve_doctor.html',{'all_approval':appro})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_district_admin_view(request,pk):
    doctor=models.DCCT.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-district-admin'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_district_admin_view(request,pk):
    doctor=models.DCCT.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-district-admin')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Vaccinator.objects.all().order_by('-id').filter(status=True)
    return render(request,'vaccine/admin_view_doctor.html',{'doctors':doctors})




# ============================================================================


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.VaccUserForm(instance=user)
    doctorForm=forms.vaccForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.VaccUserForm(request.POST,instance=user)
        doctorForm=forms.vaccForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-vaccinator')
    return render(request,'vaccine/admin_update_doctor.html',context=mydict)


# =======================================================================
@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def update_vaccinator_by_district_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.VaccUserForm(instance=user)
    doctorForm=forms.vaccForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.VaccUserForm(request.POST,instance=user)
        doctorForm=forms.vaccForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('district-admin-view-vaccinator')
    return render(request,'vaccine/admin_update_vaccinator_by_district.html',context=mydict)


# ========================================================================================================



#=========================================all district admin cridentials=======================

# @login_required(login_url='district_adminlogin')
# @user_passes_test(is_district_admin)
# def admin_approve_district_view(request):
#     #those whose approval are needed
#     doctors=models.DCCT.objects.all().order_by('-id').filter(status=False)
#     # return render(request,'vaccine/admin_approve_district.html',{'doctors':doctors})
#     return render(request,'vaccine/admin_approve_doctor.html',{'doctors':doctors})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_district_view(request,pk):
    doctor=models.DistrictAdmin.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-district_admin'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_district_view(request,pk):
    doctor=models.DistrictAdmin.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-district_admin')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_district_view(request):
    doctors=models.DCCT.objects.all().order_by('-id').filter(status=True)
    return render(request,'vaccine/admin_view_district.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_district_view(request,pk):
    doctor=models.DistrictAdmin.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DistrictUserForm(instance=user)
    doctorForm=forms.districtForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DistrictUserForm(request.POST,instance=user)
        doctorForm=forms.districtForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'vaccine/admin_update_district.html',context=mydict)





# ============================================================================================


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-vaccinator')


@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def delete_vaccinator_by_district_view(request,pk):
    doctor=models.Vaccinator.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('district-admin-view-vaccinator')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.VaccUserForm()
    doctorForm=forms.vaccForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.VaccUserForm(request.POST)
        vaccForm=forms.vaccForm(request.POST, request.FILES)
        if userForm.is_valid() and vaccForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='VACCINATOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-vaccinator')
    return render(request,'vaccine/admin_add_doctor.html',context=mydict)

# ================================================================================

@login_required(login_url='districtlogin')
@user_passes_test(is_district_admin)
def district_admin_add_vaccinator_view(request):
    userForm=forms.VaccUserForm()
    PharmacyForm=forms.vaccForm()
    mydict={'userForm':userForm,'PharmacyForm':PharmacyForm}
    if request.method=='POST':
        userForm=forms.VaccUserForm(request.POST)
        vaccForm=forms.vaccForm(request.POST,request.FILES)
        if userForm.is_valid() and vaccForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            PH=vaccForm.save(commit=False)
            PH.user=user
            PH.status=True
            PH=PH.save()
            my_PH_group = Group.objects.get_or_create(name='VACCINATOR')
            my_PH_group[0].user_set.add(user)
        return HttpResponseRedirect('district-admin-view-vaccinator')
    return render(request,'vaccine/vaccinatorsignup_by_district.html',context=mydict)



# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

def vaccinator_signup_view(request):
    userForm=forms.VaccUserForm()
    PharmacyForm=forms.vaccForm()
    mydict={'userForm':userForm,'PharmacyForm':PharmacyForm}
    if request.method=='POST':
        userForm=forms.VaccUserForm(request.POST)
        vaccForm=forms.vaccForm(request.POST,request.FILES)
        if userForm.is_valid() and vaccForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            PH=vaccForm.save(commit=False)
            PH.user=user
            PH=PH.save()
            my_PH_group = Group.objects.get_or_create(name='VACCINATOR')
            my_PH_group[0].user_set.add(user)
        return HttpResponseRedirect('pharmacylogin')
    return render(request,'vaccine/vaccinatorsignup.html',context=mydict)


# ====================================================================================







@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_district_admin_view(request):
    userForm=forms.DistrictUserForm()
    doctorForm=forms.districtForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DistrictUserForm(request.POST)
        vaccForm=forms.districtForm(request.POST, request.FILES)
        if userForm.is_valid() and vaccForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DISTRICT_ADMIN')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-district')
    return render(request,'vaccine/admin_add_district_admin.html',context=mydict)










#=======================PHARMACY view============================



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Vaccinator.objects.all().order_by('-id')
    # patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Vaccinator.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Vaccinator.objects.all().filter(status=False).count()

    # patientcount=models.Patient.objects.all().filter(status=True).count()
    # pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    # appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    # pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    # 'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    # 'patientcount':patientcount,
    # 'pendingpatientcount':pendingpatientcount,
    # 'appointmentcount':appointmentcount,
    # 'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'vaccine/admin_dashboard.html',context=mydict)



@login_required(login_url='district_adminlogin')
@user_passes_test(is_district_admin)
def district_admin_dashboard_view(request):
    #for both table in admin dashboard
    # DA=models.Vaccinator.objects.all().order_by('-id')
    # DA = Stock.objects.filter(district__contains= request.user.username)

    # DA = models.DCCT.objects.all().filter(district= request.user.username)
    DA = models.Vaccinator.objects.all().order_by('-id').filter(district= request.user.username)

   
    #  vaccinators=models.Vaccinator.objects.all().order_by('-id').filter(district='MASAKA')
    # patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    # doctorcount=models.Vaccinator.objects.all().filter(status=True).count()
    # pendingdoctorcount=models.Vaccinator.objects.all().filter(status=False).count()

    # patientcount=models.Patient.objects.all().filter(status=True).count()
    # pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    # appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    # pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'DA':DA,
    # 'patients':patients,
    # 'doctorcount':doctorcount,
    # 'pendingdoctorcount':pendingdoctorcount,
    # 'patientcount':patientcount,
    # 'pendingpatientcount':pendingpatientcount,
    # 'appointmentcount':appointmentcount,
    # 'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'vaccine/district_admin_dashboard.html',context=mydict)



def home(request):
	title = 'Welcome: This is the Home Page'
	context = {
	"title": title,
	}
	return redirect('/list_item')

##	return render(request, "home.html",context)


@login_required
def list_item_view(request):
    
    header = 'List of vaccines'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    # queryset = Stock.objects.filter(health_facility__contains='BWANDA HC')
   
	
    context = {
		"header": header,
		"queryset": queryset,
                "form": form,
	}


    if request.method == 'POST':
##                category__icontains=form['category'].value(),
                # queryset = Stock.objects.filter(vaccine_name__icontains=form['vaccine_name'].value())
                queryset = Stock.objects.filter(health_facility__icontains=form['health_facility'].value())
                if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
                        writer = csv.writer(response)
                        writer.writerow(['HEALTH FACILITY', 'VACCINE NAME', 'QUANTITY RECEIVED','BATCH NO','VIAL SIZE','MANUFACTURER'])
                        instance = queryset
                        for stock in instance:
                                writer.writerow([stock.health_facility, stock.vaccine_name,stock.quantity, stock.Batch_No, stock.vial_size,stock.manufacturer,])
                                
                        return response
                context = {
                "form": form,
                "header": header,
                "queryset": queryset,
        }
    return render(request, "list_item.html", context)



@login_required
def list_vaccine_view(request):
    
    header = 'List of vaccines'
    form = StockSearchForm(request.POST or None)
    # queryset = Stock.objects.all()
    queryset = Stock.objects.filter(health_facility__contains= request.user.username)
    # queryset = Stock.objects.filter(health_facility__contains='BWANDA HC')
   
	
    context = {
		"header": header,
		"queryset": queryset,
                "form": form,
	}


    if request.method == 'POST':
##                category__icontains=form['category'].value(),
                queryset = Stock.objects.filter(vaccine_name__icontains=form['vaccine_name'].value())
                if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
                        writer = csv.writer(response)
                        writer.writerow(['HEALTH FACILITY', 'VACCINE NAME', 'QUANTITY','BATCH NO','PACK SIZE'])
                        instance = queryset
                        for stock in instance:
                                writer.writerow([stock.health_facility, stock.vaccine_name, stock.Batch_No, stock.manufacturer,stock.vial_size,stock.vaccine_name, stock.quantity, stock.Pack_size])
                                
                        return response
                context = {
                "form": form,
                "header": header,
                "queryset": queryset,
        }
    return render(request, "list_item.html", context)



# =====================================================================

@login_required(login_url='vaccinatorlogin')
@user_passes_test(is_vaccinator)
def facility_vaccine_view(request):
    header = 'List of vaccines'
    form = StockSearchForm1(request.POST or None)
    # queryset = Stock.objects.all()
    queryset = Stock.objects.filter(health_facility__contains= request.user.username)
    
   
	
    context = {
		"header": header,
		"queryset": queryset,
                "form": form,
	}


    if request.method == 'POST':
##                category__icontains=form['category'].value(),
                queryset = Stock.objects.filter(vaccine_name__icontains=form['vaccine_name'].value(), health_facility__icontains=form['health_facility'].value())
                if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
                        writer = csv.writer(response)
                        writer.writerow(['HEALTH FACILITY', 'VACCINE NAME', 'QUANTITY','BATCH NO','PACK SIZE'])
                        instance = queryset
                        for stock in instance:
                                writer.writerow([stock.health_facility, stock.vaccine_name, stock.Batch_No, stock.manufacturer,stock.vial_size,stock.vaccine_name, stock.quantity, stock.Pack_size])
                                
                        return response
                context = {
                "form": form,
                "header": header,
                "queryset": queryset,
        }
    return render(request, "list_item_facility.html", context)
    
    
    
# ==================================================================================



# 


# ===========================================district list item==============================

@login_required(login_url='district-admin-dashboard')
@user_passes_test(is_district_admin)
def district_vaccine_view(request):
    header = 'List of vaccines'
    form = StockSearchForm(request.POST or None)
    # queryset = Stock.objects.all()
    queryset = Stock.objects.filter(district__contains= request.user.username)
    # queryset = Stock.objects.filter(health_facility__contains='BWANDA HC')
   
	
    context = {
		"header": header,
		"queryset": queryset,
                "form": form,
	}


    if request.method == 'POST':
##                category__icontains=form['category'].value(),
                # queryset = Stock.objects.filter(vaccine_name__icontains=form['vaccine_name'].value())
                queryset = Stock.objects.filter(health_facility_name__icontains=form['health_facility_name'].value())
                if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
                        writer = csv.writer(response)
                        writer.writerow(['HEALTH FACILITY', 'VACCINE NAME', 'QUANTITY','BATCH NO','PACK SIZE'])
                        instance = queryset
                        for stock in instance:
                                writer.writerow([stock.health_facility, stock.vaccine_name, stock.Batch_No, stock.manufacturer,stock.vial_size,stock.vaccine_name, stock.quantity, stock.Pack_size])
                                
                        return response
                context = {
                "form": form,
                "header": header,
                "queryset": queryset,
        }
    return render(request, "list_item.html", context)




@login_required(login_url='district-admin-dashboard')
@user_passes_test(is_district_admin)
def district_vaccine_view(request):
    header = 'List of vaccines'
    form = StockSearchForm2(request.POST or None)
    # queryset = Stock.objects.all()
    queryset = Stock.objects.filter(district__contains= request.user.username)
    # queryset = Stock.objects.filter(health_facility__contains='BWANDA HC')
   
	
    context = {
		"header": header,
		"queryset": queryset,
                "form": form,
	}


    if request.method == 'POST':
                # category__icontains=form['category'].value(),
                # queryset = Stock.objects.filter(vaccine_name__icontains=form['vaccine_name'].value())
                queryset = Stock.objects.filter(health_facility__icontains=form['health_facility'].value())
                if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
                        writer = csv.writer(response)
                        writer.writerow(['HEALTH FACILITY', 'VACCINE NAME', 'QUANTITY','BATCH NO','PACK SIZE'])
                        instance = queryset
                        for stock in instance:
                                writer.writerow([stock.health_facility, stock.vaccine_name, stock.Batch_No, stock.manufacturer,stock.vial_size,stock.vaccine_name, stock.quantity, stock.Pack_size])
                                
                        return response
                context = {
                "form": form,
                "header": header,
                "queryset": queryset,
        }
    return render(request, "list_district_item.html", context)
   
    
    
    
    







# =====================================================================


@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_item')
	context = {
		"form": form,
		"title": "Add vaccines",
	}
	return render(request, "add_items.html", context)





@login_required
def add_vaccines(request):
	form = StockCreateForm1(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/facility_vaccine')
	context = {
		"form": form,
		"title": "Add vaccines",
	}
	return render(request, "add_vaccines.html", context)




@login_required
def add_district_vaccines(request):
	form = StockCreateForm2(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/district_vaccine')
	context = {
		"form": form,
		"title": "Add vaccines",
	}
	return render(request, "add_district_vaccines.html", context)






def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/list_item')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)


# =====================================================

def update_vaccines(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/list_item')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)



# ======================================================








def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, ' Deleted Successfully')
		return redirect('/list_item')
	return render(request, 'delete_items.html')







def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)





def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        # instance.quantity =instance.quntity -instance.issue_quantity
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.vaccine_name) + "s now left in Fridge")
        instance.save()

        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.vaccine_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)



def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.vaccine_name)+"s now in Fridge")

        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "title": 'Reaceive ' + str(queryset.vaccine_name),
            "instance": queryset,
            "form": form,
            "username": 'Receive By: ' + str(request.user),
        }
    return render(request, "add_items.html", context)






def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_item")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)




#=======================PHARMACY view============================


def home(request):
	title = 'Welcome: This is the Home Page'
	context = {
	"title": title,
	}
	return redirect('/list_item')
##	return render(request, "home.html",context)




@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/list_item')
	context = {
		"form": form,
		"title": "Add Vaccines",
	}
	return render(request, "add_items.html", context)





def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/list_item')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)






def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, ' Deleted Successfully')
		return redirect('/list_item')
	return render(request, 'delete_items.html')







def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)








def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		# instance.receive_quantity = 0
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.vaccine_name)+"s now in Fridge")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.vaccine_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)






def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_item")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)



@login_required
def list_history(request):
	header = 'History Data'
	queryset = StockHistory.objects.all().order_by('-id').filter(health_facility=request.user.username)
	# queryset = StockHistory.objects.all()
	form = StockHistorySearchForm(request.POST or None)
	context = {
		"header": header,
		"queryset": queryset,
                "form": form,
        }
	if request.method == 'POST':
                health_facility = form['health_facility'].value()
                queryset = StockHistory.objects.filter(vaccine_name__icontains=form['vaccine_name'].value(),last_updated__range=[ form['start_date'].value(),form['end_date'].value()])

                if (health_facility != ''):
                        queryset = queryset.filter(health_facility=health_facility)

                if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
                        writer = csv.writer(response)
                        writer.writerow(
                                ['HF', 
                                'VACCINE NAME',
                                'QUANTITY', 
                                'ISSUE QUANTITY',
                                'ISSUE TO',
                                'RECEIVE QUANTITY', 
                                'RECEIVE BY', 
                                 
                                'LAST UPDATED'])
                        instance = queryset
                        for stock in instance:
                                writer.writerow(
                                [stock.health_facility, 
                                stock.vaccine_name, 
                                stock.quantity, 
                                stock.issue_quantity, 
                                 stock.issue_to, 
                                stock.receive_quantity, 
                                stock.receive_by, 
                               
                                stock.last_updated])
                        return response

                context = {
		"form": form,
		"header": header,
		"queryset": queryset,
	}	
	return render(request, "list_history.html",context)



# ================================================================

