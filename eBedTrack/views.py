from django.utils import timezone
from django import template
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.forms import forms
from .forms import *
from .forms import LoginForm
from django.db.models import Count
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.db.models.functions import Upper,Lower
from django.template.defaultfilters import urlencode,force_escape
from django.utils.safestring import mark_safe
from django.db.models import Value

register = template.Library()


def home(request):
    return render(request, 'eBedTrack/home.html',
                  {'eBedTrack': home})



def adminlogin(request):

    if request.user.is_staff:
        return redirect('eBedTrack/nurse_login.html')
    else:
        return redirect('eBedTrack/admin_login.html')


@login_required
def nurse_home(request):
    user_name = request.user.username
    hos = Hospital.objects.get(hospital_id=str(user_name))
    name = hos.hospital_name
    print('hosp name is h in ' + str(name))
    return render(request, 'eBedTrack/nurse_home.html',
    {'eBedTrack': nurse_home,'hosp_name':name})



def nurse_bed_availability(request):
    e=request.user.username
    s=Bed.objects.filter(bh=e).values('bh', 'bed_type').annotate(Count('bed_type'))
    dict={}
    c=[]
    for j in s:
        c=[]
        for k,v in j.items():
            if k=='bh':
                continue
            else:
                c.append(v)
        dict[c[0]]=c[1]
    hospitals = Hospital.objects.filter(created_date__lte=timezone.now())
    return render(request, 'eBedTrack/nurse_bed_availability.html',
                  {'s': dict})



def bed_count(request):
    beds = Bed.objects.all()
    return render(request, 'eBedTrack/bed_availability.html',
                  {'beds': beds})


def eBedTrack_administrator(request):
    # ...

    # Return a "created" (201) response code.
    return HttpResponse(status=201)


def contact_us(request):
   if request.method == "POST":
       form = ContactForm(request.POST)
       if form.is_valid():
           firstName=request.POST.get('firstName')
           lastName= request.POST.get('lastName')
           email=request.POST.get('inputEmail')
           question= request.POST.get('inputquestion')
           created_date=timezone.now()
           contact = ContactUs(firstName=firstName,lastName=lastName,emailId=email,question=question,created_date=created_date)
           contact.save()
           return HttpResponseRedirect('/thanks/')
   else:
       form = ContactForm()
   return render(request, 'eBedTrack/contact_us.html', {'form': form})

def hospitals_by_id(list):

    dict={}
    for each in list:
        h = Hospital.objects.filter(hospital_id=each)
        for i in h:
            e = Bed.objects.filter(bh_id=str(i),status='VACANT').count()
            bd=BlockBed.objects.filter(hospital_id_id= str(i),status='Reserved').count()
            if(e-bd >= 1):
                hos = Hospital.objects.get(hospital_id=str(i))
                dict[str(i)]=[hos.hospital_name,hos.address,hos.phone_no]

            # print("Hospitals are :",dict)
            # print(str(i))
                e = Bed.objects.filter(bh_id=str(i),status='VACANT').count()
            # print('count is :',e)
                hos = Hospital.objects.get(hospital_id=str(i))
                v = dict.get(str(i))

                v.append(e-bd)
                dict[str(i)] = v
                s=Bed.objects.filter(bh=str(i),status='VACANT').values('bh','bed_type').annotate(Count('bed_type'))
            # print('s value is '+str(s))
                bedtype={}
                for j in s:
                    c=[]
                    for k,v in j.items():
                        if k=='bh':
                            continue
                        else:
                            c.append(v)
                    bedtype[c[0]]=c[1]
                for k,v in bedtype.items():
                    s=dict.get(str(i))
                    s.append(k)
                    s.append(v)

                    dict[str(i)] = s
            else:
                bedtype={}
        # print('bedtype outside ' +str(dict))
    return dict


def hospitals_in_city(city_name):
    # print('hospital_in_city')
    dict={}
    h = Hospital.objects.filter(city=city_name)
    for i in h:
        e = Bed.objects.filter(bh_id=str(i),status='VACANT').count()
        bd=BlockBed.objects.filter(hospital_id_id= str(i),status='Reserved').count()
        if(e-bd >= 1):
            hos = Hospital.objects.get(hospital_id=str(i))
            dict[str(i)]=[hos.hospital_name,hos.address,hos.phone_no]

            # print("Hospitals are :",dict)
            # print(str(i))
            e = Bed.objects.filter(bh_id=str(i),status='VACANT').count()
            # print('count is :',e)
            hos = Hospital.objects.get(hospital_id=str(i))
            v = dict.get(str(i))

            v.append(e-bd)
            dict[str(i)] = v
            s=Bed.objects.filter(bh=str(i),status='VACANT').values('bh','bed_type').annotate(Count('bed_type'))
            bedtype={}
            for j in s:
                c=[]
                for k,v in j.items():
                    if k=='bh':
                        continue
                    else:
                        c.append(v)
                bedtype[c[0]]=c[1]
            for k,v in bedtype.items():
                s=dict.get(str(i))
                s.append(k)
                s.append(v)

                dict[str(i)] = s
        else:
            bedtype={}
    return dict



def city_search(request):
    if(request.method=="POST"):
        final_dict={}
        form = CitySearchForm(request.POST)
        # print('method is post')
        if(form.is_valid()):
            hosp_dict={}
            city_name=request.POST.get('city')
            if (city_name==''):
                return render(request, 'eBedTrack/bed_availability.html')
            else:
                city_name=city_name.upper()
                # print(city_name)
                # print('city name to be serached is :',city_name)
                hosp_dict=hospitals_in_city(city_name)
                # print('bool of dict ',bool(hosp_dict))
                if (bool(hosp_dict)==True):
                    return render(request, 'eBedTrack/city_search.html',
                    {'hospitals': hosp_dict})
                else:
                    result={}
                    list=[]
                    loc=Location.objects.all().filter(city=city_name)
                    if not loc:
                        return render(request, 'eBedTrack/city_notfound.html')

                    loc2 = Location.objects.filter(state=loc[0].state,county=loc[0].county)
                    for i in loc2:
                        otherhosp=Hospital.objects.filter(state=i.state,city=i.city,county=i.county)
                        for j in otherhosp:
                            list.append(j.hospital_id)
                    result=hospitals_by_id(list)
                    return render(request, 'eBedTrack/nearby_hospital.html',{'hospitals': result})
        else:
            form=CitySearchForm()
            # print('form is invalid')
            return render(request,'eBedTrack/home.html')
    else:
        form = CitySearchForm()
        return render(request, 'eBedTrack/home.html')






@login_required
def patient_list(request):

    patient = Patient.objects.filter(hospital_id=request.user.username)
    return render(request, 'eBedTrack/patient_list.html', {'patients': patient})


@login_required
def blockbed_list(request):

    user_name=request.user.username
    b=BlockBed.objects.filter(hospital_id_id=user_name).exclude(status="Completed")
    return render(request, 'eBedTrack/blockbed_list.html', {'blockbed': b})


@login_required
def blockbed_delete(request, pk):
    blockbed = get_object_or_404(BlockBed, pk=pk)
    blockbed.delete()
    return redirect('eBedTrack:blockbed_list')


def hospital_list(request):
    hospitals = Hospital.objects.filter(created_date__lte=timezone.now())
    return render(request, 'eBedTrack/hospital_list.html',
                  {'hospitals': hospitals})





@login_required()
def nurse_bed_availability(request):
    e=request.user.username
    #bedtype = Bed.objects.raw("select bed_id,bed_type,count(*) from eBedTrack_Bed where status='VACANT' group by bed_type")
    #print('query o/p' +str(bedtype))
    s=Bed.objects.filter(bh=e,status='VACANT').values('bh', 'bed_type').annotate(Count('bed_type'))
    bedtype={}
    for j in s:
        c=[]
        for k,v in j.items():
            if k=='bh':
                continue
            else:
                c.append(v)
        bedtype[c[0]]=c[1]
    h = Hospital.objects.all()
    hospitals = Hospital.objects.filter(created_date__lte=timezone.now())
    return render(request, 'eBedTrack/nurse_bed_availability.html',
                  {'s': bedtype})

@login_required
def patient_list(request):
   patient = Patient.objects.filter(hospital_id=request.user.username)
   return render(request, 'eBedTrack/patient_list.html', {'patients': patient})



@login_required()
def confirm_patient(request):
    # b=BlockBed.objects.filter(phone_no=phone).update(status="Completed")

    un = request.user.username


    if request.method == "POST":
        form = PatientForm(request.POST)
        bid = form.data['bed_id']

        pbid = str(un) + str(bid)

        mutable = request.POST._mutable


        request.POST._mutable = True
        request.POST['bed_id'] = pbid
        request.POST._mutable = mutable

        if form.is_valid():
            patient = form.save(commit=False)
            s = form.cleaned_data.get('patient_tag')
            patient.created_date = timezone.now()
            hh = Hospital.objects.filter(hospital_id=request.user.username)[0]
            patient.hospital_id = hh
            patient.hospital_id = hh
            patient.save()
            pat = Patient.objects.filter(hospital_id=request.user.username)
            h = Hospital.objects.all()
            hbed = form.cleaned_data.get('bed_id')
            q = Bed.objects.filter(bed_id=str(hbed)).update(status='OCCUPIED')
            return render(request, 'eBedTrack/patient_list.html', {'patients': pat})
        else:
            return render(request, 'eBedTrack/patient_new.html', {'form': form})
    else:
        form = PatientForm()
        return render(request, 'eBedTrack/patient_new.html', {'form': form})





@login_required()
def patient_new(request):
    un = request.user.username
    if request.method == "POST":
        form = PatientForm(request.POST)
        bid = form.data['bed_id']

        pbid = str(un) + str(bid)

        mutable = request.POST._mutable


        request.POST._mutable = True
        request.POST['bed_id'] = pbid
        request.POST._mutable = mutable

        if form.is_valid():
            patient = form.save(commit=False)
            s = form.cleaned_data.get('patient_tag')
            patient.created_date = timezone.now()
            hh = Hospital.objects.filter(hospital_id=request.user.username)[0]
            patient.hospital_id = hh
            patient.hospital_id = hh
            patient.save()
            pat = Patient.objects.filter(hospital_id=request.user.username)
            h = Hospital.objects.all()
            hbed = form.cleaned_data.get('bed_id')

            q = Bed.objects.filter(bed_id=str(hbed)).update(status='OCCUPIED')
            return render(request, 'eBedTrack/patient_list.html', {'patients': pat})
        else:
            return render(request, 'eBedTrack/patient_new.html', {'form': form})
    else:
        form = PatientForm()
        return render(request, 'eBedTrack/patient_new.html', {'form': form})

@login_required()
def onclick_update(request,phone):
    b=BlockBed.objects.filter(phone_no=phone).update(status="Completed")
    if(request.method=="POST"):
        patient_new(request)
    else:
        return HttpResponseRedirect("/patient_new")



@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.updated_date = timezone.now()
            patient.save()
            s = form.cleaned_data.get('patient_status')
            if s=='Discharged':
                Pat=Patient.objects.filter(id=pk).values('bed_id')
                for i in Pat:
                    for k,v in i.items():
                        Bed.objects.filter(bed_id=v).update(status='VACANT')

            # patient = Patient.objects.filter(created_date__lte=timezone.now())
            patient = Patient.objects.filter(hospital_id=request.user.username)
            return render(request, 'eBedTrack/patient_list.html',
                         {'patients': patient})
        else:
            form = PatientForm(instance=patient)
            return render(request, 'eBedTrack/patient_edit.html', {'form':form })

    else:
        form = PatientForm(instance=patient)
        return render(request, 'eBedTrack/patient_edit.html', {'form': form})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    Pat=Patient.objects.filter(id=pk).values('bed_id')
    for i in Pat:
        for k,v in i.items():
            Bed.objects.filter(bed_id=v).update(status='VACANT')
    patient.delete()

    return redirect('eBedTrack:patient_list')



@login_required()
def personal(request):
    if request.method == "POST":
        form = PersonalForm(request.POST)
        if form.is_valid():
            personal = form.save(commit=False)
            personal.created_date = timezone.now()
            personal.save()
            pat = Patient.objects.filter(hospital_id=request.user.username)
            return render(request, 'eBedTrack/patient_list.html',
                          {'pat': pat})

    else:
        form = PersonalForm()
        return render(request, 'eBedTrack/personal.html',
                      {'form': form})





@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    Pat = Patient.objects.filter(id=pk).values('bed_id')
    for i in Pat:
        for k, v in i.items():
            Bed.objects.filter(bed_id=v).update(status='VACANT')
    patient.delete()

    return redirect('eBedTrack:patient_list')

@login_required()
def new_bed(request):
    uname = request.user.username
    if request.method == "POST":
        form = BedForm(request.POST)
        bid =form.data['bed_id']
        pbid = str(uname) + str(bid)

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['bed_id'] = pbid
        request.POST._mutable = mutable

        if form.is_valid():
            print('yes, form is valid')
            bed = form.save(commit=False)
            bed.created_date = timezone.now()
            hh = Hospital.objects.filter(hospital_id=request.user.username)[0]
            print('printing hh value '+str(hh))
            bed.bh=hh
            bed.save()
            e=request.user.username
            print('printing hh value '+str(hh))
            s=Bed.objects.filter(bh=e).values('bh', 'bed_type').annotate(Count('bed_type'))
            dict={}
            c=[]
            for j in s:
                c=[]
                for k,v in j.items():
                    if k=='bh':
                        continue
                    else:
                        c.append(v)
                dict[c[0]]=c[1]
            return render(request, 'eBedTrack/nurse_bed_availability.html',
                    {'s': dict})
        else:
            form = BedForm()
            print('form is invalid')
            return render(request, 'eBedTrack/new_bed.html',
                      {'form': form})
    else:
        form = BedForm()
        print('form is invalid')
        return render(request, 'eBedTrack/new_bed.html',
                      {'form': form})



def press_report(request):
    h = Hospital.objects.all()
    p = Patient.objects.all()
    pdict = {}
    dict = {}
    for x in h:
        e = Hospital.objects.get(hospital_name=x.hospital_name)
        dict[e.hospital_name] = e
        for y in p:
            pc = Patient.objects.filter(hospital_id=x).count()
            con = Patient.objects.get(patient_tag=str(y))
            pdict[con.condition] = pc

    pdict = Patient.objects.all().values('hospital_id', 'condition').annotate(count=Count('condition'))
    hdict = Hospital.objects.all().values('hospital_id', 'hospital_name')

    list_pdict = [result for result in pdict]
    list_hosp = [result for result in hdict]
    return render(request, 'eBedTrack/press_report.html', {'press': list_pdict, 'hospitals': list_hosp})



@login_required
def bedcount_update(request):
    if request.method == "POST":
        form = BedForm(request.POST)
        if form.is_valid():
            bed = form.save(commit=False)
            bed.created_date = timezone.now()
            bed.save()
            beds = Bed.objects.filter(created_date__lte=timezone.now())
            return render(request, 'eBedTrack/bedcount_update.html',
                {'beds': beds})

    else:
        form = BedForm()
       # print("Else")
        return render(request, 'eBedTrack/bedcount_update.html',
                      {'form': form})


def bed_availability(request):
    h = Hospital.objects.all()
    dict ={}

    for i in h:
        e = Bed.objects.filter(bh_id=str(i),status='VACANT').count()
        bd=BlockBed.objects.filter(hospital_id_id= str(i),status='Reserved').count()
        if(e-bd >= 1):
            hos = Hospital.objects.get(hospital_id=str(i))
            dict[str(i)]=[hos.hospital_name,hos.address,hos.phone_no]

            e = Bed.objects.filter(bh_id=str(i),status='VACANT').count()
            hos = Hospital.objects.get(hospital_id=str(i))
            v = dict.get(str(i))

            v.append(e-bd)
            dict[str(i)] = v
            s=Bed.objects.filter(bh=str(i),status='VACANT').values('bh','bed_type').annotate(Count('bed_type'))
            bedtype={}
            for j in s:
                c=[]
                for k,v in j.items():
                    if k=='bh':
                        continue
                    else:
                        c.append(v)
                bedtype[c[0]]=c[1]
            for k,v in bedtype.items():
                s=dict.get(str(i))
                s.append(k)
                s.append(v)

                dict[str(i)] = s
        else:
            bedtype={}
    return render(request, 'eBedTrack/bed_availability.html',
                  {'hospitals': dict,'bedtype':bedtype})





def block_bed(request,pk):
    if request.method == "POST":
        form = BlockForm(request.POST)
        firstName=request.POST.get('firstName')
        lastName= request.POST.get('lastName')
        email=request.POST.get('email')
        message= request.POST.get('message')
        phone=request.POST.get('phone')
        created_date=timezone.now()
        status='Reserved'
        bed_type=request.POST.get('bed_type')
        blockbed = BlockBed(hospital_id_id=str(pk),first_name=firstName,last_name=lastName,email=email,phone_no=phone,message=message,created_date=created_date,status=status)
        blockbed.save()
        return HttpResponseRedirect("/thanks/")

    else:
        form=BlockForm()
        return render(request, 'eBedTrack/block_bed.html',{'form': form,'pk':pk} )


def success(request):
    return render(request, 'eBedTrack/success.html',
                  {'success': success})


def thanks(request):
    return render(request, 'eBedTrack/thanks.html',
                  {'thank': thanks})


def view_details(request):
    # return render(request, 'eBedTrack/view_details.html',
    #               {'view_details': view_details})

    hosp = Hospital.objects.all()
    be = Bed.objects.all()
    pdict = {}

    for x in hosp:
        e = Hospital.objects.filter(hospital_id=x)
        print(e)
        for y in be:
            f = Bed.objects.filter(bed_type=y).count()
            b = Bed.objects.get(bed_type=str(y))
            print(b)
            print(f)
            pdict[b.bed_type] = f
            print(pdict)
    return render(request, 'eBedTrack/view_details.html',
                {'pdict': pdict})


def privacy_statement(request):
    return render(request, 'eBedTrack/privacy_statement.html',
                  {'privacy_statement': privacy_statement})


def legal_notice(request):
    return render(request, 'eBedTrack/legal_notice.html',
                  {'legal_notice': legal_notice})


@permission_required('is_staff')
def admin_hospital_new(request):
   if request.method == "POST":
       form = HospitalForm(request.POST)
       if form.is_valid():
           hospital = form.save()
           hospital.created_date = timezone.now()
           hospital.save()

           hospitals = Hospital.objects.all()

           return render(request, 'eBedTrack/admin_hospital_list.html',
                         {'hospitals': hospitals})
   else:
       form = HospitalForm()
   return render(request, 'eBedTrack/admin_hospital_new.html', {'form': form})

@permission_required('is_staff')
def nurse_list(request):
    nurses = Nurse.objects.all()
    return render(request, 'eBedTrack/nurse_list.html', {'nurses': nurses})



@permission_required('is_staff')
def admin_home(request):

    return render(request, 'eBedTrack/admin_home.html',
                  {'eBedTrack': admin_home})

@permission_required('is_staff')
def nurse_new(request):
    nurseDetail = Nurse.objects.all()
    if request.method == "POST":
        form = NurseForm(request.POST)
        if form.is_valid():
            nurse = form.save(commit=False)
            nurse.created_date = timezone.now()
            nurse.save()
            nurses = Nurse.objects.filter(created_date__lte=timezone.now())
            return render(request, 'eBedTrack/nurse_list.html',
                {'nurses': nurses})
    else:
        form = NurseForm()
        return render(request, 'eBedTrack/nurse_new.html',
                      {'form': form})


@login_required
def foo_view(request):
   if not request.user.is_staff:
        user_name = request.user.username
        hos = Hospital.objects.get(hospital_id=str(user_name))
        name = hos.hospital_name
        return render(request, 'eBedTrack/nurse_home.html', {'eBedTrack': nurse_home,'hosp_name':name,})
   else:
        return render(request, 'eBedTrack/admin_home.html', {'eBedTrack': admin_home})



def admin_login(request):
    return render(request, 'eBedTrack/admin_login.html', {'eBedTrack': admin_login})
     # return HttpResponseRedirect('admin_login')

@permission_required('is_staff')
def admin_hospital_list(request):
    hospitals = Hospital.objects.filter(created_date__lte=timezone.now())
    return render(request, 'eBedTrack/admin_hospital_list.html',
                  {'hospitals': hospitals})

@permission_required('is_staff')
def admin_hospital_delete(request, pk):
   hospital = Hospital.objects.get(pk = pk)
   hospital.delete()
   hospitals = Hospital.objects.filter(created_date__lte=timezone.now())
   return render(request, 'eBedTrack/admin_hospital_list.html', {'hospitals': hospitals})

@permission_required('is_staff')
def admin_hospital_edit(request, pk):
   hospital = get_object_or_404(Hospital, pk  = pk)
   if request.method == "POST":
       form = HospitalForm(request.POST, instance=hospital)
       if form.is_valid():
           hospital = form.save()
           hospital.created_date = timezone.now()
           hospital.save()
           hospitals = Hospital.objects.filter(created_date__lte=timezone.now())
           return render(request, 'eBedTrack/admin_hospital_list.html', {'hospitals': hospitals})
   else:
       form = HospitalForm(instance = hospital)
   return render(request, 'eBedTrack/admin_hospital_edit.html', {'form': form})

@permission_required('is_staff')
def nurse_delete(request, pk):
   nurse = Nurse.objects.get(pk = pk)
   nurse.delete()
   nurses = Nurse.objects.all()
   return render(request, 'eBedTrack/nurse_list.html', {'nurses': nurses})

@permission_required('is_staff')
def nurse_edit(request, pk):
   nurse = get_object_or_404(Nurse, pk  = pk)
   if request.method == "POST":
       form = NurseForm(request.POST, instance=nurse)
       if form.is_valid():
           nurse = form.save()
           nurse.created_date = timezone.now()
           nurse.save()
           nurses = Nurse.objects.filter(created_date__lte=timezone.now())
           return render(request, 'eBedTrack/nurse_list.html', {'nurses': nurses})
   else:
       form = NurseForm(instance = nurse)
   return render(request, 'eBedTrack/nurse_edit.html', {'form': form})
