from django.shortcuts import render,redirect
from .models import Item,Branch,Transactions,Inventory
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

# Create your views here.



def branch(request):
    if request.method == 'POST':
        if request.POST.get('branch_code') and request.POST.get('branch_name') and request.POST.get('branch_addres'):
            branch=Branch()
            branch.branch_code = request.POST.get('branch_code')
            branch.branch_name = request.POST.get('branch_name')
            branch.branch_addres = request.POST.get('branch_addres')
            branch.save()
            return redirect('/')
    else:
        return render(request,'branch.html')

def item(request):
    if request.method == 'POST':
        if request.POST.get('item_name'):
            item=Item()
            item.item_name = request.POST.get('item_name')
            item.save()
            return redirect('/')
    else:
        return render(request,'item.html')


def transaction(request):
    if request.method == 'POST':
        #extract Information
        t_item_id = request.POST.get('item_id')
        t_source_branch = request.POST.get('source_branch')
        t_destination_branch = request.POST.get('destination_branch')
        t_quantity = request.POST.get('quantity')
        t_type = request.POST.get('transaction_type')
        print(t_item_id)
        print(t_source_branch)
        print(t_destination_branch)
        print(t_quantity)
        print(t_type)
        if t_item_id and t_source_branch and t_destination_branch and t_quantity and t_type:
            transaction = Transactions()
            transaction.item_id = request.POST.get('item_id')
            transaction.source_branch = request.POST.get('source_branch')
            transaction.destination_branch = request.POST.get('destination_branch')
            transaction.quantity = request.POST.get('quantity')
            transaction.transaction_type = request.POST.get('transaction_type')
            transaction.save()
            print(Branch.objects.get(branch_code = t_source_branch))
            print(Inventory.objects.get(branch_code = t_source_branch, item_id = t_item_id))
            print(Inventory.objects.get(branch_code = t_destination_branch, item_id = t_item_id))
            source_inventory = Inventory.objects.get(branch_code = t_source_branch, item_id = t_item_id)
            destination_inventory = Inventory.objects.get(branch_code = t_destination_branch, item_id = t_item_id)
            print(source_inventory)
            print(destination_inventory)
            if request.POST.get('Transaction_Type') == 'DEBIT':
                if source_inventory is None:
                    inventory=Inventory()
                    inventory.item_id = request.POST.get('item_id')
                    inventory.branch_code = request.POST.get('branch_code')
                    inventory.quantity = request.POST.get('quantity')
                    inventory.save()
                    source_inventory.quantity = source_inventory.quantity - 2(t_quantity)
                elif destination_inventory is None:
                    inventory=Inventory()
                    inventory.item_id = request.POST.get('item_id')
                    inventory.branch_code = request.POST.get('branch_code')
                    inventory.quantity = request.POST.get('quantity')
                    inventory.save()
                else:
                    source_inventory.quantity -= t_quantity
                    destination_inventory.quantity += t_quantity
            else:
              source_inventory.quantity += t_quantity
              destination_inventory.quantity -= t_quantity
            source_inventory.save()
            destination_inventory.save()
            return redirect('/')    
    else:
        return render(request,'transaction.html')

def inventory(request):
    if request.method == 'POST':
        if request.POST.get('item_id') and request.POST.get('quantity') and request.POST.get('branch_code'):
            inventory=Inventory()
            inventory.item_id = request.POST.get('item_id')
            inventory.branch_code = request.POST.get('branch_code')
            inventory.quantity = request.POST.get('quantity')
            inventory.save()

            return redirect('/')  

    else:
        return render(request,'inventory.html')