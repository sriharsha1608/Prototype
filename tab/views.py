from django.shortcuts import render,redirect
from .models import Item,Branch,Transactions,Inventory,SubContractor,BillingMaterial,SubContractorTransactions,ContractorInventory
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

# Create your views here.



def branch(request):
    if request.method == 'POST':
        branch=Branch()
        branch.branch_code = request.POST.get('branch_code')
        branch.branch_name = request.POST.get('branch_name')
        branch.branch_addres = request.POST.get('branch_addres')
        if branch.branch_code and branch.branch_name and branch.branch_addres:
            branch.save()
            return redirect('/')
    else:
        return render(request,'branch.html')

def item(request):
    if request.method == 'POST':
        item=Item()
        item.item_name = request.POST.get('item_name')
        if item.item_name:
            item.save()
            return redirect('/')
    else:
        return render(request,'item.html')


def transaction(request):
    if request.method == 'POST':
        #extract Information
        transaction = Transactions()
        transaction.item_id = request.POST.get('item_id')
        transaction.source_branch = request.POST.get('source_branch')
        transaction.destination_branch = request.POST.get('destination_branch')
        transaction.quantity = request.POST.get('quantity')
        transaction.t_type = request.POST.get('transaction_type')
        if transaction.item_id and transaction.source_branch and transaction.destination_branch \
            and transaction.quantity and transaction.t_type:
            
            transaction.save()
            # print(Branch.objects.get(branch_code = t_source_branch))
            # print(t_source_branch)
            # print(t_item_id)
            # print(Inventory.objects.get(branch_code__branch_code = t_source_branch, item_id__id = t_item_id))
            # #print(Inventory.objects.get(branch_code = t_source_branch, item_id = t_item_id))
            # print(Inventory.objects.get(branch_code__branch_code = t_destination_branch, item_id__id = t_item_id))
            # source_inventory = Inventory.objects.get(branch_code = t_source_branch, item_id = t_item_id)
            # destination_inventory = Inventory.objects.get(branch_code = t_destination_branch, item_id = t_item_id)
            # print(source_inventory)
            # print(destination_inventory)
            if transaction.t_type == 'DEBIT':
                # source_inventory = Inventory.objects.get(branch_code = transaction.source_branch,
                #                                              item_id = transaction.item_id)
                # print(source_inventory)
                # if source_inventory is None:
                #     inventory=Inventory()
                #     item_id = request.POST.get('item_id')
                #     item = Item.objects.get(id=item_id)
                #     inventory.item_id = item
                #     branch_code = request.POST.get('branch_code')
                #     branch = Branch.objects.get(branch_code=branch_code)
                #     inventory.branch_code = branch
                #     inventory.quantity = - (t_quantity)
                #     inventory.save()
                #     source_inventory.quantity = source_inventory.quantity - 2(t_quantity)
                # elif destination_inventory is None:
                #     inventory=Inventory()
                #     item_id = request.POST.get('item_id')
                #     item = Item.objects.get(id=item_id)
                #     inventory.item_id = item
                #     branch_code = request.POST.get('branch_code')
                #     branch = Branch.objects.get(branch_code=branch_code)
                #     inventory.branch_code = branch
                #     inventory.quantity = t_quantity
                #     inventory.save()
                # else:
                #     source_inventory.quantity =int(source_inventory.quantity) - int(t_quantity)
                #     destination_inventory.quantity = int(destination_inventory.quantity) + int(t_quantity)
                try:
                    print('a')
                    source_inventory = Inventory.objects.get(branch_code = transaction.source_branch,
                                                             item_id = transaction.item_id)
                    destination_inventory = Inventory.objects.get(branch_code = transaction.destination_branch, 
                                                                  item_id = transaction.item_id)
                    source_inventory.quantity = int(source_inventory.quantity) - int(transaction.quantity)
                    destination_inventory.quantity = int(destination_inventory.quantity) + int(transaction.quantity)
                    print(source_inventory)
                    source_inventory.save()
                    destination_inventory.save()
                except:
                    inventory=Inventory()
                    # item_id = request.POST.get('item_id')
                    item = Item.objects.get(id=transaction.item_id)
                    inventory.item_id = item
                    # branch_code = request.POST.get('branch_code')
                    branch = Branch.objects.get(branch_code=transaction.source_branch)
                    inventory.branch_code = branch
                    inventory.quantity = - int(transaction.quantity)
                    inventory.save()

                    inventory=Inventory()
                    # item_id = request.POST.get('item_id')
                    item = Item.objects.get(id=transaction.item_id)
                    inventory.item_id = item
                    # branch_code = request.POST.get('branch_code')
                    branch = Branch.objects.get(branch_code=transaction.destination_branch)
                    inventory.branch_code = branch
                    inventory.quantity =  int(transaction.quantity)
                    inventory.save()

            # else:
            #     try:
            #         source_inventory = Inventory.objects.get(branch_code = t_source_branch, item_id = t_item_id)
            #         destination_inventory = Inventory.objects.get(branch_code = t_destination_branch, item_id = t_item_id)
            #         source_inventory.quantity =int(source_inventory.quantity) + int(t_quantity)
            #         destination_inventory.quantity =int(destination_inventory.quantity) - int(t_quantity)
            #         source_inventory.save()
            #         destination_inventory.save()
            #     except:
            #         inventory=Inventory()
            #         # item_id = request.POST.get('item_id')
            #         item = Item.objects.get(id=t_item_id)
            #         inventory.item_id = item
            #         # branch_code = request.POST.get('branch_code')
            #         branch = Branch.objects.get(branch_code=t_source_branch)
            #         inventory.branch_code = branch
            #         inventory.quantity =  int(t_quantity)
            #         inventory.save()

            #         inventory=Inventory()
            #         # item_id = request.POST.get('item_id')
            #         item = Item.objects.get(id=t_item_id)
            #         inventory.item_id = item
            #         # branch_code = request.POST.get('branch_code')
            #         branch = Branch.objects.get(branch_code=t_destination_branch)
            #         inventory.branch_code = branch
            #         inventory.quantity =  - int(t_quantity)
            #         inventory.save()

            # source_inventory.save()
            # destination_inventory.save()
            return redirect('/')    
    else:
        return render(request,'transaction.html')

def inventory(request):
    if request.method == 'POST':
        if request.POST.get('item_id') and request.POST.get('quantity') and request.POST.get('branch_code'):
            inventory=Inventory()
            item_id = request.POST.get('item_id')
            item = Item.objects.get(id=item_id)
            inventory.item_id = item
            branch_code = request.POST.get('branch_code')
            branch = Branch.objects.get(branch_code=branch_code)
            inventory.branch_code = branch
            inventory.quantity = request.POST.get('quantity')
            inventory.save()

            return redirect('/')  

    else:
        return render(request,'inventory.html')

def contractorinfo(request):
    if request.method == 'POST':
        #extract Information
        subc = SubContractor()
        subc.name = request.POST.get('name')
        if subc.name:
            subc.save()

            return redirect('/')
    else:
        return render(request,'contractorinfo.html')
            
def billing(request):
    if request.method == 'POST':
        billing = BillingMaterial()
        billing.item_id = request.POST.get('item_id')
        billing.contractor_id = request.POST.get("contractor_id")
        billing.quantity = request.POST.get('quantity')
        if billing.item_id and billing.contractor_id and billing.quantity:
            billing.save()
            update_cinventory = ContractorInventory.objects.get(contractor_id = billing.contractor_id,item_id = billing.item_id)
            update_cinventory.quantity = int(update_cinventory.quantity) - int(billing.quantity)
            update_cinventory.save()
            # cinventory=ContractorInventory()
            # # item_id = request.POST.get('item_id')
            # item = Item.objects.get(id=billing.item_id)
            # cinventory.item_id = item
            # # branch_code = request.POST.get('branch_code')
            # cid = SubContractor.objects.get(id=billing.contractor_id)
            # cinventory.contractor_id = cid
            # cinventory.quantity =  - int(billing.quantity)
            # cinventory.save()
            

            return redirect('/')
    else:
        return render(request,'billing.html')

def distributiontocontractors(request):
    if request.method == 'POST':
        sct = SubContractorTransactions()
        sct.item_id = request.POST.get('item_id')
        sct.branch = request.POST.get('branch')
        sct.contractor_id = request.POST.get('contractor_id')
        sct.quantity = request.POST.get('quantity')
        sct.transaction_type = request.POST.get('transaction_type')
        # print(sct.item_id,sct.branch,sct.contractor_id,sct.transaction_type,sct.quantity)
        # source_distributioninventory = Inventory.objects.get(branch_code = sct.branch,item_id = sct.item_id)
        # print(source_distributioninventory)
        if sct.item_id and sct.branch and sct.contractor_id and sct.quantity and sct.transaction_type:
            sct.save()
            if sct.transaction_type == 'OUT':
                try:
                    source_distributioninventory = Inventory.objects.get(branch_code = sct.branch,item_id = sct.item_id)
                    print(source_distributioninventory)
                    source_distributioninventory.quantity = int(source_distributioninventory.quantity) - int(sct.quantity)
                    source_distributioninventory.save()
                except:
                    inventory=Inventory()
                    # item_id = request.POST.get('item_id')
                    item = Item.objects.get(id=sct.item_id)
                    inventory.item_id = item
                    # branch_code = request.POST.get('branch_code')
                    branch = Branch.objects.get(branch_code=sct.branch)
                    inventory.branch_code = branch
                    inventory.quantity = - int(sct.quantity)
                    inventory.save()

                try:
                    destination_distributioninventory = ContractorInventory.objects.get(contractor_id = sct.contractor_id,item_id = sct.item_id)
                    print(destination_distributioninventory)
                    
                    destination_distributioninventory.quantity = int(destination_distributioninventory.quantity) + int(sct.quantity)
                    # print(source_inventory)
                    
                    destination_distributioninventory.save()
                except:
                    cinventory=ContractorInventory()
                    # item_id = request.POST.get('item_id')
                    item = Item.objects.get(id=sct.item_id)
                    cinventory.item_id = item
                    # branch_code = request.POST.get('branch_code')
                    cid = SubContractor.objects.get(id=sct.contractor_id)
                    cinventory.contractor_id = cid
                    cinventory.quantity =  int(sct.quantity)
                    cinventory.save()
                return redirect('/')       
            else:
                # try:
                #     source_distributioninventory = Inventory.objects.get(branch_code = sct.branch,
                #                                              item_id = sct.item_id)
                #     destination_distributioninventory = ContractorInventory.objects.get(contractor_id = sct.contractor_id, 
                #                                                   item_id = sct.item_id)
                #     source_distributioninventory.quantity = int(source_distributioninventory.quantity) + int(sct.quantity)
                #     destination_distributioninventory.quantity = int(destination_distributioninventory.quantity) - int(sct.quantity)

                #     # print(source_inventory)
                #     source_distributioninventory.save()
                #     destination_distributioninventory.save()
                # except:
                #     inventory=Inventory()
                #     # item_id = request.POST.get('item_id')
                #     item = Item.objects.get(id=sct.item_id)
                #     inventory.item_id = item
                #     # branch_code = request.POST.get('branch_code')
                #     branch = Branch.objects.get(branch_code=sct.branch)
                #     inventory.branch_code = branch
                #     inventory.quantity = + int(sct.quantity)
                #     inventory.save()

                #     cinventory=ContractorInventory()
                #     # item_id = request.POST.get('item_id')
                #     item = Item.objects.get(id=sct.item_id)
                #     cinventory.item_id = item
                #     # branch_code = request.POST.get('branch_code')
                #     cid = SubContractor.objects.get(id=sct.contractor_id)
                #     cinventory.contractor_id = cid
                #     cinventory.quantity = - int(sct.quantity)
                #     cinventory.save()
                try:
                    source_distributioninventory = Inventory.objects.get(branch_code = sct.branch,item_id = sct.item_id)
                    print(source_distributioninventory)
                    source_distributioninventory.quantity = int(source_distributioninventory.quantity) + int(sct.quantity)
                    source_distributioninventory.save()
                except:
                    inventory=Inventory()
                    # item_id = request.POST.get('item_id')
                    item = Item.objects.get(id=sct.item_id)
                    inventory.item_id = item
                    # branch_code = request.POST.get('branch_code')
                    branch = Branch.objects.get(branch_code=sct.branch)
                    inventory.branch_code = branch
                    inventory.quantity = + int(sct.quantity)
                    inventory.save()

                try:
                    destination_distributioninventory = ContractorInventory.objects.get(contractor_id = sct.contractor_id,item_id = sct.item_id)
                    print(destination_distributioninventory)
                    
                    destination_distributioninventory.quantity = int(destination_distributioninventory.quantity) - int(sct.quantity)
                    # print(source_inventory)
                    
                    destination_distributioninventory.save()
                except:
                    cinventory=ContractorInventory()
                    # item_id = request.POST.get('item_id')
                    item = Item.objects.get(id=sct.item_id)
                    cinventory.item_id = item
                    # branch_code = request.POST.get('branch_code')
                    cid = SubContractor.objects.get(id=sct.contractor_id)
                    cinventory.contractor_id = cid
                    cinventory.quantity =  - int(sct.quantity)
                    cinventory.save()
                return redirect('/')     
    else:
        return render(request,'distributiontocontractors.html')