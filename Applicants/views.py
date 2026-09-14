from django.shortcuts import render, redirect, get_object_or_404
from .models import Applicant, Barangay, ApplicantUpdateRequest, ApplicantTransferRequest, ApplicantReactivationRequest, ApplicantReinstatementRequest

def home(request):

    return render(
        request,
        "applicant/home.html"
    )

def new_registration(request):

    barangays = Barangay.objects.all().order_by("name")

    if request.method == "POST":

        lastname = request.POST.get("lastname", "").strip()
        firstname = request.POST.get("firstname", "").strip()
        middlename = request.POST.get("middlename", "").strip()

        age = request.POST.get("age")
        sex = request.POST.get("sex", "").strip()
        birthdate = request.POST.get("birthdate")
        birthplace = request.POST.get("birthplace", "").strip()

        brgy_id = request.POST.get("brgy")

        province = request.POST.get(
            "province",
            "Albay"
        ).strip()

        municipality = request.POST.get(
            "municipality",
            "Pio Duran"
        ).strip()

        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()

        pwd_status = request.POST.get(
            "pwd_status",
            "NO"
        )

        citizenship_status = request.POST.get(
            "citizenship_status",
            "BY_BIRTH"
        )

        father = request.POST.get(
            "father",
            ""
        ).strip()

        mother = request.POST.get(
            "mother",
            ""
        ).strip()


        # =========================================================
        # BASIC VALIDATION
        # =========================================================

        if not lastname:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Last name is required.",
                    "form_data": request.POST,
                }
            )


        if not firstname:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "First name is required.",
                    "form_data": request.POST,
                }
            )


        if not middlename:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Middle name is required.",
                    "form_data": request.POST,
                }
            )


        if not age:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Age is required.",
                    "form_data": request.POST,
                }
            )


        if not sex:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Sex is required.",
                    "form_data": request.POST,
                }
            )


        if not birthdate:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Birthdate is required.",
                    "form_data": request.POST,
                }
            )


        if not birthplace:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Birthplace is required.",
                    "form_data": request.POST,
                }
            )


        if not brgy_id:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please select a barangay.",
                    "form_data": request.POST,
                }
            )


        if not phone:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Phone number is required.",
                    "form_data": request.POST,
                }
            )


        if not email:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Email address is required.",
                    "form_data": request.POST,
                }
            )


        if not father:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Father's name is required.",
                    "form_data": request.POST,
                }
            )


        if not mother:
            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Mother's name is required.",
                    "form_data": request.POST,
                }
            )


        # =========================================================
        # CHECK EMAIL
        # =========================================================

        if Applicant.objects.filter(email=email).exists():

            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "An applicant with this email address already exists.",
                    "form_data": request.POST,
                }
            )


        # =========================================================
        # GET BARANGAY
        # =========================================================

        try:

            barangay = Barangay.objects.get(
                id=brgy_id
            )

        except Barangay.DoesNotExist:

            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Selected barangay does not exist.",
                    "form_data": request.POST,
                }
            )


        # =========================================================
        # SENIOR CITIZEN
        # =========================================================

        try:

            applicant_age = int(age)

        except (ValueError, TypeError):

            return render(
                request,
                "applicant/forms/new_registration.html",
                {
                    "barangays": barangays,
                    "error": "Invalid age.",
                    "form_data": request.POST,
                }
            )


        is_senior = applicant_age >= 60


        # =========================================================
        # CREATE APPLICANT
        # =========================================================

        applicant = Applicant.objects.create(

            lastname=lastname,

            firstname=firstname,

            middlename=middlename,

            age=applicant_age,

            sex=sex,

            birthdate=birthdate,

            birthplace=birthplace,

            brgy=barangay,

            province=province,

            municipality=municipality,

            phone=phone,

            email=email,

            # NEW REGISTRATION
            application_type="NEW",

            pwd_status=pwd_status,

            citizenship_status=citizenship_status,

            # Always pending when newly submitted
            status="PENDING",

            father=father,

            mother=mother,

            is_active=True,

            is_senior=is_senior,

        )


        # =========================================================
        # SUCCESS
        # =========================================================

        return redirect(
            "registration-success",
            applicant_id=applicant.id
        )


    # =============================================================
    # GET
    # =============================================================

    return render(
        request,
        "applicant/forms/new_registration.html",
        {
            "barangays": barangays,
        }
    )


def registration_success(request, applicant_id):

    applicant = get_object_or_404(
        Applicant,
        id=applicant_id
    )

    return render(
        request,
        "components/registration_success.html",
        {
            "applicant": applicant,
        }
    )


def verify_new_registration(request):

    if request.method == "POST":

        lastname = request.POST.get(
            "lastname",
            ""
        ).strip()

        firstname = request.POST.get(
            "firstname",
            ""
        ).strip()

        middlename = request.POST.get(
            "middlename",
            ""
        ).strip()

        birthdate = request.POST.get(
            "birthdate",
            ""
        ).strip()

        if not lastname:
            return render(
                request,
                "applicant/forms/verify_registration.html",
                {
                    "error": "Last name is required.",
                    "form_data": request.POST,
                }
            )

        if not firstname:
            return render(
                request,
                "applicant/forms/verify_registration.html",
                {
                    "error": "First name is required.",
                    "form_data": request.POST,
                }
            )

        if not middlename:
            return render(
                request,
                "applicant/forms/verify_registration.html",
                {
                    "error": "Middle name is required.",
                    "form_data": request.POST,
                }
            )

        if not birthdate:
            return render(
                request,
                "applicant/forms/verify_registration.html",
                {
                    "error": "Birthdate is required.",
                    "form_data": request.POST,
                }
            )

        applicant = Applicant.objects.filter(
            lastname__iexact=lastname,
            firstname__iexact=firstname,
            middlename__iexact=middlename,
            birthdate=birthdate,
        ).first()

        if applicant:

            return render(
                request,
                "applicant/forms/verify_registration.html",
                {
                    "applicant": applicant,
                    "form_data": request.POST,
                }
            )

        return redirect("new-registration")

    return render(
        request,
        "applicant/forms/verify_registration.html"
    )


def update_registration(request):

    barangays = Barangay.objects.all().order_by("name")

    # =========================================================
    # STEP 1: FIND APPLICANT
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "find_applicant":

        lastname = request.POST.get("lastname", "").strip()
        firstname = request.POST.get("firstname", "").strip()
        middlename = request.POST.get("middlename", "").strip()
        birthdate = request.POST.get("birthdate", "").strip()

        if not lastname:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the last name.",
                    "search_data": request.POST,
                }
            )

        if not firstname:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the first name.",
                    "search_data": request.POST,
                }
            )

        if not middlename:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the middle name.",
                    "search_data": request.POST,
                }
            )

        if not birthdate:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the birthdate.",
                    "search_data": request.POST,
                }
            )

        applicant = Applicant.objects.filter(
            lastname__iexact=lastname,
            firstname__iexact=firstname,
            middlename__iexact=middlename,
            birthdate=birthdate,
        ).first()

        if not applicant:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "error": (
                        "No registration record was found using "
                        "the information provided."
                    ),
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING REQUEST
        # =====================================================

        existing_request = ApplicantUpdateRequest.objects.filter(
            applicant=applicant,
            status__in=["PENDING", "REVIEW"]
        ).exists()

        if existing_request:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "applicant": applicant,
                    "error": (
                        "This applicant already has an "
                        "update or correction request pending review."
                    ),
                }
            )

        return render(
            request,
            "applicant/forms/update_registration.html",
            {
                "barangays": barangays,
                "applicant": applicant,
            }
        )

    # =========================================================
    # STEP 2: SUBMIT UPDATE / CORRECTION REQUEST
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "submit_update":

        applicant_id = request.POST.get("applicant_id")

        if not applicant_id:
            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "barangays": barangays,
                    "error": "Applicant record was not found.",
                    "form_data": request.POST,
                }
            )

        applicant = get_object_or_404(
            Applicant,
            id=applicant_id
        )

        lastname = request.POST.get("lastname", "").strip()
        firstname = request.POST.get("firstname", "").strip()
        middlename = request.POST.get("middlename", "").strip()
        age = request.POST.get("age")
        sex = request.POST.get("sex", "").strip()
        birthdate = request.POST.get("birthdate")
        birthplace = request.POST.get("birthplace", "").strip()
        brgy_id = request.POST.get("brgy")
        province = request.POST.get("province", "Albay").strip()
        municipality = request.POST.get("municipality", "Pio Duran").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        pwd_status = request.POST.get("pwd_status", "NO")
        citizenship_status = request.POST.get(
            "citizenship_status",
            "BY_BIRTH"
        )
        father = request.POST.get("father", "").strip()
        mother = request.POST.get("mother", "").strip()
        reason = request.POST.get("reason", "").strip()

        # =====================================================
        # REQUIRED FIELDS
        # =====================================================

        required_fields = {
            "Last name": lastname,
            "First name": firstname,
            "Middle name": middlename,
            "Age": age,
            "Sex": sex,
            "Birthdate": birthdate,
            "Birthplace": birthplace,
            "Barangay": brgy_id,
            "Province": province,
            "Municipality": municipality,
            "Phone": phone,
            "Email": email,
            "Father's name": father,
            "Mother's name": mother,
            "Reason": reason,
        }

        for field_name, value in required_fields.items():

            if not value:

                return render(
                    request,
                    "applicant/forms/update_registration.html",
                    {
                        "applicant": applicant,
                        "barangays": barangays,
                        "error": f"{field_name} is required.",
                        "form_data": request.POST,
                    }
                )

        # =====================================================
        # AGE VALIDATION
        # =====================================================

        try:
            applicant_age = int(age)

        except (ValueError, TypeError):

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Invalid age.",
                    "form_data": request.POST,
                }
            )

        if applicant_age <= 0:

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Age must be greater than 0.",
                    "form_data": request.POST,
                }
            )

        if applicant_age > 150:

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Please enter a valid age.",
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # DUPLICATE NAME
        # =====================================================

        duplicate_name = Applicant.objects.filter(
            lastname__iexact=lastname,
            firstname__iexact=firstname,
            middlename__iexact=middlename,
        ).exclude(
            id=applicant.id
        ).exists()

        if duplicate_name:

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": (
                        "Another applicant with the same "
                        "last name, first name, and middle name "
                        "already exists."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # DUPLICATE EMAIL
        # =====================================================

        duplicate_email = Applicant.objects.filter(
            email__iexact=email
        ).exclude(
            id=applicant.id
        ).exists()

        if duplicate_email:

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": (
                        "Another applicant with this email "
                        "address already exists."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING UPDATE REQUEST
        # =====================================================

        existing_request = ApplicantUpdateRequest.objects.filter(
            applicant=applicant,
            status__in=["PENDING", "REVIEW"]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": (
                        "This applicant already has an "
                        "update or correction request pending review."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # BARANGAY
        # =====================================================

        try:

            barangay = Barangay.objects.get(
                id=brgy_id
            )

        except Barangay.DoesNotExist:

            return render(
                request,
                "applicant/forms/update_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Selected barangay does not exist.",
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CREATE UPDATE REQUEST
        # =====================================================

        update_request = ApplicantUpdateRequest.objects.create(

            applicant=applicant,

            lastname=lastname,
            firstname=firstname,
            middlename=middlename,

            age=applicant_age,
            sex=sex,
            birthdate=birthdate,
            birthplace=birthplace,

            brgy=barangay,

            province=province,
            municipality=municipality,

            phone=phone,
            email=email,

            pwd_status=pwd_status,
            citizenship_status=citizenship_status,

            father=father,
            mother=mother,

            reason=reason,

            status="PENDING",
        )

        return redirect(
            "update-success",
            request_id=update_request.id
        )

    # =========================================================
    # FIRST PAGE
    # =========================================================

    return render(
        request,
        "applicant/forms/update_registration.html",
        {
            "barangays": barangays,
        }
    )


def update_success(request, request_id):

    update_request = get_object_or_404(
        ApplicantUpdateRequest,
        id=request_id
    )

    return render(
        request,
        "components/update_success.html",
        {
            "update_request": update_request,
        }
    )

def transfer_registration(request):

    barangays = Barangay.objects.all().order_by("name")

    # =========================================================
    # STEP 1: FIND APPLICANT
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "find_applicant":

        lastname = request.POST.get(
            "lastname",
            ""
        ).strip()

        firstname = request.POST.get(
            "firstname",
            ""
        ).strip()

        middlename = request.POST.get(
            "middlename",
            ""
        ).strip()

        birthdate = request.POST.get(
            "birthdate",
            ""
        ).strip()

        if not lastname:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the last name.",
                    "search_data": request.POST,
                }
            )

        if not firstname:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the first name.",
                    "search_data": request.POST,
                }
            )

        if not middlename:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the middle name.",
                    "search_data": request.POST,
                }
            )

        if not birthdate:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "error": "Please enter the birthdate.",
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # FIND APPLICANT
        # =====================================================

        applicant = Applicant.objects.filter(
            lastname__iexact=lastname,
            firstname__iexact=firstname,
            middlename__iexact=middlename,
            birthdate=birthdate,
        ).first()

        if not applicant:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "error": (
                        "No registration record was found "
                        "using the information provided."
                    ),
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING TRANSFER REQUEST
        # =====================================================

        existing_request = ApplicantTransferRequest.objects.filter(
            applicant=applicant,
            status__in=[
                "PENDING",
                "REVIEW",
            ]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "applicant": applicant,
                    "error": (
                        "This applicant already has a "
                        "transfer request pending review."
                    ),
                }
            )

        return render(
            request,
            "applicant/forms/transfer_registration.html",
            {
                "barangays": barangays,
                "applicant": applicant,
            }
        )

    # =========================================================
    # STEP 2: SUBMIT TRANSFER REQUEST
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "submit_transfer":

        applicant_id = request.POST.get(
            "applicant_id"
        )

        if not applicant_id:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "barangays": barangays,
                    "error": "Applicant record was not found.",
                    "form_data": request.POST,
                }
            )

        applicant = get_object_or_404(
            Applicant,
            id=applicant_id
        )

        new_brgy_id = request.POST.get(
            "new_brgy"
        )

        new_municipality = request.POST.get(
            "new_municipality",
            "Pio Duran"
        ).strip()

        new_province = request.POST.get(
            "new_province",
            "Albay"
        ).strip()

        reason = request.POST.get(
            "reason",
            ""
        ).strip()

        # =====================================================
        # REQUIRED FIELDS
        # =====================================================

        if not new_brgy_id:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Please select the new barangay.",
                    "form_data": request.POST,
                }
            )

        if not new_municipality:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Municipality is required.",
                    "form_data": request.POST,
                }
            )

        if not new_province:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Province is required.",
                    "form_data": request.POST,
                }
            )

        if not reason:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": (
                        "Please provide the reason "
                        "for the transfer."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # GET NEW BARANGAY
        # =====================================================

        try:

            new_barangay = Barangay.objects.get(
                id=new_brgy_id
            )

        except Barangay.DoesNotExist:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": "Selected barangay does not exist.",
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # PREVENT SAME BARANGAY
        # =====================================================

        if (
            applicant.brgy_id
            and applicant.brgy_id == new_barangay.id
            and applicant.municipality == new_municipality
            and applicant.province == new_province
        ):

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": (
                        "The new address is the same as "
                        "the applicant's current address."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING REQUEST AGAIN
        # =====================================================

        existing_request = ApplicantTransferRequest.objects.filter(
            applicant=applicant,
            status__in=[
                "PENDING",
                "REVIEW",
            ]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/transfer_registration.html",
                {
                    "applicant": applicant,
                    "barangays": barangays,
                    "error": (
                        "This applicant already has a "
                        "transfer request pending review."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CREATE TRANSFER REQUEST
        # =====================================================

        transfer_request = ApplicantTransferRequest.objects.create(

            applicant=applicant,

            current_brgy=applicant.brgy,

            new_brgy=new_barangay,

            current_municipality=applicant.municipality,

            current_province=applicant.province,

            new_municipality=new_municipality,

            new_province=new_province,

            reason=reason,

            status="PENDING",
        )

        return redirect(
            "transfer-success",
            request_id=transfer_request.id
        )

    # =========================================================
    # FIRST PAGE
    # =========================================================

    return render(
        request,
        "applicant/forms/transfer_registration.html",
        {
            "barangays": barangays,
        }
    )


def transfer_success(request, request_id):

    transfer_request = get_object_or_404(
        ApplicantTransferRequest,
        id=request_id
    )

    return render(
        request,
        "components/transfer_success.html",
        {
            "transfer_request": transfer_request,
        }
    )


def reactivate_registration(request):

    # =========================================================
    # STEP 1: FIND APPLICANT
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "find_applicant":

        lastname = request.POST.get(
            "lastname",
            ""
        ).strip()

        firstname = request.POST.get(
            "firstname",
            ""
        ).strip()

        middlename = request.POST.get(
            "middlename",
            ""
        ).strip()

        birthdate = request.POST.get(
            "birthdate",
            ""
        ).strip()

        if not lastname:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "error": "Please enter the last name.",
                    "search_data": request.POST,
                }
            )

        if not firstname:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "error": "Please enter the first name.",
                    "search_data": request.POST,
                }
            )

        if not middlename:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "error": "Please enter the middle name.",
                    "search_data": request.POST,
                }
            )

        if not birthdate:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "error": "Please enter the birthdate.",
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # FIND APPLICANT
        # =====================================================

        applicant = Applicant.objects.filter(
            lastname__iexact=lastname,
            firstname__iexact=firstname,
            middlename__iexact=middlename,
            birthdate=birthdate,
        ).first()

        if not applicant:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "error": (
                        "No registration record was found "
                        "using the information provided."
                    ),
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # CHECK IF ALREADY ACTIVE
        # =====================================================

        if applicant.is_active:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "This applicant is already active. "
                        "A reactivation request is not necessary."
                    ),
                }
            )

        # =====================================================
        # CHECK EXISTING REACTIVATION REQUEST
        # =====================================================

        existing_request = ApplicantReactivationRequest.objects.filter(
            applicant=applicant,
            status__in=[
                "PENDING",
                "REVIEW",
            ]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "This applicant already has a "
                        "reactivation request pending review."
                    ),
                }
            )

        return render(
            request,
            "applicant/forms/reactivation_registration.html",
            {
                "applicant": applicant,
            }
        )

    # =========================================================
    # STEP 2: SUBMIT REACTIVATION REQUEST
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "submit_reactivation":

        applicant_id = request.POST.get(
            "applicant_id"
        )

        if not applicant_id:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "error": "Applicant record was not found.",
                    "form_data": request.POST,
                }
            )

        applicant = get_object_or_404(
            Applicant,
            id=applicant_id
        )

        # =====================================================
        # CHECK IF ALREADY ACTIVE
        # =====================================================

        if applicant.is_active:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "This applicant is already active. "
                        "A reactivation request is not necessary."
                    ),
                    "form_data": request.POST,
                }
            )

        reason = request.POST.get(
            "reason",
            ""
        ).strip()

        if not reason:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "Please provide the reason "
                        "for reactivation."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING REQUEST
        # =====================================================

        existing_request = ApplicantReactivationRequest.objects.filter(
            applicant=applicant,
            status__in=[
                "PENDING",
                "REVIEW",
            ]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/reactivation_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "This applicant already has a "
                        "reactivation request pending review."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CREATE REQUEST
        # =====================================================

        reactivation_request = ApplicantReactivationRequest.objects.create(
            applicant=applicant,
            reason=reason,
            status="PENDING",
        )

        return redirect(
            "reactivation-success",
            request_id=reactivation_request.id
        )

    # =========================================================
    # FIRST PAGE
    # =========================================================

    return render(
        request,
        "applicant/forms/reactivation_registration.html"
    )


def reactivation_success(request, request_id):

    reactivation_request = get_object_or_404(
        ApplicantReactivationRequest,
        id=request_id
    )

    return render(
        request,
        "components/reactivation_success.html",
        {
            "reactivation_request": reactivation_request,
        }
    )


def reinstate_registration(request):

    # =========================================================
    # STEP 1: FIND APPLICANT
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "find_applicant":

        lastname = request.POST.get(
            "lastname",
            ""
        ).strip()

        firstname = request.POST.get(
            "firstname",
            ""
        ).strip()

        middlename = request.POST.get(
            "middlename",
            ""
        ).strip()

        birthdate = request.POST.get(
            "birthdate",
            ""
        ).strip()

        if not lastname:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "error": "Please enter the last name.",
                    "search_data": request.POST,
                }
            )

        if not firstname:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "error": "Please enter the first name.",
                    "search_data": request.POST,
                }
            )

        if not middlename:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "error": "Please enter the middle name.",
                    "search_data": request.POST,
                }
            )

        if not birthdate:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "error": "Please enter the birthdate.",
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # FIND APPLICANT
        # =====================================================

        applicant = Applicant.objects.filter(
            lastname__iexact=lastname,
            firstname__iexact=firstname,
            middlename__iexact=middlename,
            birthdate=birthdate,
        ).first()

        if not applicant:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "error": (
                        "No registration record was found "
                        "using the information provided."
                    ),
                    "search_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING REINSTATEMENT REQUEST
        # =====================================================

        existing_request = ApplicantReinstatementRequest.objects.filter(
            applicant=applicant,
            status__in=[
                "PENDING",
                "REVIEW",
            ]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "This applicant already has a "
                        "reinstatement request pending review."
                    ),
                }
            )

        return render(
            request,
            "applicant/forms/reinstatement_registration.html",
            {
                "applicant": applicant,
            }
        )

    # =========================================================
    # STEP 2: SUBMIT REINSTATEMENT REQUEST
    # =========================================================

    if request.method == "POST" and request.POST.get("action") == "submit_reinstatement":

        applicant_id = request.POST.get(
            "applicant_id"
        )

        if not applicant_id:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "error": "Applicant record was not found.",
                    "form_data": request.POST,
                }
            )

        applicant = get_object_or_404(
            Applicant,
            id=applicant_id
        )

        reason = request.POST.get(
            "reason",
            ""
        ).strip()

        # =====================================================
        # REQUIRED REASON
        # =====================================================

        if not reason:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "Please provide the reason "
                        "for reinstatement."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CHECK EXISTING REQUEST
        # =====================================================

        existing_request = ApplicantReinstatementRequest.objects.filter(
            applicant=applicant,
            status__in=[
                "PENDING",
                "REVIEW",
            ]
        ).exists()

        if existing_request:

            return render(
                request,
                "applicant/forms/reinstatement_registration.html",
                {
                    "applicant": applicant,
                    "error": (
                        "This applicant already has a "
                        "reinstatement request pending review."
                    ),
                    "form_data": request.POST,
                }
            )

        # =====================================================
        # CREATE REINSTATEMENT REQUEST
        # =====================================================

        reinstatement_request = ApplicantReinstatementRequest.objects.create(
            applicant=applicant,
            reason=reason,
            status="PENDING",
        )

        return redirect(
            "reinstatement-success",
            request_id=reinstatement_request.id
        )

    # =========================================================
    # FIRST PAGE
    # =========================================================

    return render(
        request,
        "applicant/forms/reinstatement_registration.html"
    )


def reinstatement_success(request, request_id):

    reinstatement_request = get_object_or_404(
        ApplicantReinstatementRequest,
        id=request_id
    )

    return render(
        request,
        "components/reinstatement_success.html",
        {
            "reinstatement_request": reinstatement_request,
        }
    )