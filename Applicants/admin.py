from django.contrib import admin

from .models import (
    Barangay,
    Applicant,
    ApplicantUpdateRequest,
    ApplicantTransferRequest,
    ApplicantReactivationRequest,
    ApplicantReinstatementRequest,
    ApplicantBiometric,
    ApplicantNotification,
)


# =========================================================
# BARANGAY
# =========================================================

@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# =========================================================
# APPLICANT
# =========================================================

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "brgy",
        "application_type",
        "status",
        "verification_status",
        "pwd_status",
        "is_senior",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "application_type",
        "status",
        "verification_status",
        "pwd_status",
        "citizenship_status",
        "is_senior",
        "is_active",
        "brgy",
        "date_joined",
    )

    search_fields = (
        "lastname",
        "firstname",
        "middlename",
        "email",
        "phone",
        "father",
        "mother",
    )

    ordering = (
        "-date_joined",
        "-id",
    )

    date_hierarchy = "date_joined"

    list_per_page = 25

    readonly_fields = (
        "date_joined",
    )

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "lastname",
                    "firstname",
                    "middlename",
                    "age",
                    "sex",
                    "birthdate",
                    "birthplace",
                    "civil_status",
                )
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "brgy",
                    "municipality",
                    "province",
                    "phone",
                    "email",
                )
            },
        ),
        (
            "Application",
            {
                "fields": (
                    "application_type",
                    "status",
                    "verification_status",
                )
            },
        ),
        (
            "PWD / Citizenship",
            {
                "fields": (
                    "pwd_status",
                    "citizenship_status",
                    "is_senior",
                )
            },
        ),
        (
            "Family Information",
            {
                "fields": (
                    "father",
                    "mother",
                )
            },
        ),
        (
            "Office Visit",
            {
                "fields": (
                    "office_visit_date",
                    "office_visit_slot",
                )
            },
        ),
        (
            "Account Status",
            {
                "fields": (
                    "is_active",
                    "date_joined",
                )
            },
        ),
    )

    @admin.display(description="Full Name")
    def full_name(self, obj):
        return f"{obj.lastname}, {obj.firstname} {obj.middlename}"


# =========================================================
# UPDATE REQUEST
# =========================================================

@admin.register(ApplicantUpdateRequest)
class ApplicantUpdateRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "requested_at",
        "status",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "requested_at",
        "reviewed_at",
    )

    search_fields = (
        "applicant__lastname",
        "applicant__firstname",
        "applicant__middlename",
        "applicant__email",
        "email",
        "phone",
        "reason",
    )

    ordering = (
        "-requested_at",
        "-id",
    )

    date_hierarchy = "requested_at"

    list_per_page = 25

    readonly_fields = (
        "requested_at",
    )

    autocomplete_fields = (
        "applicant",
        "brgy",
    )


# =========================================================
# TRANSFER REQUEST
# =========================================================

@admin.register(ApplicantTransferRequest)
class ApplicantTransferRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "current_brgy",
        "new_brgy",
        "status",
        "requested_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "current_brgy",
        "new_brgy",
        "requested_at",
        "reviewed_at",
    )

    search_fields = (
        "applicant__lastname",
        "applicant__firstname",
        "applicant__middlename",
        "applicant__email",
        "reason",
    )

    ordering = (
        "-requested_at",
        "-id",
    )

    date_hierarchy = "requested_at"

    list_per_page = 25

    readonly_fields = (
        "requested_at",
    )

    autocomplete_fields = (
        "applicant",
        "current_brgy",
        "new_brgy",
    )


# =========================================================
# REACTIVATION REQUEST
# =========================================================

@admin.register(ApplicantReactivationRequest)
class ApplicantReactivationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "status",
        "requested_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "requested_at",
        "reviewed_at",
    )

    search_fields = (
        "applicant__lastname",
        "applicant__firstname",
        "applicant__middlename",
        "applicant__email",
        "reason",
    )

    ordering = (
        "-requested_at",
        "-id",
    )

    date_hierarchy = "requested_at"

    list_per_page = 25

    readonly_fields = (
        "requested_at",
    )

    autocomplete_fields = (
        "applicant",
    )


# =========================================================
# REINSTATEMENT REQUEST
# =========================================================

@admin.register(ApplicantReinstatementRequest)
class ApplicantReinstatementRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "status",
        "requested_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "requested_at",
        "reviewed_at",
    )

    search_fields = (
        "applicant__lastname",
        "applicant__firstname",
        "applicant__middlename",
        "applicant__email",
        "reason",
    )

    ordering = (
        "-requested_at",
        "-id",
    )

    date_hierarchy = "requested_at"

    list_per_page = 25

    readonly_fields = (
        "requested_at",
    )

    autocomplete_fields = (
        "applicant",
    )


# =========================================================
# BIOMETRICS
# =========================================================

@admin.register(ApplicantBiometric)
class ApplicantBiometricAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "biometrics_completed",
        "signature_completed",
        "completed",
        "captured_at",
        "updated_at",
    )

    list_filter = (
        "biometrics_completed",
        "signature_completed",
        "completed",
        "captured_at",
        "updated_at",
    )

    search_fields = (
        "applicant__lastname",
        "applicant__firstname",
        "applicant__middlename",
        "applicant__email",
        "applicant__phone",
    )

    ordering = (
        "-updated_at",
        "-id",
    )

    date_hierarchy = "captured_at"

    list_per_page = 25

    readonly_fields = (
        "captured_at",
        "updated_at",
    )

    autocomplete_fields = (
        "applicant",
    )

    fieldsets = (
        (
            "Applicant",
            {
                "fields": (
                    "applicant",
                )
            },
        ),
        (
            "Left Finger",
            {
                "fields": (
                    "left_finger",
                    "left_finger_template",
                )
            },
        ),
        (
            "Right Finger",
            {
                "fields": (
                    "right_finger",
                    "right_finger_template",
                )
            },
        ),
        (
            "E-Signature",
            {
                "fields": (
                    "signature",
                )
            },
        ),
        (
            "Capture Status",
            {
                "fields": (
                    "biometrics_completed",
                    "signature_completed",
                    "completed",
                    "captured_at",
                    "updated_at",
                )
            },
        ),
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@admin.register(ApplicantNotification)
class ApplicantNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "notification_type",
        "title",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "applicant__lastname",
        "applicant__firstname",
        "applicant__middlename",
        "applicant__email",
        "title",
        "message",
    )

    ordering = (
        "-created_at",
        "-id",
    )

    date_hierarchy = "created_at"

    list_per_page = 25

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "applicant",
    )

    fieldsets = (
        (
            "Notification",
            {
                "fields": (
                    "applicant",
                    "notification_type",
                    "title",
                    "message",
                    "is_read",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )