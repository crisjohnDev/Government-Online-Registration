from django.urls import path
from . import views

urlpatterns = [
    path(
        "admin/",
        views.admin_login,
        name="admin-login"
    ),

    path(
        "dashboard/",
        views.admin_dashboard,
        name="dashboard"
    ),

    path(
        "admin-logout/",
        views.admin_logout,
        name="admin-logout"
    ),
    path('add-barangay/', views.add_brgy, name="add_brgy"),
    path('brgy-list/', views.brgy_list, name="brgy_list"),
    path('delete-brgy/<int:pk>/', views.delete_brgy, name="delete-brgy"),

    path(
        "admin-applications/",
        views.admin_applications,
        name="admin-applications"
    ),

    path(
        "admin-applications/new/<int:application_id>/",
        views.admin_application_new_detail,
        name="admin-application-new-detail"
    ),

    path(
        "admin-applications/update/<int:application_id>/",
        views.admin_application_update_detail,
        name="admin-application-update-detail"
    ),

    path(
        "admin-applications/transfer/<int:application_id>/",
        views.admin_application_transfer_detail,
        name="admin-application-transfer-detail"
    ),

    path(
        "admin-applications/reactivation/<int:application_id>/",
        views.admin_application_reactivation_detail,
        name="admin-application-reactivation-detail"
    ),

    path(
        "admin-applications/reinstatement/<int:application_id>/",
        views.admin_application_reinstatement_detail,
        name="admin-application-reinstatement-detail"
    ),
    path(
        "admin-applications/<str:application_type>/<int:application_id>/<str:action>/",
        views.admin_application_action,
        name="admin-application-action"
    ),
    path(
        "admin-applicants/<int:applicant_id>/biometric/",
        views.admin_applicant_biometric,
        name="admin-applicant-biometric"
    ),
    path(
        "admin-applicants/<int:applicant_id>/print-slip/",
        views.print_slip_account,
        name="print-slip-account"
    ),
    path(
        "admin-applicants/",
        views.admin_applicants,
        name="admin-applicants"
    ),

    path(
        "admin-applicants/<int:applicant_id>/",
        views.admin_applicant_detail,
        name="admin-applicant-detail"
    ),

    path(
        "admin-applicants/<int:applicant_id>/suspend/",
        views.admin_suspend_applicant,
        name="admin-suspend-applicant"
    ),
    path(
        "admin-reports/",
        views.admin_reports,
        name="admin-reports"
    ),

    path(
        "admin-reports/export/",
        views.admin_reports_export,
        name="admin-reports-export"
    ),

    path(
        "applications/<int:id>/delete/",
        views.delete_application,
        name="delete-application"
    ),

    path(
        "barangays/<int:pk>/applicants/",
        views.barangay_applicants,
        name="barangay_applicants"
    ),
]