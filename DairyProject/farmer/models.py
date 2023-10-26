from django.db import models

class Farmer(models.Model):
    FarmerId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    HouseName = models.CharField(max_length=200)
    City = models.CharField(max_length=50)
    PinCode = models.PositiveIntegerField()
    Occupation = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    DOB = models.DateField()
    RationcardNo = models.PositiveIntegerField()
    Email = models.EmailField()
    Mobile = models.DecimalField(max_digits=10, decimal_places=0)
    AccNo = models.PositiveIntegerField()
    Societycode = models.ForeignKey('Society', on_delete=models.CASCADE)

class Society(models.Model):
    Societycode = models.AutoField(primary_key=True)
    District = models.CharField(max_length=20)
    Subdistrict = models.CharField(max_length=50)
    Panchayath = models.CharField(max_length=50)
    WardNo = models.PositiveIntegerField()
    FarmerId = models.ForeignKey(Farmer, on_delete=models.CASCADE)

class Bank(models.Model):
    IFSCcode = models.AutoField(primary_key=True)
    Bankname = models.CharField(max_length=50)
    Branch = models.CharField(max_length=50)
    Accno = models.PositiveIntegerField()
    FarmerId = models.ForeignKey(Farmer, on_delete=models.CASCADE)

class Cattle(models.Model):
    CattleId = models.AutoField(primary_key=True)
    EarTagID = models.PositiveIntegerField()
    CattleType = models.CharField(max_length=10)
    BreedName = models.CharField(max_length=50)
    weight = models.PositiveIntegerField()
    Age = models.PositiveIntegerField()
    Colour = models.CharField(max_length=50)
    HealthStatus = models.CharField(max_length=50)
    FarmerId = models.ForeignKey(Farmer, on_delete=models.CASCADE)

class MilkingCattle(models.Model):
    Cattleid = models.AutoField(primary_key=True)
    CattleType = models.CharField(max_length=50)
    FarmerId = models.PositiveIntegerField()
    Eartagid = models.ForeignKey(Cattle, on_delete=models.CASCADE)

class HealthRecord(models.Model):
    CattleId = models.AutoField(primary_key=True)
    FarmerId = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    Height = models.PositiveIntegerField()
    Weight = models.PositiveIntegerField()
    Age = models.PositiveIntegerField()
    Feed = models.CharField(max_length=50)
    Medicine = models.CharField(max_length=50)
    MilkObtainedPerDay = models.PositiveIntegerField()
    HealthStatus = models.CharField(max_length=50)

class Breed(models.Model):
    BreedId = models.AutoField(primary_key=True)
    CattleId = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    BreedName = models.CharField(max_length=50)
    EarType = models.CharField(max_length=50)
    Height = models.PositiveIntegerField()

class Customer(models.Model):
    CustomerNo = models.AutoField(primary_key=True)
    OrderNo = models.PositiveIntegerField()
    CustomerName = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10)
    Email = models.EmailField()
    CardNo = models.PositiveIntegerField()
