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

    VERIFICATION_STATUS = [
        ("UNVERIFIED", "Unverified"),
        ("BIOMETRICS_PENDING", "Biometrics Pending"),
        ("VERIFIED", "Verified"),
    ]

    CITIZENSHIP_CHOICES = [
        ("BY_BIRTH", "By Birth"),
        ("NATURALIZED", "Naturalized"),
    ]

    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)

    civil_status = models.CharField(max_length=20, null=True, blank=True)

    age = models.IntegerField()
    sex = models.CharField(max_length=20)
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=255)
    civil_status = models.CharField(max_length=20, null=True, blank=True)


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

    verification_status = models.CharField(
        max_length=30,
        choices=VERIFICATION_STATUS,
        default="UNVERIFIED"
    )

    father = models.CharField(max_length=255)
    mother = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    is_senior = models.BooleanField(default=False)

    date_joined = models.DateField(auto_now_add=True)


    office_visit_date = models.DateField(
        null=True,
        blank=True
    )

    office_visit_slot = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.lastname}, {self.firstname} {self.middlename}"


class ApplicantUpdateRequest(models.Model):

    REQUEST_STATUS = [
        ("PENDING", "Pending"),
        ("REVIEW", "Review"),
        ("APPROVED", "Approved"),
        ("DISAPPROVED", "Disapproved"),
    ]

    applicant = models.ForeignKey(
        "Applicant",
        on_delete=models.CASCADE,
        related_name="update_requests"
    )

    lastname = models.CharField(
        max_length=255
    )

    firstname = models.CharField(
        max_length=255
    )

    middlename = models.CharField(
        max_length=255
    )

    age = models.IntegerField()

    sex = models.CharField(
        max_length=20
    )

    birthdate = models.DateField()

    birthplace = models.CharField(
        max_length=255
    )

    brgy = models.ForeignKey(
        "Barangay",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    province = models.CharField(
        max_length=255,
        default="Albay"
    )

    municipality = models.CharField(
        max_length=255,
        default="Pio Duran"
    )

    phone = models.CharField(
        max_length=11
    )

    email = models.EmailField()

    pwd_status = models.CharField(
        max_length=20
    )

    citizenship_status = models.CharField(
        max_length=20
    )

    father = models.CharField(
        max_length=255
    )

    mother = models.CharField(
        max_length=255
    )

    reason = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default="PENDING"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.applicant} - "
            f"Update Request #{self.id}"
        )


class ApplicantTransferRequest(models.Model):

    REQUEST_STATUS = [
        ("PENDING", "Pending"),
        ("REVIEW", "Review"),
        ("APPROVED", "Approved"),
        ("DISAPPROVED", "Disapproved"),
    ]

    applicant = models.ForeignKey(
        "Applicant",
        on_delete=models.CASCADE,
        related_name="transfer_requests"
    )

    current_brgy = models.ForeignKey(
        "Barangay",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_transfer_requests"
    )

    new_brgy = models.ForeignKey(
        "Barangay",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="new_transfer_requests"
    )

    current_municipality = models.CharField(
        max_length=255,
        default="Pio Duran"
    )

    current_province = models.CharField(
        max_length=255,
        default="Albay"
    )

    new_municipality = models.CharField(
        max_length=255,
        default="Pio Duran"
    )

    new_province = models.CharField(
        max_length=255,
        default="Albay"
    )

    reason = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default="PENDING"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.applicant} - "
            f"Transfer Request #{self.id}"
        )


class ApplicantReactivationRequest(models.Model):

    REQUEST_STATUS = [
        ("PENDING", "Pending"),
        ("REVIEW", "Review"),
        ("APPROVED", "Approved"),
        ("DISAPPROVED", "Disapproved"),
    ]

    applicant = models.ForeignKey(
        "Applicant",
        on_delete=models.CASCADE,
        related_name="reactivation_requests"
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default="PENDING"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.applicant} - "
            f"Reactivation Request #{self.id}"
        )

class ApplicantReinstatementRequest(models.Model):

    REQUEST_STATUS = [
        ("PENDING", "Pending"),
        ("REVIEW", "Review"),
        ("APPROVED", "Approved"),
        ("DISAPPROVED", "Disapproved"),
    ]

    applicant = models.ForeignKey(
        "Applicant",
        on_delete=models.CASCADE,
        related_name="reinstatement_requests"
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=REQUEST_STATUS,
        default="PENDING"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.applicant} - "
            f"Reinstatement Request #{self.id}"
        )


class ApplicantBiometric(models.Model):

    applicant = models.OneToOneField(
        Applicant,
        on_delete=models.CASCADE,
        related_name="biometric"
    )

    # =========================================================
    # LEFT FINGER
    # =========================================================

    left_finger = models.FileField(
        upload_to="biometrics/left/",
        null=True,
        blank=True
    )

    left_finger_template = models.TextField(
        null=True,
        blank=True
    )

    # =========================================================
    # RIGHT FINGER
    # =========================================================

    right_finger = models.FileField(
        upload_to="biometrics/right/",
        null=True,
        blank=True
    )

    right_finger_template = models.TextField(
        null=True,
        blank=True
    )

    # =========================================================
    # E-SIGNATURE
    # =========================================================

    signature = models.ImageField(
        upload_to="signatures/",
        null=True,
        blank=True
    )

    # =========================================================
    # CAPTURE STATUS
    # =========================================================

    biometrics_completed = models.BooleanField(
        default=False
    )

    signature_completed = models.BooleanField(
        default=False
    )

    completed = models.BooleanField(
        default=False
    )

    captured_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Biometrics - {self.applicant}"

class ApplicantNotification(models.Model):

    NOTIFICATION_TYPE = [
        ("APPROVED", "Application Approved"),
        ("BIOMETRICS", "Biometrics Required"),
        ("VERIFIED", "Registration Verified"),
        ("GENERAL", "General"),
    ]

    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPE,
        default="GENERAL"
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.title} - {self.applicant}"