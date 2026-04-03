from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Booking
import json
import openpyxl
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
import io
from datetime import datetime


def booking_form(request):
    """Main booking form page."""
    if request.method == 'POST':
        data = request.POST

        try:
            dob = data.get('date_of_birth') or None
            booking = Booking.objects.create(
                full_name=data.get('full_name', '').strip(),
                email=data.get('email', '').strip(),
                phone=data.get('phone', '').strip(),
                date_of_birth=dob if dob else None,
                gender=data.get('gender', 'prefer_not'),
                service=data.get('service', ''),
                duration=data.get('duration', '60'),
                preferred_date=data.get('preferred_date', ''),
                preferred_time=data.get('preferred_time', ''),
                therapist_preference=data.get('therapist_preference', 'any'),
                health_conditions=data.get('health_conditions', '').strip(),
                allergies=data.get('allergies', '').strip(),
                pressure_preference=data.get('pressure_preference', 'medium'),
                special_requests=data.get('special_requests', '').strip(),
                consent_given=data.get('consent_given') == 'on',
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Booking confirmed!',
                'booking_id': booking.id,
                'name': booking.full_name,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return render(request, 'bookings/booking_form.html')


def export_excel(request):
    """Export ALL bookings to a beautifully styled Excel file."""
    bookings = Booking.objects.all().order_by('-created_at')

    wb = openpyxl.Workbook()

    # ── Sheet 1: All Bookings ──────────────────────────────────────────────
    ws = wb.active
    ws.title = "All Bookings"

    # Colour palette
    gold       = "C9A84C"
    dark_bg    = "1A1A2E"
    mid_bg     = "16213E"
    accent     = "E8D5A3"
    white      = "FFFFFF"
    light_row  = "F5EFE0"
    alt_row    = "EDE3CF"
    green_ok   = "27AE60"
    red_no     = "E74C3C"

    # ---------- Title banner ----------
    ws.merge_cells('A1:R1')
    title_cell = ws['A1']
    title_cell.value = "✦  SERENITY SPA & WELLNESS  ✦  CLIENT BOOKING REGISTER"
    title_cell.font = Font(name='Georgia', size=18, bold=True, color=white)
    title_cell.fill = PatternFill("solid", fgColor=dark_bg)
    title_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 40

    ws.merge_cells('A2:R2')
    sub_cell = ws['A2']
    sub_cell.value = f"Generated on {datetime.now().strftime('%d %B %Y  •  %I:%M %p')}"
    sub_cell.font = Font(name='Calibri', size=10, italic=True, color=accent)
    sub_cell.fill = PatternFill("solid", fgColor=mid_bg)
    sub_cell.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[2].height = 20

    ws.row_dimensions[3].height = 8  # spacer

    # ---------- Column headers ----------
    headers = [
        "#", "Full Name", "Email", "Phone", "Date of Birth", "Gender",
        "Service", "Duration", "Preferred Date", "Preferred Time",
        "Therapist Pref.", "Health Conditions", "Allergies",
        "Pressure Pref.", "Special Requests", "Consent", "Booked At", "Status"
    ]

    col_widths = [5, 22, 28, 16, 14, 12, 24, 14, 15, 13, 16, 24, 20, 14, 28, 9, 22, 10]

    header_row = 4
    for col_idx, (header, width) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(row=header_row, column=col_idx, value=header)
        cell.font = Font(name='Calibri', size=11, bold=True, color=white)
        cell.fill = PatternFill("solid", fgColor=gold)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = Border(
            bottom=Side(style='medium', color=dark_bg),
            right=Side(style='thin', color='B8960C'),
        )
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.row_dimensions[header_row].height = 30

    # Freeze panes below header
    ws.freeze_panes = ws.cell(row=header_row + 1, column=1)

    # ---------- Data rows ----------
    service_map = dict(Booking._meta.get_field('service').choices)
    duration_map = dict(Booking._meta.get_field('duration').choices)
    gender_map = dict(Booking._meta.get_field('gender').choices)
    therapist_map = dict(Booking._meta.get_field('therapist_preference').choices)
    pressure_map = dict(Booking._meta.get_field('pressure_preference').choices)

    thin_border = Border(
        right=Side(style='thin', color='D4C5A0'),
        bottom=Side(style='thin', color='D4C5A0'),
    )

    for row_num, booking in enumerate(bookings, 1):
        actual_row = row_num + header_row
        fill_color = light_row if row_num % 2 == 1 else alt_row
        row_fill = PatternFill("solid", fgColor=fill_color)

        row_data = [
            row_num,
            booking.full_name,
            booking.email,
            booking.phone,
            booking.date_of_birth.strftime('%d/%m/%Y') if booking.date_of_birth else '—',
            gender_map.get(booking.gender, booking.gender),
            service_map.get(booking.service, booking.service),
            duration_map.get(booking.duration, booking.duration),
            booking.preferred_date.strftime('%d/%m/%Y') if booking.preferred_date else '—',
            booking.preferred_time.strftime('%I:%M %p') if booking.preferred_time else '—',
            therapist_map.get(booking.therapist_preference, booking.therapist_preference),
            booking.health_conditions or '—',
            booking.allergies or '—',
            pressure_map.get(booking.pressure_preference, booking.pressure_preference),
            booking.special_requests or '—',
            '✔ Yes' if booking.consent_given else '✘ No',
            booking.created_at.strftime('%d/%m/%Y %I:%M %p'),
            'Confirmed',
        ]

        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=actual_row, column=col_idx, value=value)
            cell.fill = row_fill
            cell.alignment = Alignment(vertical='center', wrap_text=True, horizontal='center' if col_idx in [1, 6, 8, 10, 11, 14, 16, 18] else 'left')
            cell.font = Font(name='Calibri', size=10)
            cell.border = thin_border

            # Consent coloring
            if col_idx == 16:
                cell.font = Font(name='Calibri', size=10, bold=True,
                                 color=green_ok if booking.consent_given else red_no)
            # Status coloring
            if col_idx == 18:
                cell.font = Font(name='Calibri', size=10, bold=True, color='1A6B3C')

        ws.row_dimensions[actual_row].height = 22

    # ---------- Summary footer ----------
    footer_row = header_row + len(bookings) + 2
    ws.merge_cells(f'A{footer_row}:C{footer_row}')
    footer = ws[f'A{footer_row}']
    footer.value = f"Total Bookings: {len(bookings)}"
    footer.font = Font(name='Calibri', size=11, bold=True, color=dark_bg)
    footer.fill = PatternFill("solid", fgColor=accent)
    footer.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[footer_row].height = 24

    # ── Sheet 2: Summary Dashboard ─────────────────────────────────────────
    ws2 = wb.create_sheet("Summary Dashboard")

    ws2.merge_cells('A1:F1')
    ws2['A1'].value = "BOOKING SUMMARY DASHBOARD"
    ws2['A1'].font = Font(name='Georgia', size=16, bold=True, color=white)
    ws2['A1'].fill = PatternFill("solid", fgColor=dark_bg)
    ws2['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 36

    # Service breakdown
    service_counts = {}
    for b in bookings:
        svc = service_map.get(b.service, b.service)
        service_counts[svc] = service_counts.get(svc, 0) + 1

    ws2['A3'].value = "SERVICE"
    ws2['B3'].value = "BOOKINGS"
    for cell in [ws2['A3'], ws2['B3']]:
        cell.font = Font(name='Calibri', size=11, bold=True, color=white)
        cell.fill = PatternFill("solid", fgColor=gold)
        cell.alignment = Alignment(horizontal='center')

    for i, (svc, count) in enumerate(sorted(service_counts.items(), key=lambda x: -x[1]), 4):
        ws2[f'A{i}'].value = svc
        ws2[f'B{i}'].value = count
        ws2[f'A{i}'].font = Font(name='Calibri', size=10)
        ws2[f'B{i}'].font = Font(name='Calibri', size=10, bold=True)
        fill_c = light_row if i % 2 == 0 else alt_row
        ws2[f'A{i}'].fill = PatternFill("solid", fgColor=fill_c)
        ws2[f'B{i}'].fill = PatternFill("solid", fgColor=fill_c)

    ws2.column_dimensions['A'].width = 28
    ws2.column_dimensions['B'].width = 14

    # Bar chart
    if service_counts:
        chart = BarChart()
        chart.type = "col"
        chart.title = "Bookings by Service"
        chart.y_axis.title = "Count"
        chart.x_axis.title = "Service"
        chart.style = 10
        chart.width = 20
        chart.height = 12

        data_ref = Reference(ws2, min_col=2, min_row=3, max_row=3 + len(service_counts))
        cats_ref = Reference(ws2, min_col=1, min_row=4, max_row=3 + len(service_counts))
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)
        ws2.add_chart(chart, "D3")

    # ── Sheet 3: Contact List ──────────────────────────────────────────────
    ws3 = wb.create_sheet("Contact List")
    ws3.merge_cells('A1:E1')
    ws3['A1'].value = "CLIENT CONTACT LIST"
    ws3['A1'].font = Font(name='Georgia', size=14, bold=True, color=white)
    ws3['A1'].fill = PatternFill("solid", fgColor=dark_bg)
    ws3['A1'].alignment = Alignment(horizontal='center', vertical='center')
    ws3.row_dimensions[1].height = 30

    contact_headers = ["Full Name", "Email", "Phone", "Service Booked", "Booking Date"]
    contact_widths = [24, 30, 18, 26, 18]
    for col, (h, w) in enumerate(zip(contact_headers, contact_widths), 1):
        c = ws3.cell(row=3, column=col, value=h)
        c.font = Font(name='Calibri', bold=True, color=white)
        c.fill = PatternFill("solid", fgColor=gold)
        c.alignment = Alignment(horizontal='center')
        ws3.column_dimensions[get_column_letter(col)].width = w

    for r, b in enumerate(bookings, 4):
        row_data = [
            b.full_name, b.email, b.phone,
            service_map.get(b.service, b.service),
            b.preferred_date.strftime('%d/%m/%Y') if b.preferred_date else '—',
        ]
        fill_c = light_row if r % 2 == 0 else alt_row
        for col, val in enumerate(row_data, 1):
            c = ws3.cell(row=r, column=col, value=val)
            c.font = Font(name='Calibri', size=10)
            c.fill = PatternFill("solid", fgColor=fill_c)
            c.alignment = Alignment(vertical='center')

    # Save to buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f"SerenitySpа_Bookings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def admin_dashboard(request):
    """Simple admin view of all bookings."""
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'bookings/admin_dashboard.html', {'bookings': bookings})


def get_booking_count(request):
    """API endpoint to get latest booking count."""
    count = Booking.objects.count()
    return JsonResponse({'count': count})
