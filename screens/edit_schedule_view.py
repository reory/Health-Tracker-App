import flet as ft
import datetime
from datetime import date, time
# Import Models.
from models.schedule import Schedule

def edit_schedule_view(page, med_id: str) -> ft.View:
    """Edit or create a schedule for a medication."""

    # Load schedule from the repository.
    schedules = page.schedule_repo.get_by_medication(med_id)
    sched = schedules[0] if schedules else None
    
    # Pre-fill fields 
    times_str = ", ".join(t.strftime("%H:%M") for t in sched.times) if sched else "" 
    days_str = ", ".join(str(d) for d in (sched.days_of_week if sched else [])) 
    frequency_str = sched.frequency if sched else "daily" 
    start_str = sched.start_date.isoformat() if sched else date.today().isoformat() 
    end_str = sched.end_date.isoformat() if (sched and sched.end_date) else "" 

    times_field = ft.TextField(label="Times (HH:MM, comma-separated)", value=times_str) 
    days_field = ft.TextField(label="Days of Week (0-6, comma-separated)", value=days_str) 
    frequency_field = ft.TextField(label="Frequency", value=frequency_str) 
    start_date_field = ft.TextField(label="Start Date (YYYY-MM-DD)", value=start_str) 
    end_date_field = ft.TextField(label="End Date (optional)", value=end_str)
    
    active_switch = ft.Switch(
        label="Active Schedule",
        value=sched.is_active if sched else True,
    )
    
    def save_schedule(e):
        """Triggered when the user submits the schedule form."""

        # Parse times.
        parsed_times = []
        for t in (times_field.value or "").split(","):
            t = t.strip()
            if t:
                hour, minute = map(int, t.split(":"))
                parsed_times.append(time(hour, minute))

        # Parse days.
        parsed_days = []
        for d in (days_field.value or "").split(","):
            d = d.strip()
            if d.isdigit():
                parsed_days.append(int(d))

        # Parse dates.
        start_raw = (start_date_field.value or "").strip()
        start_dt = date.fromisoformat(start_raw) if start_raw else date.today()

        end_raw = (end_date_field.value or "").strip()
        end_dt = date.fromisoformat(end_raw) if end_raw else None
    
        # Build schedule object.
        schedule_obj = Schedule(
            id=sched.id if sched else "",
            medication_id=med_id,
            times=parsed_times,
            days_of_week=parsed_days,
            frequency=frequency_field.value or "daily",
            start_date=start_dt,
            end_date=end_dt,
            is_active=active_switch.value,
            created_at=sched.created_at if sched else datetime.datetime.now(datetime.timezone.utc),
        )
    
        # Save or update the schedule.
        if sched:
            page.schedule_repo.update(schedule_obj)
        else:
            page.schedule_repo.add(schedule_obj)

        page.snack_bar = ft.SnackBar(ft.Text("Schedule saved"))
        page.snack_bar.open = True
        page.update()
        
        # Go back to the edit medications screen.
        page.show_edit_medication(med_id)
        
    def delete_schedule(e):
        """Delete the schedule for this medication."""
        
        page.schedule_repo.delete_by_medication(med_id)

        page.snack_bar = ft.SnackBar(ft.Text("Schedule Deleted"))
        page.snack_bar.open = True
        page.update()

        page.show_edit_medication(med_id)
    
    # UI Layout.
    return ft.View(
        route="/edit_schedule",
        controls=[
            ft.AppBar(
                title=ft.Text("Edit Schedule"),
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
                        ft.Text("Schedule Details", size=22, weight=ft.FontWeight.BOLD),

                        times_field,
                        days_field,
                        frequency_field,
                        start_date_field,
                        end_date_field,
                        active_switch,

                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Save Schedule",
                                    icon=ft.Icons.SAVE,
                                    on_click=save_schedule,
                                ),
                                ft.ElevatedButton(
                                    "Delete Schedule",
                                    icon=ft.Icons.DELETE,
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.BLACK,
                                    on_click=delete_schedule,
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
    