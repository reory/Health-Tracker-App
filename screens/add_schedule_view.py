import flet as ft
import datetime
from datetime import date, time
# Import Models.
from models.schedule import Schedule


def add_schedule_view(page, med_id: str) -> ft.View:
    """Create a schedule for a medication."""

    # Empty defaults for a new schedule
    times_field = ft.TextField(label="Times (HH:MM, comma-separated)", value="")
    days_field = ft.TextField(label="Days of Week (0-6, comma-separated)", value="")
    frequency_field = ft.TextField(label="Frequency", value="daily")
    start_date_field = ft.TextField(
        label="Start Date (YYYY-MM-DD)",
        value=date.today().isoformat(),
    )
    end_date_field = ft.TextField(label="End Date (optional)", value="")

    active_switch = ft.Switch(label="Active Schedule", value=True)

    def save_schedule(e):
        # Parse times
        parsed_times = []
        for t in (times_field.value or "").split(","):
            t = t.strip()
            if t:
                hour, minute = map(int, t.split(":"))
                parsed_times.append(time(hour, minute))

        # Parse days
        parsed_days = []
        for d in (days_field.value or "").split(","):
            d = d.strip()
            if d.isdigit():
                parsed_days.append(int(d))

        # Parse dates safely
        start_raw = (start_date_field.value or "").strip()
        start_dt = date.fromisoformat(start_raw) if start_raw else date.today()

        end_raw = (end_date_field.value or "").strip()
        end_dt = date.fromisoformat(end_raw) if end_raw else None

        # Build schedule object
        schedule_obj = Schedule(
            id="",  # repository will asign an ID.
            medication_id=med_id,
            times=parsed_times,
            days_of_week=parsed_days,
            frequency=frequency_field.value or "daily",
            start_date=start_dt,
            end_date=end_dt,
            is_active=active_switch.value,
            created_at=datetime.datetime.now(datetime.timezone.utc),
        )

        page.schedule_repo.add(schedule_obj)

        page.snack_bar = ft.SnackBar(ft.Text("Schedule created"))
        page.snack_bar.open = True
        page.update()

        page.show_edit_medication(med_id)
    
    # UI Layout.
    return ft.View(
        route="/add_schedule",
        controls=[
            ft.AppBar(
                title=ft.Text("Add Schedule"),
                bgcolor=ft.Colors.GREEN,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_edit_medication(med_id),
                ),
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text("New Schedule", size=22, weight=ft.FontWeight.BOLD),

                        times_field,
                        days_field,
                        frequency_field,
                        start_date_field,
                        end_date_field,
                        active_switch,

                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Create Schedule",
                                    icon=ft.Icons.ADD,
                                    on_click=save_schedule,
                                ),
                                ft.TextButton(
                                    "Cancel",
                                    on_click=lambda _: page.show_edit_medication(med_id),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=20,
                ),
            ),
        ],
    )
