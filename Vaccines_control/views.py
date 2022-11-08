from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
import csv


##from . models import *
# from . forms import StockCreateForm
from . forms import StockSearchForm,StockCreateForm,StockIssueCreateForm,StockHistorySearchForm,StockSearchForm1,StockCreateForm1,StockSearchForm2,StockCreateForm2,IssueForm,ReceiveForm,StockUpdateForm


from . models import Stock,StockHistory,Issue
 

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
    queryset = Stock.objects.all().order_by('-id')
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
    queryset = Stock.objects.order_by('-id').filter(health_facility__contains= request.user.username)
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



@login_required(login_url='vaccinatorlogin')
@user_passes_test(is_vaccinator)
def facility_vaccine_view(request):
    header = 'List of vaccines'
    form = StockSearchForm1(request.POST or None)
    # queryset = Stock.objects.all()
    queryset = Stock.objects.order_by('-id').filter(health_facility__contains= request.user.username)
    
   
	
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

# @login_required(login_url='district-admin-dashboard')
# @user_passes_test(is_district_admin)
# def district_vaccine_view(request):
#     header = 'List of vaccines'
#     form = StockSearchForm(request.POST or None)
#     # queryset = Stock.objects.all()
#     queryset = Stock.objects.filter(district__contains= request.user.username)
#     # queryset = Stock.objects.filter(health_facility__contains='BWANDA HC')
   
	
#     context = {
# 		"header": header,
# 		"queryset": queryset,
#                 "form": form,
# 	}


#     if request.method == 'POST':
# ##                category__icontains=form['category'].value(),
#                 # queryset = Stock.objects.filter(vaccine_name__icontains=form['vaccine_name'].value())
#                 queryset = Stock.objects.filter(health_facility_name__icontains=form['health_facility_name'].value())
#                 if form['export_to_CSV'].value() == True:
#                         response = HttpResponse(content_type='text/csv')
#                         response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
#                         writer = csv.writer(response)
#                         writer.writerow(['HEALTH FACILITY', 'VACCINE NAME', 'QUANTITY','BATCH NO','PACK SIZE'])
#                         instance = queryset
#                         for stock in instance:
#                                 writer.writerow([stock.health_facility, stock.vaccine_name, stock.Batch_No, stock.manufacturer,stock.vial_size,stock.vaccine_name, stock.quantity, stock.Pack_size])
                                
#                         return response
#                 context = {
#                 "form": form,
#                 "header": header,
#                 "queryset": queryset,
#         }
#     return render(request, "list_item.html", context)




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




def update_items_district(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/district_vaccine')

	context = {
		'form':form
	}
	return render(request, 'add_items_district.html', context)




    #=============================================================

def update_itemsx(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/facility_vaccine')

	context = {
		'form':form
	}
	return render(request, 'add_items_facility.html', context)




    #=================================================================


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



def delete_itemsf(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, ' Deleted Successfully')
		return redirect('/facility_vaccine')
	return render(request, 'delete_itemsf.html')








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

        X=Stock.objects.filter(vaccine_name=form['vaccine_name'].value())
        print(X)

        # X=Stock.objects.filter(vaccine_name=form['vaccine_name'].value(),form['end_date'].value()]).count()
       
        ModelName.objects.filter(field_name__isnull=True).aggregate(Sum('field_name'))

        # print form['my_field'].value()



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





#=========================================================================


# def issue_itemsx(request):
@login_required
def issue_itemsx(request):
    form = StockIssueCreateForm(request.POST or None)
    p=Issue.objects.filter(vaccine_name='BCG').aggregate(Sum('issue_quantity'))
    print(p)
    if form.is_valid():
        # X=Issue.objects.filter(vaccine_name=form['vaccine_name'].value())
        
        form.save()
        # y=Issue.objects.aggregate(Sum('issue_quantity'))
        # print(y)

        #  p=Issue.objects.filter(vaccine_name='BCG').aggregate(Sum('issue_quantity'))
        #  print(p)
        messages.success(request, 'Successfully Saved')
        return redirect('/list_history')
    context = {
        "form": form,
        "title": "Issue Vaccines",
    }
    return render(request, "issue_vaccines.html", context)
#====================================================================================

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



def delete_itemsDD(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, ' Deleted Successfully')
		return redirect('/district_vaccine')
	return render(request, 'delete_itemsD.html')



def search11(request):
    x=Stock.objects.get(id=pk)

def search22(request):
    x=Stock.objects.get(id=pk)


def search33(request):
    x=Stock.objects.get(id=pk)

def search44(request):
    x=Stock.objects.get(id=pk)




def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)



def stock_detailx(request):
	queryset = Stock.objects.all()
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detailx.html", context)









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


 # queryset = Issue.objects.filter(vaccine_name='BCG').aggregate(Sum('issue_quantity'))
@login_required
def list_history(request):
    header = 'History Data'
    queryset = Issue.objects.all().order_by('-id').filter(health_facility=request.user.username)
    queryset1 = Issue.objects.filter(vaccine_name='BCG').aggregate(Sum('issue_quantity'))
    print(queryset1)
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
                "form": form,
        }
    if request.method == 'POST':
                health_facility = form['health_facility'].value()
                queryset = Issue.objects.filter(vaccine_name__icontains=form['vaccine_name'].value(),last_updated__range=[ form['start_date'].value(),form['end_date'].value()])

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
                                # stock.quantity, 
                                stock.issue_quantity, 
                                stock.issue_to, 
                                # stock.receive_quantity, 
                                # stock.receive_by, 
                               
                                stock.last_updated])
                        return response

                context = {
		"form": form,
		"header": header,
		"queryset": queryset,
	}	
    return render(request, "list_history.html",context)



# ========================HISTORY NEW========================================




def your_view(request):
    header = 'HISTORY DATA'
	
    queryset = Issue.objects.all().order_by('-id').filter(health_facility=request.user.username)
    form = StockHistorySearchForm(request.POST or None)
    
    context = {
            "header": header,
            "queryset": queryset,
            "form": form,
    }


    return render(request, "vaccine/formx.html",context)



from django.http import HttpResponse
from xlsxwriter.workbook import Workbook



def your_view2(request):
    form = StockHistorySearchForm(request.POST or None)
    # your view logic here

    # create the HttpResponse object ...
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

##    anemia=models.PrescribePatient.objects.filter(Diagnosis='Anaemia',Date__gte='2021-01-01', Date__lte='2021-12-26').count()


    # .. and pass it into the XLSXWriter
    wb = Workbook(response, {'in_memory': True})
    ws = wb.add_worksheet('test')       
##    sheet.write(0, 0, queryset)
    #================================================================================

    style0 = wb.add_format({'bold': True})
##                       style0.set_text_wrap()
   
    style_rotate = wb.add_format()
    style_rotate.set_rotation(90)

##                       cell_format.set_font_size(30)
##                       cell_format.set_italic()

    horizontalCenter = wb.add_format()
    horizontalCenter.set_align('center')

    style4= wb.add_format({'bold': True, 'font_color': 'blue'})
    style4.set_font_size(14)

   
    style5= wb.add_format({'bold': True, 'font_color': 'pink'})


    sty = wb.add_format()
    sty.set_text_wrap()

    style2 = wb.add_format({'bold': True})
   
    badFontStyle = wb.add_format({'bold': True, 'font_color': 'white'})
    badFontStyle.set_bg_color('black')

    badFontStyle1 = wb.add_format({'bold': True, 'font_color': 'white'})
    badFontStyle1.set_bg_color('red')


    #===============================================================================

    ws.write(2,5, 'HISTORY DATA OF VACCINES FOR ' + form['health_facility'].value()+ ' FROM '+ str(form['start_date'].value())+ ' TO ' + str(form['end_date'].value()) ,style2)



    # ws.write(4,2, 'OPD ATTENDANCES, REFERRALS AND DIAGNOSES TOTALS FOR THE MONTH ',style2)
    # ws.write(6,1, '1.1 OUTPATIENT ATTENDANCE  ',style2)
    # ws.write(12,0, ' 1.2 OUTPATIENT REFERRALS  ',style2)



    #============================================================


    ws.write(4,0, 'COUNT  ',badFontStyle)
    ws.write(4,1, 'VACCINE NAME',badFontStyle)
    ws.write(4,2,'',badFontStyle )
    ws.write(4,3, 'RECEIVED',badFontStyle)
    ws.write(4,4,'',badFontStyle )
    
    ws.write(4,5, 'ISSUED',badFontStyle)
    ws.write(4,6,'',badFontStyle )

    ws.write(4,7, 'DOSES GIVEN TO OTHER FACILITIES',badFontStyle)
    ws.write(4,8,'',badFontStyle )
    ws.write(4,9, 'PHYSICAL COUNT',badFontStyle1)
    ws.write(4,10,'',badFontStyle1 )

    ws.write(4,11, 'NUMBER VACCINATED',badFontStyle)

    ws.write(4,12,'',badFontStyle )


    ws.write(4,13, 'WASTAGE',badFontStyle)

    ws.write(4,14,'',badFontStyle )

    

    ws.write(5,0, 1,horizontalCenter)
    ws.write(6,0, 2,horizontalCenter)
    ws.write(7,0, 3,horizontalCenter)

    ws.write(8,0, 4,horizontalCenter)
    ws.write(9,0, 5,horizontalCenter)
    ws.write(10,0, 6,horizontalCenter)

    ws.write(11,0, 7,horizontalCenter)
    ws.write(12,0, 8,horizontalCenter)
    ws.write(13,0, 9,horizontalCenter)
    ws.write(14,0, 10,horizontalCenter)

    ws.write(15,0, 11,horizontalCenter)
    ws.write(16,0, 12,horizontalCenter)
    ws.write(17,0, 13,horizontalCenter)
    ws.write(18,0, 14,horizontalCenter)

    ws.write(19,0, 15,horizontalCenter)
    ws.write(20,0, 16,horizontalCenter)
    ws.write(21,0, 17,horizontalCenter)
    ws.write(22,0, 18,horizontalCenter)

    ws.write(23,0, 19,horizontalCenter)






    ws.write(5,1, 'BCG',)
    ws.write(6,1, 'DPT-HepB-Hib',)
    ws.write(7,1, 'OPV',)
    ws.write(8,1, 'IPV',)
    ws.write(9,1, 'Rotavirus vaccine',)
    ws.write(10,1, 'Yellow Fever',)
    ws.write(11,1, 'Measles Rubella',)
    ws.write(12,1, 'PCV',)
    ws.write(13,1, 'HPV',)
    ws.write(14,1, 'Tetanus Toxiod diptheria(Td)',)

    
    ws.write(16,1, 'SYRINGES',badFontStyle)


    ws.write(17,1, '0.05mls',)
    ws.write(18,1, '0.5mls',)
    ws.write(19,1, '2mls',)
    ws.write(20,1, '5mls',)
    ws.write(21,1, '0.1mls',)

    ws.write(23,1, 'VITAMINS',badFontStyle)
    
    ws.write(24,1, 'Vitamin A 200000iu',)
    ws.write(25,1, 'Vitamin A 100000iu',)
    ws.write(27,1, 'Mabendazole',)
    ws.write(28,1, 'Albendazole',)
   




# #========================================================VACCINES  BCG===========================================================

    # bcg = Issue.objects.filter((vaccine_name='BCG').aggregate(Sum('issue_quantity')),health_facility=form['health_facility'].value(),Date__range=[form['start_date'].value(),form['end_date'].value()])
    bcg_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='BCG').aggregate(Sum('issue_quantity'))
    for values in bcg_issue.values():
        bc_i=values  
    ws.write(5,5, bc_i)


    bcg_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='BCG').aggregate(Sum('quantity'))
    for values in bcg_received.values():
        bc_r=values  
    ws.write(5,3, bc_r)

    
    doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='BCG').aggregate(Sum('doses_given_to_other_facilities'))
    for values in doses_given.values():
        bc_g=values  
    ws.write(5,7, bc_g)

    pc=bc_r- bc_i-bc_g
    ws.write(5,9, pc)



    no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='BCG').aggregate(Sum('number_vaccinated'))
    for values in no_vaccinated.values():
        bc_v=values  
    ws.write(5,11, bc_v)

    


    
#==============================DPT-HEPB-HIB=====================================================

    HEP_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='DPT-HepB-Hib').aggregate(Sum('issue_quantity'))
    for values in  HEP_issue.values():
         HEP_i=values  
    ws.write(6,5,  HEP_i)


    HEP_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='DPT-HepB-Hib').aggregate(Sum('quantity'))
    for values in  HEP_received.values():
         HEP_r=values  
    ws.write(6,3,  HEP_r)

    
    HEPdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='DPT-HepB-Hib').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  HEPdoses_given.values():
         HEP_g=values  
    ws.write(6,7, bc_g)

    HEPpc= HEP_r- HEP_i- HEP_g
    ws.write(6,9,  HEPpc)



    HEPno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='DPT-HepB-Hib').aggregate(Sum('number_vaccinated'))
    for values in  HEPno_vaccinated.values():
         HEP_v=values  
    ws.write(6,11,  HEP_v)

#============================================================================================


#==============================OPV=====================================================

    OPV_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='OPV').aggregate(Sum('issue_quantity'))
    for values in  OPV_issue.values():
         OPV_i=values  
    ws.write(7,5,  OPV_i)


    OPV_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='OPV').aggregate(Sum('quantity'))
    for values in  OPV_received.values():
         OPV_r=values  
    ws.write(7,3,  OPV_r)

    
    OPVdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='OPV').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  OPVdoses_given.values():
         OPV_g=int(values)  
    ws.write(7,7, OPV_g)

    OPVpc= (int(OPV_r- OPV_i- OPV_g))
    
    ws.write(7,9,  OPVpc)



    OPVno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='OPV').aggregate(Sum('number_vaccinated'))
    for values in  OPVno_vaccinated.values():
         OPV_v=values  
    ws.write(7,11,  OPV_v)

#==============================IPV=====================================================

    IPV_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='IPV').aggregate(Sum('issue_quantity'))
    for values in  IPV_issue.values():
         IPV_i=values  
    ws.write(8,5,  IPV_i)


    IPV_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='IPV').aggregate(Sum('quantity'))
    for values in  IPV_received.values():
         IPV_r=values  
    ws.write(8,3,  IPV_r)

    
    IPVdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='IPV').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  IPVdoses_given.values():
         IPV_g=values  
    ws.write(8,7, bc_g)

    IPVpc= IPV_r- IPV_i- IPV_g
    ws.write(8,9,  IPVpc)



    IPVno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='IPV').aggregate(Sum('number_vaccinated'))
    for values in  IPVno_vaccinated.values():
         IPV_v=values  
    ws.write(8,11,  IPV_v)




#=============================ROTAVIRUS===============================================================

    ROT_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Rotavirus vaccine').aggregate(Sum('issue_quantity'))
    for values in  ROT_issue.values():
         ROT_i=values  
    ws.write(9,5,  ROT_i)


    ROT_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Rotavirus vaccine').aggregate(Sum('quantity'))
    for values in  ROT_received.values():
         ROT_r=values  
    ws.write(9,3,  ROT_r)

    
    ROTdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Rotavirus vaccine').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ROTdoses_given.values():
         ROT_g=values  
    ws.write(9,7, bc_g)

    ROTpc= ROT_r- ROT_i- ROT_g
    ws.write(9,9,  ROTpc)



    ROTno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Rotavirus vaccine').aggregate(Sum('number_vaccinated'))
    for values in  ROTno_vaccinated.values():
         ROT_v=values  
    ws.write(9,11,  ROT_v)


    #===================================YELLOW FEVER====================================================


    YELL_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Yellow Fever').aggregate(Sum('issue_quantity'))
    for values in  YELL_issue.values():
         YELL_i=values  
    ws.write(10,5,  YELL_i)


    YELL_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Yellow Fever').aggregate(Sum('quantity'))
    for values in  YELL_received.values():
         YELL_r=values  
    ws.write(10,3,  YELL_r)

    
    YELLdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Yellow Fever').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  YELLdoses_given.values():
         YELL_g=values  
    ws.write(10,7, bc_g)

    YELLpc= YELL_r- YELL_i- YELL_g
    ws.write(10,9,  YELLpc)



    YELLno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Yellow Fever').aggregate(Sum('number_vaccinated'))
    for values in  YELLno_vaccinated.values():
         YELL_v=values  
    ws.write(10,11,  YELL_v)

    #====================================================MEASLES==================================

    MEA_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Measles Rubella').aggregate(Sum('issue_quantity'))
    for values in  MEA_issue.values():
         MEA_i=values  
    ws.write(11,5,  MEA_i)


    MEA_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Measles Rubella').aggregate(Sum('quantity'))
    for values in  MEA_received.values():
         MEA_r=values  
    ws.write(11,3,  MEA_r)

    
    MEAdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Measles Rubella').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  MEAdoses_given.values():
         MEA_g=values  
    ws.write(11,7, bc_g)

    MEApc= MEA_r- MEA_i- MEA_g
    ws.write(11,9,  MEApc)



    MEAno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Measles Rubella').aggregate(Sum('number_vaccinated'))
    for values in  MEAno_vaccinated.values():
         MEA_v=values  
    ws.write(11,11,  MEA_v)

    #============================================================================================

    PCV_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='PCV').aggregate(Sum('issue_quantity'))
    for values in  PCV_issue.values():
         PCV_i=values  
    ws.write(12,5,  PCV_i)


    PCV_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='PCV').aggregate(Sum('quantity'))
    for values in  PCV_received.values():
         PCV_r=values  
    ws.write(12,3,  PCV_r)

    
    PCVdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='PCV').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  PCVdoses_given.values():
         PCV_g=values  
    ws.write(12,7, bc_g)

    PCVpc= PCV_r- PCV_i- PCV_g
    ws.write(12,9,  PCVpc)



    PCVno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='PCV').aggregate(Sum('number_vaccinated'))
    for values in  PCVno_vaccinated.values():
         PCV_v=values  
    ws.write(12,11,  PCV_v)

    #==================================HPV==========================================================

    HPV_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='HPV').aggregate(Sum('issue_quantity'))
    for values in  HPV_issue.values():
         HPV_i=values  
    ws.write(13,5,  HPV_i)


    HPV_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='HPV').aggregate(Sum('quantity'))
    for values in  HPV_received.values():
         HPV_r=values  
    ws.write(13,3,  HPV_r)

    
    HPVdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='HPV').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  HPVdoses_given.values():
         HPV_g=values  
    ws.write(13,7, bc_g)

    HPVpc= HPV_r- HPV_i- HPV_g
    ws.write(13,9,  HPVpc)



    HPVno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='HPV').aggregate(Sum('number_vaccinated'))
    for values in  HPVno_vaccinated.values():
         HPV_v=values  
    ws.write(13,11,  HPV_v)
    #================================TT==============================================================


    TT_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('issue_quantity'))
    for values in  TT_issue.values():
         TT_i=values  
    ws.write(14,5,  TT_i)


    TT_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('quantity'))
    for values in  TT_received.values():
         TT_r=values  
    ws.write(14,3,  TT_r)

    
    TTdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  TTdoses_given.values():
         TT_g=values  
    ws.write(14,7, bc_g)

    TTpc= TT_r- TT_i- TT_g
    ws.write(14,9,  TTpc)



    TTno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('number_vaccinated'))
    for values in  TTno_vaccinated.values():
         TT_v=values  
    ws.write(14,11,  TT_v)

    #===============================================================================================

    TT_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('issue_quantity'))
    for values in  TT_issue.values():
         TT_i=values  
    ws.write(14,5,  TT_i)


    TT_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('quantity'))
    for values in  TT_received.values():
         TT_r=values  
    ws.write(14,3,  TT_r)

    
    TTdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  TTdoses_given.values():
         TT_g=values  
    ws.write(14,7, bc_g)

    TTpc= TT_r- TT_i- TT_g
    ws.write(14,9,  TTpc)



    TTno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Tetanus Toxiod diptheria(Td)').aggregate(Sum('number_vaccinated'))
    for values in  TTno_vaccinated.values():
         TT_v=values  
    ws.write(14,11,  TT_v)
    
    #===============================0.05MLS================================================================

    ML005_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.05mls').aggregate(Sum('issue_quantity'))
    for values in  ML005_issue.values():
         ML005_i=values  
    ws.write(17,5,  ML005_i)


    ML005_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.05mls').aggregate(Sum('quantity'))
    for values in  ML005_received.values():
         ML005_r=values  
    ws.write(17,3,  ML005_r)

    
    ML005doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.05mls').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ML005doses_given.values():
         ML005_g=values  
    ws.write(17,7, bc_g)

    ML005pc= ML005_r- ML005_i- ML005_g
    ws.write(17,9,  ML005pc)



    ML005no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.05mls').aggregate(Sum('number_vaccinated'))
    for values in  ML005no_vaccinated.values():
         ML005_v=values  
    ws.write(17,11,  ML005_v)

    #===========================0.5MLS=================================================================
    ML05_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.5mls').aggregate(Sum('issue_quantity'))
    for values in  ML05_issue.values():
         ML05_i=values  
    ws.write(18,5,  ML05_i)


    ML05_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.5mls').aggregate(Sum('quantity'))
    for values in  ML05_received.values():
         ML05_r=values  
    ws.write(18,3,  ML05_r)

    
    ML05doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.5mls').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ML05doses_given.values():
         ML05_g=values  
    ws.write(18,7, bc_g)

    ML05pc= ML05_r- ML05_i- ML05_g
    ws.write(18,9,  ML05pc)



    ML05no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.5mls').aggregate(Sum('number_vaccinated'))
    for values in  ML05no_vaccinated.values():
         ML05_v=values  
    ws.write(18,11,  ML05_v)


    #============================================2MLS=================================================


    ML2_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='2mls').aggregate(Sum('issue_quantity'))
    for values in  ML2_issue.values():
         ML2_i=values  
    ws.write(19,5,  ML2_i)


    ML2_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='2mls').aggregate(Sum('quantity'))
    for values in  ML2_received.values():
         ML2_r=values  
    ws.write(19,3,  ML2_r)

    
    ML2doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='2mls').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ML2doses_given.values():
         ML2_g=values  
    ws.write(19,7, bc_g)

    ML2pc= ML2_r- ML2_i- ML2_g
    ws.write(19,9,  ML2pc)



    ML2no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='2mls').aggregate(Sum('number_vaccinated'))
    for values in  ML2no_vaccinated.values():
         ML2_v=values  
    ws.write(19,11,  ML2_v)

    #============================================0.5MLS=============================================

    ML5_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='5mls').aggregate(Sum('issue_quantity'))
    for values in  ML5_issue.values():
         ML5_i=values  
    ws.write(20,5,  ML5_i)


    ML5_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='5mls').aggregate(Sum('quantity'))
    for values in  ML5_received.values():
         ML5_r=values  
    ws.write(20,3,  ML5_r)

    
    ML5doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='5mls').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ML5doses_given.values():
         ML5_g=values  
    ws.write(20,7, bc_g)

    ML5pc= ML5_r- ML5_i- ML5_g
    ws.write(20,9,  ML5pc)



    ML5no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='5mls').aggregate(Sum('number_vaccinated'))
    for values in  ML5no_vaccinated.values():
         ML5_v=values  
    ws.write(20,11,  ML5_v)

    #=======================================0.1MLS=======================================================

    ML01_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.1mls').aggregate(Sum('issue_quantity'))
    for values in  ML01_issue.values():
         ML01_i=values  
    ws.write(20,5,  ML01_i)


    ML01_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.1mls').aggregate(Sum('quantity'))
    for values in  ML01_received.values():
         ML01_r=values  
    ws.write(20,3,  ML01_r)

    
    ML01doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.1mls').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ML01doses_given.values():
         ML01_g=values  
    ws.write(20,7, bc_g)

    ML01pc= ML01_r- ML01_i- ML01_g
    ws.write(20,9,  ML01pc)



    ML01no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='0.1mls').aggregate(Sum('number_vaccinated'))
    for values in  ML01no_vaccinated.values():
         ML01_v=values  
    ws.write(20,11,  ML01_v)


    #================================================VIT2==========================================

    VIT2_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 200,000iu').aggregate(Sum('issue_quantity'))
    for values in  VIT2_issue.values():
         VIT2_i=values  
    ws.write(24,5,  VIT2_i)


    VIT2_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 200,000iu').aggregate(Sum('quantity'))
    for values in  VIT2_received.values():
         VIT2_r=values  
    ws.write(24,3,  VIT2_r)

    
    VIT2doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 200,000iu').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  VIT2doses_given.values():
         VIT2_g=values  
    ws.write(24,7, bc_g)

    VIT2pc= VIT2_r- VIT2_i- VIT2_g
    ws.write(24,9,  VIT2pc)



    VIT2no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 200,000iu').aggregate(Sum('number_vaccinated'))
    for values in  VIT2no_vaccinated.values():
         VIT2_v=values  
    ws.write(24,11,  VIT2_v)


    #=====================================================VIT1=====================================

    VIT1_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 100,000iu').aggregate(Sum('issue_quantity'))
    for values in  VIT1_issue.values():
         VIT1_i=values  
    ws.write(25,5,  VIT1_i)


    VIT1_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 100,000iu').aggregate(Sum('quantity'))
    for values in  VIT1_received.values():
         VIT1_r=values  
    ws.write(25,3,  VIT1_r)

    
    VIT1doses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 100,000iu').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  VIT1doses_given.values():
         VIT1_g=values  
    ws.write(25,7, bc_g)

    VIT1pc= VIT1_r- VIT1_i- VIT1_g
    ws.write(25,9,  VIT1pc)



    VIT1no_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Vitamin A 100,000iu').aggregate(Sum('number_vaccinated'))
    for values in  VIT1no_vaccinated.values():
         VIT1_v=values  
    ws.write(25,11,  VIT1_v)

    #===================================MABENDAZOLE=========================================================


    MAB_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Mabendazole').aggregate(Sum('issue_quantity'))
    for values in  MAB_issue.values():
         MAB_i=values  
    ws.write(27,5,  MAB_i)


    MAB_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Mabendazole').aggregate(Sum('quantity'))
    for values in  MAB_received.values():
         MAB_r=values  
    ws.write(27,3,  MAB_r)

    
    MABdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Mabendazole').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  MABdoses_given.values():
         MAB_g=values  
    ws.write(27,7, bc_g)

    MABpc= MAB_r- MAB_i- MAB_g
    ws.write(27,9,  MABpc)



    MABno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='Mabendazole').aggregate(Sum('number_vaccinated'))
    for values in  MABno_vaccinated.values():
         MAB_v=values  
    ws.write(27,11,  MAB_v)

    #===============================ALBENDAZOLE============================================================


    ALB_issue = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='ALBendazole').aggregate(Sum('issue_quantity'))
    for values in  ALB_issue.values():
         ALB_i=values  
    ws.write(28,5,  ALB_i)


    ALB_received = Stock.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='ALBendazole').aggregate(Sum('quantity'))
    for values in  ALB_received.values():
         ALB_r=values  
    ws.write(28,3,  ALB_r)

    
    ALBdoses_given = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='ALBendazole').aggregate(Sum('doses_given_to_other_facilities'))
    for values in  ALBdoses_given.values():
         ALB_g=values  
    ws.write(28,7, bc_g)

    ALBpc= ALB_r- ALB_i- ALB_g
    ws.write(28,9,  ALBpc)



    ALBno_vaccinated = Issue.objects.filter(Date__range=[form['start_date'].value(),form['end_date'].value()],health_facility=form['health_facility'].value(), vaccine_name='ALBendazole').aggregate(Sum('number_vaccinated'))
    for values in  ALBno_vaccinated.values():
         ALB_v=values  
    ws.write(28,11,  ALB_v)



    #=============================================================================================

    wb.close()
    return response
###=======================================================================================================






#====================================district histroy===========================================



def your_viewd(request):
    header = 'HISTORY DATA'
	
    queryset = Issue.objects.all().order_by('-id').filter(district=request.user.username)
    form = StockHistorySearchForm(request.POST or None)
    
    context = {
            "header": header,
            "queryset": queryset,
            "form": form,
    }


    return render(request, "vaccine/formx.html",context)


    #====================================national histroy===========================================




def your_viewN(request):
    header = 'HISTORY DATA'
	
    queryset = Issue.objects.all().order_by('-id')
    form = StockHistorySearchForm(request.POST or None)
    
    context = {
            "header": header,
            "queryset": queryset,
            "form": form,
    }


    return render(request, "vaccine/formx.html",context)



