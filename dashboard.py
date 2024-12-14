import customtkinter as ctk
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
from tkinter import messagebox, ttk
import tkinter as tk
import os


class DashboardApp:
    def __init__(self, dashboard, user_id):
        self.master = dashboard
        self.user_id = user_id
        dashboard.title("Health Tracker Dashboard")
        dashboard.geometry("925x500+300+200")

        # Initialize tabs
        self.notebook = None
        self.dashboard_tab = None
        self.mental_health_tab = None
        self.physical_health_tab = None
        self.user_info_tab = None

        # Database connection
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="MIRAI_DB"
            )
            self.cursor = self.db_connection.cursor(dictionary=True)
            self.load_userprofile()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")
            sys.exit(1)

        # Set the color theme and font
        self.custom_color = "#bc6c25"
        self.custom_font = ("Microsoft YaHei UI Light", 12)

        # Configure style
        self.style = ttk.Style()
        self.style.configure("Custom.TNotebook.Tab", font=self.custom_font)

        # Create widgets after initialization
        self.create_widgets()

        # Create initial dashboard content
        self.create_dashboard_content()

    def load_userprofile(self):
        query = """
        SELECT up.*, u.username, u.email 
        FROM userprofile_TB up 
        JOIN User_TB u ON up.user_id = u.user_id 
        WHERE up.user_id = %s
        """
        self.cursor.execute(query, (self.user_id,))
        self.userprofile = self.cursor.fetchone()

        if self.userprofile is None:
            messagebox.showerror("User Profile Error", "No user profile found for the given user_id.")
            sys.exit(1)
    def create_widgets(self):
        # Create the notebook (tabview)
        self.notebook = ctk.CTkTabview(self.master)
        self.notebook.pack(fill="both", expand=True)

        # Add tabs
        self.dashboard_tab = self.notebook.add("Dashboard")
        self.mental_health_tab = self.notebook.add("Mental Health")
        self.physical_health_tab = self.notebook.add("Physical Health")
        self.user_info_tab = self.notebook.add("User Info")

        # Add widgets to the tabs
        self.create_dashboard_content()
        self.create_mental_health_content()
        self.create_physical_health_content()
        self.create_user_info_content()

    def create_user_info_content(self):
        # Create a frame for user info
        user_info_frame = ctk.CTkFrame(self.user_info_tab)
        user_info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create labels and entry fields for user information
        fields = [
            ("Full Name", 'full_name'),
            ("Email", 'email'),
            ("Phone", 'phone_number'),
            ("Address", 'address'),
            ("Gender", 'gender'),
            ("Date of Birth", 'dob'),
            ("Medical History", 'medical_history')
        ]
        self.user_info_entries = {}

        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = i % 2

            label_widget = ctk.CTkLabel(user_info_frame, text=f"{label}:", font=self.custom_font)
            label_widget.grid(row=row, column=col * 2, sticky="e", padx=10, pady=5)

            if key == 'medical_history':
                entry = ctk.CTkTextbox(user_info_frame, height=100, width=200, font=self.custom_font)
                entry.grid(row=row, column=col * 2 + 1, sticky="w", padx=10, pady=5)
                entry.insert("1.0", str(self.userprofile.get(key, "")))
            else:
                entry = ctk.CTkEntry(user_info_frame, width=200, font=self.custom_font)
                entry.grid(row=row, column=col * 2 + 1, sticky="w", padx=10, pady=5)
                entry.insert(0, str(self.userprofile.get(key, "")))

            self.user_info_entries[key] = entry

        # Add an Edit button
        edit_button = ctk.CTkButton(user_info_frame, text="Edit", command=self.toggle_edit_mode, font=self.custom_font)
        edit_button.grid(row=len(fields), column=1, pady=20)

        # Initially disable all entries
        self.set_entries_state("disabled")

    def toggle_edit_mode(self):
        current_state = self.user_info_entries['full_name'].cget("state")
        if current_state == "disabled":
            self.set_entries_state("normal")
            self.user_info_tab.winfo_children()[0].winfo_children()[-1].configure(text="Save",
                                                                                  command=self.save_user_info)
        else:
            self.set_entries_state("disabled")
            self.user_info_tab.winfo_children()[0].winfo_children()[-1].configure(text="Edit",
                                                                                  command=self.toggle_edit_mode)

    def set_entries_state(self, state):
        for entry in self.user_info_entries.values():
            if isinstance(entry, ctk.CTkTextbox):
                entry.configure(state=state)
            else:
                entry.configure(state=state)

    def save_user_info(self):
        try:
            query = """
            UPDATE userprofile_TB
            SET full_name = %s, phone_number = %s, address = %s, gender = %s, dob = %s, medical_history = %s
            WHERE user_id = %s
            """
            values = (
                self.user_info_entries['full_name'].get(),
                self.user_info_entries['phone_number'].get(),
                self.user_info_entries['address'].get(),
                self.user_info_entries['gender'].get(),
                self.user_info_entries['dob'].get(),
                self.user_info_entries['medical_history'].get("1.0", tk.END).strip(),
                self.user_id
            )

            self.cursor.execute(query, values)
            self.db_connection.commit()

            messagebox.showinfo("Success", "Profile updated successfully!")
            self.load_userprofile()  # Reload user profile
            self.set_entries_state("disabled")
            self.user_info_tab.winfo_children()[0].winfo_children()[-1].configure(text="Edit",
                                                                                  command=self.toggle_edit_mode)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update profile: {err}")


    def create_dashboard_content(self):
        # Summary cards
        summary_frame = ctk.CTkFrame(self.dashboard_tab)
        summary_frame.pack(fill="x", padx=10, pady=10)

        # Fetch latest mental health stats
        self.cursor.execute("""
            SELECT 
                AVG(mood) as avg_mood,
                AVG(stress_level) as avg_stress,
                COUNT(*) as total_entries
            FROM MentalHealth_TB
            WHERE user_id = %s
            AND date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
        """, (self.user_id,))
        stats = self.cursor.fetchone()

        # Create summary cards
        self.create_summary_card(summary_frame, "Average Mood",
                                 f"{stats['avg_mood']:.1f}/10" if stats and stats['avg_mood'] is not None else "N/A")
        self.create_summary_card(summary_frame, "Average Stress", f"{stats['avg_stress']:.1f}/10" if stats and stats[
            'avg_stress'] is not None else "N/A")
        self.create_summary_card(summary_frame, "Monthly Entries",
                                 str(stats['total_entries']) if stats and stats['total_entries'] is not None else "0")

        # Create mood trend graph
        self.create_mood_trend_graph()

    def create_summary_card(self, parent, title, value):
        card = ctk.CTkFrame(parent)
        card.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        ctk.CTkLabel(
            card,
            text=title,
            font=self.custom_font
        ).pack(pady=5)

        ctk.CTkLabel(
            card,
            text=value,
            font=("Microsoft YaHei UI Light", 24, "bold"),
            text_color=self.custom_color
        ).pack(pady=5)

    def create_mood_trend_graph(self):
        # Fetch mood data for the last 30 days
        self.cursor.execute("""
            SELECT date, mood
            FROM MentalHealth_TB
            WHERE user_id = %s
            AND date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
            ORDER BY date
        """, (self.user_id,))
        mood_data = self.cursor.fetchall()

        dates = [entry['date'] for entry in mood_data]
        moods = [entry['mood'] for entry in mood_data]

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 4))
        if moods:
            ax.plot(dates, moods, marker='o')
        ax.set_title("Mood Trend (Last 30 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood")
        ax.set_ylim(0, 10)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Embed the plot in the dashboard
        canvas = FigureCanvasTkAgg(fig, master=self.dashboard_tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def create_mental_health_content(self):
        # Mood logging section
        mood_frame = ctk.CTkFrame(self.mental_health_tab)
        mood_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            mood_frame,
            text="Log Your Mental Health",
            font=("Microsoft YaHei UI Light", 16, "bold")
        ).pack(pady=10)

        # Mood and stress sliders
        self.mood_var = tk.IntVar(value=5)
        self.stress_var = tk.IntVar(value=5)

        self.create_slider(mood_frame, "Mood", self.mood_var)
        self.create_slider(mood_frame, "Stress Level", self.stress_var)

        # Symptoms and journaling
        ctk.CTkLabel(
            mood_frame,
            text="Symptoms (if any):",
            font=self.custom_font
        ).pack(pady=5)

        self.symptoms_entry = ctk.CTkTextbox(
            mood_frame,
            height=60,
            font=self.custom_font
        )
        self.symptoms_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            mood_frame,
            text="Journal Entry:",
            font=self.custom_font
        ).pack(pady=5)

        self.journal_entry = ctk.CTkTextbox(
            mood_frame,
            height=100,
            font=self.custom_font
        )
        self.journal_entry.pack(fill="x", padx=10, pady=5)

        # Save button
        ctk.CTkButton(
            mood_frame,
            text="Save Entry",
            command=self.save_mental_health_entry,
            font=self.custom_font,
            fg_color=self.custom_color
        ).pack(pady=10)

    def create_slider(self, parent, label, variable):
        slider_frame = ctk.CTkFrame(parent)
        slider_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            slider_frame,
            text=f"{label}:",
            font=self.custom_font
        ).pack(side="left", padx=10)

        slider = ctk.CTkSlider(
            slider_frame,
            from_=1,
            to=10,
            variable=variable,
            width=200
        )
        slider.pack(side="left", padx=10)

        # Value label
        value_label = ctk.CTkLabel(
            slider_frame,
            textvariable=variable,
            font=self.custom_font
        )
        value_label.pack(side="left", padx=5)

    def save_mental_health_entry(self):
        try:
            query = """
            INSERT INTO MentalHealth_TB 
            (user_id, mood, stress_level, symptoms, journaling, date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                self.user_id,
                self.mood_var.get(),
                self.stress_var.get(),
                self.symptoms_entry.get("1.0", "end-1c"),
                self.journal_entry.get("1.0", "end-1c"),
                datetime.now().date()
            )

            self.cursor.execute(query, values)
            self.db_connection.commit()

            messagebox.showinfo("Success", "Mental health entry saved successfully!")
            self.clear_mental_health_form()
            self.create_dashboard_content()  # Refresh dashboard

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to save entry: {err}")

    def clear_mental_health_form(self):
        self.mood_var.set(5)
        self.stress_var.set(5)
        self.symptoms_entry.delete("1.0", "end")
        self.journal_entry.delete("1.0", "end")

    def update_profile(self):
        try:
            query = """
            UPDATE userprofile_TB
            SET full_name = %s, phone_number = %s, address = %s, gender = %s, dob = %s, medical_history = %s
            WHERE user_id = %s
            """
            values = (
                self.user_info_entries['full_name'].get(),
                self.user_info_entries['phone_number'].get(),
                self.user_info_entries['address'].get(),
                self.user_info_entries['gender'].get(),
                self.user_info_entries['dob'].get(),
                self.user_info_entries['medical_history'].get("1.0", tk.END).strip(),
                self.user_id
            )

            self.cursor.execute(query, values)
            self.db_connection.commit()

            messagebox.showinfo("Success", "Profile updated successfully!")
            self.load_userprofile()  # Reload user profile

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update profile: {err}")

    def log_mood(self):
        self.notebook.select(1)  # Switch to Mental Health tab

    def add_journal(self):
        self.notebook.select(1)  # Switch to Mental Health tab
        self.journal_entry.focus_set()

    def show_exercises(self):
        exercises_window = ctk.CTkToplevel(self.master)
        exercises_window.title("Cognitive Exercises")
        exercises_window.geometry("400x300")

        exercises = ['Puzzle', 'Memory Game', 'Sudoku', 'Brain Training', 'Other']

        ctk.CTkLabel(
            exercises_window,
            text="Select an Exercise",
            font=("Microsoft YaHei UI Light", 16, "bold")
        ).pack(pady=10)

        for exercise in exercises:
            ctk.CTkButton(
                exercises_window,
                text=exercise,
                font=self.custom_font,
                fg_color=self.custom_color,
                command=lambda e=exercise: self.start_exercise(e)
            ).pack(pady=5)

    def start_exercise(self, exercise_type):
        messagebox.showinfo("Exercise", f"Starting {exercise_type}")
        # Here you would implement the actual exercise logic

    def view_history(self):
        history_window = ctk.CTkToplevel(self.master)
        history_window.title("Mental Health History")
        history_window.geometry("600x400")

        # Create a treeview
        columns = ("Date", "Mood", "Stress", "Symptoms")
        tree = ttk.Treeview(history_window, columns=columns, show='headings')

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Fetch history data
        self.cursor.execute("""
            SELECT date, mood, stress_level, symptoms
            FROM MentalHealth_TB
            WHERE user_id = %s
            ORDER BY date DESC
        """, (self.user_id,))
        history_data = self.cursor.fetchall()

        # Insert data into the treeview
        for entry in history_data:
            tree.insert('', 'end', values=(entry['date'], entry['mood'], entry['stress_level'], entry['symptoms']))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def calculate_mental_health_score(self):
        # Fetch the last 7 days of mental health data
        self.cursor.execute("""
            SELECT AVG(mood) as avg_mood, AVG(stress_level) as avg_stress
            FROM MentalHealth_TB
            WHERE user_id = %s
            AND date >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
        """, (self.user_id,))
        result = self.cursor.fetchone()

        if result and result['avg_mood'] is not None and result['avg_stress'] is not None:
            # Calculate a simple mental health score
            # Higher mood and lower stress are better
            mental_health_score = (result['avg_mood'] * 10) - (result['avg_stress'] * 5)
            return max(0, min(100, mental_health_score))  # Ensure score is between 0 and 100
        else:
            return None

    def update_dashboard(self):
        # Clear existing widgets
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()

        # Recreate dashboard content
        self.create_dashboard_content()

        # Add mental health score
        score = self.calculate_mental_health_score()
        if score is not None:
            score_frame = ctk.CTkFrame(self.dashboard_tab)
            score_frame.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                score_frame,
                text=f"Mental Health Score: {score:.1f}",
                font=("Microsoft YaHei UI Light", 18, "bold"),
                text_color=self.custom_color
            ).pack(pady=10)

        # Schedule the next update
        self.master.after(60000, self.update_dashboard)  # Update every minute

    def start_tracking(self):
        # Implement start tracking functionality
        pass

    def show_mental_health(self):
        self.notebook.select(1)

    def create_widgets(self):
        # Create the notebook (tabview)
        self.notebook = ctk.CTkTabview(self.master)
        self.notebook.pack(fill="both", expand=True)

        # Add tabs
        self.dashboard_tab = self.notebook.add("Dashboard")
        self.mental_health_tab = self.notebook.add("Mental Health")
        self.physical_health_tab = self.notebook.add("Physical Health")
        self.user_info_tab = self.notebook.add("User Info")

        # Add widgets to each tab
        self.create_dashboard_content()
        self.create_mental_health_content()
        self.create_physical_health_content()
        self.create_user_info_content()

    def create_physical_health_content(self):
        # Main frame for physical health
        physical_frame = ctk.CTkFrame(self.physical_health_tab)
        physical_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # BMI Calculator Section
        bmi_frame = ctk.CTkFrame(physical_frame)
        bmi_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            bmi_frame,
            text="BMI Calculator",
            font=("Microsoft YaHei UI Light", 16, "bold")
        ).pack(pady=5)

        # Weight and Height inputs
        weight_frame = ctk.CTkFrame(bmi_frame)
        weight_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(weight_frame, text="Weight (kg):", font=self.custom_font).pack(side="left", padx=5)
        self.weight_var = tk.StringVar()
        weight_entry = ctk.CTkEntry(weight_frame, textvariable=self.weight_var, width=100)
        weight_entry.pack(side="left", padx=5)

        height_frame = ctk.CTkFrame(bmi_frame)
        height_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(height_frame, text="Height (cm):", font=self.custom_font).pack(side="left", padx=5)
        self.height_var = tk.StringVar()
        height_entry = ctk.CTkEntry(height_frame, textvariable=self.height_var, width=100)
        height_entry.pack(side="left", padx=5)

        # Calculate BMI button
        ctk.CTkButton(
            bmi_frame,
            text="Calculate BMI",
            command=self.calculate_bmi,
            font=self.custom_font,
            fg_color=self.custom_color
        ).pack(pady=10)

        # BMI Result display
        self.bmi_result_label = ctk.CTkLabel(
            bmi_frame,
            text="",
            font=("Microsoft YaHei UI Light", 14, "bold")
        )
        self.bmi_result_label.pack(pady=5)

        # Activity Tracking Section
        activity_frame = ctk.CTkFrame(physical_frame)
        activity_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            activity_frame,
            text="Activity Tracking",
            font=("Microsoft YaHei UI Light", 16, "bold")
        ).pack(pady=5)

        # Activity type selection
        activity_type_frame = ctk.CTkFrame(activity_frame)
        activity_type_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(activity_type_frame, text="Activity:", font=self.custom_font).pack(side="left", padx=5)
        self.activity_var = tk.StringVar()
        activities = ['Walking', 'Running', 'Cycling', 'Swimming', 'Gym', 'Other']
        activity_dropdown = ctk.CTkOptionMenu(
            activity_type_frame,
            variable=self.activity_var,
            values=activities,
            width=150
        )
        activity_dropdown.pack(side="left", padx=5)

        # Duration input
        duration_frame = ctk.CTkFrame(activity_frame)
        duration_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(duration_frame, text="Duration (minutes):", font=self.custom_font).pack(side="left", padx=5)
        self.duration_var = tk.StringVar()
        duration_entry = ctk.CTkEntry(duration_frame, textvariable=self.duration_var, width=100)
        duration_entry.pack(side="left", padx=5)

        # Calories burned input
        calories_frame = ctk.CTkFrame(activity_frame)
        calories_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(calories_frame, text="Calories Burned:", font=self.custom_font).pack(side="left", padx=5)
        self.calories_var = tk.StringVar()
        calories_entry = ctk.CTkEntry(calories_frame, textvariable=self.calories_var, width=100)
        calories_entry.pack(side="left", padx=5)

        # Save activity button
        ctk.CTkButton(
            activity_frame,
            text="Log Activity",
            command=self.save_physical_activity,
            font=self.custom_font,
            fg_color=self.custom_color
        ).pack(pady=10)

        ctk.CTkButton(
            activity_frame,
            text="View Activity History",
            command=lambda: self.open_history_window("activity"),
            font=self.custom_font,
            fg_color=self.custom_color
        ).pack(pady=10)

        # Progress Chart
        self.create_physical_health_chart()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get())
            height = float(self.height_var.get()) / 100  # Convert cm to meters
            bmi = weight / (height * height)

            # Determine BMI status and color
            if bmi < 18.5:
                status = "Underweight"
                color = "orange"
            elif 18.5 <= bmi < 25:
                status = "Normal"
                color = "green"
            elif 25 <= bmi < 30:
                status = "Overweight"
                color = "orange"
            else:
                status = "Obese"
                color = "red"

            # Update BMI in database
            self.save_bmi_data(bmi, status)

            # Display result
            self.bmi_result_label.configure(
                text=f"BMI: {bmi:.1f} - {status}",
                text_color=color
            )

            # Show health suggestions
            self.show_health_suggestions(status)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height values")

    def save_bmi_data(self, bmi, status):
        try:
            query = """
            INSERT INTO physicalhealth_tb 
            (user_id, date, bmi_status, weight, height) 
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                self.user_id,
                datetime.now().date(),
                status,
                float(self.weight_var.get()),
                float(self.height_var.get())
            )

            self.cursor.execute(query, values)
            self.db_connection.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to save BMI data: {err}")

    def save_physical_activity(self):
        try:
            query = """
            INSERT INTO physicalhealth_tb 
            (user_id, date, activity_type, duration, calories_burned) 
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                self.user_id,
                datetime.now().date(),
                self.activity_var.get(),
                int(self.duration_var.get()),
                int(self.calories_var.get())
            )

            self.cursor.execute(query, values)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Activity logged successfully!")

            # Clear inputs
            self.duration_var.set("")
            self.calories_var.set("")

            # Refresh chart
            self.create_physical_health_chart()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid duration and calories values")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to save activity: {err}")

    def create_physical_health_chart(self):
        # Fetch activity data for the last 30 days
        self.cursor.execute("""
            SELECT date, SUM(calories_burned) as total_calories
            FROM physicalhealth_tb
            WHERE user_id = %s 
            AND date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
            GROUP BY date
            ORDER BY date
        """, (self.user_id,))
        activity_data = self.cursor.fetchall()

        if activity_data:
            dates = [entry['date'] for entry in activity_data]
            calories = [entry['total_calories'] for entry in activity_data]

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(dates, calories)
            ax.set_title("Daily Calories Burned (Last 30 Days)")
            ax.set_xlabel("Date")
            ax.set_ylabel("Calories")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Create chart frame if it doesn't exist
            if hasattr(self, 'chart_frame'):
                self.chart_frame.destroy()

            self.chart_frame = ctk.CTkFrame(self.physical_health_tab)
            self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)

    def open_history_window(self, record_type):
        """Opens a new window to select a date and view records for activities or journaling."""
        history_window = ctk.CTkToplevel(self.master)
        history_window.title(f"View {record_type.capitalize()} History")
        history_window.geometry("500x400")

        # Instructions label
        ctk.CTkLabel(
            history_window,
            text=f"Select a date to view {record_type.capitalize()} records:",
            font=("Microsoft YaHei UI Light", 14)
        ).pack(pady=10)

        # Date entry
        date_var = tk.StringVar()
        date_entry = ctk.CTkEntry(history_window, textvariable=date_var, placeholder_text="YYYY-MM-DD")
        date_entry.pack(pady=10)

        # Search button
        def fetch_records():
            selected_date = date_var.get()
            try:
                datetime.strptime(selected_date, "%Y-%m-%d")  # Validate date format
                query = f"""
                SELECT * FROM {"ActivityTracker_TB" if record_type == "activity" else "MentalHealth_TB"}
                WHERE user_id = %s AND date = %s
                """
                self.cursor.execute(query, (self.user_id, selected_date))
                records = self.cursor.fetchall()

                # Display results
                result_text = "\n".join([str(record) for record in records]) if records else "No records found."
                result_label.configure(text=result_text)
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

        ctk.CTkButton(
            history_window,
            text="Search",
            command=fetch_records,
            fg_color=self.custom_color,
            font=("Microsoft YaHei UI Light", 12)
        ).pack(pady=10)

        # Results display
        result_label = ctk.CTkLabel(history_window, text="", font=("Microsoft YaHei UI Light", 12), wraplength=450)
        result_label.pack(pady=10)


    def show_health_suggestions(self, bmi_status):
        suggestions = {
            "Underweight": [
                "Increase caloric intake with nutrient-rich foods",
                "Include protein-rich foods in every meal",
                "Consider strength training exercises",
                "Consult a healthcare provider for guidance"
            ],
            "Normal": [
                "Maintain a balanced diet",
                "Regular exercise (150 minutes/week)",
                "Stay hydrated",
                "Get adequate sleep"
            ],
            "Overweight": [
                "Monitor portion sizes",
                "Increase physical activity",
                "Choose whole foods over processed foods",
                "Consider consulting a nutritionist"
            ],
            "Obese": [
                "Consult healthcare provider for personalized plan",
                "Start with low-impact exercises",
                "Focus on gradual, sustainable changes",
                "Keep a food and activity journal"
            ]
        }

        suggestion_text = "\n".join([f"• {s}" for s in suggestions[bmi_status]])
        messagebox.showinfo(
            "Health Suggestions",
            f"Based on your BMI status ({bmi_status}), here are some suggestions:\n\n{suggestion_text}"
        )

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else None
    if user_id is None:
        print("Error: User ID not provided.")
        sys.exit(1)

    dashboard = ctk.CTk()
    app = DashboardApp(dashboard, user_id)
    dashboard.mainloop()

