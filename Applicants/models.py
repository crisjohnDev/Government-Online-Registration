from django.db import models

class Barangay(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Applicant(models.Model):

    APPLICATION_CHOICES = [
        ("NEW", "New Registration"),
        ("UPDATE", "Update Information"),
        ("TRANSFER", "Transfer"),
        ("REACTIVATION", "Reactivation"),
        ("REINSTATEMENT", "Reinstatement"),
    ]

    APPLICATION_STATUS = [
        ("APPROVED", "Approved"),
        ("DISAPPROVED", "Disapproved"),
        ("PENDING", "Pending"),
        ("REVIEW", "Review"),
    ]

    PWD_CHOICES = [
        ("NO", "Not PWD"),
        ("VISUAL", "Visual Disability"),
        ("HEARING", "Hearing Disability"),
        ("PHYSICAL", "Physical Disability"),
        ("INTELLECTUAL", "Intellectual Disability"),
        ("PSYCHOSOCIAL", "Psychosocial Disability"),
        ("MULTIPLE", "Multiple Disabilities"),
        ("OTHER", "Other"),
    ]

    CITIZENSHIP_CHOICES = [
        ("BY_BIRTH", "By Birth"),
        ("NATURALIZED", "Naturalized"),
    ]

    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)

    age = models.IntegerField()
    sex = models.CharField(max_length=20)
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=255)


    # Address
    brgy = models.ForeignKey(
        Barangay,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    province = models.CharField(max_length=255, default="Albay")
    municipality = models.CharField(max_length=255, default="Pio Duran")
    phone = models.CharField(max_length=11)
    email = models.EmailField(unique=True)

    application_type = models.CharField(
        max_length=20,
        choices=APPLICATION_CHOICES,
        default="NEW"
    )

    pwd_status = models.CharField(
        max_length=20,
        choices=PWD_CHOICES,
        default="NO"
    )

    citizenship_status = models.CharField(
        max_length=20,
        choices=CITIZENSHIP_CHOICES,
        default="BY_BIRTH"
    )

    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS,
        default='PENDING'
    )

    father = models.CharField(max_length=255)
    mother = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    is_senior = models.BooleanField(default=False)

    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.lastname}, {self.firstname} {self.middlename}"