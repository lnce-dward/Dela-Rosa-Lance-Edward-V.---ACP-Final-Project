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
        self.dashboard_tab
        dashboard.title("Health Tracker Dashboard")
        dashboard.geometry("925x500+300+200")

        
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
        
        self.create_widgets()

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
    # Replace ttk.Notebook with CustomTkinter's CTkTabview
    self.notebook = ctk.CTkTabview(self.master)  # Use self.master instead of self
    self.notebook.pack(fill="both", expand=True)  # Pack it into the window

    # Add the "Mental Health" tab to the notebook (CTkTabview)
    self.mental_health_tab = self.notebook.add("Mental Health")  # Adding the tab
    self.dashboard_tab = self.notebook.add("Dashboard")  # Add another tab for Dashboard

    # Add widgets to the Mental Health tab
    label = ctk.CTkLabel(self.mental_health_tab, text="Welcome to the Mental Health Tracker!")
    label.pack(pady=20)  # Add label to the mental health tab

    # Optionally, add more widgets to the Mental Health tab, such as buttons
    button = ctk.CTkButton(self.mental_health_tab, text="Start Tracking", command=self.start_tracking)
    button.pack(pady=10)  # Add button to the mental health tab

    # Add widgets to the Dashboard tab
    dashboard_label = ctk.CTkLabel(self.dashboard_tab, text="Welcome to the Dashboard")
    dashboard_label.pack(pady=20)  # Add label to the dashboard tab

    # Optionally, add more widgets to the Dashboard tab
    dashboard_button = ctk.CTkButton(self.dashboard_tab, text="Go to Mental Health", command=self.show_mental_health)
    dashboard_button.pack(pady=10)  # Add button to the dashboard tab

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
        self.create_summary_card(summary_frame, "Average Mood", f"{stats['avg_mood']:.1f}/10")
        self.create_summary_card(summary_frame, "Average Stress", f"{stats['avg_stress']:.1f}/10")
        self.create_summary_card(summary_frame, "Monthly Entries", str(stats['total_entries']))

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

    def create_profile_content(self):
        profile_frame = ctk.CTkFrame(self.profile_tab)
        profile_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Profile information
        fields = [
            ("Full Name", 'full_name'),
            ("Email", 'email'),
            ("Phone", 'phone_number'),
            ("Address", 'address'),
            ("Gender", 'gender'),
            ("Date of Birth", 'dob'),
            ("Medical History", 'medical_history')
        ]

        self.profile_entries = {}

        for label, key in fields:
            field_frame = ctk.CTkFrame(profile_frame)
            field_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                field_frame,
                text=f"{label}:",
                font=self.custom_font,
                width=120
            ).pack(side="left", padx=10)
            
            value = str(self.userprofile.get(key, ""))
            entry = ctk.CTkEntry(field_frame, font=self.custom_font, width=200)
            entry.insert(0, value)
            entry.pack(side="left", padx=10)
            self.profile_entries[key] = entry

        # Update profile button
        ctk.CTkButton(
            profile_frame,
            text="Update Profile",
            command=self.update_profile,
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
                self.profile_entries['full_name'].get(),
                self.profile_entries['phone_number'].get(),
                self.profile_entries['address'].get(),
                self.profile_entries['gender'].get(),
                self.profile_entries['dob'].get(),
                self.profile_entries['medical_history'].get(),
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

        if result['avg_mood'] is not None and result['avg_stress'] is not None:
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

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else None
    if user_id is None:
        print("Error: User ID not provided.")
        sys.exit(1)

    dashboard = ctk.CTk()
    app = DashboardApp(dashboard, user_id)
    app.update_dashboard() 
    dashboard.mainloop()

