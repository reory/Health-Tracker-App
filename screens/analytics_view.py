import flet as ft

# Core plotting library - used for charts, analytics and visualizations.
import matplotlib
matplotlib.use("Agg") # Use a non-GUI backend. Use Flet GUI only.

# Pyplot interface that creates charts.
import matplotlib.pyplot as plt

# Enables creating byte buffers for passing images to Flet.
import io

# Used for serializing images/charts into text-safe Base64 form.
import base64
from typing import Any, Dict, List

# Shared page interface for typed navigation.
from ui_types.typed_page import TypedPage


def fig_to_image(fig) -> ft.Image:
    """Convert Matplotlib figure into Flet Image."""

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return ft.Image(src_base64=img_data, expand=True)


def build_intake_time_series(page: TypedPage) -> ft.Image:
    """Chart 1: Intake over time (Grouped by medication)."""

    intake_logs = page.db.intake_logs.get_all()
    medications = {m.id: m for m in page.db.medications.get_all()}

    # Group logs by medication.
    grouped: Dict[str, Dict[str, List]] = {}
    for log in intake_logs:
        med = medications.get(log.medication_id)
        if med is None:
            # Skip if medication is unknown.
            continue

        if med.id not in grouped:
            grouped[med.id] = {
                "name": med.name,
                "times": [],
                "amounts": [],
            }

        grouped[med.id]["times"].append(log.taken_time)
        grouped[med.id]["amounts"].append(log.amount_taken)

    # Build the figure.
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.style.use("seaborn-v0_8")

    if not grouped:
        ax.text(
            0.5, 0.5,
            "No intake data yet",
            ha="center", va="center",
            fontsize=14
        )
        ax.set_axis_off()
        return fig_to_image(fig)
    
    for med_id, data in grouped.items():
        ax.plot(
            data["times"],
            data["amounts"],
            marker="o",
            label=data["name"]
        )

    ax.set_title("Medication intake over time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount Taken")
    ax.legend()
    fig.autofmt_xdate()

    return fig_to_image(fig)

def analytics_view(page: TypedPage) -> ft.View:
    """Main chart/analytics view"""
    
    # Create the chart visualizing intake patterns across days.
    chart = build_intake_time_series(page)
    
    # UI Layout.
    return ft.View(
        route="/analytics",
        controls=[
            ft.AppBar(
                title=ft.Text("Analytics"),
                bgcolor=ft.Colors.RED,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_dashboard(), #type:ignore
                ),
            ),
            ft.Container(
               content=ft.Column( 
                   [
                       ft.Text(
                           "Insights Dashboard",
                           size=22,
                           weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Visual analytics based on your medication intake logs",
                            size=14,
                        ),
                        ft.Divider(),
                        chart,
                    ],
                    spacing=15,
                    expand=True,
                ),
                padding=15,
                expand=True,
            ),
        ],
    )