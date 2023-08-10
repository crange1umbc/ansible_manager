from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from django.templatetags.static import static
from django.conf import settings
import os
from ansible_runner import run
import json
import pandas as pd
import random
from django.contrib.auth.decorators import login_required
from .models import Exercise,VM,VMRequest,CryptRequest,CryptText
from dotenv import load_dotenv
import csv

load_dotenv()
# Create your views here.

IP_NAME={
        '130.85.121.26':'bhar-ub22',
        '130.85.121.27':'bhar-kali',
        '133.228.78.3':'bhar-ub20',
    }
VM_TEMPLATES={
   'kali':'CyberRange/vm/CRCSEE/Template/Template-Kali-crg',
   'ub20':'CyberRange/vm/CRCSEE/Template/template-ub20',
   'ub22':'CyberRange/vm/bhargavi/ub-22-template',
}

become_password='Crcsee2#'
static=settings.STATIC_ROOT
inventory_path=static+'/forms/playbooks/inventory'
vault_password_cmd='--vault-password-file '+static+'/forms/playbooks/pass.txt'
ssh_key_path=static+'/forms/playbooks/ansible'

with open(ssh_key_path,'r') as key_file:
    private_key_file=key_file.read()

#ansible_runner_config_file=static+'/forms/playbooks/ansible.cfg'

def dashboard(request):
    exercises=Exercise.objects.all()
    return render(request,'forms/main.html',{'exercises':exercises})

@login_required
def launch_vm_request(request):
    return render(request,'forms/vm_request.html')

@login_required
def new_vm(request):
    if request.method=='POST':
        playbook_path=static+'/forms/playbooks/deploy_template.yml'
        course_number=request.POST['course_number']
        prof_name=request.POST['instructor_name']
        os=request.POST['os']
        num_vm=request.POST['num_vm']
        folder_name=course_number+prof_name.split(' ')[0]
        vm_name=course_number+prof_name.split(' ')[0]+'-'+os
        template=VM_TEMPLATES[os]


        extra_vars={
            'create_folder_name':folder_name,
            'create_vm_name':vm_name,
            'create_template':template,
            'num_vm':int(num_vm)
        }
        options={
            'extravars':extra_vars,
            'cmdline':vault_password_cmd,
        }
        result=run(playbook=playbook_path,**options)
        # print("\n\n\n------------------After execution--------------------")
        # for event in result.events:
        #     # print(event)
        #     print(event[0])
        
        # return redirect('dashboard')
        return JsonResponse({'success':True,'message':"VM's created"})
        
    else:
        return render(request,'forms/new_vm_form.html')

@login_required
def power_on(request):
    
    if request.method=='POST':
        
        playbook_path=static+'/forms/playbooks/power_server.yml'
        ip_addr=[IP_NAME.get(ip.strip()) for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        
        machine_list=json.dumps(ip_addr)
        
        extra_vars={
            'machine_list':machine_list
        }
        options={
            'envvars':{
                'ANSIBLE_SUDO_PASS':become_password,
            },
            'extravars':extra_vars,
            'cmdline':vault_password_cmd,
        }
        result=run(playbook=playbook_path,**options)
        if result.rc==0:
            return JsonResponse({'success':True,'message':"Powered on"})
        else:
            return JsonResponse({'success':False,'message':"Power on failed"})
    else:
        return render(request,'forms/power_on.html')

@login_required
def power_off(request):
    if request.method=='POST':
        ip_addr=[IP_NAME.get(ip.strip()) for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        machine_list=json.dumps(ip_addr)
        playbook_path=static+'/forms/playbooks/power_off.yml'
        extra_vars={
            'machine_list':machine_list
        }
        options={
            'envvars':{
                'ANSIBLE_SUDO_PASS':become_password,
            },
            'extravars':extra_vars,
            'cmdline':vault_password_cmd,
        }
        result=run(playbook=playbook_path,**options)
        if result.rc==0:
            return JsonResponse({'success':True,'message':"Powered off"})
        else:
            return JsonResponse({'success':False,'message':"Power off failed"})
    else:
        return render(request,'forms/power_off.html')

@login_required
def restart(request):
    if request.method=='POST':
        ip_addr=[IP_NAME.get(ip.strip()) for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        machine_list=json.dumps(ip_addr)
        playbook_path=static+'/forms/playbooks/restart.yml'
        extra_vars={
            'machine_list':machine_list
        }
        options={
            'envvars':{
                'ANSIBLE_SUDO_PASS':become_password,
            },
            'extravars':extra_vars,
            'cmdline':vault_password_cmd,
        }
        result=run(playbook=playbook_path,**options)
        if result.rc==0:
            return JsonResponse({'success':True,'message':"Restarted"})
        else:
            return JsonResponse({'success':False,'message':"Restart failed"})
        
    else:
        return render(request,'forms/restart.html')

@login_required
def user_add(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        add_host_name=['crange1@'+ip for ip in ip_addr]
        
        if request.POST.get('users')!='':
            add_users=request.POST.get('users').split('\r\n')
            add_users_list=json.dumps(add_users)
        
        elif request.FILES:
            add_file=request.FILES.get('user_add_file').read()
            add_file=add_file.decode('utf-8')
            add_users=list(filter(None,add_file.split('\n')))
            add_users_list=json.dumps(add_users)
        else:
            return JsonResponse({'success':False,'message':"Users don't exist"})

        playbook_path=static+'/forms/playbooks/user_add.yml'
        extra_vars={
            'host_name':add_host_name,
            'add_users_list':add_users_list
        }
        result=ansible_run(playbook_path,extra_vars)
        if result.rc==0:
            return JsonResponse({'success':True,'message':"User's added successfully"})
        else:
            return JsonResponse({'success':False,'message':"Add Users Failed"})

    else:
        return render(request,'forms/user_add.html')

@login_required
def user_remove(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        remove_host_name=['crange1@'+ip for ip in ip_addr]
        if request.POST.get('users')!='':
            remove_users=request.POST.get('users').split(',')
            remove_users_list=json.dumps(remove_users)
            playbook_path=static+'/forms/playbooks/user_remove.yml'
            extra_vars={
                'host_name':remove_host_name,
                'remove_users_list':remove_users_list
            }
            result=ansible_run(playbook_path,extra_vars)
            if result.rc==0:
                return JsonResponse({'success':True,'message':"User's removed successfully"})
            else:
                return JsonResponse({'success':False,'message':"Remove Users Failed"})
        else:
            return JsonResponse({'success':False,'message':"Users Don't exist"})
    else:
        return render(request,'forms/user_remove.html')

@login_required
def create_dir(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        create_host_name=['crange1@'+ip for ip in ip_addr]
        if request.POST.get('dir_path')!='':
            create_path=request.POST.get('dir_path').split('\r\n')
            create_dir_list=json.dumps(create_path)
            playbook_path=static+'/forms/playbooks/create_directory.yml'
            extra_vars={
                'host_name':create_host_name,
                'create_dir_list':create_dir_list
            }
            result=ansible_run(playbook_path,extra_vars)
            if result.rc==0:
                return JsonResponse({'success':True,'message':"Directory Created successfully"})
            else:
                return JsonResponse({'success':False,'message':"Directory Creation Failed"})
        else:
            return JsonResponse({'success':False,'message':"Directory not provided"})
    else:
        return render(request,'forms/create_dir.html')

@login_required
def delete_dir(request):
    if request.method=='POST':
        ip_addr=[ip.strip() for ip in request.POST.get('ip_addr').split(',')]
        if None in ip_addr:
            return JsonResponse({'message':"VM Not Found"})
        delete_host_name=['crange1@'+ip for ip in ip_addr]
        if request.POST.get('dir_path')!='':
            delete_path=request.POST['dir_path'].split(',')
            delete_dir_list=json.dumps(delete_path)
            playbook_path=static+'/forms/playbooks/del_dir.yml'
            extra_vars={
                'host_name':delete_host_name,
                'delete_dir_list':delete_dir_list
            }
            result=ansible_run(playbook_path,extra_vars)
            if result.rc==0:
                return JsonResponse({'success':True,'message':"Directory Deleted successfully"})
            else:
                return JsonResponse({'success':False,'message':"Directory Deletion Failed"})
        else:
            return JsonResponse({'success':False,'message':"Directory not provided"})
            
    else:
        return render(request,'forms/delete_dir.html')

def ansible_run(playbook_path,extra_vars):
    os.environ['ANSIBLE_LOCAL_TEMP']='/tmp'
    options={
        'inventory':inventory_path,
        'ssh_key':private_key_file,
        'envvars':{'ANSIBLE_SUDO_PASS':become_password},
        'extravars':extra_vars
    }

    return run(playbook=playbook_path,**options)

@login_required
def open_pdf(request,exercise_id):
    exercise=get_object_or_404(Exercise,id=exercise_id)
    with open(exercise.pdf_file.path,'rb') as pdf_file:
        response=HttpResponse(pdf_file.read(),content_type='application/pdf')
        response['Content-Disposition']=f'inline; filename="{exercise.pdf_file.name}"'
        return response

def get_plaintexts_from_file(filepath,num):
    with open(filepath,"r") as file:
        text=file.read()
        file.close()
    plaintexts=text.split("\n\n")
    return plaintexts[:num]

@login_required
def crypt(request):
    if request.method=='POST':
        technique=request.POST.get('tech')
        random_key='yes' if technique=='ceaser' or technique=='vernam' else request.POST.get('random_key') 
        key=request.POST.get('key')
        if random_key=='no':
            if key=='':
                return JsonResponse({'success':False,'message':"Key not provided. If you don't want to give key, select random key"})
        default=request.POST.get('default')
        num=request.POST.get('num_cipher')
        if default=='no':
            if request.POST.get('plain')=='':
                return JsonResponse({'success':False,'message':"Plaintext not provided. If you don't want to give plaintext, select default plaintext"})
            else:
                plaintexts=[r for r in request.POST.get('plain').split('\n\n')]
        else:
            if num=='':
                return JsonResponse({'success':False,'message':"Number of ciphertext not given"})
            file_path=static+"/forms/default_Plain.txt"
            plaintexts=get_plaintexts_from_file(file_path,int(num))
        ip_addr=request.POST.get('ip_addr')
        
        crypt_request=CryptRequest(user=request.user,technique=technique,random_key=random_key,key=key,num_cipher=num,ip_address_list=ip_addr)
        crypt_request.save()

        if technique=='rotation':
            if key.isdigit():
                ciphertexts,keys=rotation(plaintexts,key)
            else:
                return JsonResponse({'success':False,'message':"Key for rotation cipher should be a number"})
        elif technique=='ceaser':
            ciphertexts,keys=ceaser(plaintexts)
        elif technique=='transposition':
            ciphertexts,keys=transposition(plaintexts,key)
        elif technique=='vernam':
            ciphertexts,keys=vernam(plaintexts)
        elif technique=='vigenere':
            ciphertexts,keys=vigenere(plaintexts,key)

        if ip_addr!='':
            ip_address=[r.strip() for r in ip_addr.split(',')]
            host_name=[f'crange1@{r.strip()}' for r in ip_addr.split(',')]
            
            if len(host_name)!=len(ciphertexts):
                return JsonResponse({'success':False,'message':"Number of ip_address is incorrect, it should be same as number of plaintexts"})

            cipher=[]
            for i in range(len(host_name)):
                cipher.append(host_name[i]+','+ ciphertexts[i])
            
            cipher_list=json.dumps(cipher)
            playbook_path=static+'/forms/playbooks/crypt.yml'
            extra_vars={
                'host_name':host_name,
                'cipher_list':cipher_list
            }
            result=ansible_run(playbook_path,extra_vars)
            if result.rc==0:
                for i in range(len(ciphertexts)):
                    text=CryptText(cryptreq=crypt_request,plaintext=plaintexts[i],ciphertext=ciphertexts[i],key=keys[i],ip_addr=ip_address[i])
                    text.save()
                return JsonResponse({'success':True,'message':"Ciphertexts copied successfully"})
            else:
                return JsonResponse({'success':False,'message':"Ciphertexts copy failed"})
        else:
            for i in range(len(ciphertexts)):
                text=CryptText(cryptreq=crypt_request,plaintext=plaintexts[i],ciphertext=ciphertexts[i],key=keys[i])
                text.save()
            return JsonResponse({'success':True,'message':"Ciphertexts created successfully"})

    else:
        return render(request,'forms/crypt.html')



def ceaser(plaintexts):

    Ciphertexts=[]
    keys=[]

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 
    
    # Combine upper, lower and symbols
    plain = plainu + plainl + plainm
   
    for i in range(len(plaintexts)):

        cipheru = [ chr(letter) for letter in range(65, 65+26)] 
        cipherl = [ chr(letter) for letter in range(97, 97+26)]
        cipherm = ['@', '_']

        # Shuffle cipher chars randomly
        random.shuffle(cipheru)
        random.shuffle(cipherl)
        random.shuffle(cipherm)

        cipher = cipheru + cipherl + cipherm
        
        ciphertext=[]
        keycount = dict()
        for ch in plaintexts[i]: # For every character in plaintext
            if ch in plain: # If it is in plain
                index = plain.index(ch) # Get index of the plain
                ciphertext.append(cipher[index]) # append the cipher at that index in cipher

                # To keep frequency count
                if ch not in plainm: # If ch is a letter (and not symbol)
                    val = keycount.get(ch,0) # Get Value(count) of char, return 0 if char not in keycount
                    keycount[ch] = val + 1 # Increment the count 
            else:
                ciphertext.append(ch) # If plaintext is not a upper, lower, space and dot, dont replace

        Ciphertexts.append(''.join(ciphertext))
        key=''.join(plain)+'\n'+''.join(cipher)
        keys.append(key)
    return (Ciphertexts,keys)

def rotation(plaintexts,key):

    Ciphertexts=[]
    keys=[]

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 
    
    # Combine upper, lower and symbols
    plain = plainu + plainl + plainm

    for i in range(len(plaintexts)):
        
        if key!='':
            rot_key=int(key)
        else:
            rot_key = random.choice([num for num in range(1, 101) if num % 26 != 0])

        cipheru = [ chr(((letter-65+rot_key) % 26)+65) for letter in range(65, 65+26)] 
        # Rotate each letter by key
        cipherl = [ chr(((letter-97+rot_key) % 26)+97) for letter in range(97, 97+26)]
        cipherm = ['@', '_']

        cipher = cipheru + cipherl + cipherm
        ciphertext = [] # List for cipertext

        for ch in plaintexts[i]: # For every character in plaintext
            if ch in plain: # If it is in plain
                index = plain.index(ch) # Get index of the plain
                ciphertext.append(cipher[index]) # append the cipher at that index in cipher

            else:
                ciphertext.append(ch) # If plaintext is not a upper, lower, space and dot, dont replace
        Ciphertexts.append(''.join(ciphertext))
        keys.append(rot_key)

    return (Ciphertexts,keys)

def vernam(plaintexts):
    Ciphertexts=[]
    keys=[]

    cipherm = ['@', '_']

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 

    # Combine upper, lower and symbols
    plain = plainu + plainl + plainm
    
    for i in range(len(plaintexts)):

        keytext=""
        for _ in range(len(plaintexts[i])):
            random_char = chr(random.randint(65, 90))
            keytext += random_char

        ciphertext = [] # List for cipertext

        for idx in range(len(plaintexts[i])): # For every character in plaintext
            
            if plaintexts[i][idx] in plainu: # If it is in plain
                rot_key=ord(keytext[idx])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-65^rot_key) % 26)+65)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainl:
                rot_key=ord(keytext[idx])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-97^rot_key) % 26)+97)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainm:
                index = plainm.index(plaintexts[i][idx]) # Get index of the plain
                ciphertext.append(cipherm[index])
            else:
                ciphertext.append(plaintexts[i][idx]) 
                # If plaintext is not a upper, lower, space and dot, dont replace
        
        Ciphertexts.append(''.join(ciphertext))
        keys.append(keytext)

    return (Ciphertexts,keys)

def vigenere(plaintexts,key):

    Ciphertexts=[]
    keys=[]

    plainu = [ chr(letter) for letter in range(65, 65+26)] # Uppercase Letters
    plainl = [ chr(letter) for letter in range(97, 97+26)] # Lowercase Letters
    plainm = [' ', '.'] 

    cipherm = ['@', '_']

    for i in range(len(plaintexts)):

        if key!='':
            keytext=key.upper()
        else:
            keytext=""
            for _ in range(10):
                random_char = chr(random.randint(65, 90))
                keytext += random_char

        ciphertext = [] # List for cipertext

        for idx in range(len(plaintexts[i])): # For every character in plaintext
            
            if plaintexts[i][idx] in plainu: # If it is in plain
                rot_key=ord(keytext[idx%len(keytext)])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-65+rot_key) % 26)+65)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainl:
                rot_key=ord(keytext[idx%len(keytext)])-ord('A')
                subs=chr(((ord(plaintexts[i][idx])-97+rot_key) % 26)+97)
                ciphertext.append(subs)
            elif plaintexts[i][idx] in plainm:
                index = plainm.index(plaintexts[i][idx]) # Get index of the plain
                ciphertext.append(cipherm[index])
            else:
                ciphertext.append(plaintexts[i][idx]) # If plaintext is not a upper, lower, space and dot, dont replace
        
        Ciphertexts.append(''.join(ciphertext))
        keys.append(keytext)

    return (Ciphertexts,keys)


def transposition(plaintexts,key):

    Ciphertexts=[]
    keys=[]

    for idx in range(len(plaintexts)):

        ciphertext = [] # List for ciphertext

        plain=plaintexts[idx].replace(" ","@")
        plain=plain.replace(".","_")

        if key!='':
            keytext=key
        else:    
            key_length=random.randint(10,20)
        
            keytext=""

            for _ in range(key_length):
                random_char = chr(random.randint(65, 90))
                keytext += random_char

        l_key = list(keytext) # list of key characters 
        s_key = sorted(l_key) # sorted key 

        plain_list = list(plain) # list of plain cipher text characters 

        # # Encryption 

        rem = len(plaintexts[idx]) % len(keytext) 
        emp = len(keytext)-rem # Finding empty characters at the end in matrix 
        
        for i in range(emp): 
            plain_list.append('@') # replacing empty space at the end with @

        matrix = [[] for j in range(len(keytext))] 
        cipher = [] 

        for i in range(len(matrix)): 
            for j in range(i, len(plain_list), len(keytext)): 
                matrix[i].append(plain_list[j])

        mat_t=list(map(list, zip(*matrix)))

        # Rearranging matrix according to the key 
        for i in range(len(keytext)): 
            cipher.append(matrix[l_key.index(s_key[i])]) 

        cip_t=list(map(list, zip(*cipher)))

        # Converting matrix to list 
        for i in range(len(keytext)): 
            cipher[i] = ''.join(cipher[i]) 

        # Converting list to string 
        ciphertext = ''.join(cipher) 

        Ciphertexts.append(''.join(ciphertext))
        keys.append(keytext)

    return (Ciphertexts,keys)

@login_required
def crypt_request(request):
    user=request.user
    crypt_requests=CryptRequest.objects.filter(user=user)
    return render(request,'forms/crypt_request.html',{'crypt_requests':crypt_requests})

@login_required
def download_csv(request, request_id):
    response=HttpResponse(content_type='text_csv')
    response['Content-Disposition']='attachment; filename="ciphertexts.csv"'

    writer=csv.writer(response)
    writer.writerow(['Plaintext','Ciphertext','Key','IP Address'])

    ciphertexts=CryptText.objects.filter(cryptreq=request_id)

    for cipertext in ciphertexts:
        writer.writerow([cipertext.plaintext,cipertext.ciphertext,cipertext.key,cipertext.ip_addr])
    
    return response