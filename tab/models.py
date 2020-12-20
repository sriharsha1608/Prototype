from django.db import models
import uuid

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=300, unique=True, null=True)
    id = models.AutoField(primary_key=True,unique=True, null=False)

class Branch(models.Model):
    branch_code = models.CharField(max_length=300,unique=True)
    branch_name = models.CharField(max_length=300)
    branch_addres = models.CharField(max_length=300)

class Transactions(models.Model):
    id = models.AutoField(primary_key=True,unique=True, null=False)
    #transactions_id = models.CharField(max_length=100, null=True, blank=True, unique=True, default=uuid.uuid4)
    item_id = models.IntegerField()
    source_branch = models.CharField(max_length=300)
    destination_branch = models.CharField(max_length=300)
    transaction_type = models.TextField(max_length=300)
    quantity = models.IntegerField(null=False)

class Inventory(models.Model):
    
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE,to_field='id',null=True)
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE,to_field='branch_code',null=True)
    quantity = models.IntegerField()

class SubContractor(models.Model):
    id = models.AutoField(primary_key=True,unique=True, null=False)
    name = models.CharField(max_length=300)

class SubContractorTransactions(models.Model):
    id = models.AutoField(primary_key=True,unique=True, null=False)
    #transactions_id = models.CharField(max_length=100, null=True, blank=True, unique=True, default=uuid.uuid4)
    item_id = models.IntegerField()
    branch = models.CharField(max_length=300)
    contractor_id = models.IntegerField()
    transaction_type = models.TextField(max_length=300)
    quantity = models.IntegerField(null=False)

class ContractorInventory(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE,to_field='id',null=True)
    contractor_id = models.ForeignKey(SubContractor, on_delete=models.CASCADE,to_field='id',null=True)
    #name = models.CharField(max_length=300)
    quantity = models.IntegerField()

class BillingMaterial(models.Model):
    item_id = models.IntegerField()
    contractor_id = models.IntegerField()
    quantity = models.IntegerField()


